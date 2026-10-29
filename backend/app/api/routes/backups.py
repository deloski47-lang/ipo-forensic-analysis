from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
import tempfile
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path, PurePosixPath
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db, get_engine, _engine_for_path
from app.models import ResearchCase, EvidenceItem, RestoreValidation
from app.schemas.backups import BackupResponse, RestoreRequest, RestoreResponse, RestoreValidationResponse

router = APIRouter()
MAX_ARCHIVE_BYTES = 250 * 1024 * 1024
MAX_UNCOMPRESSED_BYTES = 1024 * 1024 * 1024
MAX_ARCHIVE_FILES = 10_000
MAX_MEMBER_BYTES = 250 * 1024 * 1024
SUPPORTED_REVISIONS = {
    "0001_research_cases", "0002_evidence_items", "0003_identity", "0004_market_observations",
    "0005_scenarios", "0006_fact_records", "0007_analysis_runs", "0008_reports",
    "0009_restore_validations",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_uuid(value: str) -> str:
    try:
        return str(UUID(value))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Backup or restore validation not found.") from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def current_revision(database_path: Path) -> str | None:
    with sqlite3.connect(f"file:{database_path.as_posix()}?mode=ro", uri=True) as connection:
        row = connection.execute("SELECT version_num FROM alembic_version LIMIT 1").fetchone()
        return str(row[0]) if row else None


def backup_archive(db: Session) -> BackupResponse:
    settings = get_settings()
    settings.ensure_data_directories()
    backup_id = str(uuid4())
    created = now_iso()
    temporary_db = settings.data_dir / "tmp" / f"{backup_id}.sqlite3"
    archive_path = settings.data_dir / "backups" / f"{backup_id}.zip"
    source = sqlite3.connect(f"file:{settings.database_path.as_posix()}?mode=ro", uri=True)
    destination = sqlite3.connect(temporary_db)
    try:
        source.backup(destination)
    finally:
        destination.close()
        source.close()

    files: dict[str, Path] = {"database/ipo_forensic.sqlite3": temporary_db}
    evidence_dir = settings.data_dir / "evidence"
    reports_dir = settings.data_dir / "reports"
    evidence_files = sorted(path for path in evidence_dir.rglob("*") if path.is_file()) if evidence_dir.exists() else []
    report_files = sorted(path for path in reports_dir.rglob("*") if path.is_file()) if reports_dir.exists() else []
    for path in evidence_files:
        files[PurePosixPath("evidence", *path.relative_to(evidence_dir).parts).as_posix()] = path
    for path in report_files:
        files[PurePosixPath("reports", *path.relative_to(reports_dir).parts).as_posix()] = path

    manifest_files = {
        name: {"sha256": sha256_file(path), "sizeBytes": path.stat().st_size}
        for name, path in files.items()
    }
    manifest = {
        "formatVersion": 1,
        "createdAt": created,
        "schemaRevision": current_revision(temporary_db),
        "files": manifest_files,
    }
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, path in files.items():
            archive.write(path, arcname=name)
        archive.writestr("manifest.json", json.dumps(manifest, sort_keys=True, separators=(",", ":")))
    temporary_db.unlink(missing_ok=True)
    return BackupResponse(
        backup_id=backup_id,
        created_at=datetime.fromisoformat(created.replace("Z", "+00:00")),
        size_bytes=archive_path.stat().st_size,
        sha256=sha256_file(archive_path),
        case_count=int(db.scalar(select(func.count()).select_from(ResearchCase)) or 0),
        evidence_file_count=len(evidence_files),
        download_url=f"/api/v1/local-data/backups/{backup_id}/download",
    )


def inspect_archive(path: Path, scratch_dir: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    case_count = 0
    evidence_count = 0
    schema_revision = None
    database_temp = scratch_dir / "validation.sqlite3"
    try:
        with zipfile.ZipFile(path, "r") as archive:
            infos = [info for info in archive.infolist() if not info.is_dir()]
            if len(infos) > MAX_ARCHIVE_FILES:
                raise ValueError("Archive contains too many files.")
            total_size = sum(info.file_size for info in infos)
            if total_size > MAX_UNCOMPRESSED_BYTES:
                raise ValueError("Archive exceeds the maximum uncompressed size.")
            names = set()
            for info in infos:
                name = info.filename
                pure = PurePosixPath(name)
                if "\\" in name or pure.is_absolute() or ".." in pure.parts or (pure.parts and ":" in pure.parts[0]):
                    raise ValueError("Archive contains an unsafe path.")
                if not pure.parts or pure.parts[0] not in {"database", "evidence", "reports", "manifest.json"}:
                    raise ValueError("Archive contains an unexpected top-level path.")
                if info.file_size > MAX_MEMBER_BYTES:
                    raise ValueError(f"Archive member is too large: {name}")
                if info.file_size > 0 and info.compress_size > 0 and info.file_size / info.compress_size > 1000:
                    raise ValueError(f"Archive member has an unsafe compression ratio: {name}")
                if ((info.external_attr >> 16) & 0o170000) == 0o120000:
                    raise ValueError("Archive contains a symbolic link.")
                names.add(name)
            if "manifest.json" not in names or "database/ipo_forensic.sqlite3" not in names:
                raise ValueError("Backup is missing manifest.json or the SQLite database.")
            manifest = json.loads(archive.read("manifest.json"))
            if manifest.get("formatVersion") != 1 or not isinstance(manifest.get("files"), dict):
                raise ValueError("Backup manifest version or file list is invalid.")
            expected_names = set(manifest["files"].keys())
            if expected_names != names - {"manifest.json"}:
                raise ValueError("Backup manifest does not match the archive file list.")
            for name, metadata in manifest["files"].items():
                digest = hashlib.sha256()
                size = 0
                with archive.open(name) as source:
                    while chunk := source.read(1024 * 1024):
                        size += len(chunk)
                        digest.update(chunk)
                if size != metadata.get("sizeBytes") or digest.hexdigest() != metadata.get("sha256"):
                    raise ValueError(f"Backup checksum or size mismatch: {name}")
            with archive.open("database/ipo_forensic.sqlite3") as source, database_temp.open("wb") as target:
                shutil.copyfileobj(source, target, length=1024 * 1024)
            with sqlite3.connect(f"file:{database_temp.as_posix()}?mode=ro", uri=True) as connection:
                integrity = connection.execute("PRAGMA integrity_check").fetchone()
                if not integrity or integrity[0] != "ok":
                    raise ValueError("SQLite integrity check failed.")
                tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                required = {"alembic_version", "research_cases", "evidence_items"}
                if not required.issubset(tables):
                    raise ValueError("SQLite database is missing required application tables.")
                revision_row = connection.execute("SELECT version_num FROM alembic_version LIMIT 1").fetchone()
                schema_revision = str(revision_row[0]) if revision_row else None
                case_count = int(connection.execute("SELECT COUNT(*) FROM research_cases").fetchone()[0])
            if schema_revision not in SUPPORTED_REVISIONS:
                return {
                    "status": "incompatible", "case_count": case_count, "evidence_file_count": len([n for n in names if n.startswith("evidence/")]),
                    "warnings": warnings, "errors": [f"Unsupported database schema revision: {schema_revision or 'unknown'}."],
                }
            evidence_count = len([name for name in names if name.startswith("evidence/")])
            if evidence_count == 0:
                warnings.append("Backup contains no evidence files.")
            if not any(name.startswith("reports/") for name in names):
                warnings.append("Backup contains no report exports.")
            return {"status": "valid", "case_count": case_count, "evidence_file_count": evidence_count, "warnings": warnings, "errors": errors}
    except (zipfile.BadZipFile, json.JSONDecodeError, OSError, sqlite3.DatabaseError, ValueError, KeyError) as exc:
        errors.append(str(exc))
        return {"status": "invalid", "case_count": case_count, "evidence_file_count": evidence_count, "warnings": warnings, "errors": errors}
    finally:
        database_temp.unlink(missing_ok=True)


@router.post("/local-data/backups", response_model=BackupResponse, status_code=201)
def create_backup(db: Session = Depends(get_db)) -> BackupResponse:
    return backup_archive(db)


@router.get("/local-data/backups/{backup_id}/download")
def download_backup(backup_id: str) -> FileResponse:
    settings = get_settings()
    path = (settings.data_dir / "backups" / f"{parse_uuid(backup_id)}.zip").resolve()
    if settings.data_dir.resolve() not in path.parents or not path.is_file():
        raise HTTPException(status_code=404, detail="Backup file not found.")
    return FileResponse(path, media_type="application/zip", filename=path.name)


@router.post("/local-data/restore/validate", response_model=RestoreValidationResponse, status_code=201)
async def validate_restore(file: UploadFile = File(...), db: Session = Depends(get_db)) -> RestoreValidationResponse:
    settings = get_settings()
    validation_id = str(uuid4())
    relative = Path("tmp") / f"restore-validation-{validation_id}.zip"
    target = settings.data_dir / relative
    digest = hashlib.sha256()
    size = 0
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with target.open("xb") as destination:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_ARCHIVE_BYTES:
                    raise HTTPException(status_code=413, detail="Backup archive exceeds the 250 MB upload limit.")
                digest.update(chunk)
                destination.write(chunk)
        scratch = settings.data_dir / "tmp" / f"validate-{validation_id}"
        scratch.mkdir(parents=True, exist_ok=False)
        try:
            result = inspect_archive(target, scratch)
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
        validated = now_iso()
        record = RestoreValidation(
            id=validation_id, status=result["status"], archive_relative_path=relative.as_posix(),
            archive_sha256=digest.hexdigest(), archive_size_bytes=size,
            case_count=result["case_count"], evidence_file_count=result["evidence_file_count"],
            warnings_json=json.dumps(result["warnings"]), errors_json=json.dumps(result["errors"]), validated_at=validated,
        )
        db.add(record)
        db.commit()
        return RestoreValidationResponse(
            validation_id=validation_id, status=result["status"], case_count=result["case_count"],
            evidence_file_count=result["evidence_file_count"], warnings=result["warnings"], errors=result["errors"],
            validated_at=datetime.fromisoformat(validated.replace("Z", "+00:00")),
        )
    finally:
        await file.close()


@router.post("/local-data/restore", response_model=RestoreResponse)
def restore_backup(payload: RestoreRequest, db: Session = Depends(get_db)) -> RestoreResponse:
    settings = get_settings()
    validation = db.get(RestoreValidation, parse_uuid(payload.validation_id))
    if validation is None:
        raise HTTPException(status_code=404, detail="Restore validation record not found.")
    if validation.status != "valid":
        raise HTTPException(status_code=409, detail="Only a valid backup archive can be restored.")
    validated_at = datetime.fromisoformat(validation.validated_at.replace("Z", "+00:00"))
    if datetime.now(timezone.utc) - validated_at > timedelta(hours=24):
        raise HTTPException(status_code=409, detail="Restore validation has expired. Validate the archive again.")
    archive_path = (settings.data_dir / validation.archive_relative_path).resolve()
    if settings.data_dir.resolve() not in archive_path.parents or not archive_path.is_file():
        raise HTTPException(status_code=404, detail="Validated archive file is unavailable.")
    if archive_path.stat().st_size != validation.archive_size_bytes or sha256_file(archive_path) != validation.archive_sha256:
        raise HTTPException(status_code=409, detail="Validated archive changed after validation.")
    safety = backup_archive(db)
    stage = settings.data_dir / "tmp" / f"restore-stage-{validation.id}"
    stage.mkdir(parents=True, exist_ok=False)
    old_evidence = stage / "old-evidence"
    old_reports = stage / "old-reports"
    old_database = stage / "old-ipo_forensic.sqlite3"
    replaced = False
    try:
        with zipfile.ZipFile(archive_path, "r") as archive:
            for info in archive.infolist():
                if info.is_dir() or info.filename == "manifest.json":
                    continue
                pure = PurePosixPath(info.filename)
                if "\\" in info.filename or pure.is_absolute() or ".." in pure.parts:
                    raise HTTPException(status_code=422, detail="Archive contains an unsafe path.")
                target = stage.joinpath(*pure.parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(info) as source, target.open("xb") as destination:
                    shutil.copyfileobj(source, destination, length=1024 * 1024)
        staged_db = stage / "database" / "ipo_forensic.sqlite3"
        if not staged_db.is_file():
            raise HTTPException(status_code=422, detail="Backup database file is missing.")
        db.commit()
        engine = get_engine()
        db.close()
        engine.dispose()
        _engine_for_path.cache_clear()
        shutil.copy2(settings.database_path, old_database)
        if (settings.data_dir / "evidence").exists():
            os.replace(settings.data_dir / "evidence", old_evidence)
        if (settings.data_dir / "reports").exists():
            os.replace(settings.data_dir / "reports", old_reports)
        os.replace(staged_db, settings.database_path)
        if (stage / "evidence").exists():
            os.replace(stage / "evidence", settings.data_dir / "evidence")
        else:
            (settings.data_dir / "evidence").mkdir(parents=True, exist_ok=True)
        if (stage / "reports").exists():
            os.replace(stage / "reports", settings.data_dir / "reports")
        else:
            (settings.data_dir / "reports").mkdir(parents=True, exist_ok=True)
        _engine_for_path.cache_clear()
        from app.main import run_migrations
        run_migrations()
        replaced = True
        return RestoreResponse(
            status="completed", restored_at=datetime.now(timezone.utc), safety_backup_id=safety.backup_id,
            message="Restore completed. A safety backup of the pre-restore data was created first.",
        )
    except Exception as exc:
        if old_database.exists():
            shutil.copy2(old_database, settings.database_path)
        if (settings.data_dir / "evidence").exists():
            shutil.rmtree(settings.data_dir / "evidence", ignore_errors=True)
        if old_evidence.exists():
            os.replace(old_evidence, settings.data_dir / "evidence")
        if (settings.data_dir / "reports").exists():
            shutil.rmtree(settings.data_dir / "reports", ignore_errors=True)
        if old_reports.exists():
            os.replace(old_reports, settings.data_dir / "reports")
        _engine_for_path.cache_clear()
        if isinstance(exc, HTTPException):
            raise
        raise HTTPException(status_code=500, detail="Restore failed; the pre-restore data was restored from the safety copy.") from exc
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        if replaced:
            archive_path.unlink(missing_ok=True)
