---
title: IPO Forensic Analysis Engine — Implementation Blueprint and Data Contract
document_id: IB-IPO-001
version: 1.0
status: Frozen P0 contract; case-persistence slice implemented on review branch; full application and runtime verification remain incomplete
last_updated: 29 October 2026
canonical_source: Markdown in GitHub
scope: Indian Mainboard IPOs only; local-first; single-user; manual-first; ₹0 total budget
---

# Implementation Blueprint and Data Contract

## 1. Purpose, authority and freeze rules

This is the canonical **implementation blueprint** for the first build. It combines the P0 Data Contract with the planned repository/file layout, file ownership, backend module boundaries, frontend routes, API variables, shared status values, local file storage, runtime configuration and build sequence.

It answers three questions:
1. **What are we building?** A local-first, single-user IPO research web application.
2. **What files/modules will own it?** The repository tree in Section 4 and responsibility map in Section 5.
3. **How do frontend and backend communicate?** The exact API paths, JSON property names, nullability, enums, timestamp and decimal rules in Sections 7–13.

This file is the canonical source for the **API/wire contract and target application code layout**. The existing [Application Flow](app-flow.md) remains authoritative for user-visible steps and screen behaviour. [Technical Design](TECHNICAL_DESIGN.md) remains authoritative for architectural rationale and system principles. [Database Schema](database-schema.md) remains authoritative for persisted relational schema and must stay aligned with this file. The PRD, Indicator Catalogue, Data Source & Feasibility Audit and UI/UX Design remain authoritative for their respective product, analytical, source and visual decisions.

### 1.1 Binding build decisions

| Area | Decision | Status |
|---|---|---|
| Product scope | Indian Mainboard IPOs only; SME analysis is out of scope | Fixed |
| Budget | ₹0 total budget; no paid APIs, datasets, hosting, AI, private UI kits or paid fallback services | Fixed |
| Application shape | One repository, local web frontend + local API + local database/files | Fixed |
| Frontend | React + TypeScript + Vite SPA | Fixed for P0 |
| Routing | React Router | Fixed for P0 |
| Styling | Plain CSS with centralized design tokens and the approved UI/UX specification | Fixed for P0 |
| Motion | CSS for simple states; free/open-source Motion for React for complex motion | Fixed, subject to compatible version pinning |
| Backend | Python + FastAPI | Fixed for P0 |
| Request/response validation | Pydantic v2 models + FastAPI OpenAPI schema | Fixed for P0 |
| Wire JSON property casing | camelCase | Fixed |
| Python names | snake_case | Fixed |
| TypeScript names | camelCase for variables/properties; PascalCase for React components/types | Fixed |
| API path prefix | /api/v1 | Fixed |
| API/TS type consistency | Generate TypeScript API types from backend OpenAPI; generated files are never hand-edited | Fixed |
| Database | SQLite | Fixed |
| ORM and migrations | SQLAlchemy 2.x + Alembic | Adopted for P0; pin compatible supported versions during scaffold |
| Financial arithmetic | Python Decimal, never JavaScript floating-point or binary float as authoritative money | Fixed |
| Numeric API values | Decimal values crossing the JSON boundary are strings | Fixed |
| Uploaded evidence | Original files stored locally; SQLite stores metadata/checksum/relative path | Fixed |
| P0 extraction | PDF extraction may produce untrusted candidates; user review required | Fixed |
| Reports | Immutable report snapshot, HTML preview and DOCX export first | Fixed; verify offline DOCX export in tests |
| PDF export | Not promised for P0; reconsider only after a free offline conversion path is tested | Deferred |
| AI | No AI provider required; an optional later adapter may not invent evidence or results | Fixed |
| External source connectors | Build provider-neutral acquisition orchestrator now; enable each connector only after terms, free access, coverage, timestamps and failure behaviour pass the audit gate | Fixed |
| Jobs/microservices | Synchronous local API calls for P0; no Redis, Celery, Kafka, microservices or hosted database | Fixed |
| Authentication | No login/account system; backend binds to loopback only | Fixed |
| Broker/trading integration | None | Out of scope |
| Hero component | Do not select/implement until the owner provides the exact 21st.dev component URL/code | Existing owner decision; still open |

These are implementation choices, not claims that the app, dependencies or tests already exist or work. Dependency versions must be checked for compatibility, pinned in lockfiles and validated in the local scaffold.

### 1.2 Frozen versus deliberately not invented

Route shapes, JSON property names, core enums, error envelope, identity flow, money/time conventions, file layout and P0 module boundaries are frozen here. A contract change requires a deliberate edit to this file plus corresponding backend models, OpenAPI-generated types, database schema/migration and tests.

The actual indicator/formula catalogue, which rules are enabled in the first P0 formula register, and which third-party data connectors are approved are **not** invented here. Use the existing Indicator Catalogue and dated Data Source & Feasibility Audit as the authorities. An endpoint or module may exist before a provider is enabled; the app must report “not enabled” honestly.

---

## 2. System shape and request/data flow

Run the app as two local development processes while building:

- Frontend: Vite at http://127.0.0.1:5173.
- Backend: FastAPI at http://127.0.0.1:8000.
- API base URL: http://127.0.0.1:8000/api/v1.
- Data: per-user local application-data directory outside the Git repository.

When packaged/served locally later, the frontend may be built to static assets, but the Python API and local data directory remain. Do not add Next.js: server-side rendering/SEO is not needed for this local single-user product, and the existing technical design calls for a Vite SPA.

A normal request follows this flow:

1. React page gathers user input and calls a typed API function.
2. The shared API client sends JSON or a multipart upload to FastAPI.
3. Pydantic validates the request and rejects unknown fields.
4. The route calls an application/domain service; route handlers must not implement financial formulas or database workflows themselves.
5. The service applies product rules, calls repositories, and coordinates evidence storage or deterministic engines as needed.
6. SQLAlchemy persists structured records; the file store persists original evidence/export files. Changes that must succeed together use a database transaction plus cleanup/compensation for filesystem failures.
7. FastAPI returns a response validated by Pydantic and serialized with camelCase property names.
8. React handles the returned status; show “Saved” only after the server confirms persistence.

Source retrieval, parsing and analysis must not run inside React components. The browser never connects directly to a provider source or SQLite.

---

## 3. Toolchain, runtime and environment variables

### 3.1 Frontend dependencies

Use compatible pinned versions of React, React DOM, TypeScript, Vite, React Router, Motion for React (package name motion; imports from motion/react), and a free icon library only if needed. Use CSS and the tokens in docs/design.md; do not add an unapproved paid component library or CSS framework.

Development/test tooling: ESLint, TypeScript compiler, Vitest, React Testing Library and Playwright for the core end-to-end acceptance test. Generate/check API types with openapi-typescript or a compatible OpenAPI TypeScript generator. Exact installed versions belong in package-lock.json after scaffold validation, not in this file before testing.

Required commands in frontend/package.json:

| Command | Required behaviour |
|---|---|
| npm run dev | Start Vite on 127.0.0.1:5173 |
| npm run build | Run type-checking and create production frontend build |
| npm run typecheck | Run tsc --noEmit with strict TypeScript settings |
| npm run lint | Run ESLint |
| npm run test | Run frontend unit/component tests |
| npm run test:e2e | Run Playwright core flow when configured |
| npm run api:types | Regenerate TS API types from FastAPI OpenAPI |

Vite transpilation alone is not a TypeScript type-check. The build must fail when type-checking fails.

### 3.2 Backend dependencies

Adopt Python, FastAPI, Pydantic v2, Uvicorn, SQLAlchemy 2.x, Alembic, and standard-library Decimal/pathlib/hashlib/zipfile support as appropriate. Use pypdf for text extraction and python-docx for DOCX export only after representative offline tests. Use httpx for approved HTTP adapters and API tests. Use pytest and FastAPI TestClient/HTTPX for tests.

Do not add OCR, a PDF conversion executable, an AI package, or a new external provider just because it might be useful. Validate representative PDFs and export files before enabling a feature that depends on a library or OS executable.

### 3.3 Environment variables

These are the P0 configuration variables. They are configuration names, not evidence or user-entered data.

| Variable | Default | Meaning |
|---|---|---|
| IPOFA_DATA_DIR | Platform-specific per-user application-data directory | Optional override for database/evidence/reports/backups. Tests use a temporary directory. Never default to repository root. |
| IPOFA_API_HOST | 127.0.0.1 | FastAPI bind host. Never default to 0.0.0.0. |
| IPOFA_API_PORT | 8000 | FastAPI port. |
| IPOFA_ALLOWED_ORIGINS | http://127.0.0.1:5173,http://localhost:5173 | Explicit local-development CORS origins. |
| IPOFA_MAX_UPLOAD_BYTES | 26214400 | Maximum upload size: 25 MiB. |
| IPOFA_HTTP_TIMEOUT_SECONDS | 15 | Per-request timeout for any later approved source adapter. |
| IPOFA_LOG_LEVEL | INFO | Log threshold; omit document contents, secrets and unnecessary absolute paths. |
| VITE_API_BASE_URL | http://127.0.0.1:8000/api/v1 | Frontend API base URL; Vite variables start with VITE_. |

Provide backend/.env.example and frontend/.env.example. Real .env files are local-only and gitignored. P0 does not need API keys or credentials. Do not add speculative provider-key variables until a provider has passed its approval gate.

### 3.4 Local data directory

Use platform application-data conventions:

- Windows: %LOCALAPPDATA%/IPOForensicAnalysis/
- macOS: ~/Library/Application Support/IPOForensicAnalysis/
- Linux: $XDG_DATA_HOME/ipo-forensic-analysis/, falling back to ~/.local/share/ipo-forensic-analysis/

IPOFA_DATA_DIR overrides the default for tests or explicit owner configuration.

Target layout:

    <IPOFA_DATA_DIR>/
      ipo_forensic.sqlite3
      evidence/
        <caseId>/
          <evidenceId>/
            original.pdf
      reports/
        <caseId>/
          <reportId>/
            report.json
            exports/
              <artifactId>.docx
              <artifactId>.html
      backups/
        <backupId>.zip
      tmp/
      logs/

Database records store safe relative paths, never absolute paths. Public API responses do not return internal filesystem paths. Downloads go through API routes that verify the resource belongs to the requested case. Originals are SHA-256 hashed; replacing a file creates a new evidence version rather than silently overwriting it. Temporary files are cleaned up on success/failure. Real case databases, uploaded files, reports, backups, caches and logs must never be committed to Git.

---

## 4. Complete target repository/file layout

This is the planned application layout. Create files phase by phase when their responsibilities are implemented; do not create dozens of empty placeholders. File names are fixed unless a concrete technical incompatibility is documented and the change is recorded here.

    ipo-forensic-analysis/
      .github/
        workflows/
          ci.yml
      README.md
      AGENTS.md
      CLAUDE.md
      .gitignore
      docs/
        IPO_Forensic_Analysis_Project_Brief_v1.0.md
        IPO_Forensic_Analysis_PRD_v1.0_APPROVED.md
        IPO_Indicator_Catalogue_and_Data_Dictionary_v1.0.md
        IPO_Data_Source_and_Feasibility_Audit_v1.0.md
        app-flow.md
        design.md
        TECHNICAL_DESIGN.md
        database-schema.md
        implementation-blueprint.md
        implementation-plan.md
      scripts/
        check_contract.py
        create_test_fixtures.py
      frontend/
        package.json
        package-lock.json
        index.html
        vite.config.ts
        tsconfig.json
        eslint.config.js
        playwright.config.ts
        .env.example
        src/
          main.tsx
          App.tsx
          app/
            router.tsx
          api/
            client.ts
            errors.ts
            cases.ts
            identity.ts
            evidence.ts
            facts.ts
            observations.ts
            acquisition.ts
            analysis.ts
            scenarios.ts
            reports.ts
            local-data.ts
            generated/
              schema.d.ts
              .gitkeep
          components/
            layout/
              AppShell.tsx
              PageHeader.tsx
            feedback/
              StatusBadge.tsx
              LoadingState.tsx
              EmptyState.tsx
              ErrorState.tsx
              ErrorSummary.tsx
              ConfirmDialog.tsx
            forms/
              FormField.tsx
              FileUploadField.tsx
            evidence/
              EvidenceCitation.tsx
            findings/
              FindingCard.tsx
            hero/
              ResearchHero.tsx
          pages/
            CasesPage.tsx
            NewCasePage.tsx
            CaseOverviewPage.tsx
            EvidencePage.tsx
            FactsPage.tsx
            AnalysisPage.tsx
            RunDetailPage.tsx
            ScenariosPage.tsx
            ReportPage.tsx
            SettingsPage.tsx
          features/
            cases/
              CaseForm.tsx
              IssueIdentityPanel.tsx
            evidence/
              EvidenceList.tsx
              EvidenceUploadForm.tsx
              ExtractionReviewPanel.tsx
            facts/
              FactEntryForm.tsx
              FactTable.tsx
              ConflictReviewPanel.tsx
            acquisition/
              AcquisitionStatusPanel.tsx
            analysis/
              ReadinessPanel.tsx
              ResultsTable.tsx
              FindingsList.tsx
            scenarios/
              ScenarioForm.tsx
              ScenarioResultCard.tsx
            reports/
              ReportContent.tsx
              ExportControls.tsx
          lib/
            format.ts
            dates.ts
          styles/
            tokens.css
            global.css
        tests/
          setup.ts
          App.test.tsx
          cases.test.tsx
          evidence.test.tsx
          facts.test.tsx
          analysis.test.tsx
          scenarios.test.tsx
      backend/
        pyproject.toml
        alembic.ini
        .env.example
        migrations/
          env.py
          script.py.mako
          versions/
            0001_initial_schema.py
        app/
          __init__.py
          main.py
          config.py
          database.py
          ids.py
          errors.py
          api/
            __init__.py
            router.py
            dependencies.py
            routes/
              health.py
              cases.py
              identity.py
              evidence.py
              facts.py
              observations.py
              acquisition.py
              analysis.py
              scenarios.py
              reports.py
              local_data.py
          schemas/
            __init__.py
            common.py
            cases.py
            identity.py
            evidence.py
            facts.py
            observations.py
            acquisition.py
            analysis.py
            scenarios.py
            reports.py
            local_data.py
          domain/
            __init__.py
            enums.py
            decimals.py
            timestamps.py
            identity.py
            freshness.py
            conflicts.py
          models/
            __init__.py
            identity.py
            research_case.py
            evidence.py
            facts.py
            analysis.py
            scenarios.py
            reports.py
          repositories/
            cases.py
            identity.py
            evidence.py
            facts.py
            observations.py
            acquisition.py
            analysis.py
            scenarios.py
            reports.py
          services/
            cases.py
            identity.py
            evidence.py
            facts.py
            observations.py
            acquisition.py
            analysis.py
            scenarios.py
            reports.py
            local_data.py
          acquisition/
            orchestrator.py
            registry.py
            base.py
            adapters/
              README.md
          extraction/
            pdf_extractor.py
            candidate_mapper.py
          analysis/
            preflight.py
            engine.py
            formula_registry.py
            calculations/
              decimal_math.py
            rules/
              README.md
          storage/
            file_store.py
            hashing.py
            backup_restore.py
          reporting/
            report_model.py
            html_renderer.py
            docx_renderer.py
        tests/
          conftest.py
          unit/
            test_decimal_math.py
            test_identity.py
            test_preflight.py
            test_acquisition_orchestrator.py
            test_scenarios.py
            test_report_model.py
          integration/
            test_cases_api.py
            test_evidence_api.py
            test_facts_api.py
            test_acquisition_api.py
            test_analysis_api.py
            test_reports_api.py
            test_backup_restore.py
          contract/
            test_openapi_contract.py
          fixtures/
            README.md

### 4.1 File ownership rules

| File/module | Owns | Must not own |
|---|---|---|
| frontend/src/main.tsx | React entry and global styles | Business/API logic |
| frontend/src/App.tsx | Root shell/providers and router mount | Data access or formulas |
| frontend/src/app/router.tsx | Route definitions and not-found state | Backend endpoint definitions |
| frontend/src/api/client.ts | Base URL, fetch wrapper, JSON/multipart, safe error conversion | Feature-specific UI |
| frontend/src/api/generated/schema.d.ts | Generated OpenAPI types only | Hand-written edits |
| frontend/src/api/*.ts | Typed calls for one resource group | Wire field definitions that contradict OpenAPI |
| frontend/src/pages/*.tsx | Screen composition and user journey | Authoritative finance calculations or SQL |
| frontend/src/features/* | Reusable workflow panels/forms | Alternate copies of API types |
| frontend/src/components/* | Reusable presentational components | Hidden network requests |
| backend/app/main.py | FastAPI construction, router inclusion, CORS, lifespan and exception handlers | Domain logic |
| backend/app/api/routes/*.py | HTTP parsing/status codes, dependency injection and service calls | SQL-heavy code or formulas |
| backend/app/schemas/*.py | Pydantic request/response models and JSON aliases | Persistence queries/business workflow |
| backend/app/services/*.py | Application use cases and transaction orchestration | HTTP framework details |
| backend/app/models/*.py | SQLAlchemy table models and relational constraints | API presentation logic |
| backend/app/repositories/*.py | Database queries/persistence | Provider HTTP calls/report rendering |
| backend/app/acquisition/* | Provider-neutral orchestration and adapter boundary | Unapproved web scraping |
| backend/app/extraction/* | Local PDF extraction to untrusted candidates | Automatically accepting extracted values |
| backend/app/analysis/* | Readiness, deterministic formulas/rules, immutable run snapshots | AI-generated arithmetic |
| backend/app/storage/* | Safe local paths, hashes, backup/restore | Exposing raw local paths |
| backend/app/reporting/* | Report snapshot and HTML/DOCX rendering | Re-running analysis during export |
| backend/migrations/* | Versioned schema evolution | Ad-hoc startup schema mutation |
| tests | Verify one layer or end-to-end contract | Fake success statuses masking unavailable providers |

No single “main Python file” should contain the whole app. main.py is a small entry point; routes, schemas, services, persistence, acquisition, analysis, storage and reporting have explicit responsibilities.

### 4.2 File creation order

1. Scaffold/configuration, health endpoint, frontend shell, API client and test setup.
2. Shared Pydantic schemas, OpenAPI type generation, SQLAlchemy models/migration, case and identity.
3. Evidence file/metadata, manual facts and observations, review UI.
4. Acquisition orchestrator and adapter registry; no third-party adapter is enabled until approved.
5. Formula registry, readiness and run snapshots.
6. First cross-signal rules and finding lineage.
7. Scenario definitions/results, report snapshot and HTML/DOCX renderers.
8. Backup/restore, full end-to-end tests and release checks.

A file listed in the target tree is planned, not claimed to exist yet. Add source-specific modules only after their source passes the audit gate. The adapters/README.md and rules/README.md document registration contracts while those folders have no approved provider/rule implementation.

---

## 5. Backend domain models and fixed identifiers

Use UUIDv4 identifiers generated by the backend and stored as canonical lowercase UUID strings. Identifiers are opaque to the UI. Never use issuer display name, ticker, publisher name or URL as a primary key.

| Identifier/property | Meaning |
|---|---|
| caseId | Stable local research case identifier |
| issueId | Confirmed IPO issue record identifier |
| issuerId | Issuer/company identifier distinct from the issue |
| candidateId | Saved identity candidate from a discovery pass |
| sourceId | Registry entry identifying a publisher/provider |
| acquisitionAttemptId | One real source/category retrieval attempt |
| evidenceId | Local document, source capture, manual note or manual-value evidence |
| factId | One company/offer/financial fact record |
| observationId | One time-sensitive market/subscription/GMP observation |
| analysisRunId | One immutable deterministic analysis run |
| resultId | One formula result emitted by a run |
| findingId | One rule/cross-signal finding for a specific run |
| scenarioId | One saved set of user assumptions |
| scenarioResultId | One scenario calculation under one run |
| reportId | Immutable structured report snapshot tied to one run |
| artifactId | One rendered report/export file |
| requestId | API diagnostic ID; not a user-data primary key |

Database column names remain snake_case. API JSON uses camelCase. These are two representations of the same logical concept.

### 5.1 Case and issue semantics

- New case: caseStatus = identity_pending; identityStatus = unresolved; issue = null.
- Ambiguous match: identityStatus = ambiguous; issue = null until the user resolves it.
- Confirmed Mainboard issue: identityStatus = confirmed; issue is present; caseStatus = active.
- Out-of-scope SME result: identityStatus = out_of_scope; no supported SME analysis is created.
- Archived case: caseStatus = archived; history remains readable.

A discovery candidate's marketSegment may be MAINBOARD, SME or UNKNOWN. A persisted confirmed ipo_issue must have marketSegment = MAINBOARD. Never allow a client to change the market segment of an already-confirmed issue without a dedicated identity-review workflow and evidence.

### 5.2 Source identity and evidence integrity

Source names do not imply approval. A source-registry item has an accessStatus and connectorStatus. A source may be public but still not approved for automated collection/reuse. Acquisition attempts record real attempts; a disabled provider is shown in provider state but does not get a fake successful attempt.

Facts and market observations keep source-specific values separately. Do not silently merge, overwrite, average or claim independence for republished observations. A correction creates a new fact/observation or marks the previous record superseded with a reason; the old row remains auditable.

---

## 6. Canonical JSON, timestamp, money and status rules

### 6.1 Casing and strictness

- JSON request/response properties are camelCase.
- Python functions/fields/modules and database columns are snake_case.
- TypeScript properties/functions are camelCase; React components and TS types are PascalCase.
- Pydantic schemas use one shared camelCase alias generator and serialize by alias. Request models reject unknown fields using extra = "forbid".
- FastAPI OpenAPI is the contract source. Generate frontend API types into frontend/src/api/generated/schema.d.ts. Never patch that generated file by hand.
- Backend validation is authoritative even if React validates first.

### 6.2 Identifiers

- API IDs are strings containing canonical UUIDv4 values.
- Every child resource must belong to the supplied parent case/run/report.
- If an evidenceId from another case is supplied, return a not-found/ownership error rather than leaking its existence or path.
- IDs never encode meaning; the UI must not parse them.

### 6.3 Dates and timestamps

- Date-only values use YYYY-MM-DD for IPO/financial period dates.
- Instants use RFC 3339 / ISO 8601 with explicit offset; persistence normalizes instants to UTC. Example: 2026-10-29T10:00:40+05:30.
- observedAt = when the value applies/was observed according to source.
- publishedAt = when the publisher says the item was published.
- retrievedAt = when the app retrieved it from a source.
- recordedAt = when the value was entered/registered locally.
- createdAt/updatedAt = persistence audit timestamps, not market-observation timestamps.
- Unknown event/publication/observation times are null. Never infer observedAt from retrievedAt or feed generatedAt.
- Analysis requires explicit informationCutoffAt. Preflight returns the effective cutoff; the run request sends that exact timestamp if the cutoff is unchanged.

### 6.4 Monetary/decimal values

All monetary amounts, prices, percentages and ratios requiring decimal precision cross the API as **decimal strings**, never JSON floating-point numbers. Examples: "150", "150.25", "12.5", "-2.75". No exponent notation, NaN or Infinity. Integer counts (shares, quantity, page numbers, bytes and counts) use JSON integers.

- Backend arithmetic uses decimal.Decimal and documented rounding at the defined result/display boundary.
- The frontend displays returned values; it is not the authoritative financial calculator.
- Unknown decimal = null plus status/reason; never an empty string or zero sentinel.
- Price band uses nullable priceBandLow and priceBandHigh decimal strings.
- Currency code is INR internally/API-facing; the UI may display ₹.
- Zero is valid only when actually observed/calculated and allowed by source semantics.

### 6.5 Exact P0 status enums

These values are contract constants. Keep spelling and case exactly as listed.

| Enum | Values |
|---|---|
| CaseStatus | identity_pending, active, archived |
| IdentityStatus | unresolved, ambiguous, confirmed, out_of_scope, rejected |
| CandidateMarketSegment | MAINBOARD, SME, UNKNOWN |
| EvidenceKind | document, web_page, manual_note, manual_value, imported_file |
| EvidenceVerificationStatus | unverified, reviewed, rejected, superseded |
| FactReviewStatus | candidate, accepted, rejected, conflicted, superseded |
| ObservationReviewStatus | candidate, accepted, rejected, conflicted, superseded |
| EntryMethod | manual, extracted_candidate, imported, connector, derived |
| ConnectorAccessStatus | unreviewed, approved, blocked, unavailable |
| ConnectorStatus | enabled, not_enabled, blocked, unavailable |
| AcquisitionAttemptStatus | succeeded, partial, unavailable, blocked, failed |
| AcquisitionCategoryStatus | found, partial, not_enabled, not_attempted, blocked, unavailable, failed, stale, conflicted |
| SignalCategory | issue_terms, company_financials, valuation, subscription_qib, subscription_nii, subscription_retail, gmp, market_context, company_events |
| ReadinessStatus | ready, qualified, blocked |
| ReadinessSeverity | info, warning, blocking |
| AnalysisRunStatus | completed, partial, failed |
| CalculationStatus | calculated, qualified, skipped, not_applicable, invalid |
| FindingSeverity | info, low, medium, high, critical |
| FindingStatus | active, unresolved, not_run, superseded |
| EvidenceLinkRole | supports, contradicts, context |
| ReviewAction | accept, reject, mark_conflicted, supersede |
| ScenarioCalculationStatus | calculated, incomplete, not_applicable |
| ReportExportFormat | html, docx |
| RestoreValidationStatus | valid, invalid, incompatible |

AcquisitionCategoryStatus describes source/category coverage in the UI; AcquisitionAttemptStatus describes a real persisted attempt. A failed attempt and a not-enabled provider are not the same. Freshness/conflict is evaluated against actual timestamps and records; do not rewrite source history to set a stale flag without retaining the underlying evidence.

---

## 7. Common API envelope and conventions

Base path: /api/v1

All successful JSON responses use the property names/nullability below and are validated against Pydantic response models. Binary downloads return file responses, not JSON.

### 7.1 Standard error envelope

All API errors use this shape, including normalized request-validation failures:

~~~json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Review the highlighted fields and try again.",
    "details": [
      {
        "field": "enteredName",
        "issueCode": "required",
        "message": "Enter an IPO or issuer name."
      }
    ],
    "requestId": "8fc9b640-9e4e-4c57-b0d7-2f965850c211"
  },
  "timestamp": "2026-10-29T10:00:40Z"
}
~~~

- details is an array and may be empty.
- field and issueCode may be null when not applicable.
- requestId is a UUID per request, included in the response and safe to show/copy for debugging.
- Error messages are actionable but never include stack traces, credentials, full private paths or uploaded document content.
- Unexpected failures are logged with requestId and a redacted diagnostic, then return INTERNAL_ERROR.

### 7.2 Fixed error codes

| HTTP status | Error code | Meaning |
|---|---|---|
| 400 | INVALID_REQUEST | Request malformed or logically inconsistent |
| 404 | NOT_FOUND | Resource not found in the supplied context |
| 409 | IDENTITY_UNRESOLVED | Identity must be confirmed before this action |
| 409 | IDENTITY_AMBIGUOUS | More than one issue remains plausible |
| 409 | OUT_OF_SCOPE_SME | SME issue outside product scope |
| 409 | ANALYSIS_BLOCKED | No permitted useful run can execute; includes readiness details |
| 409 | CONFLICT_UNRESOLVED | Required fact conflict remains unresolved |
| 409 | SOURCE_NOT_ENABLED | Requested source adapter is not enabled |
| 409 | RESTORE_CONFIRMATION_REQUIRED | Restore requires explicit confirmation |
| 413 | FILE_TOO_LARGE | Upload exceeds IPOFA_MAX_UPLOAD_BYTES |
| 415 | UNSUPPORTED_FILE_TYPE | File type not accepted |
| 422 | VALIDATION_ERROR | Field/type/constraint validation failed |
| 422 | FILE_PARSE_FAILED | Extraction failed; original file remains saved |
| 429 | SOURCE_RATE_LIMITED | Approved adapter was rate limited |
| 500 | STORAGE_ERROR | Local SQLite/filesystem persistence failed |
| 500 | INTERNAL_ERROR | Unexpected server error |

Field errors/readiness details appear inside error.details with stable issueCode values. A provider network failure normally belongs in an acquisition result, not a global HTTP 500, because manual work may continue.

### 7.3 API compatibility

- All first-version routes live under /api/v1.
- A breaking payload/enum/nullability change requires edits to this file, Pydantic models, database migration if affected, generated TS types, API client and contract tests.
- Preserve backward compatibility for saved data through Alembic migrations.
- Avoid hidden defaults where the choice materially changes analysis. Return and persist the effective default.
- Do not expose SQLite table names as public API properties unless explicitly specified below.

---

## 8. Exact P0 HTTP API route inventory

All paths are relative to /api/v1. {caseId}, {evidenceId}, {factId}, {observationId}, {analysisRunId}, {scenarioId}, {reportId}, {artifactId} and {backupId} are UUID path parameters. Child resources must belong to the supplied parent case/run/report.

| Method and path | Request | Success response | Purpose |
|---|---|---|---|
| GET /health | None | HealthResponse | API/local-storage health; not source coverage |
| GET /cases | Optional query status | CaseListResponse | List cases |
| POST /cases | CreateCaseRequest | 201 CaseDetail | Create case before identity resolution |
| GET /cases/{caseId} | None | CaseDetail | Reopen case |
| PATCH /cases/{caseId} | UpdateCaseRequest | CaseDetail | Update title only |
| POST /cases/{caseId}/archive | None | CaseDetail | Archive a case without deleting its records/history |
| POST /cases/{caseId}/identity/discover | IdentityDiscoveryRequest | IdentityDiscoveryResponse | Discover through actually enabled/approved mechanisms and report unavailable/not-enabled accurately |
| POST /cases/{caseId}/identity/confirm | ConfirmIdentityRequest | CaseDetail | Confirm evidence-backed Mainboard identity |
| GET /cases/{caseId}/acquisition/attempts | Optional signalCategory | AcquisitionAttemptListResponse | View actual persisted attempts |
| POST /cases/{caseId}/acquisition/run | AcquisitionRunRequest | AcquisitionRunResponse | Run provider-neutral orchestrator |
| GET /cases/{caseId}/evidence | Optional evidenceKind | EvidenceListResponse | List evidence |
| POST /cases/{caseId}/evidence | CreateEvidenceRequest | 201 EvidenceItem | Register URL/manual note/manual-value evidence |
| POST /cases/{caseId}/evidence/files | multipart file + metadata | 201 EvidenceItem | Save a PDF locally |
| GET /cases/{caseId}/evidence/{evidenceId} | None | EvidenceItem | Evidence metadata and safe download URL |
| GET /cases/{caseId}/evidence/{evidenceId}/download | None | PDF binary | Download original after ownership checks |
| POST /cases/{caseId}/evidence/{evidenceId}/extract | None | ExtractionResponse | Create candidate facts from a local PDF; never auto-accept |
| GET /cases/{caseId}/facts | Optional indicatorCode, reviewStatus | FactListResponse | List facts |
| POST /cases/{caseId}/facts | CreateFactRequest | 201 FactRecord | Add evidence-linked fact |
| POST /cases/{caseId}/facts/{factId}/review | ReviewRecordRequest | FactRecord | Review without overwriting raw fact |
| GET /cases/{caseId}/observations | Optional indicatorCode, signalCategory, reviewStatus | ObservationListResponse | List time-sensitive observations |
| POST /cases/{caseId}/observations | CreateObservationRequest | 201 MarketObservation | Add source-linked observation |
| POST /cases/{caseId}/observations/{observationId}/review | ReviewRecordRequest | MarketObservation | Review observation and preserve history |
| GET /cases/{caseId}/analysis/readiness | Optional informationCutoffAt | AnalysisReadiness | Explain blockers/warnings |
| POST /cases/{caseId}/analysis-runs | CreateAnalysisRunRequest | 201 AnalysisRunDetail | Run deterministic analysis and save immutable snapshot |
| GET /cases/{caseId}/analysis-runs | None | AnalysisRunListResponse | List historical runs |
| GET /cases/{caseId}/analysis-runs/{analysisRunId} | None | AnalysisRunDetail | Reopen exact run/results/findings |
| POST /cases/{caseId}/scenarios | CreateScenarioRequest | 201 ScenarioDefinition | Save user assumptions |
| GET /cases/{caseId}/scenarios | None | ScenarioListResponse | List case scenarios |
| POST /cases/{caseId}/analysis-runs/{analysisRunId}/scenario-results | EvaluateScenarioRequest | 201 ScenarioResult | Evaluate scenario under a saved run |
| GET /cases/{caseId}/analysis-runs/{analysisRunId}/scenario-results | None | ScenarioResultListResponse | List calculations attached to that run |
| GET /cases/{caseId}/reports | None | ReportListResponse | List saved reports |
| POST /cases/{caseId}/reports | CreateReportRequest | 201 ReportDetail | Save immutable report snapshot; no analysis rerun |
| GET /cases/{caseId}/reports/{reportId} | None | ReportDetail | Preview/reopen saved report |
| POST /cases/{caseId}/reports/{reportId}/exports | CreateReportExportRequest | 201 ReportArtifact | Render HTML or DOCX from the report snapshot |
| GET /cases/{caseId}/reports/{reportId}/exports/{artifactId}/download | None | File binary | Download a saved artifact |
| POST /local-data/backups | None | BackupResponse | Create ZIP backup plus manifest/checksums |
| GET /local-data/backups/{backupId}/download | None | ZIP binary | Download backup |
| POST /local-data/restore/validate | multipart backup file | RestoreValidationResponse | Validate without replacing live data |
| POST /local-data/restore | RestoreRequest | RestoreResponse | Restore after explicit confirmation and a safety backup |

No provider-specific endpoints are exposed. Provider selection/credentials must not be user-controlled URL inputs. The orchestrator owns approved adapters, allowlisted source domains, timeouts and rate limits.

---

## 9. Exact request and response fields

### 9.1 Health

HealthResponse:
- status: ok | degraded
- appVersion: string
- apiVersion: "v1"
- databaseStatus: ok | error
- dataDirectoryStatus: ok | error
- timestamp: RFC3339 timestamp

status = degraded if required local storage is not healthy. Disabled sources do not make the core API unhealthy.

### 9.2 Cases

CreateCaseRequest:
- enteredName: string, required, trimmed, 2–200 characters.
- title: string | null, optional, maximum 160 characters. If omitted/null, derive a display title from enteredName.
- issueId is not accepted on create. A symbol/ticker is not required.

UpdateCaseRequest:
- title: string, trimmed, 1–160 characters.
- Other properties are forbidden.

CaseDetail:
- caseId: UUID string.
- enteredName: string.
- title: string.
- caseStatus: CaseStatus.
- identityStatus: IdentityStatus.
- issue: ConfirmedIssue | null.
- createdAt, updatedAt, lastActivityAt: RFC3339 timestamps.
- latestAnalysisRunId: UUID string | null.
- latestReportId: UUID string | null.
- caseChangedSinceLastRun: boolean.
- readinessSummary: ReadinessStatus | null.
- warningCount: integer >= 0.

ConfirmedIssue:
- issueId, issuerId: UUID strings.
- issuerLegalName, displayName: strings.
- marketSegment: "MAINBOARD" only.
- openDate, closeDate, listingDate: date string | null.
- priceBandLow, priceBandHigh: DecimalString | null.
- issueSizeAmount: DecimalString | null.
- issueSizeUnit: string | null.
- identifiers: IssueIdentifier[].
- identityEvidenceIds: UUID string[].

IssueIdentifier:
- identifierType, identifierValue: non-empty bounded strings.
- sourceId, evidenceId: UUID string | null.

CaseListResponse:
- items: CaseSummary[].
- total: integer >= 0.

GET /cases optional query status is CaseStatus; when omitted, return all cases in lastActivityAt descending order. Do not add offset/cursor pagination in P0. GET evidence optional evidenceKind is EvidenceKind. GET facts reviewStatus is FactReviewStatus. GET observations reviewStatus is ObservationReviewStatus; signalCategory/indicatorCode filters are exact enum/catalogue values. Unknown query values return VALIDATION_ERROR, not an empty list.

POST /cases/{caseId}/archive returns the updated CaseDetail. It does not delete data or files. A case may be archived in any identity state. All archived cases remain readable/exportable and are included by GET /cases unless filtered. No destructive case deletion exists in P0.

CaseSummary fields: caseId, enteredName, title, caseStatus, identityStatus, issueDisplayName: string | null, lastActivityAt, latestAnalysisRunId: UUID string | null, latestReportId: UUID string | null, warningCount: integer. Do not invent issue metadata.

### 9.3 Issue discovery and confirmation

IdentityDiscoveryRequest:
- additionalContext: string | null, maximum 1000 characters.
- knownIdentifiers: IssueIdentifierInput[]; default empty array.

IssueIdentifierInput:
- identifierType: string.
- identifierValue: string.

IdentityDiscoveryResponse:
- caseId: UUID string.
- discoveryStatus: found | partial | not_enabled | unavailable | failed.
- candidates: IssueCandidate[].
- sourceStates: SourceStateSummary[].
- attempts: AcquisitionAttemptSummary[]; only real attempts, not disabled-provider placeholders.
- checkedAt: RFC3339 timestamp.

IssueCandidate:
- candidateId: UUID string.
- issuerLegalName: string | null.
- displayName: string.
- marketSegment: CandidateMarketSegment.
- openDate, closeDate, listingDate: date string | null.
- priceBandLow, priceBandHigh: DecimalString | null.
- identifiers: IssueIdentifier[].
- sourceName: string.
- sourceUrl, sourceRecordId: string | null.
- evidenceIds: UUID string[].
- candidateNotes: string | null.
- discoveredAt: RFC3339 timestamp.

ConfirmIdentityRequest:
- exactly one of candidateId or manualIssue is required.
- candidateId: UUID string | null.
- manualIssue: ManualIssueInput | null.
- identityEvidenceIds: UUID string[], minimum 1.
- confirmationNote: string | null, maximum 1000 characters.

ManualIssueInput:
- issuerLegalName, displayName: strings, required, 1–200 characters.
- marketSegment: must equal MAINBOARD.
- openDate, closeDate, listingDate: date string | null.
- priceBandLow, priceBandHigh, issueSizeAmount: DecimalString | null.
- issueSizeUnit: string | null.
- identifiers: IssueIdentifierInput[], default empty.

The backend verifies every identityEvidenceId belongs to the case. Reject confirmation if identity evidence is absent, market segment is SME/UNKNOWN, candidate details materially conflict, or candidateId belongs to another case. If an SME is positively identified, return OUT_OF_SCOPE_SME. A name-string match alone cannot confirm identity.

### 9.4 Evidence

CreateEvidenceRequest (JSON, non-file):
- evidenceKind: web_page | manual_note | manual_value.
- title: string, required, 1–200 characters.
- sourceUrl: valid http/https URL | null; required for web_page.
- publishedAt: RFC3339 timestamp | null.
- notes: string | null, maximum 10,000 characters.
- Client cannot set localRelativePath, sha256, file size or verification status.

File upload (multipart POST /evidence/files):
- file: required binary; P0 accepts PDF only, maximum IPOFA_MAX_UPLOAD_BYTES (25 MiB).
- title: optional string, default safe original filename.
- sourceUrl: optional valid http/https URL.
- publishedAt: optional RFC3339 timestamp.
- notes: optional string, maximum 10,000 characters.

EvidenceItem:
- evidenceId, caseId: UUID strings.
- sourceId: UUID string | null.
- evidenceKind: EvidenceKind.
- title: string.
- sourceUrl, originalFileName, mimeType: string | null.
- sizeBytes: integer | null.
- sha256: 64-character lowercase hexadecimal string | null.
- publishedAt: RFC3339 timestamp | null.
- capturedAt: RFC3339 timestamp.
- locator: string | null.
- verificationStatus: EvidenceVerificationStatus.
- notes: string | null.
- downloadUrl: API-relative URL | null.
- localAvailable: boolean.

Never expose absolute data directory or stored relative path. Original PDFs are immutable; updated files create new evidence items. Failed parsing must not delete the saved original.

ExtractionResponse:
- evidenceId: UUID string.
- extractorStatus: completed | partial | failed.
- candidates: ExtractedFactCandidate[].
- warnings: string[].
- completedAt: RFC3339 timestamp.

ExtractedFactCandidate:
- factId: UUID string for the saved candidate record.
- indicatorCode: string | null; non-null only if mapped to a registered indicator.
- rawValueText: string.
- valueNumeric: DecimalString | null.
- valueText: string | null.
- unit, currency: string | null.
- periodStart, periodEnd, asOfDate: date string | null.
- evidenceId: UUID string.
- pageNumber: integer >= 1 | null.
- locator, quotedContext: string | null.
- reviewStatus: candidate.
- A candidate is not an accepted input until user review.

### 9.5 Facts and review

CreateFactRequest:
- indicatorCode: string, required and present in the approved indicator registry.
- rawValueText: string, required, 1–5000 characters.
- valueNumeric: DecimalString | null.
- valueText: string | null.
- unit, currency: string | null.
- periodStart, periodEnd, asOfDate: date string | null.
- evidenceId: UUID string, required and belongs to this case.
- definitionNote: string | null, maximum 2000 characters.

FactRecord:
- factId, caseId: UUID strings.
- indicatorCode, rawValueText: strings.
- valueNumeric: DecimalString | null.
- valueText, unit, currency: string | null.
- periodStart, periodEnd, asOfDate: date string | null.
- evidenceId: UUID string.
- entryMethod: EntryMethod set by the backend.
- reviewStatus: FactReviewStatus.
- definitionNote: string | null.
- recordedAt, createdAt: RFC3339 timestamps.
- reviewedAt: RFC3339 timestamp | null.
- reviewRationale: string | null.
- supersedesFactId: UUID string | null.

FactListResponse: items: FactRecord[], total: integer >= 0.

ReviewRecordRequest:
- action: ReviewAction.
- rationale: string | null, max 2000 characters; required for mark_conflicted and supersede.
- supersededRecordIds: UUID string[], default empty; may be used with accept/supersede to make conflict resolution explicit.
- Server verifies related records belong to this case and have compatible indicator/period/basis.
- No endpoint edits a raw fact in place. To correct a value, create a replacement with provenance, then mark the former superseded when appropriate.
- Conflict detection groups values by indicator, period, unit/basis and source meaning. Different definitions/periods must not be falsely treated as the same conflict.

### 9.6 Market observations

CreateObservationRequest:
- indicatorCode: string, present in the approved indicator registry.
- signalCategory: SignalCategory.
- segment: QIB | NII | RETAIL | null. Use these values for subscription; otherwise null.
- rawValueText: string, required, 1–5000 characters.
- valueNumeric: DecimalString | null.
- valueText: string | null.
- unit, currency: string | null.
- metricDefinition: string, required, 1–2000 characters. Preserve source denominator/definition where applicable.
- observedAt, publishedAt: RFC3339 timestamp | null.
- retrievedAt: RFC3339 timestamp | null; set only when the process actually knows retrieval time.
- sourceId: UUID string | null.
- evidenceId: UUID string, required and belongs to this case.
- definitionMetadata: JSON object, default empty; validated against a schema, never executable content.

MarketObservation:
- observationId, caseId: UUID strings.
- indicatorCode: string.
- signalCategory: SignalCategory.
- segment: QIB | NII | RETAIL | null.
- rawValueText: string.
- valueNumeric: DecimalString | null.
- valueText, unit, currency: string | null.
- metricDefinition: string.
- observedAt, publishedAt, retrievedAt: RFC3339 timestamp | null.
- recordedAt: RFC3339 timestamp set by server.
- sourceId, acquisitionAttemptId: UUID string | null.
- evidenceId: UUID string.
- entryMethod: EntryMethod set by server.
- reviewStatus: ObservationReviewStatus.
- definitionMetadata: JSON object.
- reviewedAt: RFC3339 timestamp | null.
- reviewRationale: string | null.
- supersedesObservationId: UUID string | null.

ObservationListResponse: items: MarketObservation[], total: integer >= 0.

Subscription data must preserve QIB, NII and RETAIL separately. GMP stays an unofficial secondary observation. Unknown observedAt remains null even when retrievedAt is known. Do not treat feed-generated time as the individual quote time.

### 9.7 Source acquisition

AcquisitionRunRequest:
- signalCategories: SignalCategory[], default to all P0 categories if omitted.
- forceRefresh: boolean, default false; server still enforces adapter rate limits and source policy.
- Client cannot supply arbitrary provider URL, credentials or adapter name.

SourceStateSummary:
- sourceId: UUID string | null.
- sourceName: string.
- signalCategory: SignalCategory.
- accessStatus: ConnectorAccessStatus.
- connectorStatus: ConnectorStatus.
- latestCategoryStatus: AcquisitionCategoryStatus.
- latestAttemptAt, latestObservedAt: RFC3339 timestamp | null.
- message: string.
- latestObservationIds: UUID string[].

AcquisitionAttemptSummary:
- acquisitionAttemptId: UUID string.
- sourceId: UUID string | null.
- sourceName: string.
- signalCategory: SignalCategory.
- status: AcquisitionAttemptStatus.
- startedAt: RFC3339 timestamp.
- finishedAt: RFC3339 timestamp | null.
- returnedFields: string[].
- failureCode, message: string | null.

AcquisitionAttemptListResponse: items: AcquisitionAttemptSummary[], total: integer >= 0.

AcquisitionRunResponse:
- caseId: UUID string.
- startedAt, finishedAt: RFC3339 timestamps.
- overallStatus: found | partial | not_enabled | unavailable | failed.
- categories: CategoryAcquisitionResult[].
- sourceStates: SourceStateSummary[].
- attempts: AcquisitionAttemptSummary[].
- message: string.

CategoryAcquisitionResult:
- signalCategory: SignalCategory.
- status: AcquisitionCategoryStatus.
- observationIds, attemptIds: UUID string[].
- message: string.
- nextAction: string | null.

If no source adapter is approved/enabled, return not_enabled (or another accurate state), preserve the orchestrator result, and still permit manual entry and eligible local analysis. The core orchestrator must exist; provider absence does not justify omitting orchestration, source state, attempt history, error handling or cross-signal readiness.

### 9.8 Analysis readiness and runs

AnalysisReadiness:
- caseId: UUID string.
- status: ReadinessStatus.
- checkedAt, informationCutoffAt: RFC3339 timestamps.
- blockers, warnings: ReadinessIssue[].
- readyFormulaCodes, skippedFormulaCodes: string[].
- eligibleFindingRuleCodes, skippedFindingRuleCodes: string[].
- sourceCoverage: SourceStateSummary[].

ReadinessIssue:
- code: string.
- severity: ReadinessSeverity.
- message: string.
- affectedIndicatorCodes: string[].
- affectedSignalCategories: SignalCategory[].
- evidenceIds: UUID string[].
- nextAction: string | null.

GET readiness accepts optional informationCutoffAt. If omitted, the server sets it once at preflight start and returns that exact value. Send that exact timestamp in the run request if using the same cutoff.

CreateAnalysisRunRequest:
- informationCutoffAt: RFC3339 timestamp, required.
- Client cannot supply formula/rule versions or arbitrary formulas; server owns the enabled version set.

AnalysisRunDetail:
- analysisRunId, caseId: UUID strings.
- runStatus: AnalysisRunStatus.
- informationCutoffAt, startedAt: RFC3339 timestamps.
- finishedAt: RFC3339 timestamp | null.
- schemaVersion, formulaSetVersion, ruleSetVersion, softwareVersion: strings.
- inputSnapshotHash: 64-character lowercase hexadecimal string.
- results: AnalysisResult[].
- findings: Finding[].
- readiness: AnalysisReadiness.
- errorSummary: string | null.

AnalysisResult:
- resultId: UUID string.
- indicatorCode: string.
- calculationStatus: CalculationStatus.
- valueDecimal: DecimalString | null.
- valueText, unit, currency, displayValue: string | null.
- formulaCode, formulaVersion: string | null.
- inputFactIds, inputObservationIds, evidenceIds: UUID string[].
- explanation: string.
- reason: string | null.

Finding:
- findingId: UUID string.
- ruleCode, ruleVersion, findingType: strings.
- severity: FindingSeverity.
- status: FindingStatus.
- title, explanation: strings.
- limitationNote: string | null.
- relatedIndicatorCodes: string[].
- inputFactIds, inputObservationIds: UUID string[].
- evidenceLinks: FindingEvidenceLink[].

FindingEvidenceLink:
- evidenceId: UUID string.
- role: EvidenceLinkRole.
- note: string | null.

AnalysisRunListResponse: items: AnalysisRunSummary[], total: integer >= 0. Each summary has analysisRunId, caseId, runStatus, informationCutoffAt, startedAt, finishedAt and inputSnapshotHash.

Analysis rules:
- Unconfirmed identity blocks issue-specific analysis.
- Missing input blocks/qualifies only affected formulas/rules where possible.
- If no useful eligible calculation exists, do not create a misleading empty completed run; return ANALYSIS_BLOCKED with readiness diagnostics.
- If some calculations legitimately run and others are skipped/qualified, persist runStatus = partial. Use completed only when enabled checks satisfy the approved readiness policy.
- Save immutable input snapshot, source/evidence IDs, units, periods, review states, timestamp semantics, cutoff and formula/rule versions. Do not reconstruct historical output only from mutable live facts.
- Formula meaning comes from the Indicator Catalogue and approved P0 formula register; this file does not invent financial definitions.

### 9.9 Scenario definitions and results

CreateScenarioRequest:
- label: string, required, 1–100 characters.
- entryPrice: DecimalString, required and > 0.
- exitPrice: DecimalString, required and >= 0.
- quantity: integer | null, optional, >= 1 when provided.
- assumptionNote: string | null, maximum 2000 characters.
- Scenario prices are user assumptions, not external observations.

ScenarioDefinition:
- scenarioId, caseId: UUID strings.
- label: string.
- entryPrice, exitPrice: DecimalString.
- quantity: integer | null.
- assumptionNote: string | null.
- createdAt, updatedAt: RFC3339 timestamps.
- A correction creates a new scenario definition/version; saved scenario results remain unchanged.

EvaluateScenarioRequest:
- scenarioId: UUID string, required and belongs to this case.
- Copy scenario inputs into the immutable result snapshot.

ScenarioResult:
- scenarioResultId, analysisRunId, scenarioId: UUID strings.
- scenarioLabel: string.
- entryPrice, exitPrice: DecimalString.
- quantity: integer | null.
- grossReturnPct, grossProfitAmount: DecimalString | null.
- netReturnPct: null in P0 until approved costs/tax/slippage methodology and inputs exist.
- calculationStatus: ScenarioCalculationStatus.
- inputSnapshot: JSON object containing exact inputs used.
- limitationNote: string.
- createdAt: RFC3339 timestamp.

P0 arithmetic:
- grossReturnPct = ((exitPrice - entryPrice) / entryPrice) × 100, computed with Decimal and the approved rounding/display policy.
- grossProfitAmount = (exitPrice - entryPrice) × quantity when quantity is supplied; otherwise null.
- Net return must not be fabricated. Do not assume charges/taxes/slippage are zero.
- Allotment probability is separate and outside this formula.

### 9.10 Reports and exports

CreateReportRequest:
- analysisRunId: UUID string, required and belongs to this case.
- Report creation reads the selected immutable run; it does not trigger another analysis.

ReportDetail:
- reportId, caseId, analysisRunId: UUID strings.
- generatedAt: RFC3339 timestamp.
- templateVersion: string.
- reportSnapshotHash: 64-character lowercase hexadecimal string.
- title, issueDisplayName: strings.
- informationCutoffAt: RFC3339 timestamp.
- sections: ReportSection[].
- warnings: string[].
- exportArtifacts: ReportArtifact[].

ReportSection:
- sectionCode, heading, bodyMarkdown: strings.
- relatedEvidenceIds, relatedResultIds, relatedFindingIds: UUID string[].
- statusNote: string | null.

The report snapshot retains values/statuses/qualifications needed to display that report even if facts later change. Material factual claims and calculations link to their evidence/result/finding where relevant.

CreateReportExportRequest:
- format: html | docx.

ReportArtifact:
- artifactId, reportId: UUID strings.
- format: ReportExportFormat.
- sha256: 64-character lowercase hexadecimal string.
- sizeBytes: integer >= 0.
- createdAt: RFC3339 timestamp.
- downloadUrl: API-relative URL.

Exporting never reruns analysis. Export failure does not delete the saved report. P0 produces HTML preview and tested DOCX export. PDF export is deferred until the offline conversion route is validated.

### 9.11 Backup and restore

BackupResponse:
- backupId: UUID string.
- createdAt: RFC3339 timestamp.
- sizeBytes: integer >= 0.
- sha256: 64-character lowercase hexadecimal string.
- caseCount, evidenceFileCount: integers >= 0.
- downloadUrl: API-relative URL.

Restore validation accepts ZIP archives and checks manifest/checksums, safe path names, database schema version, required files and path traversal/ZIP-bomb limits without replacing live data.

RestoreValidationResponse:
- validationId: UUID string.
- status: RestoreValidationStatus.
- caseCount, evidenceFileCount: integers >= 0.
- warnings, errors: string[].
- validatedAt: RFC3339 timestamp.

RestoreRequest:
- validationId: UUID string, required.
- confirmationText: must equal "RESTORE".
- Backend verifies the validation record is recent and for the validated archive, creates a safety backup, then performs a recoverable restore.

RestoreResponse:
- status: completed | failed.
- restoredAt: RFC3339 timestamp | null.
- safetyBackupId: UUID string | null.
- message: string.

Never extract archive paths outside the configured data directory. Restore cannot accept arbitrary server paths. Test in a disposable directory first.

---

### 9.12 Fully specified shared list and summary response models

The following wrappers are also used by the route inventory and must be implemented with these exact fields. Do not return a bare array where an envelope is declared.

- EvidenceListResponse: items: EvidenceItem[]; total: integer >= 0.
- FactListResponse: items: FactRecord[]; total: integer >= 0.
- ObservationListResponse: items: MarketObservation[]; total: integer >= 0.
- AcquisitionAttemptListResponse: items: AcquisitionAttemptSummary[]; total: integer >= 0.
- AnalysisRunListResponse: items: AnalysisRunSummary[]; total: integer >= 0.
- ScenarioListResponse: items: ScenarioDefinition[]; total: integer >= 0.
- ScenarioResultListResponse: items: ScenarioResult[]; total: integer >= 0.
- ReportListResponse: items: ReportSummary[]; total: integer >= 0.

AnalysisRunSummary fields: analysisRunId, caseId (UUID strings), runStatus (AnalysisRunStatus), informationCutoffAt, startedAt (RFC3339 timestamps), finishedAt (RFC3339 timestamp | null), inputSnapshotHash (64 lowercase hex characters).

ReportSummary fields: reportId, caseId, analysisRunId (UUID strings), generatedAt (RFC3339 timestamp), templateVersion (string), reportSnapshotHash (64 lowercase hex characters), title (string), issueDisplayName (string), informationCutoffAt (RFC3339 timestamp), warningCount (integer >= 0), exportArtifacts (ReportArtifact[]). Include only properties actually saved in the report metadata; never synthesize a report from the current case.

Additional wire status types used above:

| Type | Allowed values |
|---|---|
| HealthStatus | ok, degraded |
| DiscoveryStatus | found, partial, not_enabled, unavailable, failed |
| ExtractorStatus | completed, partial, failed |
| RestoreStatus | completed, failed |

All list wrappers return total as the count of returned items in P0 because no pagination is implemented. If pagination is later added, it is a deliberate contract change with new fields and tests.

### 9.13 Download and error details

Binary download endpoints return the appropriate Content-Type, Content-Disposition with a safe display filename, and Content-Length when known. Evidence PDF uses application/pdf; ZIP backup uses application/zip; DOCX uses the Open XML Word document MIME type; HTML export uses text/html; no binary endpoint reveals its local storage path. Reject a download request if the identifier is not under the supplied parent resource.

Validation errors use error.details entries with field, issueCode and message. field may be null for a request-level error. Readiness error detail fields use code, severity, message, affectedIndicatorCodes, affectedSignalCategories, evidenceIds and nextAction as defined for ReadinessIssue. Do not place arbitrary nested Python exceptions into JSON.

---

## 10. Backend module and function contracts

The file ownership rules in Section 4 are binding. Suggested public service functions establish readable module boundaries; private helpers may be added without changing the API.

| Module | Required public use-case functions | Key responsibility |
|---|---|---|
| services/cases.py | create_case, list_cases, get_case, update_case_title | Case persistence and case response |
| services/identity.py | discover_issue_candidates, confirm_issue_identity | Candidate discovery and evidence-backed identity |
| services/evidence.py | register_evidence, save_uploaded_pdf, get_evidence, list_evidence, download_evidence, extract_evidence_candidates | Original file, metadata, checksum, extraction candidates |
| services/facts.py | create_fact, list_facts, review_fact | Source-linked facts and review state |
| services/observations.py | create_observation, list_observations, review_observation | Time-aware signals and review state |
| services/acquisition.py | run_acquisition, list_attempts, get_source_states | Per-category/source status and attempt history |
| analysis/preflight.py | evaluate_readiness | Case snapshot + cutoff → blockers/warnings/eligible/skipped codes |
| analysis/engine.py | run_analysis | Confirmed issue + cutoff → immutable run/results/findings |
| analysis/formula_registry.py | get_enabled_formulas, get_formula_version | Server-owned versioned formula metadata |
| services/scenarios.py | create_scenario, list_scenarios, evaluate_scenario | User assumptions → deterministic result snapshot |
| services/reports.py | create_report_snapshot, get_report, list_reports, export_report | Saved run → immutable report and export artifact |
| services/local_data.py | create_backup, validate_restore, restore_backup | ZIP manifest/checksums and safe local restore |

Routes parse HTTP input, call services and return declared response models/status codes. Repositories own SQLAlchemy queries. Analysis/formula functions accept explicit inputs and return explicit statuses/reasons; they do not query global state or call external services secretly.

### 10.1 Transaction and file-system rules

- Do not hold an SQLite transaction open during network requests, PDF parsing or rendering.
- Upload flow: validate extension/MIME/size, write a temporary safe path, hash bytes, persist metadata transactionally, move to final path, clean up on failure. If DB/file state disagree, surface recoverable storage failure and preserve enough diagnostics to recover.
- File download verifies case/resource relationship before returning bytes.
- Acquisition creates an attempt record before/around network I/O, then records actual status/fields/times after completion/failure.
- Analysis captures an input snapshot before calculations and saves results/findings under the run ID. A failed run is not shown as completed.
- Report creation snapshots the selected run; export uses that snapshot, never current case data.
- Backup includes SQLite, all referenced evidence/report files, manifest and checksums. Restore validates before touching live data.

---

## 11. P0 database alignment requirements

The persisted-schema authority is docs/database-schema.md. Amend it to match these semantics **before Alembic migration 0001 is written**. It must include at least:

| Table | Purpose / critical fields |
|---|---|
| issuers | Issuer identity and timestamps |
| ipo_issues | Confirmed issue, MAINBOARD only, issue terms, identity status |
| issue_identifiers | Source/namespace-specific identifier linked to issue/evidence |
| identity_candidates | Per-case saved candidate snapshot, source/evidence and discovery time |
| research_cases | entered_name, title, nullable issue_id, case_status and timestamps |
| sources | Publisher, access/use status, terms review and connector state |
| evidence_items | Case/source, kind, original filename/MIME/size/hash, safe relative path, publication/capture time, locator, verification status |
| acquisition_attempts | Case/source/category, start/finish, status, returned fields and failure cause |
| fact_records | Indicator code, raw/canonical values, units/currency/period/as-of, evidence, entry method, review history/rationale/supersession |
| market_observations | Category/segment, raw/canonical values, definition/unit/currency, observed/published/retrieved/recorded times, source/evidence/attempt and review history |
| analysis_runs | Cutoff, run status, schema/formula/rule/software versions, immutable input snapshot and hash |
| analysis_results | One result per run/result key, calculation status, decimal/text value, input fact/observation/evidence links, formula version and reason |
| findings | Rule/version/type/severity/title/explanation/limitations and run linkage |
| finding_evidence_links | Finding/evidence role supports, contradicts or context |
| scenario_definitions | Case-level saved assumptions and timestamps |
| scenario_results | Scenario/run links, immutable input assumptions, gross result, null net result in P0, status/limitations |
| reports | Immutable report snapshot/content, run/case link, template version/hash/time |
| report_artifacts | Report link, HTML/DOCX format, safe relative path/hash/size/time |

Database rules:
- UUIDs are TEXT primary keys.
- Money/percent/ratio values are canonical decimal strings in SQLite TEXT, not SQLite REAL.
- Timestamps persist UTC ISO/RFC3339; unknown source timestamps remain nullable.
- Enable SQLite foreign keys on every connection and test rejection of invalid references.
- Use explicit Alembic migrations; never silently alter schema at startup.
- Keep previous records when correcting facts/observations. Completed run/report snapshots are immutable.
- Validate JSON snapshots with schemas and persist a version plus hash.
- Index case/time, case/indicator/review state, run/severity, source/category/attempt time and identifier lookup.
- Schema and Data Contract must change together; a persisted structure/semantics change requires a migration and migration test.

---

## 12. Case-level API examples

These demonstrate the contract; they are not claims that the routes already work.

### 12.1 Create case

Request:

~~~json
{
  "enteredName": "Example Industries IPO",
  "title": "Example Industries IPO research"
}
~~~

The HTTP 201 response includes UUID caseId, caseStatus = identity_pending, identityStatus = unresolved, issue = null, timestamps, latestAnalysisRunId = null, latestReportId = null, caseChangedSinceLastRun = true, readinessSummary = null and warningCount.

### 12.2 Manually enter a time-sensitive observation

Request:

~~~json
{
  "indicatorCode": "EXISTING_CATALOGUE_CODE",
  "signalCategory": "gmp",
  "segment": null,
  "rawValueText": "₹51 per share",
  "valueNumeric": "51",
  "valueText": null,
  "unit": "INR/share",
  "currency": "INR",
  "metricDefinition": "Publisher-described unofficial grey market premium",
  "observedAt": null,
  "publishedAt": null,
  "retrievedAt": null,
  "sourceId": null,
  "evidenceId": "d3427e1a-3a58-4b7d-8f70-4fd25cde09cb",
  "definitionMetadata": {}
}
~~~

This succeeds only when indicatorCode is registered and evidenceId belongs to the case. The server sets observationId, recordedAt, entryMethod = manual and reviewStatus = candidate (unless a separately approved review policy says otherwise). The sample indicator code is a placeholder, not a newly invented catalogue code. Source timestamps are not inferred from entry time.

### 12.3 Run preflight then analysis

Readiness returns effective informationCutoffAt and eligible/skipped formulas. Pass that exact timestamp to CreateAnalysisRunRequest:

~~~json
{
  "informationCutoffAt": "2026-10-29T10:00:40Z"
}
~~~

If identity is unresolved or no useful eligible analysis exists, the API returns HTTP 409 ANALYSIS_BLOCKED with readiness details. If some checks work while others are skipped/qualified, runStatus = partial and each skipped result has a reason.

---

## 13. Frontend conventions and route map

Use the browser routes defined in docs/app-flow.md:

| Browser route | Page component |
|---|---|
| /cases | CasesPage |
| /cases/new | NewCasePage |
| /cases/:caseId | CaseOverviewPage |
| /cases/:caseId/evidence | EvidencePage |
| /cases/:caseId/facts | FactsPage |
| /cases/:caseId/analysis | AnalysisPage |
| /cases/:caseId/runs/:analysisRunId | RunDetailPage |
| /cases/:caseId/scenarios | ScenariosPage |
| /cases/:caseId/reports/:reportId | ReportPage |
| /settings | SettingsPage |
| * | Not-found state |

Requirements:
- Navigate using caseId/run/report IDs, never issuer display names.
- Keep case identity/status visible in the workspace.
- Show loading, empty, validation, error, blocked, partial, stale, conflicting and not-applicable states where relevant.
- Do not clear forms after failed saves. Do not show Saved until a successful server response.
- Do not rerun analysis when navigating to a saved run/report.
- UI validation helps usability; backend/Pydantic validation is authoritative.
- API/generated types originate from OpenAPI; do not duplicate request/response interfaces by hand in feature folders.
- api/errors.ts converts API errors to a typed user-safe error preserving code, field details and requestId.
- Frontend code never directly reads/writes SQLite or the app-data directory.

frontend/src/components/hero/ResearchHero.tsx is reserved in the target tree only. Do not implement an invented layout before the owner supplies the exact 21st.dev component URL/code and approves licence/dependency review. Build other pages independently without a fake hero.

---

## 14. Source acquisition and cross-signal rules

The acquisition orchestrator is P0. It must:
1. Resolve the confirmed issue and enabled signal categories.
2. Read only source adapters whose use/access state is approved and connectorStatus is enabled.
3. Enforce adapter-specific allowlist, rate limits, timeout/response-size limits and attribution/disclaimer requirements.
4. Record actual attempt start/end, source/category, status, returned fields and failure cause.
5. Retain each source-specific observation with observed/published/retrieved/recorded time semantics.
6. Expose missing/not-enabled/failed/partial/stale/conflicting state to readiness and reports.
7. Continue manual workflow after provider failure.

At this snapshot no connector is production-approved. The dated Data Source & Feasibility Audit makes IPOS Markets a priority subscription-data candidate, GMP Today a limited-sample GMP candidate and Xflot a conditional directory/GMP-detail candidate that has not demonstrated QIB/NII/retail rows. Provider enablement remains gated by usage terms, coverage, timestamp and repeatability checks. Honour Xflot's 65-second minimum polling safeguard if it is ever approved. Do not scrape NSE without written permission.

Signal checks combine available, valid, time-appropriate evidence from the approved Indicator Catalogue/formula register. Expected categories include company financials, issue/valuation terms, QIB/NII/retail demand, unofficial GMP, market context and company events. The engine must evaluate enabled supported relationships; a placeholder UI that only lists signals is insufficient. If a critical signal has no free/permitted route, record and escalate that feasibility gap before release—do not silently relabel a manual-only system as a complete automated acquisition workflow.

---

## 15. Testing and quality gates

### 15.1 Backend
- Unit: Decimal arithmetic, identity validation, timestamps, input mapping, readiness, freshness/conflict decisions, formula registry, scenario arithmetic, file path safety and manifest hashing.
- Integration: cases/identity, evidence upload/download, manual facts/observations, acquisition attempts, analysis snapshots, reports and backup/restore using a temporary data directory.
- Database: migrate empty DB, foreign-key rejection, indexes, restart persistence and migration safety.
- Source adapters: no ordinary test depends on live providers. Use deterministic fixtures; live tests are opt-in and separately approved.
- PDF extraction: known fixture PDF, wrong file, corrupt file, scanned-only PDF behaviour and candidate-only status.
- Reports: saved report snapshot matches the run; DOCX export reopens and retains caveats/links/unknown values.

### 15.2 Frontend
- Strict TypeScript typecheck, ESLint, Vitest/React Testing Library.
- Test state/error/empty/loading behaviour, no silent data replacement, API errors, evidence review/correction, scenario assumptions and immutable run/report navigation.
- Playwright core path: create case → confirm identity with fixture evidence → add PDF/manual values → readiness → deterministic run → scenario → report preview/export → reopen after restart.
- Accessibility: keyboard path, field-associated errors, visible focus, text labels for statuses and reduced-motion behaviour.

### 15.3 Continuous integration

.github/workflows/ci.yml runs the backend pytest suite and frontend typecheck, lint, unit tests and production build on pushes to main/build branches and pull requests to main. CI is a verification mechanism, not a substitute for local review. Its results must be checked before merge; a green result does not approve an unverified data source or formula.

### 15.4 Contract drift

Required checks:
1. Start backend and retrieve its OpenAPI schema.
2. Run npm run api:types and verify generated types are current.
3. Run backend OpenAPI/route contract tests and frontend typecheck.
4. Test required/null fields, enum values, error envelopes and parent-child ownership.
5. When a contract changes, review schema/migration diff and verify old saved cases still open.

Do not claim migration, test, build, generated-type or source-integration success until actually executed. Documentation review is not a runtime test.

---

## 16. Security and local-data handling

- Bind FastAPI to 127.0.0.1 by default. Do not expose the app publicly.
- No login is needed for P0, but loopback binding, explicit CORS, ownership checks, safe paths and download routes are mandatory.
- PDFs are untrusted. Verify suffix/MIME/size, generate server-side storage names, hash original bytes and prevent traversal.
- Restrict source URL schemes to HTTP/HTTPS and never create an unrestricted server-side URL proxy. Future adapters must enforce allowlists and reject local/private network targets.
- Never execute file contents, spreadsheet formulas, embedded scripts or macros.
- Do not store PAN, bank, allotment identifiers, broker logins, cookies, source credentials or order/execution data.
- Never log full local paths, secrets or full document contents by default.
- Backups can contain sensitive research and documents; keep them local, checksum them and let the user choose where to copy/download.
- Restore must validate path safety/manifest/checksums, create a safety backup and require explicit confirmation.
- AI is not in the P0 execution path. If later introduced, do not send evidence externally without a separately approved privacy/terms flow.

---

## 17. Build order and acceptance gates

Use docs/implementation-plan.md for phase tracking. The dependency order is fixed:

1. **Scaffold gate:** frontend/backend projects; health endpoint; typed fetch client; tests; local data directory; basic shell. Verify loopback and storage path.
2. **Contract/database gate:** Pydantic schemas, OpenAPI-generated types, migration 0001, foreign keys and schema tests. Do not build screens against guessed fields.
3. **Case/identity gate:** list/create/open/rename, candidate discovery status, evidence-backed Mainboard confirmation and SME out-of-scope.
4. **Evidence/input gate:** PDF registration/hash/storage, URL/manual evidence, candidate-only extraction, manual facts/observations and review/correction/conflict workflow.
5. **Acquisition gate:** provider-neutral orchestrator, source registry/attempt history/status display and category results. Individual provider adapters remain disabled unless approved.
6. **Analysis gate:** approved P0 formula register, readiness/preflight, Decimal calculations, input snapshots, skipped/qualified reasons and first cross-signal rules.
7. **Scenario/report gate:** saved scenario assumptions/results, immutable report snapshot, HTML preview and offline DOCX export.
8. **Reliability gate:** local backup/restore, error injection, restart tests, accessibility/end-to-end tests, reviewed diff and release checks.

### MVP release acceptance

The user can complete the local path without internet or paid services: create a case, resolve a Mainboard issue from evidence, register an official PDF, enter facts/observations manually, see accurate source acquisition status, run supported deterministic calculations, trace findings to evidence, calculate a conditional gross-return scenario, preview/export a report, reopen history and back up/restore data. Acquisition is visibly orchestrated, and unapproved providers/categories are honestly marked rather than simulated. Previous runs/reports remain unchanged.

---

## 18. How to build this repository with Claude

**Primary recommendation: use Claude Code against a local clone opened in VS Code (or the Claude Desktop Code tab connected to that local folder), not ordinary Claude web chat as the main coding environment.** This project needs coordinated multi-file edits, local Python/Node installs, database migrations, generated TypeScript types, tests, browser verification and careful Git diffs. Claude Code is designed to inspect a repository, edit files, run commands and work with Git. Its approval prompts and Plan mode are useful safeguards.

Recommended loop:
1. Clone the existing GitHub repository and open the folder in VS Code.
2. Verify Git, Python and Node.js are installed; install Claude Code using current official instructions rather than an old npm command.
3. Start Claude Code from the repository root so it reads CLAUDE.md and AGENTS.md.
4. Ask it to read canonical docs and propose Phase 0 only. Use Plan mode first; do not request the entire app in one prompt.
5. Review each diff. Implement one measurable vertical slice, run tests/build/typecheck, explain failures and list changed files.
6. Review Git status/diff and commit a working milestone before the next phase. Do not blindly accept a huge rewrite.
7. Treat this file as the fixed contract. If Claude proposes a different field/path, stop and resolve the contract first.
8. Never share tokens/passwords in chat; keep .env out of Git and instruct tools not to read secrets.

If the repository is not cloned locally or local setup is temporarily impractical, **Claude Code on the web at claude.ai/code** is an alternative: it connects to a GitHub repo and uses a cloud coding environment. That is not the same as ordinary Claude chat. Local Claude Code is preferable for this actively evolving project because you can watch tests, inspect files and course-correct immediately. Confirm availability and usage limits for your own plan before relying on either; this document does not claim a particular account entitlement or that Claude Code is free.

For any UI/UX implementation, follow docs/design.md and the repository's required Frontend Design skill/plugin gate. The hero remains unimplemented until the owner provides the exact approved component source.

Official references to recheck when installing:
- Claude Code setup/install: https://code.claude.com/docs/en/getting-started
- Claude Code CLI use and permission/plan options: https://code.claude.com/docs/en/cli-usage
- Claude Code use with Claude Pro/Max subscriptions and rate-limit guidance: https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan

---

## 19. Change control and definition of done

A contract/architecture change must include:
1. Reason and affected requirement.
2. Update to this canonical file.
3. Matching Pydantic/OpenAPI changes.
4. TypeScript type regeneration.
5. Database migration when persisted structure/semantics change.
6. API, integration and relevant end-to-end test updates.
7. Updates to linked docs where user-visible behaviour changes.
8. Reviewed diff and clear report of tests actually run.

A feature is not done because its route or screen renders. It is done when backend validation, persistence, error recovery, provenance, status semantics, user-facing states, immutability and tests are demonstrated.

**Current status:** this file freezes the first implementation blueprint and P0 API contract. The repository still contains specifications rather than a completed application. No claim is made that code, database migration, frontend build, tests, hero integration or any third-party connector has already been implemented or verified.
