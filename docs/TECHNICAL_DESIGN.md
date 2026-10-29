---
title: IPO Forensic Analysis Engine — Technical Design
document_id: TD-IPO-001
version: 0.1
status: Proposed technical baseline; validate marked decisions before implementation
last_updated: 29 October 2026
canonical_source: Markdown in GitHub
scope: Indian Mainboard IPOs; local-first; single-user; manual-first; zero-budget
---

# IPO Forensic Analysis Engine
## Technical Design

> **Purpose:** Translate the project's brief, approved product requirements, indicator catalogue, data-source feasibility audit and decisions discussed with the product owner into a practical engineering design. It defines the recommended architecture, responsibilities, end-to-end data flow, persistence, validation, report pipeline, testing and implementation order. It is written so a developer or coding agent can build the intended product without inventing a different one or silently changing requirements.

**This is a proposed architecture baseline, not a claim that every technical choice has already been tested or approved.** Decisions are classified as fixed constraints, recommended baselines, decisions requiring validation, or deferred. The exact field-by-field Data Contract is intentionally not frozen yet: its purpose and readiness gate are defined here, but precise API payloads must be finalized after the module boundaries and end-to-end flow are settled.

---

## 1. Authority and source material

### 1.1 Canonical project documents

Read this file together with:

1. **Project Brief:** vision, forensic analysis framework, intended local-first architecture and longer-term direction.
2. **Approved PRD:** MVP scope, functional requirements, non-functional requirements and acceptance criteria.
3. **Data Source & Feasibility Audit:** evidence hierarchy, source feasibility, access/usage constraints, source acceptance tests and manual fallbacks.
4. **Indicator Catalogue & Data Dictionary:** indicator meanings, logical data-record semantics, formula and normalization standards, cross-indicator dependencies, claim/finding semantics and test expectations.
5. **AGENTS.md, CLAUDE.md and README.md:** repository rules and binding project constraints.

At present the detailed reference documents are stored in the repository under their versioned filenames within docs/. Preserve their contents and current history. Do not create replacement summaries or duplicate versions as part of this design.

### 1.2 Authority when sources conflict

Use the following order:

1. Explicit, recorded product-owner decisions and binding project constraints.
2. Approved PRD for product behaviour and MVP scope.
3. This Technical Design for technical decisions after they are accepted.
4. Indicator Catalogue & Data Dictionary for indicator meaning, formula definitions, cross-check semantics and data integrity.
5. Data Source & Feasibility Audit for source feasibility, source trust and allowed-use review.
6. Project Brief for the broader product vision.

If two sources conflict, identify the conflict and its consequences, then propose a resolution. Never choose whichever version is easiest to implement and silently call it approved.

### 1.3 Decision-status labels

| Label | Meaning |
|---|---|
| **Fixed constraint** | Must be obeyed; not a design preference. |
| **Recommended baseline** | Preferred engineering choice for the MVP; use unless a concrete incompatibility is found and the change is recorded. |
| **Requires validation** | Must be tested or checked before it can be relied on. |
| **Deferred** | Intentionally outside the MVP or blocked until evidence exists. |
| **Not approved** | Must not be implemented as an assumed requirement. |

---

## 2. Executive technical recommendation

Build a **local-first modular monolith**: a small web frontend, a local Python API, a local SQLite database, and a local evidence-file directory. Keep calculations, cross-checks, scenarios and report orchestration as ordinary Python modules in the same backend codebase. Do not introduce microservices, cloud infrastructure, a remote database, a distributed job queue, login/authentication, or paid provider dependencies for the MVP.

### 2.1 Recommended baseline

| Concern | Recommendation | Rationale |
|---|---|---|
| Application shape | Single-user local web application | Fits personal research use and keeps data under the user's control. |
| Frontend | React + TypeScript + Vite SPA | The local app does not need server-side rendering or SEO; a simple SPA makes the API boundary clear. This is a recommendation, not a product requirement. |
| Backend/API | Python + FastAPI | Fits the Python analytical and document-processing layer and provides typed request/response models and an OpenAPI description. |
| Contract and validation | Pydantic models + OpenAPI + generated or automatically checked TypeScript API types | Avoids independently hand-maintained contracts that drift between frontend and backend. |
| Persistence | SQLite for structured records | Local embedded storage requires no database server and is suitable for the single-user MVP. |
| Original evidence and exports | Local filesystem, referenced from SQLite | Preserves original files without storing every PDF as a database blob. |
| Persistence tooling | SQLAlchemy and Alembic are the recommended baseline | Provides explicit persistence models and controlled migrations; validate setup before adopting. |
| Financial math | Deterministic Python functions with decimal-safe arithmetic | Financial calculations must be reproducible, traceable and independently tested. |
| Document processing | Manual review first; extraction is optional and candidate-only | PDF tables, footnotes, units and scans are error-prone; manual entry must remain complete. |
| Reports | Structured report model, HTML preview, DOCX-first polished export | Separates report content from rendering; DOCX is the PRD's recommended first export. PDF may follow after an offline conversion test. |
| AI | Optional, isolated adapter only; no AI provider is required | The core workflow must work at ₹0 and survive the absence of any free-tier service. |
| External data | No live provider integration required for P0 | The audit has not established a dependable, unrestricted, free automated pipeline for all needed fields. |
| Runtime | Local development processes bound to loopback | No cloud deployment or public network exposure is required for the MVP. |
| Tests | Backend unit/integration tests, frontend tests, API contract tests and an end-to-end acceptance path | A polished report is not trustworthy unless arithmetic, statuses, lineage and interfaces are tested. |

Versions must be selected at implementation time from compatible supported releases and pinned in dependency lockfiles. Do not guess future version numbers in this specification.

### 2.2 Why this should stay small

A distributed architecture would add deployment, configuration, data-transfer, security and debugging work without satisfying an approved MVP requirement. The frontend and backend can run as separate local processes but remain parts of one repository and one product.

Do not add Redis, Celery, Kafka, a vector database, a cloud object store, Kubernetes, hosted analytics, a paid AI API or a managed database merely because a tutorial includes them. Add a component only when an approved requirement and reproducible test demonstrate the need.

### 2.3 What this design does not prove

This architecture makes the manual-first product practical to build. It does not prove that every metric can be populated, every PDF will parse correctly, every data source is free or permitted, or that the engine can predict profitable listings. Predictive claims require a separate point-in-time historical dataset and leakage-controlled out-of-sample evaluation.

---

## 3. Non-negotiable project constraints

1. **Total budget is ₹0.** Do not introduce paid APIs, datasets, AI services, hosting, managed databases, software upgrades, paid fallback services, or trials that require payment details. A free tier may be an optional convenience only; the core workflow must remain functional if it is unavailable, rate-limited, withdrawn or requires an upgrade.
2. **Mainboard IPOs only.** SME IPOs are excluded from MVP case creation, source logic, supported examples and the test corpus.
3. **Local-first and single-user.** Core case data, evidence, calculations, reports and run history live on the user's machine. No public SaaS, multi-user collaboration, login system or cloud database.
4. **Manual-first operation.** Users must be able to register documents and enter facts/observations manually. Missing internet, API, model, OCR result or extractor must not block the core workflow.
5. **Evidence before narrative.** Every material factual claim traces to evidence or is explicitly labeled unresolved, user-supplied, hypothetical or interpretive.
6. **No invented information.** Never fabricate numbers, source URLs, document pages, timestamps, disclosures, issuer identity, market observations or citations. Unknown is not zero.
7. **Deterministic finance.** Calculations run in tested code, not in an AI model. Every enabled MVP formula has a documented definition, inputs, units, periods, rounding/display rules, missing/invalid-input behaviour and automated tests.
8. **Conflicts stay visible.** Do not silently average, overwrite or conveniently choose between conflicting source values.
9. **Listing-day scenarios are conditional calculations.** A user-entered scenario price is an assumption unless registered separately as an observed market price with provenance.
10. **No unvalidated prediction claims.** Do not present an arbitrary score or percentage as a calibrated probability of listing gain.
11. **Allotment and return are separate.** Allotment probability and listing-day return conditional on allotment must not be combined.
12. **No order execution.** The tool never places, modifies or sells market orders.
13. **Do not collect application identifiers.** PAN, bank information, application number, DP/client ID and similar personal investor application identifiers are not part of the research engine.
14. **AI is assistive only.** Future AI may explain evidence or suggest hypotheses but cannot bypass validation, invent facts or replace deterministic calculations.

### Explicitly outside MVP

- Broker/order execution.
- Public hosting, public accounts, teams or multi-user features.
- Mandatory live news, subscription, GMP, Trends, market-price or exchange APIs.
- Paid data or AI subscriptions.
- AI-based extraction as a prerequisite.
- Full implementation of every indicator in the catalogue.
- A universal IPO score or guaranteed BUY/AVOID label.
- Full automated historical backfill/backtesting.
- Automated news sentiment, search-attention collection or a predictive model as launch blockers.
- Claims that the system detects every fraud, accounting manipulation or hidden relationship.
- Cloud backups or required always-on internet access.

---

## 4. Architecture principles

### 4.1 Separate responsibility by layer

Do not mix these concerns into one large route file or catch-all module:

- User interaction and presentation.
- API parsing, validation, status codes and response serialization.
- Use-case orchestration.
- Domain concepts and status semantics.
- Evidence/source persistence.
- Document parsing and candidate extraction.
- Fact validation and normalization.
- Deterministic formulas.
- Cross-indicator rule execution.
- Scenario calculations.
- Report construction and export.
- Optional external-source adapters.
- Optional AI assistance.

A route validates and dispatches a request; it does not own financial formulas. A report template renders prepared results; it does not perform source collection or calculation. AI must never become the source of truth, calculation engine or database.

### 4.2 Explicit status beats silent fallback

Every operation must return a validated result or a clear status/error. Missing input, non-applicable input, stale data, conflicting evidence, parser failure and invalid data are distinct conditions. A blank screen, zero, fabricated default or neutral risk label is not a valid fallback.

### 4.3 Provenance is part of the domain

Evidence lineage is not a report-only decoration. Store source identity, locator, time, period, validation status and calculation lineage so a report can be audited and a run can be reproduced.

### 4.4 Deterministic core; optional integrations at the edge

Source or AI adapters are optional boundaries. They can propose observations or candidate facts, but cannot directly mutate trusted facts or silently change a saved run. Their failures stay contained.

### 4.5 Deliver one working vertical slice first

First demonstrate this path end to end: create one Mainboard IPO case, register an official offer PDF, enter a small approved set of fields manually, validate them, calculate an approved formula set, produce a traceable report, save a run and reopen it. Do not build many empty screens or implement all indicators before this path works.

---

## 5. System architecture and process model

### 5.1 High-level system

~~~mermaid
flowchart TB
    U[Single user]
    FE[Local web frontend]
    API[FastAPI API layer]
    APP[Application services and orchestration]
    DOM[Domain rules and deterministic calculations]
    DOC[Evidence registration and document parsing]
    REP[Report construction and export]
    DB[(Local SQLite database)]
    FS[(Local evidence and export files)]
    EXT[Optional future source adapters]
    AI[Optional future AI adapter]

    U <--> FE
    FE <--> API
    API --> APP
    APP --> DOM
    APP --> DOC
    APP --> REP
    APP <--> DB
    APP <--> FS
    DOC --> DB
    DOC --> FS
    EXT -. optional .-> APP
    AI -. optional and non-authoritative .-> APP
~~~

The frontend and API communicate over an explicit local HTTP interface. Python services own analysis orchestration and calculations. Structured records live in SQLite; original documents and generated files live on disk. Internal Python services call each other directly; they do not call HTTP endpoints to communicate internally.

### 5.2 Local process model

- During development, run the frontend and FastAPI backend as two local processes.
- Frontend requests use one configured API base URL; components must not invent their own base URLs.
- Bind the backend to a loopback address such as 127.0.0.1, not 0.0.0.0.
- Restrict CORS to the exact local frontend origin.
- Keep local paths and ports in documented configuration rather than hard-coding a personal machine path.
- No Docker, reverse proxy, cloud deployment or process supervisor is required for the first local workflow.
- If later packaging is justified, evaluate a simple local launcher that starts both processes. Do not package the application before the development workflow stabilizes.

### 5.3 Layer responsibilities

| Layer | Owns | Must not own |
|---|---|---|
| Frontend | Navigation, forms, upload interaction, status display, candidate review, findings, scenario inputs, report preview | Financial formulas, source trust decisions, trusted-fact promotion, database access |
| API layer | HTTP routes, request validation, status/error mapping, serialization | Core business rules or scattered SQL |
| Application services | Use-case orchestration and transaction boundaries | UI rendering or large embedded formulas |
| Domain layer | Entities, status semantics, formulas, rule definitions, scenario arithmetic | HTTP request objects, UI concepts, provider SDKs |
| Evidence/document layer | Original file registration, checksum, candidate extraction, page/section locators | Automatic promotion of extracted values into trusted inputs |
| Persistence layer | SQLite access, repositories, migrations and file-reference operations | Product logic or calculation rules |
| Report layer | Report model built from a saved run and renderers | Missing-data invention or independent recalculation |
| Adapter layer | A specific optional source connection and mapping | Bypassing validation or becoming required for the core path |
| AI adapter | Optional evidence-grounded suggestions/drafts | Trusted fact entry, arithmetic, autonomous actions or uncited factual claims |

---

## 6. Recommended technology baseline

### 6.1 Frontend: React, TypeScript and Vite

Use a single-page application because the initial product is local and does not need public SEO or server-side rendering. TypeScript should be strict. Use reusable feature components and a dedicated API client.

Recommended structure:
- Page-level components for screens.
- Reusable components for evidence status, citations, validation messages, findings and data tables.
- Feature folders for cases, evidence, facts, analysis, scenarios and reports.
- One API client to control base URL, serialization, error handling and request behaviour.
- Generated API types in a clearly marked generated directory.
- Shared design tokens and accessible styles; a paid UI kit is prohibited.
- Local React state and simple request-state handling by default; do not add Redux or another global store until a demonstrated workflow needs it.

Show loading, empty, failure, stale, conflict and not-applicable states explicitly. Do not infer a status merely because a value is blank.

### 6.2 Backend: Python and FastAPI

Use FastAPI for the local API and Python for document/data processing, formula execution, rule evaluation and report construction.

Rules:
- Use explicit type hints.
- Keep route functions small and delegate to application services.
- Keep domain functions callable directly from unit tests without an HTTP server.
- Keep financial calculations outside route handlers.
- Do not create a catch-all main.py containing routes, extraction, formulas, database logic and report generation. The app entry point should configure the application and register routers only.
- Be deliberate with blocking file/CPU work; an async route does not automatically make CPU-heavy parsing non-blocking.

### 6.3 API schema and frontend/backend consistency

**Recommended:** Pydantic at the Python API boundary, FastAPI-generated OpenAPI as the interface description, and generated or automatically checked TypeScript types.

This directly addresses the project owner's stated risk: frontend/backend integration must not depend on guessing field names or types.

Requirements:
1. API property names, types, nullability, enum values, timestamp formats and error structures are explicit contract decisions.
2. The completed Data Contract is the authority for payload shapes.
3. Generate or mechanically check TypeScript API types against OpenAPI; do not manually copy interfaces into frontend code.
4. Never rename a wire property in a component simply for convenience. Any mapping belongs in one API-client/mapper module and must be intentional.
5. TypeScript checks do not validate runtime JSON; server-side validation is still required.
6. A contract change updates the backend schema, OpenAPI representation, generated frontend types, tests and documentation together.
7. A contract test must fail if the implementation no longer matches the agreed schema.

The detailed field-by-field Data Contract is **not finalized in this document version**. Define it after module responsibilities and the end-to-end flow are reviewed, but before implementing multiple endpoint payloads. Do not invent endpoint schemas by guesswork.

### 6.4 Persistence: SQLite and local files

Use SQLite for structured records and local filesystem storage for original source documents and exports.

Recommended baseline:
- Database under the application's per-user data directory, never as a committed project file.
- SQLAlchemy and Alembic as the recommended ORM/migration pair; validate the initial setup and keep migrations explicit.
- Use transactions for operations writing related records.
- Enable foreign-key enforcement and add sensible constraints.
- Use stable internal identifiers, not display names as primary keys.
- Keep database timestamps consistent and date-only fields separate.
- Store file references and checksums in the database; preserve original bytes on disk.
- Do not make an in-memory dictionary the only store of accepted facts, evidence or reports.

SQLite fits a local single-user MVP. It is not an implicit future choice for a high-concurrency hosted service; that is outside current scope.

### 6.5 Document parsing

The core MVP must work without extraction.

Recommended staged path:
1. Register and preserve the original file.
2. Test text extraction against representative Mainboard offer PDFs.
3. Treat extracted text/numeric values as candidates, linked to page/section locators where available.
4. Present candidate facts for user review and correction before they become trusted inputs.
5. When parsing cannot reliably handle tables, footnotes, signs, units or pages, make the limitation visible and offer manual entry.
6. OCR is optional and must run locally if added; no paid OCR service. OCR output is also untrusted pending review.
7. Final supported file types, size limits, parser libraries and OCR method require representative-file testing. Do not claim universal PDF compatibility.

Optimize for reliability and traceability, not the number of fields appearing to be automatically filled.

### 6.6 Reports

Recommended approach:
- Construct a structured report model from a saved run.
- Render a local HTML preview.
- Use DOCX as the recommended first polished export, provided the export path passes an offline test.
- Add PDF export after a no-cost, offline conversion approach is tested.
- Keep report content/model separate from templates so layout changes do not change calculations.
- Preserve citations, timestamps/cutoff, statuses, conflicts, assumptions, caveats and counter-thesis.
- Record which saved analysis run a report belongs to.
- Rendering/export must not rerun analysis implicitly.

### 6.7 AI services

AI is not a P0 dependency. Do not require a paid AI SDK or API key.

If optional AI is added later:
- Keep it behind a provider interface so it can be disabled or replaced.
- The core workflow must work when the provider is absent, unavailable, rate-limited or returning invalid output.
- Extraction results stay candidates until reviewed.
- AI cannot invent citations, page locators, timestamps, prices, disclosures or source observations.
- AI cannot directly mutate trusted facts or past runs.
- Uploaded text is untrusted data, not instructions for the application.
- Validate AI output against an explicit schema and stored evidence references.
- Reject any provider or workflow that requires spending, payment details or unacceptable data terms.
- A local model may be considered only if its hardware requirements and setup burden are practical; do not make it a blocker.

---

## 7. Code repository and module map

Use one repository for the frontend, backend, tests and canonical documents. Do not split the product into separate repositories in the MVP.

The existing detailed source documents should keep their current filenames until a focused repository housekeeping change is approved. The following is a target layout for application code; do not create empty folders without an implemented responsibility.

~~~text
ipo-forensic-analysis/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── docs/
│   ├── IPO_Forensic_Analysis_Project_Brief_v1.0.md
│   ├── IPO_Forensic_Analysis_PRD_v1.0_APPROVED.md
│   ├── IPO_Data_Source_and_Feasibility_Audit_v1.0.md
│   ├── IPO_Indicator_Catalogue_and_Data_Dictionary_v1.0.md
│   └── TECHNICAL_DESIGN.md
├── frontend/
│   └── src/
│       ├── app/
│       ├── components/
│       ├── features/
│       │   ├── cases/
│       │   ├── evidence/
│       │   ├── facts/
│       │   ├── analysis/
│       │   ├── findings/
│       │   ├── scenarios/
│       │   └── reports/
│       ├── lib/
│       │   └── api/
│       ├── generated/
│       │   └── api-types/
│       └── styles/
├── backend/
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── migrations/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── router.py
│   │   │   └── routes/
│   │   ├── application/
│   │   │   ├── cases/
│   │   │   ├── evidence/
│   │   │   ├── facts/
│   │   │   ├── analysis/
│   │   │   ├── reports/
│   │   │   └── backup/
│   │   ├── domain/
│   │   │   ├── identity/
│   │   │   ├── evidence/
│   │   │   ├── facts/
│   │   │   ├── indicators/
│   │   │   ├── formulas/
│   │   │   ├── findings/
│   │   │   ├── scenarios/
│   │   │   └── runs/
│   │   ├── schemas/
│   │   ├── persistence/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   └── database.py
│   │   ├── ingestion/
│   │   │   ├── file_registry.py
│   │   │   ├── pdf_text.py
│   │   │   └── candidate_extraction.py
│   │   ├── rules/
│   │   │   ├── cross_checks/
│   │   │   └── sector_checks/
│   │   ├── reporting/
│   │   │   ├── report_builder.py
│   │   │   ├── html/
│   │   │   └── docx/
│   │   ├── adapters/
│   │   │   └── optional_sources/
│   │   ├── ai/
│   │   │   └── providers/
│   │   └── config.py
│   └── tests/
│       ├── unit/
│       ├── integration/
│       ├── contract/
│       └── fixtures/
├── scripts/
└── .env.example
~~~

### 7.1 Structure rules

- The tree is a target boundary map, not a requirement to generate every folder up front.
- Keep app/main.py minimal; route files dispatch to application services.
- Formulas live in named, unit-testable domain functions.
- Keep database-specific code in persistence models/repositories and migrations.
- Give each optional provider its own adapter.
- Generated TypeScript files must be clearly identified and must not be edited by hand.
- Keep tests for individual layers and cross-layer contracts.
- Never commit uploaded offer documents, local databases, research-case content, exports, local caches or credentials.
- Do not rename the existing source documents as part of the first code scaffold. If canonical stable aliases are adopted later, update every affected README/agent link in the same focused change.

---

## 8. Domain ownership and responsibilities

This section defines logical responsibilities, not the final field-by-field schema. Exact names and payload properties belong to the Data Contract step.

### 8.1 Issuer, IPO issue and research case

The issuer is the company; the issue is one specific Mainboard IPO; the research case is the user's saved investigation of that issue. Keep these concepts separate when persistence and future analysis require it.

Required behaviour:
- Different IPOs by the same issuer are different issues/cases.
- Display name is not a stable identifier.
- Record aliases and source-specific identifiers where available.
- Preserve the basis for identity resolution.
- Flag ambiguity and prevent final analysis against an unconfirmed identity.
- SME issues are out of scope.

### 8.2 Source and evidence registry

Owns registration of uploaded documents and user-entered observations. It preserves:
- Source identity/publisher/title and exact URL or local file reference.
- Document/observation version where available.
- Original filename, content type and checksum for uploaded files when supported.
- Publication time, event time, observation time, capture/retrieval time and relevant data period as separate concepts.
- Page, section, table, paragraph or other source locator where available.
- Capture method and source-terms note where relevant.
- Links from evidence to supported facts and observations.
- History of corrections, rejection, conflict and superseding versions.

Trust belongs to the evidence item and the claim it can support. A source category or website does not give every value a blanket score.

### 8.3 Facts and observations

Keep the following semantic categories separate:
- Raw source value.
- Normalized value with explicit unit/currency/period.
- Manually entered value.
- Extracted candidate awaiting review.
- Verified or cross-checked fact.
- Deterministically calculated metric.
- Rule-generated finding.
- Interpretation/hypothesis.
- Scenario assumption.
- Missing, stale, conflicting, invalid, failed or not-applicable value.

Never overwrite the raw sourced value during normalization. Corrections must preserve the original input/source context.

### 8.4 Formula and indicator engine

Owns:
- Only the formulas enabled in the approved MVP formula register.
- Prerequisite checks for input status, units, periods, denominator and applicability.
- Deterministic calculation or an explicit blocked/unavailable/not-meaningful result.
- Formula identifier/version, named inputs, source references, input periods, calculation time and information cutoff.
- Internal precision and documented display rounding.

The catalogue is a broad research framework; an indicator appearing there does not automatically authorize implementation in MVP.

### 8.5 Cross-indicator findings

The rule engine checks explicit relationships across facts and indicators. Each finding should explain the tested relationship, inputs, why it matters, limitations and unresolved alternatives. Preserve positive and negative evidence.

Do not assert causation or fraud because a rule triggers. Do not add correlated indicators into a composite score that double-counts the same issue. Start with a small, well-tested rule set.

### 8.6 Scenario calculations

MVP scenario input is user-supplied. It is not a model-generated forecast.

For issue price Pi and scenario/exit price Ps:

**Gross return percent = ((Ps − Pi) / Pi) × 100**

Calculate only when inputs are valid and Pi is positive. Per-share or per-lot profit is possible only when quantity is known. Do not show net return unless fees, taxes, charges, slippage and their assumptions are defined and supplied. Keep scenario price visibly separate from a source-verified market price.

### 8.7 Analysis runs

A case may have multiple analysis runs. Each run must preserve:
- Exact case/issue identity.
- Input/evidence snapshot.
- Information cutoff.
- Scenario assumptions.
- Formula/rule versions.
- Software/schema version sufficient to explain behaviour.
- Validation warnings, conflicts, missingness and unresolved limitations.
- Result/finding/report references.

A later run must not rewrite a previous run or report.

### 8.8 Report builder

Build a report from a saved run. Rendering does not recalculate, fetch new sources, or silently fill missing content. The report builder creates the report model; templates only render it.

### 8.9 Optional adapters

Each optional source or AI adapter has a narrow interface, explicit mapping, timeouts, failure handling and tests. It cannot bypass evidence/fact validation. No adapter belongs on the core startup path if the manual workflow can run without it.

---

## 9. End-to-end data flow

### 9.1 Create a case

1. User submits an IPO name and available identifiers.
2. API validates the request shape and creates a research case.
3. Identity handling uses only supported/manual or approved evidence; automated live resolution is not required.
4. If identity is ambiguous, the case is flagged and the user must resolve it before a finalized analysis.
5. The UI shows the case and an evidence checklist.
6. The case can be saved and reopened.

### 9.2 Register evidence

1. User uploads/registers an official offer document, issuer disclosure, exchange item, secondary article or manual observation.
2. API verifies supported file type/content and configured size limits. Limits are selected after representative tests, not guessed here.
3. Backend stores the original under a generated safe path, computes checksum where supported and records metadata.
4. Extraction/normalization never changes original bytes.
5. Record known source, version, dates/times and precise locator.
6. Failure must be visible and must not leave a false successful evidence record.

### 9.3 Enter or extract facts

1. User enters data manually or requests optional extraction.
2. Raw input, method, source locator, unit and period are captured where applicable.
3. Extracted values remain candidate facts until reviewed.
4. User can accept, correct, reject or leave unresolved, preserving history where relevant.
5. Conflicting values remain visible.
6. Incompatible units, periods, identity or validation states block affected formulas.

### 9.4 Run analysis

1. User starts analysis and sets/accepts a known information cutoff.
2. System captures the run input snapshot and linked evidence.
3. Validate identity, required inputs, units, periods, freshness, conflicts and formula prerequisites.
4. Run only valid, enabled deterministic formulas.
5. Run only cross-check rules whose prerequisites are satisfied.
6. Calculate user-defined scenarios from explicit assumptions.
7. Mark unavailable, blocked or not-applicable outputs explicitly.
8. Save the run and diagnostics.
9. Display outputs, missing evidence, warnings, conflicts and follow-up questions.

### 9.5 Produce and export report

1. Report builder uses the saved run.
2. It assembles required report sections where evidence supports them.
3. Unsupported/deferred sections display a limitation or status instead of fabricated content.
4. Material claims link to evidence/calculation lineage or are explicitly labeled as hypothesis/unresolved.
5. HTML preview and selected export are generated from the same report model.
6. Export records the originating run.
7. New runs do not mutate old reports.

### 9.6 Reopen/reproduce

1. User opens a saved case and sees its prior runs and reports.
2. User can inspect cutoff, inputs, sources, formula/rule versions and unresolved issues.
3. Re-running creates a new run.
4. Missing or corrupted source files generate an integrity warning, never a false claim that the original is still available.

---

## 10. Conceptual data model

These concepts are not yet a field-by-field schema. Exact properties, foreign keys, cardinality details, API representation and final field names will be agreed in the Data Contract/persistence step.

| Concept | Purpose | Invariants |
|---|---|---|
| Issuer | Company identity separate from one offering | Display name alone is not a stable key. |
| IPO Issue | A particular Mainboard IPO | Different issues of the same issuer remain distinct. |
| Research Case | Saved user investigation | Resolves to one exact issue before final report. |
| Source Record | Origin/publisher metadata | Distinct from each specific evidence item. |
| Evidence Item | Specific file, observation or source item | Preserve source/version/time/locator and original file where applicable. |
| Fact/Observation | Value from a source, manual entry or extraction | Carries unit/period/provenance/status. |
| Formula Definition | Approved deterministic formula and version | Defines inputs, unit, period, rounding and invalid/missing handling. |
| Indicator Result | Formula/rule output | Traceable to inputs and formula version. |
| Cross-check Rule | Declared relationship/check | Has prerequisites and explicit interpretation limits. |
| Finding | User-facing analytical result | Links inputs/evidence and identifies unresolved status. |
| Scenario | Conditional price/quantity/cost assumptions | Assumptions are not observed facts or probabilities. |
| Analysis Run | Saved snapshot of inputs, cutoff and logic | New run does not overwrite past run. |
| Report Artifact | Rendered report based on a run | Retains lineage, limitations and qualified language. |
| Audit/Change Event | Meaningful acceptance/correction/rejection/resolution | Preserves changes that affect trust or reproducibility. |

~~~mermaid
erDiagram
    ISSUER ||--o{ IPO_ISSUE : issues
    IPO_ISSUE ||--o{ RESEARCH_CASE : investigated_as
    RESEARCH_CASE ||--o{ EVIDENCE_ITEM : registers
    SOURCE_RECORD ||--o{ EVIDENCE_ITEM : identifies_origin
    EVIDENCE_ITEM ||--o{ FACT_OBSERVATION : supports
    RESEARCH_CASE ||--o{ ANALYSIS_RUN : has
    ANALYSIS_RUN ||--o{ INDICATOR_RESULT : produces
    ANALYSIS_RUN ||--o{ FINDING : produces
    ANALYSIS_RUN ||--o{ SCENARIO : evaluates
    ANALYSIS_RUN ||--o{ REPORT_ARTIFACT : renders
    FORMULA_DEFINITION ||--o{ INDICATOR_RESULT : defines
~~~

The final schema may require join tables for multiple evidence sources supporting one claim, aliases, conflicting values, scenario input sets, report claims and calculation lineage.

### 10.1 Required record semantics

Persist the concepts specified in the Indicator Catalogue and Data Source Audit:
- Stable identifiers for issuer, issue, case, evidence, fact, run and report.
- Raw values separate from normalized and derived values.
- Explicit unit, currency, period and denominator meaning.
- Evidence source and page/section/table/paragraph locator where available.
- Publication, event, observation, capture/retrieval time and analysis cutoff as separate concepts.
- Input/extraction method, validation status and applicability.
- Confidence rationale for interpreted/extracted items, not an unexplained percentage.
- Formula/rule version and named input lineage for calculated results.
- Source/document version and checksum where supported.
- Conflict references and resolution history.
- Prior run/report snapshots not overwritten by new evidence.

### 10.2 Missingness/status semantics

The design must preserve distinct statuses consistent with the catalogue: verified, cross-checked, unverified, candidate awaiting review, conflicting, stale, missing/unavailable, not applicable, failed/invalid, corrected, rejected and resolved as needed.

Not every entity uses every status. Do not flatten status into a single Boolean. Missing data and not-applicable data mean different things.

**Unknown must not be represented by zero, empty string, invented timestamp, arbitrary default or neutral risk label.**

---

## 11. Time, money, units and identity

### 11.1 Time concepts

| Concept | Meaning |
|---|---|
| Publication time | When source was made public, if known. |
| Event time | When the reported event occurred. |
| Observation time | What instant or interval a market observation represents. |
| Capture/retrieval time | When the application/user obtained or entered it. |
| Financial period | Period the number describes. |
| Information cutoff | Latest information allowed in a run. |
| Analysis/report time | When calculations/report were generated. |

Use ISO 8601 timestamps with explicit timezone at interfaces. Store timestamps consistently, preferably UTC, retaining original source timezone when material. Fiscal period-end dates and offer dates are date-only values and must not be converted into invented midnight timestamps.

If a time is unknown, leave it unknown and surface the limitation. File retrieval time is not the publication time of the source.

### 11.2 Money and numeric values

- Use decimal-safe arithmetic in Python for prices, financial amounts and ratio calculations. Do not use binary floating-point as the authoritative financial representation.
- Preserve raw source text and normalized numeric value separately.
- Store currency and scale explicitly: rupees, lakhs, crores, thousands, millions, shares, per-share amounts and percentages must not be inferred from magnitude.
- Store standalone/consolidated basis and reporting period with the value.
- Never compare a partial period with a full year without an explicit defensible adjustment.
- Define behaviour for zero, negative or near-zero denominators. Return not-meaningful/blocked with an explanation when appropriate.
- Retain internal precision and round for display according to the documented convention.
- Before implementing the Data Contract, decide consistently whether high-precision decimal values cross the API as JSON numbers or decimal strings. Never leave serialization to accidental defaults.

### 11.3 Identity rules

- Resolve issue identity from multiple identifiers where possible, not display name alone.
- Preserve issuer aliases and source-specific identifiers.
- Never join data solely because names look similar.
- Record identity-resolution basis and evidence.
- If identity remains ambiguous, block final analysis or mark affected parts unavailable until the user resolves it.
- Mainboard-only scope is enforced by the product flow, not offered as a toggle for SME support.

---

## 12. API and module contract strategy

This section defines how the contract will be designed and enforced. **It is not the final Data Contract.** Exact JSON properties, endpoint payloads and function signatures are intentionally deferred until module ownership and the end-to-end flow are reviewed.

### 12.1 API resource groups required

The first API contract should cover:
1. Health/application status.
2. Case creation, listing, detail, rename and reopen.
3. IPO issue identity review/resolution.
4. Evidence upload, registration, listing and metadata inspection.
5. Manual fact/observation entry and candidate review/correction/rejection.
6. Source locator and conflict inspection.
7. Analysis run creation, diagnostics/status and history retrieval.
8. Indicator results and findings retrieval.
9. Scenario input and deterministic scenario calculation.
10. Report preview and export.
11. Backup/restore if included in MVP operational scope.

This is a resource inventory, not a final route list. Do not implement all route payloads directly from this table.

### 12.2 Naming and type conventions to settle

The Data Contract must define:
- API JSON property naming convention.
- Internal Python identifiers.
- TypeScript API property convention and generated-type policy.
- Stable identifier format.
- Enum names and permitted values.
- Required/optional/null fields.
- Date-only versus timestamp representation and timezone rules.
- Decimal/money serialization and display rounding.
- Collection filtering/pagination only where needed.
- File upload/download request/response semantics.
- Standard error structure.
- Status transitions for facts, conflicts, runs and reports.
- API versioning and compatibility policy.

Recommended language convention: Python functions, variables and module names use snake_case. TypeScript local variables, functions and React components follow TypeScript/React conventions. API wire-property names are chosen once and used exactly; frontend code cannot independently rename them. Generated types must be marked as generated and regenerated through a documented command. The exact wire casing is a contract decision, not something to improvise per endpoint.

### 12.3 Proposed error behaviour

Define one consistent, machine-readable error response in the Data Contract. It must distinguish:
- Invalid request/input.
- Resource not found.
- Ambiguous identity.
- Field-level validation failure.
- Conflicting source/fact state.
- Operation blocked by missing prerequisites.
- Unsupported file type/size.
- Parse failure.
- Local database/filesystem failure.
- Optional provider unavailable/rate-limited/not approved.
- Unexpected internal error.

User-facing messages must be safe and actionable. Do not leak credentials, stack traces, full private file paths or uploaded document contents. A provider failure cannot be disguised as valid empty data or successful analysis.

### 12.4 Contract change workflow

For every intentional contract change:
1. State the reason and affected requirement.
2. Update the contract within this canonical file.
3. Update backend schema/models.
4. Regenerate or check OpenAPI and TypeScript types.
5. Update API client and frontend states.
6. Add/update contract and integration tests.
7. Run the checks and inspect the diff.
8. Record compatibility and stored-data migration impact.

Never rename a backend field and expect the frontend to discover it through trial and error. Never manually patch generated types just to make a build appear green.

---

## 13. Local storage, file lifecycle and backup

### 13.1 Separate structured records and binary files

Use SQLite for structured records and the local filesystem for original PDFs, retained text snapshots needed for reproducibility, generated exports and backup bundles.

Suggested logical directory layout under the user's application data directory:

~~~text
<application_data_root>/
├── database/
│   └── ipo_forensic.sqlite3
├── evidence/
│   └── <generated_evidence_id>/
│       ├── original.pdf
│       └── extracted/
├── reports/
│   └── <case_id>/<analysis_run_id>/
├── backups/
└── logs/
~~~

This is a logical layout, not a literal hard-coded path. Use a safe per-user application-data path abstraction and agree supported OS behaviour before storing irreplaceable cases.

### 13.2 Original-file preservation

- Store files under application-generated IDs, not raw user filenames.
- Preserve original filename as display metadata.
- Compute a content hash/checksum where supported.
- Same display name never means the new file overwrites an old file.
- New versions and addenda become new evidence records linked to a case.
- Extraction retries may create new extraction outputs but never rewrite original bytes.
- Prevent path traversal and arbitrary user-selected write paths.
- If the file write succeeds but database write fails, clean up or mark the orphan recoverably. If file storage fails, do not record the evidence as available.

### 13.3 Transactions and partial failures

- Use clear transaction boundaries for related DB writes.
- Do not mark a fact/run/file complete until its required persistence succeeds.
- Partial failure must be visible and recoverable.
- A report-render failure must not destroy a completed analysis run.
- Failure of a later run must not destroy the last completed run.
- File/database consistency checks should detect missing or orphaned files.

### 13.4 Backup and restore

Recommended:
- Document a manual backup procedure for the database and all referenced evidence/report files.
- Prefer a local backup bundle with a manifest and checksums if implementable safely.
- Do not depend on cloud backup or paid storage.
- Warn if the backup is incomplete.
- Define whether the app must be closed or the database checkpointed before copying.
- Test restore into a clean data directory and verify that cases, evidence, reports and history work.
- Do not claim restore support until a real restore test passes.

The exact backup UX and supported operating systems must be settled before storing valuable user research.

---

## 14. Validation and evidence lifecycle

### 14.1 Lifecycle

~~~text
Captured or uploaded
        |
        v
Registered evidence and source metadata
        |
        v
Manual input or extraction candidate
        |
        v
Validation and user review
        |
        +----> rejected / unresolved
        |
        v
Accepted fact or observation
        |
        v
Formula and rule prerequisite checks
        |
        v
Calculation or finding with traceability
        |
        v
Saved analysis run
        |
        v
Report claim linked to evidence or calculation
~~~

Rejected or unresolved candidates should not disappear. A rejected candidate must not be a trusted formula input; a deliberate correction should create a separately traceable accepted value.

### 14.2 Boundary and domain validation

Boundary validation includes required text, allowable lengths, supported file type/content, identifier formats when defined, enum values, parseable dates/timestamps and input numeric constraints.

Domain validation includes:
- Positive issue price before return calculations.
- Valid denominator before ratio calculations.
- Compatible financial period and statement basis.
- Candidate-review status checks before formula input.
- Freshness checks before a value is called current.
- Conflict checks so formulas cannot silently choose one of two values.
- Not-applicable logic so irrelevant metrics are not scored negatively.
- Identity/evidence gates before a report claims completeness.

### 14.3 Reconciliation

Where inputs support it, test arithmetic totals, compatible share/price/issue-size relationships, financial statement sums and ratio inputs/period basis. Store outcomes such as passed, failed, not testable or unresolved. A failed reconciliation is a finding; it does not authorize silently adjusting a source value.

### 14.4 Forbidden implicit defaults

Never:
- Replace missing numeric input with zero.
- Infer a missing reporting period from chronology.
- Guess page numbers, source links or timestamps.
- Infer scale from magnitude alone.
- Pick one conflicting value without showing the conflict and rationale.
- Treat extraction success as validation success.
- Treat missing signal as neutral/positive.
- Treat a provider's empty response as proof that no event occurred.

---

## 15. Formula engine and cross-check rules

### 15.1 Formula register

Before an indicator is enabled in MVP, its approved formula-register entry must specify:
- Stable formula/indicator ID.
- Definition and purpose.
- Required inputs, units, periods and statement basis.
- Calculation method and denominator handling.
- Output unit and display convention.
- Rounding rule.
- Missing/invalid-input behaviour.
- Applicability and sector limitations.
- Source/data requirements.
- At least one independently verified known-answer fixture.
- Missing, invalid, incompatible-period and denominator edge-case tests.
- Version/change notes.

Only formulas in the approved register may be enabled. Release gate: **100% of enabled MVP formula tests pass**, including known-answer and invalid-input cases.

### 15.2 Deterministic execution

A formula receives explicit validated inputs and returns a value plus status or a blocked/not-meaningful result. It must not perform network retrieval, call an LLM for arithmetic, read hidden global state or infer missing inputs. It must be callable directly from unit tests. Formula version changes must not rewrite historical run outputs.

### 15.3 Cross-check engine

Start with a small high-value subset of catalogue relationships, for example:
- PAT growth vs operating cash-flow support, other-income dependency and one-off effects.
- Revenue growth vs receivables/debtor days and customer concentration.
- Margin expansion vs input costs, discounts, one-off gains or capitalized costs when disclosed.
- Fresh issue/OFS split vs use of proceeds, seller context and potential supply.
- Valuation vs growth, margins, returns and comparable-company quality.
- Subscription demand vs valuation, GMP history, market context and timestamps when those inputs exist.
- Material news/event vs issuer-specific exposure and time known.
- Search-attention change vs news novelty and subscription observations, if later available.

These are examples, not permission to implement every rule now. Use the catalogue's indicator IDs and definitions. Each rule declares prerequisites, trigger logic, evidence/input references, meaning, limitations, applicability and tests for trigger/non-trigger/missing/stale/conflicting/not-applicable cases where relevant.

Do not apply universal red-flag thresholds across all sectors without a documented basis. Do not assert causation or fraud from a triggered rule.

### 15.4 Scenario engine

For MVP:
- Accept user-entered scenario/exit price.
- Validate price and formula prerequisites.
- Compute gross return deterministically.
- Compute per-share/lot gross profit only when quantity is known.
- Show assumptions and source status.
- Keep net return incomplete/disabled until cost components are defined and supplied.
- Keep allotment probability separate.
- Do not auto-generate a predicted price distribution.
- Never label a scenario price as a forecast or actual market observation.

---

## 16. Report architecture and claim lineage

### 16.1 Build the report model first

The report builder creates a structured model from the saved analysis run. HTML/DOCX templates render it; they do not independently query the database, perform arithmetic or invent unsupported content.

The model should carry:
- Case/issue identity and run identity.
- Information cutoff and creation time.
- Evidence inventory, source versions and data-quality warnings.
- Verified facts and locators.
- Calculated metrics and formula traces.
- Cross-check findings and their inputs.
- User assumptions and scenario results.
- Missing/stale/conflicting/invalid/not-applicable states.
- Unresolved questions, limitations and confidence rationale.
- Methodology and formula/rule versions.
- Source bibliography and timestamps where known.

### 16.2 Required report sections

The PRD remains the report-content baseline. A section may be unavailable or deferred when evidence does not support it, but it must not be silently replaced by fabricated text.

1. Executive assessment for the listing-day objective and evidence sufficiency.
2. Issue identity, offer dates, price, lot size, issue size, fresh issue/OFS and offer mechanics.
3. Evidence inventory, versions, time metadata, missing documents and data-quality warnings.
4. Financial trends with formulas and source/page references.
5. Earnings quality, cash-flow conversion and accounting/working-capital checks where supported.
6. Customer, supplier, product, geographic and operational concentration where disclosed.
7. Promoter, governance, related-party, legal, litigation and regulatory findings.
8. Valuation and peer-comparability limitations.
9. Subscription, anchor data, GMP, float/supply and market context only when timestamped evidence exists.
10. News/attention review only when evidence exists; it is not a P0 dependency.
11. Contradiction matrix: relationship tested, conflicting inputs, explanations considered and unresolved status.
12. Material risks with rationale rather than unsupported precision.
13. Scenario results and qualifications; no auto-forecast is required by MVP.
14. Counter-thesis: strongest evidence-based reasons a positive thesis may be wrong.
15. Data gaps, manual-review questions, confidence rationale and cutoff.
16. Source bibliography with exact locators and timestamps where available.
17. Methodology appendix with formulas, units, periods, versions, traces and caveats.

### 16.3 Claim classification

Every material claim should be classifiable as:
- Verified/source-backed fact.
- Cross-checked fact.
- User-entered, externally unverified observation.
- Extraction candidate awaiting review.
- Deterministically calculated result.
- Rule-generated finding.
- Interpretation/hypothesis.
- User-defined scenario assumption/result.
- Unknown, conflicting, stale, unavailable or not applicable.

Do not state all claim types with the same certainty. Wording and/or visible status must communicate the difference.

### 16.4 Export integrity

Before accepting a report:
- Citations/locators point to stored evidence.
- Calculation references exist.
- Correct run and cutoff are used.
- Limitations and statuses survive export.
- Required sections are not silently dropped when data are missing.
- HTML preview and DOCX output are checked in regression tests.
- Reopening or changing display filters does not implicitly rerun calculations.

---

## 17. Runtime, configuration and failure handling

### 17.1 Keep operation simple

Do not add a queue or distributed job runner by default. Start with normal local API calls and service execution. Test representative evidence registration, parsing and analysis to identify actual latency/memory needs. If an operation proves too slow, measure it and then consider a minimal local persisted-operation/background-worker design. Do not introduce Redis/Celery pre-emptively.

### 17.2 Health and diagnostics

- Provide a local health endpoint.
- Distinguish “API is running” from “this case has enough evidence for a complete report.”
- Show optional provider configuration/availability separately from core health.
- Keep logs useful but avoid full document content, secrets and unnecessary private paths.
- Surface a stable error code and actionable message for failures.
- Optional provider failure is not a successful empty dataset.

### 17.3 Configuration

- Core MVP must not require external API keys.
- Include an example configuration file only for documented optional future integrations; never commit credentials.
- Ignore local database files, evidence, generated reports, caches, logs and real environment files in Git.
- A missing optional credential disables that adapter with a clear status.
- No fallback may secretly use a paid provider.

### 17.4 Internet requirement

After installation, the core case/evidence/calculation/report workflow must work without internet. Users can research source material externally and register it manually. Avoid arbitrary URL fetching in P0. If retrieval is later added, restrict it to reviewed source domains, enforce timeouts/size limits, validate redirects and document access terms.

---

## 18. Security and privacy

Local-first does not mean input is trusted or a local service should be exposed to a network.

### 18.1 Local access

- Bind frontend/backend development servers to loopback by default.
- Do not expose the backend on a LAN or public internet.
- Restrict CORS to the configured local frontend origin.
- Do not add authentication in the single-user MVP unless the deployment model changes.
- Any non-loopback/public deployment requires a separate security design and must not be treated as a trivial configuration change.

### 18.2 File processing

- Support only explicitly configured file types; check content as well as extension.
- File-size limits are selected after testing representative documents.
- Use generated paths and prevent path traversal.
- Fail safely on malformed, encrypted, corrupt or unsupported documents.
- Never execute macros, scripts, attachments or embedded active content from source files.
- Treat filenames, document metadata, OCR text, extracted text and hyperlinks as untrusted input.

### 18.3 Prompt injection and AI

Uploaded documents and web text are evidence, not instructions for the app or AI agent.
- Document text must never change app policy, permissions, configuration or tool access.
- Never execute instructions embedded in a source.
- Extracted content must not trigger arbitrary network requests, code execution or file-system operations.
- If AI is later added, delimit source content as untrusted and give the model the narrowest possible tool/action permissions.
- Validate model output against an explicit schema and evidence links; reject malformed or unsupported fields.

### 18.4 Privacy and logs

- Do not collect PAN, bank details or IPO application identifiers.
- Keep research files local unless the user explicitly uses an approved external service and the transfer is documented.
- Never send documents to an AI provider as a hidden side effect.
- No analytics or telemetry is needed.
- Do not log secrets, unnecessary file paths or full private document contents.
- Define a local deletion and backup policy before implementing destructive deletion.

---

## 19. Data-source integration strategy

### 19.1 Evidence hierarchy

Default hierarchy:
1. Regulatory filings and official offer documents.
2. Official exchange and issuer disclosures.
3. Official registrar/process records when relevant.
4. Reputable secondary reporting for discovery/context.
5. Unofficial observations such as GMP, visibly labeled and timestamped.
6. User input or unreviewed extraction, with status shown.
7. Derived results, labeled as calculated rather than observed.

Source class alone does not guarantee quality. Assess the exact item, version, period, timestamps, applicability and locator.

### 19.2 P0 source behaviour

P0 requires **no live provider adapter**. It must support:
- Local upload/registration of official offer PDFs and supporting material.
- Manual issue, financial and offer-data entry.
- Manual time-sensitive observations if the user has them.
- Source metadata and locators.
- Visible missing data, stale observations and conflicts.
- Deterministic local calculations and report generation.

The source audit did not establish a dependable, unrestricted, free historical pipeline. Do not design the core around one.

### 19.3 Adapter approval gate

Before approving any external adapter, document and test:
- Exact fields and their definitions.
- Issue/security identity mapping.
- Source authority and timestamps (publication, event, observation and retrieval).
- Historical coverage, gaps and corrections.
- Format/API stability, pagination, rate limits and failure behaviour.
- Current access/use terms, storage/retention, caching, derived data, export/redistribution and attribution.
- Total cost, overage and upgrade requirements.
- Repeatable representative tests.
- Manual fallback when the adapter is missing or unavailable.
- Whether it improves an approved requirement enough to justify maintenance.

A visible public webpage does not automatically mean a stable public API or permission to scrape/reuse the data. Exchange data access and redistribution require source-specific review. An adapter must fail clearly rather than guess or return a silently empty dataset.

### 19.4 SAWA lessons

Prior SAWA work attempted Google Trends via pytrends, but it did not work as expected; the exact root cause is unknown. NewsAPI was explored as an alternative, but ticker-only queries could be weak and missing/placeholder credentials or request failures could leave news unavailable.

Apply these lessons without turning SAWA into the IPO Engine's architecture:
- Google Trends is P2 at most and never an MVP dependency.
- NewsAPI is not selected or approved as a core provider.
- No paid endpoint or API key is required.
- Any news/attention adapter must be tested for coverage, current terms, timestamps, historical availability, failure behaviour and compliant fallback.
- Attention indicates attention, not truth, actual demand or a standalone listing-gain prediction.

---

## 20. Test strategy and release gates

A fluent report with wrong arithmetic is worse than an incomplete report with visible limitations.

### 20.1 Backend unit tests

Cover:
- Known-answer fixtures for every enabled formula.
- Missing, null, malformed and invalid inputs.
- Zero, negative and near-zero denominators where relevant.
- Unit/scale mismatch.
- Period and standalone/consolidated mismatch.
- Applicability and not-applicable states.
- Stale/conflicting input handling.
- Decimal precision and display rounding.
- Listing return arithmetic.
- Cross-check trigger and non-trigger logic.
- Identity ambiguity.
- Information-cutoff inclusion/exclusion.
- File hash and evidence status transitions.

Expected values must be independently verified; do not generate expected answers by calling the same implementation under test.

### 20.2 Backend integration tests

Cover:
- Create/reopen case.
- Register evidence and metadata.
- Duplicate filename without overwriting.
- Manual fact entry and validation.
- Candidate review, correction and rejection.
- Preservation of conflicting values.
- Save/retrieve analysis run and input snapshot.
- Report generated from a saved run.
- Database/filesystem failure handling.
- Operation without internet or optional credentials.

Use temporary directories and temporary test databases. Tests must not touch real user research data.

### 20.3 API contract tests

Cover:
- Actual API matches OpenAPI description.
- Success request/response shapes.
- Validation errors and required fields.
- Enum values and nullability.
- Time and decimal representation.
- Consistent error envelope.
- Reproducible generation/check of TypeScript API types.
- Field removal/rename fails a contract test or frontend check.

After the Data Contract is approved, add representative JSON fixtures for each major API resource group.

### 20.4 Frontend tests

Cover loading, empty, success, failure, validation errors, stale/conflicting/not-applicable states, review actions, exact API field use, identity/prerequisite blocking, scenario labels, citation navigation and accessible controls. Status must not rely on colour alone.

### 20.5 End-to-end acceptance case

1. Create a Mainboard IPO case.
2. Resolve the issue identity.
3. Register an official offer PDF and another source.
4. Manually enter a small approved set of facts with unit, period and provenance.
5. Include a missing value and a conflicting pair.
6. Confirm the UI shows missing/conflict state.
7. Run approved formulas and cross-checks.
8. Enter a scenario price and reproduce the known gross-return answer.
9. Generate HTML and DOCX while preserving citations, warnings and scenario labels.
10. Close/reopen the case and inspect the saved run/report.
11. Run a new analysis and prove the previous one is unchanged.
12. Repeat the core path without live provider, paid API or AI service.

### 20.6 Release gate

Do not release until enabled formula tests pass; API contract checks pass; manual/offline core workflow passes; missing values are not zero-filled; conflicts remain visible; material claims are traceable or marked unresolved/hypothesis; old runs/reports are preserved; exports retain caveats; no paid service is required; and no critical defect is hidden by a successful-looking report.

---

## 21. Implementation sequence

This order is recommended; it does not authorize deferred scope.

### Phase 0 — validate the architecture scaffold

Deliver:
- Confirm frontend/backend/dependency combination installs and runs locally at no cost.
- Implement a minimal frontend-to-FastAPI health request.
- Verify OpenAPI can generate/check TypeScript API types.
- Establish test commands and local validation scripts.
- Confirm a safe application data directory and ignored runtime paths.

Exit gate: both processes run locally, frontend reaches API, type generation works, and no user data/secrets enter Git.

### Phase 1 — case and identity

Deliver:
- Case creation/list/detail/reopen.
- Mainboard-only enforcement.
- Identity ambiguity and resolution.
- Initial persistence models/migrations.
- Data Contract for this vertical slice.

Exit gate: case survives restart; ambiguous issue identity is visible.

### Phase 2 — evidence and manual input

Deliver:
- Original evidence registration and source metadata.
- File integrity/checksum.
- Manual fact/observation entry.
- Unit/period/status/locator capture.
- Candidate review and conflict states.
- Safe file handling and no-provider fallback.

Exit gate: research can be completed using local evidence and manual input alone.

### Phase 3 — approved formula register

Deliver:
- Select a limited P0 formula set from the Indicator Catalogue.
- Approve definitions and independently verified golden fixtures.
- Implement deterministic decimal-safe calculations.
- Add prerequisite/status checks and calculation lineage.
- Keep unapproved catalogue formulas disabled.

Exit gate: all enabled formulas pass known-answer and invalid-input tests.

### Phase 4 — initial cross-checks

Deliver:
- Small high-value set of deterministic cross-checks.
- Evidence/input links on every finding.
- Visible conflicts and competing explanations.
- Correct missing/stale/not-applicable behaviour.

Exit gate: seeded conflicts and rule triggers are surfaced correctly.

### Phase 5 — scenarios and reports

Deliver:
- User-entered scenario prices.
- Gross-return calculation.
- Report model, HTML preview and DOCX export if offline path tests pass.
- Saved run/report artifacts.

Exit gate: one report is auditable, export-safe and reproducible.

### Phase 6 — reliability and recovery

Deliver:
- Error handling and local diagnostics.
- Migration and integrity checks.
- Backup/restore procedure and test.
- End-to-end regression suite.
- Clean setup/run/test/restore instructions.

Exit gate: a restored test bundle can reopen its case, evidence and saved report.

### Later phases only after P0 works

- Improved table extraction and local OCR.
- Sector-specific checks and expanded catalogue coverage.
- Subscription/GMP/news observations and optional approved adapters.
- Google Trends only if access and evaluation plan justify it.
- Historical backtesting with point-in-time inputs and an explicit outcome definition.
- Model calibration only after representative history and out-of-sample validation.

---

## 22. Decisions register

| Decision | Status/recommendation | Rationale or next action |
|---|---|---|
| Overall architecture | **Recommended:** local modular monolith | Smallest design that separates UI, API, analysis and persistence. |
| Frontend | **Recommended:** React + TypeScript + Vite | Fits local SPA; validate scaffold. |
| Backend | **Recommended:** Python + FastAPI | Fits document/financial analysis. |
| API schema | **Recommended:** Pydantic + OpenAPI + generated/checked TypeScript types | Prevents hand-maintained contract drift. |
| Exact API field names/payloads | **Deferred to Data Contract step** | Finalize after module responsibilities and end-to-end flow. |
| Wire property casing | **Must be decided in Data Contract** | Choose once and enforce everywhere. |
| Persistence | **Recommended:** SQLite | Single-user local app without server. |
| ORM/migrations | **Recommended:** SQLAlchemy + Alembic | Validate setup; use controlled migrations. |
| Local path/OS support | **Requires validation** | Confirm safe per-user paths and recovery strategy. |
| Evidence files | **Recommended:** filesystem plus DB metadata/checksum | Preserve originals and versions. |
| PDF types/size limits | **Requires representative tests** | Do not invent compatibility claims. |
| Extraction method | Manual first; extraction candidates; OCR later if justified | Reviewability and accuracy over auto-fill volume. |
| P0 formula list | **Open analytical decision** | Approve small formula register and golden test data. |
| Cross-check set | Small tested subset first | Avoid enabling all catalogue rules at once. |
| AI provider | None required; optional adapter only | Respects ₹0 and manual-first constraints. |
| News/Trends/subscription/GMP providers | Not selected; not P0 | Source audit and SAWA lessons require caution. |
| Report export | HTML preview; DOCX first recommended; PDF later | Test offline export. |
| Backup/restore | Required to be specified/tested before valuable data storage | No paid/cloud dependency. |
| Background jobs | Not required initially | Profile first; add only for measured latency need. |
| Public hosting/authentication | Out of MVP | Separate security/product decision. |
| Historical model/backtest | Deferred | Requires timestamped data, outcome definition, leakage controls and out-of-sample test. |

---

## 23. Data Contract readiness checklist

Do not implement a large set of endpoint payloads until these items are agreed and written in this same canonical file.

- [ ] Confirm module responsibilities and case-to-report data flow.
- [ ] Agree conceptual entities/relationships and which objects need persistent IDs.
- [ ] Define the endpoint list and methods.
- [ ] Choose canonical wire property naming.
- [ ] Define exact request/response schemas, required/optional/null fields and enums.
- [ ] Define identifiers, timestamps, date-only fields and time zones.
- [ ] Define decimal/money serialization and display rounding.
- [ ] Define all statuses and allowed transitions.
- [ ] Define the common error envelope and field validation errors.
- [ ] Define upload/download behaviour and cleanup/error rules.
- [ ] Define collection retrieval/pagination only where needed.
- [ ] Define API versioning and contract-change policy.
- [ ] Generate OpenAPI and TypeScript API types from the approved contract.
- [ ] Write contract tests before frontend features depend on the endpoints.
- [ ] Review the contract against PRD requirements, the Indicator Catalogue and Data Source Audit.

The project owner explicitly identified frontend/backend interconnection and exact variable names as a major implementation risk. The answer is to formalize the interface before building UI features, not to invent every payload before architecture and flow are understood.

---

## 24. Pre-implementation checklist

Before the first substantive feature:
- [ ] Confirm the React/Vite + FastAPI baseline runs on the development machine.
- [ ] Confirm all required dependencies are open source and need no payment/billing.
- [ ] Confirm core operation without internet after installation.
- [ ] Confirm local database/evidence/reports/logs/secrets are excluded from Git.
- [ ] Confirm initial app-data path and backup approach.
- [ ] Approve the first Data Contract vertical slice.
- [ ] Approve the first P0 formula register and independently checked fixtures.
- [ ] Test representative Mainboard IPO documents for preservation and extraction feasibility.
- [ ] Define minimal report sections and export acceptance test.
- [ ] Check that repository instructions and README links point to files that actually exist; do this as a focused link correction, not a broad documentation rewrite.

---

## 25. MVP technical acceptance criteria

The implementation is technically acceptable only when:

1. Frontend and backend interoperate through the agreed, tested contract.
2. API schemas and generated TypeScript types do not drift.
3. One Mainboard IPO case can be created, saved, reopened and resolved correctly.
4. Original source documents are preserved and are not overwritten by extraction or later versions.
5. Facts/observations preserve unit, period, provenance and status, or clearly indicate unknowns.
6. Manual entry works without internet or optional provider/AI.
7. Unreviewed extraction cannot silently become a trusted formula input.
8. Missing, conflicting, stale, invalid and not-applicable states remain distinct.
9. Every enabled formula passes approved known-answer and invalid-input tests.
10. Material calculated outputs include input lineage and formula/rule version.
11. Cross-check findings explain triggers and limitations without unsupported causal/fraud claims.
12. Listing-return calculations are deterministic and scenario assumptions are not presented as observed prices.
13. Allotment and conditional return are separate.
14. A new run does not rewrite an earlier run/report snapshot.
15. Reports retain citations, cutoff, missingness, conflicts, assumptions and limitations.
16. Manual-first workflow needs no paid service, cloud host, remote database, AI API or market-data API.
17. Backup/restore succeeds before valuable research is stored.
18. A clean setup can install, test and run using documented steps without undeclared local files.

---

## 26. Instructions for coding and review agents

Any coding agent must:
1. Read AGENTS.md and the canonical project documents before implementation.
2. Follow fixed constraints and respect any decision still marked deferred/requires validation.
3. Identify relevant PRD requirement IDs and indicator IDs before changing behaviour.
4. Never invent field names, formula definitions, statuses, source metadata or API payloads; use the approved Data Contract.
5. Keep deterministic calculations separate from AI-generated prose.
6. Add no paid or mandatory online dependency.
7. Do not implement SME IPO support or order execution.
8. Do not fabricate missing data or suppress source conflicts.
9. Add and run relevant tests; report actual results and failures.
10. Never silently overwrite prior evidence, runs or reports.
11. Keep changes scoped; inspect the diff and do not discard unrelated work.
12. Update this same canonical file when a technical decision changes. Do not make numbered or dated copies; Git history is the revision history.
13. If an unresolved decision blocks safe implementation, identify the exact decision and impact rather than making an unapproved assumption.

---

## 27. Glossary

| Term | Meaning |
|---|---|
| Issuer | Company identity, separate from a specific offering. |
| IPO issue | One specific Indian Mainboard IPO. |
| Research case | Saved workspace for one IPO investigation. |
| Evidence item | Specific source document, observation or registered evidence object. |
| Source record | Metadata about the evidence origin. |
| Fact | A sourced, entered or reviewed value with unit/period/provenance. |
| Candidate fact | Extracted/unreviewed value not yet trusted as a calculation input. |
| Indicator | Defined measure or check with prerequisites and limitations. |
| Formula | Deterministic calculation definition for a metric or scenario output. |
| Cross-check | Explicit test of a relationship between multiple facts/indicators. |
| Finding | User-facing analytical result linked to its input/evidence basis. |
| Analysis run | Saved execution based on a particular input snapshot, cutoff and rule versions. |
| Information cutoff | Latest information permitted in a specific run. |
| Scenario assumption | Hypothetical/user-entered input, not an observed fact. |
| Listing-day return | Conditional return from issue price to specified scenario/observed exit price, before costs unless modeled. |
| Allotment probability | Separate concept from return conditional on allotment. |
| Manual-first | Core workflow works with user-supplied evidence and manually entered data. |
| Local-first | Core application operations and data remain on the user's machine. |

---

## 28. Technical references

Official references informing the recommended technologies. Check compatibility and supported versions at implementation time:

- FastAPI features, OpenAPI and JSON Schema support: https://fastapi.tiangolo.com/features/
- OpenAPI Specification: https://spec.openapis.org/oas/latest.html
- Pydantic model validation: https://docs.pydantic.dev/latest/concepts/models/
- SQLite appropriate-use guidance: https://www.sqlite.org/whentouse.html
- Next.js App Router documentation (considered but not the baseline because server rendering is unnecessary for the local SPA): https://nextjs.org/docs/app

Project-specific evidence-source research stays in the Data Source & Feasibility Audit and Project Brief. This design is not a legal, licensing or market-data certification.

---

## 29. Current recommended sequence

**Technical baseline:** React + TypeScript + Vite frontend, Python + FastAPI backend, OpenAPI-driven contract with generated/checked TypeScript types, SQLite, local evidence-file storage, deterministic Python formula/rule engine, local HTML preview and DOCX-first export.

**Engineering order:** validate the local scaffold → agree module responsibilities → confirm the end-to-end IPO-case-to-report data flow → finalize the Data Contract in this same document → approve the initial formula register → implement the first vertical slice.

**Do not implement a large list of endpoints or indicators before the Data Contract and formula register are agreed.** The next step is to review the proposed architecture and resolve its marked decisions, not to generate more versions or redo the existing four documents.
