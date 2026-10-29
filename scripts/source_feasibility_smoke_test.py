#!/usr/bin/env python3
"""Read-only smoke test for free IPO subscription/GMP API candidates.

No third-party dependencies. The script does not scrape exchange webpages,
submit forms, authenticate, or write to the IPO application database.
It prints a JSON report to stdout; --output optionally saves that report.

Xflot documents a maximum polling frequency of once per minute. This script
uses a persistent local guard under ~/.ipo-source-benchmark so running it
repeatedly cannot accidentally exceed that frequency.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IPOS_INDEX_URL = "https://ipos.markets/api/v1/subscription"
GMPTODAY_URL = "https://gmptoday.in/api/gmp.json"
XFLOT_INDEX_URL = "https://xflot.com/api/public/market/ipos?limit=200"
XFLOT_DETAIL_BASE = "https://xflot.com/api/public/market/ipos/"

USER_AGENT = "IPO-Forensic-Analysis-Source-Benchmark/0.1 (read-only; attribution retained)"
TIMEOUT_SECONDS = 20

# Aliases are used only to match records in a provider's returned manifest.
# Matching never creates or fills a financial value.
TARGETS: dict[str, tuple[str, ...]] = {
    "BLS Polymers": ("BLS Polymers", "BLS Polymers Limited"),
    "SFC Environmental Technologies": ("SFC Environmental Technologies", "SFC Environmental Technologies Limited"),
    "EAAA India Alternatives": ("EAAA India Alternatives", "EAAA India Alternatives Limited"),
    "M.K. Sons Fine Jewels": ("M.K. Sons Fine Jewels", "MK Sons Fine Jewels"),
    "Bombay Coated and Special Steels": ("Bombay Coated and Special Steels", "Bombay Coated"),
    "Jio Platforms": ("Jio Platforms", "Jio Platforms Limited"),
    "Paras Healthcare": ("Paras Healthcare", "Paras Health"),
    "Zetwerk Manufacturing Businesses": ("Zetwerk Manufacturing Businesses", "Zetwerk"),
    "Data Patterns (India)": ("Data Patterns (India)", "Data Patterns India"),
    "Burger King India": ("Burger King India", "Burger King India Limited"),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalized(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").casefold())


def request_json(url: str) -> dict[str, Any]:
    """Perform one GET and return response telemetry and decoded JSON."""
    started_at = utc_now()
    start = time.monotonic()
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            raw = response.read()
            status = response.status
            content_type = response.headers.get("Content-Type", "")
            response_headers = {
                "cache_control": response.headers.get("Cache-Control"),
                "date": response.headers.get("Date"),
                "etag": response.headers.get("ETag"),
                "last_modified": response.headers.get("Last-Modified"),
            }
        elapsed_ms = round((time.monotonic() - start) * 1000, 1)
        result: dict[str, Any] = {
            "url": url,
            "attempted_at_utc": started_at,
            "finished_at_utc": utc_now(),
            "http_status": status,
            "content_type": content_type,
            "response_bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "latency_ms": elapsed_ms,
            "headers": response_headers,
            "json_valid": False,
            "error": None,
            "data": None,
        }
        try:
            decoded = json.loads(raw.decode("utf-8-sig"))
            result["json_valid"] = isinstance(decoded, (dict, list))
            result["data"] = decoded
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            result["error"] = "JSON parse error: " + str(exc)
        return result
    except urllib.error.HTTPError as exc:
        elapsed_ms = round((time.monotonic() - start) * 1000, 1)
        body = exc.read()
        return {
            "url": url,
            "attempted_at_utc": started_at,
            "finished_at_utc": utc_now(),
            "http_status": exc.code,
            "content_type": exc.headers.get("Content-Type", ""),
            "response_bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "latency_ms": elapsed_ms,
            "headers": {
                "cache_control": exc.headers.get("Cache-Control"),
                "date": exc.headers.get("Date"),
                "etag": exc.headers.get("ETag"),
                "last_modified": exc.headers.get("Last-Modified"),
            },
            "json_valid": False,
            "error": "HTTP error: " + str(exc),
            "data": None,
        }
    except Exception as exc:  # DNS, TLS, timeout, refused connection, etc.
        elapsed_ms = round((time.monotonic() - start) * 1000, 1)
        return {
            "url": url,
            "attempted_at_utc": started_at,
            "finished_at_utc": utc_now(),
            "http_status": None,
            "content_type": None,
            "response_bytes": None,
            "sha256": None,
            "latency_ms": elapsed_ms,
            "headers": {},
            "json_valid": False,
            "error": type(exc).__name__ + ": " + str(exc),
            "data": None,
        }


def coverage_for_record(record: dict[str, Any]) -> dict[str, Any]:
    categories = record.get("categories")
    categories = categories if isinstance(categories, dict) else {}
    def cat_value(code: str) -> Any:
        part = categories.get(code)
        return part.get("times") if isinstance(part, dict) else None

    return {
        "name": record.get("name"),
        "symbol": record.get("symbol"),
        "slug": record.get("slug"),
        "board": record.get("board"),
        "status": record.get("status"),
        "as_of": record.get("as_of"),
        "final": record.get("final"),
        "basis": record.get("basis"),
        "overall_times": record.get("total_times"),
        "overall_lower_bound_times": record.get("lower_bound_times"),
        "qib_times": cat_value("QIB"),
        "nii_times": cat_value("NII"),
        "rii_times": cat_value("RII"),
        "rti_times": cat_value("RETAIL"),
        "category_keys_present": sorted(categories.keys()),
        "source": record.get("source"),
        "has_source_timestamp": bool(record.get("as_of")),
    }


def ipos_markets_test(max_issues: int) -> dict[str, Any]:
    index_result = request_json(IPOS_INDEX_URL)
    data = index_result.get("data")
    if not index_result.get("json_valid") or not isinstance(data, dict):
        return {
            "provider": "ipos.markets",
            "index_request": telemetry_only(index_result),
            "candidate_status": "FAIL_OR_UNREACHABLE",
            "reason": "Index did not return a decodable JSON object.",
            "matched_issues": [],
        }

    issues = data.get("issues")
    if not isinstance(issues, list):
        return {
            "provider": "ipos.markets",
            "index_request": telemetry_only(index_result),
            "candidate_status": "SCHEMA_UNEXPECTED",
            "reason": "Expected top-level issues array was not found.",
            "top_level_keys": sorted(data.keys()),
            "matched_issues": [],
        }

    matches: list[tuple[str, dict[str, Any]]] = []
    for target, aliases in TARGETS.items():
        found = None
        for item in issues:
            if not isinstance(item, dict):
                continue
            haystack = " ".join(str(item.get(k) or "") for k in ("name", "slug", "symbol", "bse", "path"))
            nh = normalized(haystack)
            if any(normalized(alias) in nh for alias in aliases):
                found = item
                break
        if found is not None:
            matches.append((target, found))

    # Prefer the 10 named representatives; detail requests are sequential and small.
    details: list[dict[str, Any]] = []
    for target, brief in matches[:max_issues]:
        if brief.get("board") and str(brief["board"]).casefold() not in ("mainboard", "main board"):
            details.append({
                "target": target,
                "candidate_status": "EXCLUDED_NON_MAINBOARD",
                "manifest_record": {k: brief.get(k) for k in ("name", "symbol", "slug", "board", "status", "as_of", "path")},
            })
            continue
        detail_url = brief.get("path")
        if isinstance(detail_url, str) and detail_url.strip():
            if detail_url.startswith("/"):
                detail_url = "https://ipos.markets" + detail_url
            elif not detail_url.startswith("http"):
                detail_url = "https://ipos.markets/api/v1/subscription/" + urllib.parse.quote(detail_url, safe="")
        else:
            lookup = brief.get("symbol") or brief.get("bse") or brief.get("slug")
            if not lookup:
                details.append({
                    "target": target,
                    "candidate_status": "NO_LOOKUP_KEY",
                    "manifest_record": {k: brief.get(k) for k in ("name", "symbol", "slug", "board", "status", "as_of")},
                })
                continue
            detail_url = IPOS_INDEX_URL + "?" + urllib.parse.urlencode({"symbol": lookup})

        response = request_json(detail_url)
        record = response.get("data")
        if isinstance(record, dict) and isinstance(record.get("issue"), dict):
            record = record["issue"]
        if isinstance(record, dict) and isinstance(record.get("data"), dict):
            record = record["data"]
        if not isinstance(record, dict):
            details.append({
                "target": target,
                "candidate_status": "DETAIL_GET_FAILED_OR_SCHEMA_UNEXPECTED",
                "request": telemetry_only(response),
                "manifest_record": {k: brief.get(k) for k in ("name", "symbol", "slug", "board", "status", "as_of", "path")},
                "returned_top_level_keys": sorted(record.keys()) if isinstance(record, dict) else None,
            })
            continue

        projected = coverage_for_record(record)
        mainboard = str(projected.get("board") or brief.get("board") or "").casefold() in ("mainboard", "main board")
        required_category_count = sum(v is not None for v in (projected["qib_times"], projected["nii_times"], projected["rii_times"]))
        details.append({
            "target": target,
            "candidate_status": "RECORD_RETURNED",
            "request": telemetry_only(response),
            "is_mainboard": mainboard,
            "required_category_count_present": required_category_count,
            "required_category_count": 3,
            "has_as_of_timestamp": projected["has_source_timestamp"],
            "record": projected,
        })

    eligible = [d for d in details if d.get("candidate_status") == "RECORD_RETURNED"]
    all_coverage = sum(1 for d in eligible if d.get("is_mainboard") and d.get("required_category_count_present") == 3)
    with_timestamp = sum(1 for d in eligible if d.get("has_as_of_timestamp"))
    return {
        "provider": "ipos.markets",
        "index_request": telemetry_only(index_result),
        "index_top_level_keys": sorted(data.keys()),
        "manifest_issue_count": len(issues),
        "target_count": len(TARGETS),
        "targets_matched_in_manifest": len(matches),
        "details_tested": len(details),
        "details_returned": len(eligible),
        "mainboard_records_with_qib_nii_rii": all_coverage,
        "records_with_as_of_timestamp": with_timestamp,
        "candidate_status": "CANDIDATE_REQUIRES_REVIEW" if eligible else "FAIL_OR_UNREACHABLE",
        "details": details,
    }


def gmptoday_test() -> dict[str, Any]:
    response = request_json(GMPTODAY_URL)
    data = response.get("data")
    if not response.get("json_valid") or not isinstance(data, dict):
        return {
            "provider": "gmptoday.in",
            "request": telemetry_only(response),
            "candidate_status": "FAIL_OR_UNREACHABLE",
            "reason": "Endpoint did not return a decodable JSON object.",
        }
    ipos = data.get("ipos")
    if not isinstance(ipos, list):
        ipos = []
    projected = []
    for item in ipos:
        if not isinstance(item, dict):
            continue
        projected.append({
            "name": item.get("name"),
            "status": item.get("status"),
            "gmp_median": item.get("gmp_median"),
            "gmp_min": item.get("gmp_min"),
            "gmp_max": item.get("gmp_max"),
            "gmp_sources": item.get("gmp_sources"),
            "confidence": item.get("confidence"),
            "updated_at": item.get("updated_at"),
            "open_date": item.get("open_date"),
            "close_date": item.get("close_date"),
            "listing_date": item.get("listing_date"),
        })
    return {
        "provider": "gmptoday.in",
        "request": telemetry_only(response),
        "candidate_status": "CANDIDATE_REQUIRES_REVIEW",
        "generated_at": data.get("generated_at"),
        "updated_at": data.get("updated_at"),
        "license": data.get("license"),
        "attribution": data.get("attribution"),
        "sample_flag": data.get("sample"),
        "n_ipos_in_sample": data.get("n_ipos_in_sample"),
        "n_ipos_tracked": data.get("n_ipos_tracked"),
        "returned_ipo_count": len(projected),
        "ipos": projected,
        "warning": "This is a limited sample feed; do not treat absence as zero or assume full GMP coverage.",
    }


def xflot_guard_file() -> Path:
    return Path.home() / ".ipo-source-benchmark" / "xflot-last-request.json"


def guarded_xflot_request(url: str, force: bool = False) -> dict[str, Any]:
    guard = xflot_guard_file()
    guard.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()
    if guard.exists():
        try:
            previous = json.loads(guard.read_text(encoding="utf-8"))
            elapsed = now - float(previous.get("epoch", 0))
            if elapsed < 65 and not force:
                return {
                    "url": url,
                    "attempted_at_utc": utc_now(),
                    "http_status": None,
                    "json_valid": False,
                    "error": "Xflot polling guard: a request was made less than 65 seconds ago. Wait before retrying; do not use --force unless you have verified the provider's current terms.",
                    "next_allowed_in_seconds": round(65 - elapsed, 1),
                    "blocked_by_local_guard": True,
                }
        except (OSError, ValueError, json.JSONDecodeError):
            pass
    # Record before the request so a failed network call cannot cause rapid retries.
    guard.write_text(json.dumps({"epoch": now, "recorded_at_utc": utc_now()}), encoding="utf-8")
    return request_json(url)


def xflot_test(slug: str | None, force: bool = False) -> dict[str, Any]:
    # One Xflot request per run, with a cross-run local 65-second guard.
    if slug:
        safe_slug = urllib.parse.quote(slug, safe="-_")
        url = XFLOT_DETAIL_BASE + safe_slug
        mode = "single_issue_detail"
    else:
        url = XFLOT_INDEX_URL
        mode = "directory_only"
    response = guarded_xflot_request(url, force=force)
    data = response.get("data")
    if not response.get("json_valid"):
        return {
            "provider": "Xflot",
            "mode": mode,
            "request": telemetry_only(response),
            "candidate_status": "BLOCKED_BY_POLLING_GUARD" if response.get("blocked_by_local_guard") else "FAIL_OR_UNREACHABLE",
        }
    if not isinstance(data, dict):
        return {
            "provider": "Xflot",
            "mode": mode,
            "request": telemetry_only(response),
            "candidate_status": "SCHEMA_UNEXPECTED",
            "root_type": type(data).__name__,
        }
    if slug:
        ipo = data.get("ipo") if isinstance(data.get("ipo"), dict) else data
        subs = ipo.get("subs") if isinstance(ipo, dict) else None
        gmp = ipo.get("gmp") if isinstance(ipo, dict) else None
        return {
            "provider": "Xflot",
            "mode": mode,
            "request": telemetry_only(response),
            "candidate_status": "CANDIDATE_REQUIRES_REVIEW",
            "ok": data.get("ok"),
            "disclaimer": data.get("disclaimer"),
            "ipo": {
                "name": ipo.get("name"),
                "slug": ipo.get("slug"),
                "board": ipo.get("board"),
                "status": ipo.get("status"),
                "priceMin": ipo.get("priceMin"),
                "priceMax": ipo.get("priceMax"),
                "lastGmp": ipo.get("lastGmp"),
                "lastSubX": ipo.get("lastSubX"),
                "gmpSources": ipo.get("gmpSources"),
                "gmpSpread": ipo.get("gmpSpread"),
                "gmpDisputed": ipo.get("gmpDisputed"),
            } if isinstance(ipo, dict) else None,
            "subscription_rows": subs if isinstance(subs, list) else None,
            "gmp_history_count": len(gmp) if isinstance(gmp, list) else None,
            "warning": "Detail response is source-reported data; inspect timestamps, board and discrepancies before use.",
        }

    ipos = data.get("ipos")
    if not isinstance(ipos, list):
        return {
            "provider": "Xflot",
            "mode": mode,
            "request": telemetry_only(response),
            "candidate_status": "SCHEMA_UNEXPECTED",
            "top_level_keys": sorted(data.keys()),
        }
    projected = [{
        "slug": i.get("slug"),
        "name": i.get("name"),
        "board": i.get("board"),
        "status": i.get("status"),
        "openDate": i.get("openDate"),
        "closeDate": i.get("closeDate"),
        "lastGmp": i.get("lastGmp"),
        "lastSubX": i.get("lastSubX"),
        "gmpSources": i.get("gmpSources"),
        "gmpSpread": i.get("gmpSpread"),
        "gmpDisputed": i.get("gmpDisputed"),
    } for i in ipos if isinstance(i, dict)]
    mainboard_count = sum(1 for i in projected if str(i.get("board") or "").casefold() == "mainboard")
    return {
        "provider": "Xflot",
        "mode": mode,
        "request": telemetry_only(response),
        "candidate_status": "CANDIDATE_REQUIRES_REVIEW",
        "ok": data.get("ok"),
        "disclaimer": data.get("disclaimer"),
        "returned_ipo_count": len(projected),
        "mainboard_count": mainboard_count,
        "ipo_summaries": projected,
        "warning": "Directory response does not include category-wise detail; run a separate --provider xflot --xflot-slug <slug> call at least 65 seconds later to inspect one issue. Do not exceed the provider polling terms.",
    }


def telemetry_only(result: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in result.items() if k != "data"}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only source feasibility smoke test for candidate IPO subscription/GMP feeds."
    )
    parser.add_argument(
        "--provider",
        choices=("all", "ipos", "gmptoday", "xflot"),
        default="all",
        help="Provider to test; default runs all candidates (one Xflot request maximum).",
    )
    parser.add_argument(
        "--max-issues",
        type=int,
        default=10,
        help="Maximum matched ipos.markets records to GET for detail (default 10; max 10).",
    )
    parser.add_argument(
        "--xflot-slug",
        help="Optional Xflot issue slug; if supplied, tests the single-IPO detail endpoint instead of directory.",
    )
    parser.add_argument(
        "--output",
        help="Optional path to save the report JSON. By default, JSON is printed to stdout only.",
    )
    parser.add_argument(
        "--force-xflot",
        action="store_true",
        help="Bypass the local Xflot 65-second guard only after checking current provider terms.",
    )
    args = parser.parse_args()
    max_issues = max(1, min(args.max_issues, 10))
    report: dict[str, Any] = {
        "benchmark": "IPO Forensic Analysis Engine source API smoke test",
        "script_version": "0.1",
        "started_at_utc": utc_now(),
        "scope": "Indian Mainboard IPO subscription and unofficial GMP data",
        "budget": "INR 0",
        "note": "A successful HTTP response is not by itself connector approval. Review access terms, provenance, timestamps, definitions, cross-source accuracy and sample coverage.",
        "providers": [],
    }
    providers = ("ipos", "gmptoday", "xflot") if args.provider == "all" else (args.provider,)
    for provider in providers:
        if provider == "ipos":
            report["providers"].append(ipos_markets_test(max_issues))
        elif provider == "gmptoday":
            report["providers"].append(gmptoday_test())
        else:
            report["providers"].append(xflot_test(args.xflot_slug, force=args.force_xflot))
    report["finished_at_utc"] = utc_now()
    serialized = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        destination = Path(args.output).expanduser().resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(serialized + os.linesep, encoding="utf-8")
        print("Report saved to: " + str(destination), file=sys.stderr)
    print(serialized)
    return 0 if all(
        p.get("candidate_status") not in ("FAIL_OR_UNREACHABLE", "SCHEMA_UNEXPECTED")
        for p in report["providers"]
    ) else 2


if __name__ == "__main__":
    raise SystemExit(main())
