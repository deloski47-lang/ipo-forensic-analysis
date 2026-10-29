import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import (
    AnalysisResult as ResultModel, AnalysisRun as RunModel, EvidenceItem, FactRecord,
    Finding as FindingModel, IpoIssue, Issuer, MarketObservation, ResearchCase,
    ScenarioDefinition,
)
from app.schemas.analysis import (
    AnalysisResult, AnalysisRunDetail, AnalysisRunListResponse, AnalysisRunSummary,
    CreateAnalysisRunRequest, Finding, FindingEvidenceLink,
)
from app.schemas.readiness import AnalysisReadiness, ReadinessIssue

router = APIRouter()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_uuid(value: str) -> str:
    try:
        return str(UUID(value))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Research resource not found.") from exc


def get_case(db: Session, case_id: str) -> ResearchCase:
    case = db.get(ResearchCase, parse_uuid(case_id))
    if case is None:
        raise HTTPException(status_code=404, detail="Research case not found.")
    return case


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def json_load(value: str):
    return json.loads(value)


def serialize_result(item: ResultModel) -> AnalysisResult:
    return AnalysisResult(
        result_id=item.id, indicator_code=item.indicator_code, calculation_status=item.calculation_status,
        value_decimal=item.value_decimal, value_text=item.value_text, unit=item.unit, currency=item.currency,
        display_value=item.display_value, formula_code=item.formula_code, formula_version=item.formula_version,
        input_fact_ids=json_load(item.input_fact_ids_json), input_observation_ids=json_load(item.input_observation_ids_json),
        evidence_ids=json_load(item.evidence_ids_json), explanation=item.explanation, reason=item.reason,
    )


def serialize_finding(item: FindingModel) -> Finding:
    return Finding(
        finding_id=item.id, rule_code=item.rule_code, rule_version=item.rule_version, finding_type=item.finding_type,
        severity=item.severity, status=item.status, title=item.title, explanation=item.explanation,
        limitation_note=item.limitation_note, related_indicator_codes=json_load(item.related_indicator_codes_json),
        input_fact_ids=json_load(item.input_fact_ids_json), input_observation_ids=json_load(item.input_observation_ids_json),
        evidence_links=[FindingEvidenceLink.model_validate(link) for link in json_load(item.evidence_links_json)],
    )


def serialize_run(db: Session, item: RunModel) -> AnalysisRunDetail:
    results = list(db.scalars(select(ResultModel).where(ResultModel.analysis_run_id == item.id)))
    findings = list(db.scalars(select(FindingModel).where(FindingModel.analysis_run_id == item.id)))
    return AnalysisRunDetail(
        analysis_run_id=item.id, case_id=item.case_id, run_status=item.run_status,
        information_cutoff_at=parse_time(item.information_cutoff_at), started_at=parse_time(item.started_at),
        finished_at=parse_time(item.finished_at) if item.finished_at else None,
        schema_version=item.schema_version, formula_set_version=item.formula_set_version,
        rule_set_version=item.rule_set_version, software_version=item.software_version,
        input_snapshot_hash=item.input_snapshot_hash,
        results=[serialize_result(result) for result in results],
        findings=[serialize_finding(finding) for finding in findings],
        readiness=AnalysisReadiness.model_validate(json_load(item.readiness_json)),
        error_summary=item.error_summary,
    )


@router.post("/cases/{case_id}/analysis-runs", response_model=AnalysisRunDetail, status_code=201)
def create_analysis_run(
    case_id: str, payload: CreateAnalysisRunRequest, db: Session = Depends(get_db)
) -> AnalysisRunDetail:
    case = get_case(db, case_id)
    started = datetime.now(timezone.utc)
    cutoff = payload.information_cutoff_at.astimezone(timezone.utc)
    if cutoff > started:
        raise HTTPException(status_code=422, detail="Information cutoff cannot be in the future.")
    if case.identity_status != "confirmed" or not case.issue_id:
        raise HTTPException(status_code=409, detail={
            "code": "ANALYSIS_BLOCKED",
            "message": "Confirm the exact Mainboard IPO identity before running issue-specific analysis.",
        })
    issue = db.get(IpoIssue, case.issue_id)
    issuer = db.get(Issuer, issue.issuer_id) if issue else None
    if issue is None or issuer is None or parse_time(issue.created_at) > cutoff:
        raise HTTPException(status_code=409, detail={
            "code": "ANALYSIS_BLOCKED",
            "message": "The confirmed issue identity is not available at the requested information cutoff.",
        })

    facts = [item for item in db.scalars(select(FactRecord).where(FactRecord.case_id == case.id)) if parse_time(item.recorded_at) <= cutoff]
    observations = [item for item in db.scalars(select(MarketObservation).where(MarketObservation.case_id == case.id)) if parse_time(item.recorded_at) <= cutoff]
    evidence = [item for item in db.scalars(select(EvidenceItem).where(EvidenceItem.case_id == case.id)) if parse_time(item.captured_at) <= cutoff]
    scenarios = [item for item in db.scalars(select(ScenarioDefinition).where(ScenarioDefinition.case_id == case.id)) if parse_time(item.created_at) <= cutoff]
    if not scenarios:
        raise HTTPException(status_code=409, detail={
            "code": "ANALYSIS_BLOCKED",
            "message": "No saved scenario exists at this information cutoff. Add at least one user-defined listing-price scenario.",
        })

    finished = datetime.now(timezone.utc)
    snapshot = {
        "schemaVersion": "1.0",
        "case": {"caseId": case.id, "enteredName": case.entered_name, "title": case.title},
        "issue": {
            "issueId": issue.id, "issuerLegalName": issuer.legal_name, "displayName": issue.display_name,
            "marketSegment": issue.market_segment, "openDate": issue.open_date, "closeDate": issue.close_date,
            "listingDate": issue.listing_date, "priceBandLow": issue.price_band_low,
            "priceBandHigh": issue.price_band_high, "issueSizeAmount": issue.issue_size_amount,
            "issueSizeUnit": issue.issue_size_unit,
        },
        "informationCutoffAt": cutoff.isoformat().replace("+00:00", "Z"),
        "evidence": [{
            "evidenceId": item.id, "title": item.title, "evidenceKind": item.evidence_kind,
            "sourceUrl": item.source_url, "sha256": item.sha256, "capturedAt": item.captured_at,
            "verificationStatus": item.verification_status, "notes": item.notes,
        } for item in sorted(evidence, key=lambda row: row.id)],
        "facts": [{
            "factId": item.id, "indicatorCode": item.indicator_code, "rawValueText": item.raw_value_text,
            "valueNumeric": item.value_numeric, "valueText": item.value_text, "unit": item.unit,
            "currency": item.currency, "periodStart": item.period_start, "periodEnd": item.period_end,
            "asOfDate": item.as_of_date, "evidenceId": item.evidence_id, "reviewStatus": item.review_status,
            "recordedAt": item.recorded_at,
        } for item in sorted(facts, key=lambda row: row.id)],
        "observations": [{
            "observationId": item.id, "indicatorCode": item.indicator_code, "signalCategory": item.signal_category,
            "segment": item.segment, "rawValueText": item.raw_value_text, "valueNumeric": item.value_numeric,
            "valueText": item.value_text, "unit": item.unit, "currency": item.currency,
            "metricDefinition": item.metric_definition, "observedAt": item.observed_at,
            "publishedAt": item.published_at, "retrievedAt": item.retrieved_at,
            "evidenceId": item.evidence_id, "reviewStatus": item.review_status, "recordedAt": item.recorded_at,
        } for item in sorted(observations, key=lambda row: row.id)],
        "scenarios": [{
            "scenarioId": item.id, "label": item.label, "entryPrice": item.entry_price,
            "exitPrice": item.exit_price, "quantity": item.quantity, "assumptionNote": item.assumption_note,
            "createdAt": item.created_at,
        } for item in sorted(scenarios, key=lambda row: row.id)],
        "enabledFormulaCodes": ["RISK-03"],
        "disabledFormulaScope": "All non-scenario IPO analysis formulas remain disabled until the P0 formula register is approved.",
    }
    canonical = json.dumps(snapshot, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    snapshot_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    now = finished.isoformat().replace("+00:00", "Z")
    current_readiness = {
        "caseId": case.id,
        "status": "blocked",
        "checkedAt": now,
        "informationCutoffAt": cutoff.isoformat().replace("+00:00", "Z"),
        "blockers": [
            {"code": "FORMULA_REGISTRY_PARTIAL", "severity": "blocking", "message": "Only RISK-03 gross scenario arithmetic is enabled; the full IPO formula register is not enabled.", "affectedIndicatorCodes": ["RISK-03"], "affectedSignalCategories": [], "evidenceIds": [], "nextAction": "Complete and validate the P0 formula register."}
        ],
        "warnings": [
            {"code": "SOURCE_CONNECTORS_NOT_ENABLED", "severity": "warning", "message": "No external source connectors are enabled.", "affectedIndicatorCodes": [], "affectedSignalCategories": [], "evidenceIds": [], "nextAction": "Use source-linked manual evidence."}
        ],
        "readyFormulaCodes": ["RISK-03"],
        "skippedFormulaCodes": [],
        "eligibleFindingRuleCodes": ["DATA-01"],
        "skippedFindingRuleCodes": [],
        "sourceCoverage": [],
    }
    run = RunModel(
        id=str(uuid4()), case_id=case.id, run_status="partial",
        information_cutoff_at=cutoff.isoformat().replace("+00:00", "Z"),
        started_at=started.isoformat().replace("+00:00", "Z"), finished_at=now,
        schema_version="1.0", formula_set_version="scenario-gross-v1",
        rule_set_version="data-coverage-v1", software_version="0.1.0",
        input_snapshot_hash=snapshot_hash, input_snapshot_json=canonical,
        readiness_json=json.dumps(current_readiness, sort_keys=True, separators=(",", ":")),
        error_summary=None,
    )
    db.add(run)
    db.flush()
    for scenario in scenarios:
        entry = Decimal(scenario.entry_price)
        exit_price = Decimal(scenario.exit_price)
        with localcontext() as ctx:
            ctx.prec = 28
            gross_return = ((exit_price - entry) / entry) * Decimal("100")
        db.add(ResultModel(
            id=str(uuid4()), analysis_run_id=run.id, indicator_code="RISK-03",
            calculation_status="calculated", value_decimal=format(gross_return, "f"),
            value_text=None, unit="%", currency=None, display_value=format(gross_return, "f") + "%",
            formula_code="RISK-03", formula_version="scenario-gross-v1",
            input_fact_ids_json="[]", input_observation_ids_json="[]", evidence_ids_json="[]",
            explanation=f"Gross return for user-defined scenario '{scenario.label}': (exit price {scenario.exit_price} - entry price {scenario.entry_price}) / entry price × 100.",
            reason="This is a hypothetical scenario, not a realized listing return or a forecast. Costs and taxes are excluded.",
        ))
    accepted_facts = [item for item in facts if item.review_status == "accepted"]
    accepted_observations = [item for item in observations if item.review_status == "accepted"]
    db.add(FindingModel(
        id=str(uuid4()), analysis_run_id=run.id, rule_code="DATA-01", rule_version="data-coverage-v1",
        finding_type="coverage_gap", severity="high" if not accepted_facts else "medium", status="unresolved",
        title="Full IPO analysis is not yet available",
        explanation=f"This partial run calculated {len(scenarios)} user-defined gross scenario return(s). It did not calculate issuer financial, valuation, demand, GMP-trend or cross-signal conclusions. Accepted facts: {len(accepted_facts)}; accepted observations: {len(accepted_observations)}.",
        limitation_note="No external source connector is enabled. Missing information is not treated as zero, and this finding is not an investment recommendation.",
        related_indicator_codes_json=json.dumps(["RISK-03", "DATA-01"]),
        input_fact_ids_json=json.dumps([item.id for item in accepted_facts]),
        input_observation_ids_json=json.dumps([item.id for item in accepted_observations]),
        evidence_links_json="[]",
    ))
    case.latest_analysis_run_id = run.id
    case.case_changed_since_last_run = False
    case.last_activity_at = now
    case.updated_at = now
    db.commit()
    db.refresh(run)
    return serialize_run(db, run)


@router.get("/cases/{case_id}/analysis-runs", response_model=AnalysisRunListResponse)
def list_analysis_runs(case_id: str, db: Session = Depends(get_db)) -> AnalysisRunListResponse:
    case = get_case(db, case_id)
    rows = list(db.scalars(select(RunModel).where(RunModel.case_id == case.id).order_by(RunModel.started_at.desc())))
    return AnalysisRunListResponse(items=[
        AnalysisRunSummary(
            analysis_run_id=item.id, case_id=item.case_id, run_status=item.run_status,
            information_cutoff_at=parse_time(item.information_cutoff_at), started_at=parse_time(item.started_at),
            finished_at=parse_time(item.finished_at) if item.finished_at else None,
            input_snapshot_hash=item.input_snapshot_hash,
        ) for item in rows
    ], total=len(rows))


@router.get("/cases/{case_id}/analysis-runs/{analysis_run_id}", response_model=AnalysisRunDetail)
def get_analysis_run(case_id: str, analysis_run_id: str, db: Session = Depends(get_db)) -> AnalysisRunDetail:
    case = get_case(db, case_id)
    run_id = parse_uuid(analysis_run_id)
    run = db.get(RunModel, run_id)
    if run is None or run.case_id != case.id:
        raise HTTPException(status_code=404, detail="Analysis run not found.")
    return serialize_run(db, run)
