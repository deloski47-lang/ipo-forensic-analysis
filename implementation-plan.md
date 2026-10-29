---
title: IPO Forensic Analysis Engine — Implementation Plan
document_id: IP-IPO-001
version: 0.1
status: Proposed implementation sequence; no application implementation is claimed
last_updated: 29 October 2026
scope: Indian Mainboard IPOs only; local-first, single-user; INR 0; deterministic core; manual/offline fallback
canonical_source: Markdown in GitHub
---

# IPO Forensic Analysis Engine — Implementation Plan

## 1. Purpose and authority

This document turns the approved product requirements and current technical/design specifications into a sequenced implementation backlog with explicit exit gates. It is a plan, not evidence that the app, database, API, connectors or tests have already been implemented.

Use it together with the existing canonical files:

1. [Project Brief](docs/IPO_Forensic_Analysis_Project_Brief_v1.0.md)
2. [Approved PRD](docs/IPO_Forensic_Analysis_PRD_v1.0_APPROVED.md)
3. [Indicator Catalogue & Data Dictionary](docs/IPO_Indicator_Catalogue_and_Data_Dictionary_v1.0.md)
4. [Data Source & Feasibility Audit](docs/IPO_Data_Source_and_Feasibility_Audit_v1.0.md)
5. [Application Flow](docs/app-flow.md)
6. [UI/UX Design Specification](docs/design.md)
7. [Technical Design](docs/TECHNICAL_DESIGN.md)
8. [Proposed Database Schema v0.1](docs/database-schema.md)
9. [Repository rules](AGENTS.md)

If this plan conflicts with an approved requirement, the PRD and binding decisions in AGENTS.md take priority. A technology, provider or formula marked proposed/open remains unapproved until its stated gate is passed. Update this document in place as the sequence changes; use Git history rather than numbered duplicates.

## 2. Binding constraints

- **Budget: INR 0.** No paid APIs, datasets, AI, hosting, database service, software upgrades or paid fallback.
- **Market scope: Indian Mainboard IPOs only.** SME issues must be rejected by identity validation and excluded from fixtures and supported source logic.
- **Local-first, single-user.** Case data, evidence, calculation runs and reports stay on the user's machine. No login, public SaaS, multi-user collaboration, cloud database or public deployment in the MVP.
- **Manual/offline core is complete.** User-provided documents and manually entered facts/observations must support the core case-to-report workflow when internet or any provider is unavailable.
- **IPO-name-triggered acquisition orchestration is still a P0 capability.** The app must attempt reviewed/approved connectors after identity resolution, record attempt outcomes, show missing categories and interconnect available signals. A provider not yet approved must not be called as if trusted; show its status and preserve the manual route. Any critical signal category without a free/permitted route is an explicit release decision, not a silent downgrade to manual-only operation.
- **Deterministic financial calculations.** Material calculations use code and decimal-safe arithmetic, not AI-generated arithmetic. Each enabled formula needs documented inputs, units, periods, definitions, rounding/display policy, missing/invalid-input behaviour, and passing known-answer plus invalid-input tests.
- **Evidence and missingness stay honest.** Keep source identity, raw values, units, periods, timestamps, retrieval attempts and review status. Unknown is not zero. Conflicts are preserved, not silently averaged or overwritten.
- **No unsupported prediction claims or execution.** Scenarios are conditional calculations; no calibrated probability or profitable-listing guarantee is claimed. No order placing/modifying/selling features. Do not collect PAN, bank information or application identifiers for this research product.
- **No prohibited automated exchange collection.** Do not scrape NSE pages absent written permission. Public visibility is not itself permission for automated collection, storage or redistribution.

## 3. Starting point and source-readiness snapshot

The repository currently contains product/technical specifications and a proposed SQLite schema; it does not yet contain an implemented application, working migrations or a demonstrated end-to-end app. No runtime or acceptance test should be marked passed until it is executed.

### Source evidence available on 29 October 2026

| Candidate | What the historical reports support | Current disposition | What remains open |
|---|---|---|---|
| IPOS Markets | Version 0.1 report matched 9/10 target IPOs. Version 0.2 matched 10/10 and returned QIB/NII/RII fields plus an as-of timestamp for all ten. Bombay Coated and Special Steels used basis = bids_only and had a null overall multiple. | Priority subscription candidate; not production-approved. | Repeatability, precise timestamp meaning, source accuracy, upstream rights, access terms and representative coverage over time. |
| GMP Today | Both reports returned valid JSON with three IPOs. The tracked count changed from 18 to 17; all version 0.2 returned records had updated_at = null. Some quoted medians changed between snapshots. | Limited-sample, attribution-required GMP candidate; not production-approved. | Per-observation timing/freshness, coverage, accuracy and terms for intended storage/use. |
| Xflot | Version 0.2 directory returned 182 records, including 110 Mainboard. Its BLS Polymers single-issue detail endpoint succeeded only in the version 0.1 run, which returned GMP/issue detail but no subscription rows. | Conditional issue/GMP detail candidate; not a subscription source on current evidence. | Repeat the single-issue detail route with the current runner if it is considered for integration; validate source values, timestamps, coverage, terms, attribution and disclaimer. Observe a minimum 65-second gap between Xflot polls. |

The saved combined smoke-test reports are useful dated evidence. They do not establish strict version-0.2 repeatability, accuracy, comprehensive coverage or permitted upstream reuse. **Do not make another smoke-test run a blocker to the provider-neutral scaffold, Data Contract, manual-input workflow or deterministic core.** Revisit the relevant provider gate before enabling any connector for real use. Do not commit generated test JSON or patch files as application inputs.

## 4. Recommended architecture baseline

Use the existing Technical Design as the technology baseline, validating compatible supported versions when the scaffold is created:

- **Frontend:** React + TypeScript + Vite SPA. Strict TypeScript, reusable feature components, accessible UI and one typed API client.
- **Backend:** Python + FastAPI. Thin route handlers; application services for workflows; domain functions for calculations and rules.
- **Contracts:** Pydantic request/response models and FastAPI OpenAPI; generate or mechanically check TypeScript API types. Do not independently hand-maintain drifting wire types.
- **Persistence:** SQLite and local filesystem for original evidence and exported files. SQLAlchemy/Alembic are recommended by Technical Design; validate their setup before adopting. Explicit migrations and foreign-key enforcement are required.
- **Calculation layer:** isolated deterministic Python functions using decimal-safe numeric arithmetic. Formula/rule versions and exact input snapshots are retained.
- **Reporting:** structured report model, HTML preview, and DOCX first if the selected export path passes a no-cost offline test. PDF may follow only after a free/offline path is validated.
- **Provider integrations:** provider-neutral acquisition orchestrator plus isolated adapters. Only approved adapters can retrieve data; no vendor-specific assumptions leak into core domain entities.
- **AI/document extraction:** optional and later. No AI API, OCR service or model is required for case creation, manual entry, calculations or reporting.
- **Runtime:** local processes bound to loopback. No public network exposure or cloud service is needed.

Do not introduce Redis, queues, a hosted database, paid UI kits, analytics, container orchestration or other infrastructure without a separately approved, tested requirement. The proposed module map in Technical Design is a responsibility map: create modules only when their behaviour is implemented.

## 5. Implementation phases

Each phase has a concrete exit gate. Build an end-to-end vertical slice incrementally; do not create empty folders or non-functional screens for every feature upfront.

### Phase 0 — Freeze the first-slice decisions

**Deliverables**
- A short first-slice scope: create/resolve a Mainboard issue, create a research case, register evidence and manual observations, record acquisition statuses, run a small approved set of formulas/checks, save a run snapshot, and preview/export a traceable report.
- The first Data Contract: endpoint list/methods, request/response schemas, nullability, field casing, enums/status transitions, timestamps/time zones, decimal serialization, validation errors and shared error envelope.
- Database-schema alignment for only the first slice, including stable IDs, case/evidence/observation/acquisition-attempt/run relationships.
- An initial formula/rule register selected from the Indicator Catalogue. Include only formulas whose definitions and independently checked golden examples are approved.
- Fixture plan covering at least one unambiguous Mainboard IPO, one ambiguous identity, one missing signal, one stale/time-misaligned observation, one contradiction, and one bids-only record with a null overall multiple.

**Exit gate**
- Contract and schema are reviewed together against the PRD, app-flow and technical design.
- No field name, enum, formula or threshold has been invented to unblock coding.
- The initial user journeys and acceptance criteria are explicit. Future/P1/P2 decisions remain deferred unless they block this slice.

### Phase 1 — Validate the local scaffold

**Deliverables**
- Minimal frontend and FastAPI backend in one repository.
- One frontend-to-backend health request and clear startup/error behaviour.
- Dependency files and lockfiles with compatible versions selected at implementation time and no payment/billing requirements.
- Repeatable scripts for install, run, lint, type-check, tests and local OpenAPI/type generation.
- A per-user data directory for SQLite, source files, exports and logs; runtime paths, local reports, user data and secrets excluded from Git.
- A concise local setup guide. Do not put real evidence, user research data, credentials or local databases in the repository.

**Exit gate**
- Both processes start locally and the frontend reaches the API.
- TypeScript type-checking is explicitly run (not only Vite transpilation); backend tests run.
- OpenAPI-to-TypeScript type generation or equivalent contract checking is reproducible.
- Core local startup needs no internet after dependencies are installed and does not require a paid service.

### Phase 2 — Data Contract, database migration v1, cases and identity

**Deliverables**
- Implement the approved first Data Contract and contract tests before building multiple dependent screens.
- Implement explicit migration v1 for the first-slice tables, constraints and indexes from the proposed schema, modifying that schema only through documented, reviewed alignment.
- Enable and test SQLite foreign-key enforcement on each connection.
- Case list/create/open/rename/archive as defined by app-flow; issue candidate/confirmed/rejected identity states.
- Mainboard-only validation; ambiguous names require confirmation before a full analysis run.
- Repository/service boundaries so route handlers remain thin.

**Exit gate**
- A case and confirmed issue survive restart.
- SME issues are rejected with a clear message.
- Ambiguous identities remain unresolved until the user confirms.
- Contract tests, migration tests and foreign-key tests pass.

### Phase 3 — Evidence registry, manual facts and observations

**Deliverables**
- Evidence/source registration, original-file preservation, checksum, source URL, capture time, publication time if known, document version and page/section locator.
- Manual company/offer fact entry and time-sensitive market-observation entry.
- Separate accepted, candidate, rejected, conflicted and superseded states based on the approved contract.
- Capture units, currency/scale, period/basis, source definition and separate observed/published/retrieved times; unknown times remain null.
- Candidate values remain untrusted until review; replacing an evidence file creates a new version rather than silently overwriting the original.
- Safe file validation and upload limits after representative-file tests. Unsupported/failed parsing falls back to manual entry.

**Exit gate**
- A case can be completed with local evidence and manual inputs without internet or any provider.
- QIB, NII and retail observations are stored separately.
- Conflicting GMP observations from two publishers remain separate and visible.
- Missing, unavailable, stale, invalid and not-applicable remain distinct.
- An extracted candidate cannot enter a trusted calculation until accepted under the review policy.

### Phase 4 — Provider-neutral source-acquisition orchestrator

**Deliverables**
- Source registry with approval status, terms note/date and required attribution/disclaimer.
- An orchestrator that, after issue identity is confirmed, initiates attempts for adapters explicitly approved for the tested signal categories.
- Persistent attempt history: adapter/source, signal category, start/end time, outcome (succeeded/partial/unavailable/blocked/failed), returned fields and a safe error summary.
- Per-category coverage/freshness diagnostics and visible explanation of skipped, blocked or missing data.
- Adapter interface and contract tests using deterministic fixture responses. Do not enable live candidate adapters just because the interface exists.
- Manual source registration/import as an equal fallback path. A provider failure does not block other valid calculations or erase last-known observations.

**Connector enable gate**
1. Current terms/access method and permitted storage/use are reviewed and recorded.
2. Required issue identity, Mainboard board, exact fields and definitions map correctly.
3. Time semantics, status/finality and null meanings are established.
4. Representative coverage, source accuracy/cross-checks, failure responses and schema behaviour are tested.
5. Attribution, disclaimer, cache/rate limits and polling safeguards are implemented and tested.
6. A connector is then explicitly marked approved in configuration/docs. Otherwise its UI state remains unapproved/blocked/unavailable and it is not silently treated as having been checked.

**Current candidate treatment**
- IPOS Markets may be implemented behind this gate as the priority subscription candidate, but must remain disabled/unapproved until its open rights, semantics and data-quality questions are resolved.
- GMP Today can be evaluated only as a limited-sample GMP source. Per-record updated_at is null in the saved run, so do not manufacture quote timestamps from the feed-level generated time.
- Xflot must not populate subscription categories based on the current evidence. If later tested for issue/GMP detail, retain its published attribution and disclaimer and enforce a minimum 65-second polling interval.
- Do not build an automated NSE-page scraper without written permission.
- If no free/permitted retrieval path exists for a critical source category, record the gap and obtain an explicit product-owner release decision; do not claim full automation or quietly redefine the product as manual-only.

**Exit gate**
- A simulated/source-fixture success, partial response, timeout, blocked adapter, invalid schema and unavailable source all persist correct statuses.
- No unapproved provider is invoked by default.
- The case remains usable and reportable with manual inputs when all connectors are unavailable.

### Phase 5 — Approved deterministic formula register

**Deliverables**
- Select and approve a limited P0 formula list from the Indicator Catalogue. Do not activate the whole catalogue.
- For every enabled metric, document identifier, definition, source inputs, units, periods, denominator rules, normalization, precision, display rounding, missing/invalid handling and interpretation limits.
- Use exact decimal-safe arithmetic for financial amounts and percentages where applicable.
- Persist formula/rule version and input/evidence IDs for each result.
- Implement known-answer fixtures verified independently by hand, plus boundary, invalid-input, zero/negative/near-zero denominator and missing-input tests.
- Unapproved formulas stay disabled. Thresholds must be evidence-based and sector-aware; do not add universal thresholds by intuition.

**Exit gate**
- Every enabled formula has passing known-answer and invalid-input tests.
- Missing or invalid prerequisites yield an explicit unavailable/not-meaningful result and reason, never a fabricated number.
- Changing a source fact cannot silently rewrite a prior completed run.

### Phase 6 — First interconnected cross-signal findings

**Deliverables**
- A small, reviewed P0 rule set linking relevant financial/offer quality and valuation with category-wise subscription, GMP, issue/free-float context and available market/company-event evidence.
- Use the Indicator Catalogue's dependency map and IDs as the authority. Do not invent indicator codes or relationships.
- Every finding records its rule/version, triggering inputs, source links, supporting/contradicting/context evidence and limitations.
- Rules check information-time compatibility; stale or post-cutoff observations are rejected or explicitly qualified.
- Show counter-evidence and alternative explanations. A contradiction is a finding, not a reason to choose the most attractive value.

**Exit gate**
- Seeded examples produce expected findings, and removal/staleness of a prerequisite gives a specific skipped/qualified reason.
- One missing signal does not prevent unrelated valid rules from running.
- High subscription or positive GMP does not, by itself, imply a profitable listing or causal conclusion.

### Phase 7 — Scenarios, immutable analysis runs and reports

**Deliverables**
- Preflight/readiness summary showing missing, stale, conflicted, rejected and not-applicable inputs.
- A reproducible analysis run with information cutoff, exact input snapshot, evidence references, schema/software/formula/rule versions and outcomes.
- User-entered listing-price scenarios and documented gross-return arithmetic. Scenario inputs are labelled assumptions unless separately supported as observed prices.
- Allotment probability remains separate from return conditional on allotment.
- Structured report model, local HTML preview and DOCX export after the offline export path is tested. PDF is optional and must not introduce a paid/online dependency.
- Report preview/export preserves citations, source status, timestamps/cutoff, conflicts, missingness, assumptions and caveats; export does not implicitly rerun the analysis.
- Reports and runs are immutable snapshots: new inputs create a new run.

**Exit gate**
- One Mainboard IPO case goes end-to-end from evidence and manual/source attempts to saved findings, scenarios and a traceable report.
- The report can trace every material fact to evidence or label it unresolved/hypothesis/user-supplied.
- An export and its saved run remain consistent after new observations are added.

### Phase 8 — Security, backup/restore and release acceptance

**Deliverables**
- Safe local file handling, parameterized database access, environment configuration without secrets in Git, loopback-only service binding and bounded/safe logs.
- Backup and restore of the SQLite database and evidence directory as a consistent bundle.
- Regression, API contract, frontend interaction/accessibility and end-to-end tests.
- Setup, run, test, backup and restore instructions tested on the supported development environment.
- Release checklist mapping requirements and acceptance scenarios to actual test results. A test can be marked passed only if it was executed.
- Explicit review of unresolved critical source-category access/permission gaps before MVP release.

**Exit gate**
- A restored test bundle reopens its case, evidence, run and saved report.
- The agreed P0 acceptance tests pass, including manual/offline operation, null/missing behaviour, conflict visibility, source acquisition outcomes, run immutability and export integrity.
- All enabled formulas pass 100% of their required tests.
- No paid service is required and no connector is labelled production-approved without its own gate.
- Any critical signal with no free/permitted acquisition route has an explicit product-owner release decision.

## 6. First end-to-end vertical slice

The first usable slice should stay narrow but prove the product's core architecture:

1. User enters a company/IPO name.
2. The app resolves a Mainboard issue or stops for identity confirmation.
3. A research case is created and saved locally.
4. Source discovery/acquisition is orchestrated; approved connectors are attempted, and unapproved/blocked/unavailable candidates are explicitly identified without being falsely described as successful.
5. User registers an offer document and enters/reviews a small set of company/offer facts plus QIB/NII/retail and GMP observations when available.
6. Every fact/observation keeps provenance, definition, units and time fields; conflicts and nulls remain visible.
7. Preflight identifies which approved calculations/rules can run.
8. The deterministic formula/rule set produces findings with evidence links; missing inputs qualify/skip only the affected checks.
9. User enters a transparent listing-price scenario; supported gross-return arithmetic is calculated.
10. The app saves an immutable run snapshot and generates an HTML preview plus tested DOCX export.
11. The case can be closed, reopened and restored from backup.

This slice is not complete merely because each route or page exists; the full path and its failure/missing-data cases must pass acceptance tests.

## 7. Test strategy and fixture matrix

Maintain fixtures for at least:

| Fixture | Must prove |
|---|---|
| Clean, unambiguous Mainboard IPO | Case creation, identity confirmation and end-to-end path |
| Ambiguous issuer/issue name | No full analysis until identity is resolved |
| SME IPO candidate | Rejected as out of scope |
| Valid subscription record with all categories | Correct category mapping and source/time preservation |
| Bids-only record with overall multiple null | No inferred overall multiple; reason/basis visible |
| GMP with missing per-record timestamp | Timestamp remains unknown; feed-generated time is not substituted silently |
| Two different GMP sources or times | Both observations remain visible and are not treated as independent without checking provenance |
| Provider fixture success, partial, malformed, blocked and unavailable | Correct attempt history and safe recovery |
| PAT/OCF or receivables-growth divergence | Approved cross-check is surfaced with evidence and no automatic fraud conclusion |
| Stale/post-cutoff input | Rejected or qualified by information-time rules |
| Invalid/zero/negative denominator | Formula follows its registered invalid-input treatment |
| Changed facts after a completed run | New run is created; old snapshot/report remains unchanged |
| Export and backup restore | Citations/statuses persist; restored case/evidence/report are usable |

Test layers: backend domain/unit tests; persistence/migration/integration tests; API contract tests against OpenAPI; frontend component/interaction/accessibility tests; and one end-to-end acceptance case. All test commands and pass/fail outcomes must be recorded honestly in the delivery summary.

## 8. UI and design gates

Follow [design.md](docs/design.md) and [app-flow.md](docs/app-flow.md). Implement the app shell and core pages incrementally: cases/home; create case and identity resolution; case overview; evidence inventory; facts/observations/review; analysis readiness; findings; scenarios; report preview/history; minimal local-data settings.

Every data-backed view needs loading, empty, validation, failure, partial, stale, conflict and not-applicable states as relevant. Status styling and animation must reflect real persisted outcomes, not optimistic UI assumptions. Keyboard access, visible focus, contrast, reduced-motion handling and responsive layouts are acceptance items, not polish to postpone indefinitely.

**Hero-specific hold:** the design spec reserves selection of the exact 21st.dev hero component and its intended screen for the product owner. Do not invent, clone or implement a placeholder hero as if final. This does not block the API, database, case workflow or non-hero application shell. Before integrating the chosen component, verify its author/licence, attribution, dependencies, network requests, compatibility, responsiveness, accessibility and INR 0 fit.

## 9. Decisions still open (do not silently invent)

- Final first-slice Data Contract and exact enums/property names.
- Final schema adjustments and migration mechanism after validating the recommended SQLAlchemy/Alembic setup.
- Initial P0 formula/rule register and independently checked golden fixtures.
- File types/size limits and representative PDF extraction coverage; manual entry remains fully supported.
- First report export: DOCX is the recommendation; PDF depends on a tested offline path.
- Local data directory, backup/restore behaviour and supported operating systems.
- Exact hero component URL/code and screen placement, supplied by the product owner.
- Provider rights/terms and the enablement of each individual adapter.
- Any critical source category that remains without a free/permitted route after validation; requires an explicit product-owner release decision.

Do not let future P1/P2 choices block the scaffold or provider-neutral/manual-first vertical slice. Do block the affected feature when its missing decision would make it unsafe or untestable.

## 10. Out of scope until P0 passes

- Automated historical backfill or predictive model calibration.
- Google Trends/search-attention as a launch dependency.
- Broad news sentiment or firehose ingestion.
- Full catalogue implementation, universal score, guaranteed BUY/AVOID label or claims to detect all fraud.
- Intraday execution-price simulation without verified licensed/permitted data.
- Broker integration/order execution, login, multi-user features, public hosting, cloud database, paid APIs/AI/OCR or managed infrastructure.
- Automatic source adapters for providers that have not passed their own free/permitted-use and data-quality gate.

## 11. Definition of done for the MVP

The MVP is ready for release only when:

- A user can create, confirm, save, reopen and archive a Mainboard research case.
- Issue/source acquisition attempts and per-category coverage/status are observable; unapproved connectors are not invoked or represented as successful.
- Original evidence and observations preserve identity, unit, period/definition, provenance, timestamps and review state.
- Manual/offline completion does not require any data provider or AI.
- All enabled calculations are documented and have 100% passing known-answer and invalid-input tests.
- First cross-signal checks connect available fundamentals/valuation, subscription, GMP and relevant market/company-event evidence, while showing counter-evidence and missing/stale limitations.
- No material fact, timestamp, source, citation or numeric result is invented.
- Scenario calculations are conditional and distinct from allotment probability.
- Prior analysis runs and reports remain immutable.
- A saved report preserves citations, limitations, conflict/missingness states and assumptions.
- Backup/restore, security, setup instructions and end-to-end acceptance pass.
- The source audit and release notes state the actual status of each connector and resolve any critical free/permitted-source gap by explicit product-owner decision.

The objective is not maximum automation on paper. It is a working, auditable and locally usable forensic workflow whose automated results are enabled only when their evidence and permissions support them.
