---
title: IPO Forensic Analysis Engine — Application Flow
document_id: AF-IPO-001
version: 1.0
status: Proposed MVP flow specification; validate in design review before implementation
last_updated: 29 October 2026
canonical_source: Markdown in GitHub
scope: Indian Mainboard IPOs only; local-first; single-user; manual-first; ₹0 budget
---

# IPO Forensic Analysis Engine
## Application Flow and User Journey Specification

> **Purpose:** Define how a user moves through the IPO Forensic Analysis Engine, what each screen is responsible for, what must happen before each action is allowed, how success/failure/missing-data states are presented, and what must be tested before implementation is considered complete. This document turns the approved PRD journeys into an implementable interaction flow. It is not a visual design system, a database schema, or the final API/Data Contract.

**The aim is to prevent integration rework.** The frontend should not invent behaviour that the backend cannot support, the backend should not require data that the UI has no way to provide, and missing or conflicting evidence must not result in a misleadingly successful report. Every MVP screen/action below must eventually be mapped to a backend use case, a contract definition, and an acceptance test.

---

## 1. Document authority and how to use this specification

Read this document together with the repository's existing canonical files:

1. Project Brief — overall vision and forensic-research principles.
2. Approved PRD — functional requirements and acceptance criteria.
3. Data Source & Feasibility Audit — evidence/source limits, access constraints and manual fallback.
4. Indicator Catalogue & Data Dictionary — indicator meaning, data status and formula requirements.
5. Technical Design — proposed architecture, module responsibilities, persistence, validation, reporting and testing.

This document describes **user-visible flow and interaction behaviour**. The Technical Design describes **how the application is structured technically**. The proposed [Database Schema](database-schema.md) v0.1 defines the initial SQLite persistence entities, fields and relationships; it still requires alignment with the first Data Contract and migration tests. The Data Contract will define **exact API field names, types, requests/responses and wire status enums**. The UI/UX Design defines **visual layout, component styling and responsive behaviour**.

Do not copy all of these subjects into each document. Link them and keep one authoritative home for each decision.

### 1.1 Binding project decisions

- **Coverage:** Indian Mainboard IPOs only. Do not provide an SME IPO mode.
- **Budget:** ₹0 total project budget. No paid API, dataset, AI service, hosting, managed database, software upgrade or paid fallback.
- **Operation:** local-first, single-user and manual-first.
- **No mandatory online source:** case creation, evidence registration, manual entry, deterministic calculation and reporting must not require an external source API or an AI service.
- **Evidence integrity:** AI/extraction may not invent facts, values, citations, pages, timestamps or sources.
- **Unknown is not zero:** missing, stale, invalid, conflicting and not-applicable inputs must remain distinguishable.
- **Reproducibility:** a new analysis run must not silently rewrite a previous run or report.
- **No trading:** the application never submits or modifies market orders.
- **No prediction claim without validation:** user-entered scenarios are conditional calculations, not model forecasts or guaranteed outcomes.

If this document or an old source uses wider wording, the binding constraints above take precedence until the source is deliberately reconciled.

### 1.2 Status labels used throughout the flow

These labels describe behaviour. Their exact wire enum spelling will be finalized in the Data Contract.

| Conceptual state | Meaning for the user |
|---|---|
| Ready | Required prerequisites for the immediate action are satisfied. |
| Needs attention | The user can continue with a warning or review task. |
| Blocked | A required prerequisite is unsatisfied; the action cannot produce the claimed result. |
| Missing | Expected input/evidence has not been supplied or found. |
| Not applicable | The metric or workflow step does not apply to this issue. |
| Unverified / review required | The value exists but has not been sufficiently checked. |
| Conflicting | Material sources disagree; both remain visible. |
| Stale | The data may no longer be suitable for the decision time. |
| Failed | The attempted operation did not complete. |
| Saved | The application confirms that the change was persisted. Do not show “saved” optimistically before persistence succeeds. |

---

## 2. Main user objective

The primary user is one person conducting research on a specific Indian Mainboard IPO, usually to evaluate possible listing-day exit outcomes. The app should help the user build a defensible evidence record, review company-specific risks, identify conflicting signals, calculate conditional scenarios and produce a source-cited report.

The main journey is:

**Create case → confirm issue identity → register evidence → enter/review facts → check readiness → run analysis → investigate findings → enter scenarios → preview/export report → reopen previous run.**

The workflow is deliberately not “enter ticker → automatic score → buy/sell answer”. Automatic retrieval is not dependable enough to be an MVP prerequisite, and the product must be useful with manual evidence.

### 2.1 User should always be able to answer

At every stage, the interface should make these questions clear:

- Which IPO issue am I researching?
- What have I saved, and what is still unsaved?
- Which evidence supports a material fact?
- Which values are accepted, unverified, conflicting, stale or missing?
- Why can or cannot I run a particular analysis?
- Which calculations were actually performed, and which were blocked?
- What assumptions produced a scenario result?
- Which report/run am I viewing?
- Has my case changed since that report was created?
- What can I do next to fix a problem without losing prior work?

---

## 3. Product-wide navigation and screen map

### 3.1 Primary navigation

The local application should use a small, predictable navigation structure:

1. **Home / Cases** — list saved research cases and start a new one.
2. **New IPO Case** — enter identifying information and resolve the issue.
3. **Case Workspace** — central location for issue overview, evidence, facts, analysis, scenarios, reports and prior runs.
4. **Settings / Local Data** — only essential local application settings and data-location/backup guidance, if implemented in MVP. Do not create account/profile settings or analytics screens.

The user should not need to remember which feature page is separate from which case. Evidence, facts, analysis and reports are sub-sections of one case workspace.

### 3.2 Recommended frontend route map

These are **frontend navigation routes only**, not backend API endpoints. They may be adjusted in UI design, but route identity must be stable and based on saved identifiers rather than issuer display names.

| Screen ID | Recommended frontend route | Purpose |
|---|---|---|
| HOME-01 | /cases | List cases, show their current state, reopen or create a case. |
| CASE-01 | /cases/new | Create an IPO research case. |
| CASE-02 | /cases/{caseId} | Case overview and readiness summary. |
| EVID-01 | /cases/{caseId}/evidence | Evidence inventory, upload and source registration. |
| FACT-01 | /cases/{caseId}/facts | Review facts, enter manual values and resolve conflicts. |
| ANAL-01 | /cases/{caseId}/analysis | Preflight readiness, run analysis and inspect run results. |
| SCEN-01 | /cases/{caseId}/scenarios | Enter and compare user-defined listing-day scenarios. |
| RUN-01 | /cases/{caseId}/runs/{runId} | Inspect an immutable saved run. |
| REPT-01 | /cases/{caseId}/reports/{reportId} | Preview, export and reopen a saved report. |
| SET-01 | /settings | Minimal local settings/backup guidance, if in MVP. |

Do not create all routes as empty placeholders. Implement each route when its underlying use case is ready. Direct navigation to an unknown case/run/report must show a clear not-found state and a way back to the case list.

### 3.3 Case workspace navigation

A saved case workspace should contain these sub-sections:

- **Overview**
- **Evidence**
- **Facts & Review**
- **Analysis & Findings**
- **Scenarios**
- **Reports & History**

Use persistent case context in the workspace, including the issue display name and identity state. Do not create separate, duplicate “IPO projects” for the evidence, facts, analysis and report of the same issue.

### 3.4 Navigation rules

- Navigation must use stable case/run/report identifiers.
- Moving between screens must not discard unsaved form edits silently.
- If an operation is in progress, navigating away must either be safe or provide a clear warning about work that is not saved.
- Returning to a case restores persisted state; it must not implicitly rerun analysis.
- Opening a saved report displays the saved report, not an automatically refreshed analysis.
- Browser refresh, app restart and reopening a saved case must not lose successfully persisted data.
- A deleted/unknown identifier must not silently fall back to a different case with a similar name.
- Do not add user accounts, team navigation, a public dashboard or trading links.

---

## 4. Global screen and interaction rules

### 4.1 Every data-backed screen has defined states

Every screen that loads or saves data must define and implement:

- Initial/loading state.
- Successful state.
- Empty state with an actionable next step.
- Validation-error state.
- Recoverable operation-error state.
- Persistent storage failure state.
- Stale/conflicting/unverified data state where relevant.
- Not-found state for deleted/unknown records.
- Partial state when some information is available but other sections are blocked or missing.

A screen is not complete if only the successful state has been designed.

### 4.2 Save behaviour

- Each user action that changes persistent data must have a clear save/confirm action or a clearly described auto-save mechanism.
- For MVP, prefer explicit Save/Accept/Resolve actions for facts, evidence metadata and scenario inputs; do not rely on hidden auto-save for consequential research edits.
- Show a saving indicator while persistence is pending.
- Show Saved only after the backend confirms success.
- If saving fails, retain the user's current form values where safe, show an actionable error and allow retry. Do not clear the form or claim the data was saved.
- If a submission may have succeeded but the response was lost, prevent blind duplicate creation where possible; refresh/reconcile persisted state before retrying destructive or duplicating actions.
- When a change affects a prior analysis, show that the case has changed since the last run. Never silently modify that run/report.

### 4.3 Action labels

Use specific verbs that describe the actual operation:
- Create case
- Confirm issue identity
- Add evidence
- Enter observation
- Review candidate
- Accept value
- Correct value
- Reject candidate
- Mark unresolved
- Resolve conflict
- Check readiness
- Run analysis
- Add scenario
- Generate report
- Export report
- Open previous run

Avoid vague labels such as “Process”, “AI Analyze”, “Fix Data” or “Predict” where they hide the actual outcome.

### 4.4 Information hierarchy

Every important value should be distinguishable as one of:
- Source-observed fact.
- User-entered unverified observation.
- Candidate extraction.
- Accepted/verified fact.
- Calculated indicator.
- Rule-generated finding.
- Interpretation/hypothesis.
- Scenario assumption/result.
- Unknown/blocked/not applicable.

Never rely on colour alone. Pair status colour/icon with accessible status text. Show units, reporting period, issue identity, source and relevant as-of time beside values, or provide a direct path to inspect them.

### 4.5 Single-user/local-first context

- No login screen is required.
- Do not display account, subscription, billing, cloud sync or team-management UI.
- If a source API/AI adapter is disabled or unavailable, the app still supports manual evidence and analysis.
- The UI must not imply that a value is live/current when it is only a saved snapshot.
- No external service should receive a file or fact without an explicit, approved flow and source/terms decision.

---

## 5. Screen specifications

## 5.1 HOME-01 — Cases / Home

### Purpose

Provide a reliable starting point for creating a new case or reopening existing research.

### Primary content

- Application title and short purpose statement.
- “New IPO case” primary action.
- List of saved cases with issuer/issue display name, issue identity status, last activity, latest analysis/report state and visible warnings where relevant.
- Search/filter may be basic and local; do not make network search a dependency.
- Empty-state guidance for the first case.
- Clear storage/application error if the local data store cannot be read.

### Primary actions

- Create a new case.
- Open an existing case.
- Resume a case with unresolved identity/evidence tasks.
- Open minimal settings/backup guidance if implemented.

### Required states

| State | Behaviour |
|---|---|
| First use / no cases | Explain that the user can start a Mainboard IPO research case and enter evidence manually. Do not show dummy cases as real data. |
| Cases loaded | Show saved cases and each case's real status. |
| Loading | Display an accessible loading message/skeleton without implying that no cases exist. |
| Database unavailable/corrupt | Show a clear local-data problem and safe recovery guidance; do not present an empty case list as if the user has no data. |
| Partial item metadata | Show known values and an explicit unknown status; do not invent last-run or issue details. |
| No matching filter | Show “no matches” and allow clearing the filter. |

### Acceptance checks

- Creating a case opens the new-case flow.
- Opening a case uses its stable identifier.
- Empty state appears only after a successful read returning zero cases, not after a failed read.
- A storage/read error never masquerades as an empty project.
- Reloading the app preserves successfully saved cases.

---

## 5.2 CASE-01 — Create IPO Research Case

### Purpose

Create a saved case without assuming that the user has a ticker or complete issue record. After a likely issue is identified, initiate acquisition using reviewed/approved source connectors; do not assume that every source has a free API or is retrievable.

### Inputs

The form should request the minimum information needed to establish a case:
- User-entered issuer/issue display name.
- Optional known identifiers or issue details that help disambiguate it.
- Optional note for the research purpose.

Exact field names and the final validation schema belong in the Data Contract. Do not require a symbol/ticker if a Mainboard IPO may not have a useful listing symbol yet.

### Behaviour

1. User opens New IPO Case.
2. User enters the known name and any optional identifiers.
3. Input is validated for basic completeness and length.
4. The system creates a draft/research case with identity status reflecting what is actually known.
5. The app attempts issue discovery using approved sources/connectors and presents candidate matches with supporting identifiers and provenance. Do not assume a universal free search API exists.
6. If there are multiple plausible issues or the issue is not yet confirmed, the case remains identity-unresolved; do not attach fetched observations to an uncertain issue or run final analysis.
7. Once identity is confirmed, the core acquisition orchestrator attempts retrieval from enabled/approved connectors for the critical signal categories they support, including official category subscription (QIB/NII/retail) and named unofficial GMP sources where a compliant route has been verified.
8. The app records and displays which sources were attempted, which fields were returned, source and observed/publication/retrieval times, freshness, partial coverage and failures/unavailable/blocked categories. A failed attempt is not represented as a successful check.
9. User may register supporting documents, retry a connector, import data or enter an observation manually where any signal is unavailable. Saving and manual research must remain usable offline.
10. The app clearly indicates whether full or partial analysis is currently blocked by identity uncertainty, unavailable sources, stale observations or missing evidence.

### Mainboard-only behaviour

- Do not offer an SME/Mainboard switch.
- If the user identifies the requested issue as an SME IPO, stop the in-scope analysis flow and explain that the product currently supports Mainboard IPOs only.
- Do not silently reclassify an ambiguous issue as Mainboard.
- If market segment is unknown, identity remains unresolved until there is adequate evidence to confirm it.

### Required actions

- Create case.
- Cancel/back to cases.
- Confirm/correct issue identity once supporting information is adequate.

### Required states and recovery

- Empty required name: inline validation; do not create the case.
- Save failure: retain form input and permit retry.
- Duplicate-looking case: warn/offer to open the existing case where confidently identified, but do not merge or discard without user choice.
- Ambiguous identity: allow evidence entry and correction; block finalized analysis.
- Out-of-scope SME issue: clear explanation and safe return path.
- Unknown segment: ask for source evidence/confirmation rather than guessing.
- Duplicate-submit/retry: avoid creating multiple identical cases if the first save succeeded but the response failed.

### Acceptance checks

- FR-001: a case is saved and can be reopened.
- FR-002: user-entered search text is distinct from confirmed issue identity.
- Ambiguous identity is visible and correctable before full analysis.
- SME support is not accidentally introduced.
- No online API is required to create a case.

---

## 5.3 CASE-02 — Case Overview / Workspace

### Purpose

Show the state of a particular case and provide a clear route to the next useful action.

### Primary content

- Confirmed issue name and available identifying details.
- Identity state and the basis/source used to confirm it.
- Source-acquisition summary: connector status, last attempt/refresh, returned fields, partial coverage, freshness, unavailable/blocked categories and actionable retry/manual fallback.
- Summary of registered evidence and missing expected evidence.
- Fact review summary: candidates to review, unverified facts, conflicts, stale items and missing inputs.
- Last completed analysis run and report, if any.
- Whether the case has changed since the latest run.
- Analysis readiness summary with actionable blockers.
- Links into Evidence, Facts & Review, Analysis & Findings, Scenarios and Reports & History.

### Readiness display

Readiness is not a single confidence score. Show concrete items:
- Identity confirmed or unresolved.
- Evidence available/missing.
- Candidate values awaiting review.
- Conflicts needing resolution or explicitly left unresolved.
- Formula prerequisites missing/invalid.
- Acquisition status for relevant signal categories: latest attempt, freshness, source coverage, unavailable/blocked connector and manual fallback.
- Analysis can run partially, or final assessment is blocked for a stated reason.
- Report availability and freshness relative to the current case.

### Required behaviours

- Refresh the overview from saved state; do not run analysis implicitly. Source acquisition runs only from an explicit supported action or the defined post-identity-confirmation flow, never as a hidden side effect of opening the overview.
- Every warning should navigate to the relevant review screen where possible.
- A section marked “complete” must be based on persisted data/status, not only frontend-local state.
- Distinguish “not started” from “failed to load”.
- If the case has changed since its last completed analysis, show that the latest report reflects an earlier snapshot.

### Acceptance checks

- User can understand the current case state without opening every screen.
- All blockers link to a specific next action.
- Reopening the case displays persisted evidence, acquisition-attempt history and run history.
- A failed API call never displays a falsely complete readiness summary.
- The user can distinguish a successfully checked source with no relevant value from a source that was not attempted, was blocked, failed or returned partial data.
- The UI exposes manual entry/import when a relevant approved source is unavailable.

---

## 5.4 EVID-01 — Evidence Inventory and Registration

### Purpose

Register the source material used for the IPO investigation and preserve provenance.

### Evidence types

The workflow may register:
- DRHP/RHP/final prospectus/addenda and other offer documents.
- Official exchange/issuer/regulatory disclosures.
- Audited statements/annual reports or related evidence files.
- News/event source records when relevant.
- Manual market observations such as subscription/GMP with explicit source/time.
- User notes or manual values, clearly labeled as user-supplied when not externally verified.

The list above does not mean that every evidence type is required for every issuer or that each has an approved automatic source adapter.

### Add evidence flow

1. User chooses Add Evidence.
2. User chooses a local file or manual/source-record entry.
3. For a file, the UI explains supported file types and any configured size limit. The limit must reflect implementation-tested values.
4. User provides source metadata available to them: source type, title/publisher, URL if applicable, document/version date, publication/event time and relevant period/locator where known.
5. Unknown metadata may be left unknown; the app must not invent it.
6. User confirms registration.
7. Backend stores the original file safely, records metadata and calculates a checksum when supported.
8. UI confirms Saved only after the operation succeeds.
9. The evidence appears in the case inventory with a link to inspect metadata and relevant locators.

### Evidence inventory columns/information

Show the information most useful for audit, such as:
- Display title and evidence type.
- Source/publisher.
- Document/observation date and capture time when known.
- Version or relevant period.
- Verification status.
- Local-file availability/checksum status where appropriate.
- Facts or report claims that use this evidence, when linkage is implemented.
- Any error or limitation.

Do not crowd the default list with every technical metadata field; detailed metadata belongs in an inspect/details view.

### Duplicate and version behaviour

- The same filename is not proof that two files are identical.
- An exact content-hash match may trigger a duplicate warning, but do not silently delete or merge the new upload.
- A new version/addendum must be registered as a new evidence item linked to the relevant document family/case.
- Replacing a local file must not rewrite evidence used by prior runs.
- Preserve original bytes. Reprocessing creates new derived output, not a modified original.

### Required states

- No evidence yet: explain the recommended first official offer document and allow manual entry.
- Upload in progress: show progress where the platform supports it.
- Unsupported type/size: explain the exact reason and supported alternative; no partial success.
- Corrupt/encrypted/unreadable PDF: register original only if storage succeeded, mark parse as failed/unavailable, and allow manual entry or replacement.
- Metadata incomplete: allow save while visibly marking unknown metadata where the field is not a hard requirement.
- Save failure: preserve current form state and allow retry; never show success optimistically.
- Missing file on reopen: show an integrity error and do not claim its contents are available.
- Optional provider offline: not relevant to local/manual evidence registration and must not block it.

### Acceptance checks

- FR-010–FR-014.
- Original is preserved and no same-name file overwrites another.
- Unknown metadata remains unknown.
- An upload failure cannot create an evidence record that falsely claims an accessible file.
- Manual source records are possible without URL automation.
- A new document version cannot silently change a prior report.

---

## 5.5 FACT-01 — Facts, Observations and Review Queue

### Purpose

Provide one place to enter manual facts, inspect extracted candidates, accept/correct/reject values and resolve conflicting evidence.

### Views

Recommended tabs/filters within the same screen:
- All facts/observations.
- Needs review.
- Conflicting.
- Missing/expected.
- Stale.
- Not applicable.
- Accepted/verified.
- Rejected/resolved history, where useful.

Do not make each status a separate application module. These are views over the case's facts and observations.

### Manual entry flow

1. User selects Add Fact/Observation.
2. User identifies the kind of value or observation to record.
3. The form asks for value and necessary semantics: unit/currency, reporting/observation period, source/evidence link or user-supplied designation, relevant timestamp, and notes as applicable.
4. User saves the entry.
5. If a verifiable source is not attached, the value is marked user-entered/unverified; it is not represented as an official observed fact.
6. The UI shows validation result and any missing semantic details.
7. Accepted values become eligible only for calculations whose prerequisites/status policy allow them.

### Candidate extraction review flow

1. The user requests optional extraction from a registered document, if available.
2. The app displays a candidate value with the original text/context and page/section/table locator when available.
3. It displays extraction method, unit/period interpretation and any ambiguity.
4. The user can Accept, Correct, Reject or Mark unresolved.
5. Correcting creates a traceable corrected value; it does not rewrite the original extraction candidate.
6. Accepting does not erase the extraction origin or locator.
7. If locator/page extraction is unreliable, visibly state that the candidate cannot be independently located and require manual verification before a material calculation uses it.

Extraction is optional. If there is no extractor, no internet or a parser fails, the screen must still support manual entry.

### Conflict resolution flow

1. The app identifies materially disagreeing values for the same fact/period/basis.
2. The UI shows all competing values, their source/date/locator, units, periods and validation states.
3. User may mark the conflict resolved with a reason/evidence basis, or leave it unresolved.
4. Resolving must preserve the old values and the resolution note.
5. A formula may use a selected value only when the resolution policy makes the choice explicit and traceable; unresolved conflict must block or qualify affected calculations.
6. Never automatically average conflicting values or select the most recent source without an applicable documented rule.

### Required states

- No facts entered: show manual entry and evidence-registration next steps.
- Candidate review queue empty: state that no candidates currently await review, not that the data are complete.
- Candidate without locator: visible low traceability; review limitation shown.
- Invalid unit/period/value: inline field-level validation and explanation.
- Conflicting values: both (or all) remain visible.
- Stale value: show as-of time and impact on analysis readiness.
- Not applicable: require rationale when needed; do not score it as a failure.
- Save/update error: preserve edit form and retry option.
- User cancels review: candidate remains pending; no silent accept.

### Acceptance checks

- FR-020–FR-024.
- Extracted facts never become trusted without a visible review/validation path.
- Manual entry is available whether extraction succeeds or fails.
- Correct/reject/resolve actions preserve history where required.
- A fact without compatible unit/period/status cannot silently enter a calculation.

---

## 5.6 ANAL-01 — Analysis Readiness and Run

### Purpose

Validate the current case snapshot, tell the user what can be calculated, then run only the approved formulas/rules whose prerequisites are satisfied.

### Preflight step

Before a run, show an analysis readiness review with:
- Issue identity state.
- Inputs ready for use.
- Candidate facts still requiring review.
- Missing required inputs for each enabled formula/rule.
- Conflicting/stale/invalid values affecting specific calculations.
- Data/source limitations.
- Formulas or checks that are not applicable.
- The proposed information cutoff.
- Whether the run will be complete, partial/qualified, or blocked.

The app must not use a single generic “data completeness score” as a replacement for this detail.

### Information cutoff

The user must be able to inspect or set the cutoff used for the run. The defaulting policy is a remaining product decision and must be settled before implementation. Regardless of default:
- The actual cutoff is visible before the run.
- Evidence later than the cutoff is excluded from that historical decision snapshot or clearly flagged as outside cutoff.
- Unknown source times must not be fabricated to force inclusion.
- The saved run records the chosen cutoff.
- Historical backtests, if added later, must enforce point-in-time availability to prevent look-ahead leakage.

### Run action

1. User reviews readiness and initiates Run Analysis.
2. Backend validates the snapshot again; frontend validation alone is not sufficient.
3. The system saves a run record/snapshot according to the Technical Design.
4. Only approved and enabled formulas/rules execute.
5. Unsupported, missing-input, stale, conflicting or not-applicable calculations receive explicit states.
6. Run results and diagnostics are persisted.
7. UI navigates to or opens the saved run result.
8. If execution fails, show the failure and retain the last successful run/report.

The initial technical design recommends synchronous local service execution until measured performance justifies background processing. The UI must support a pending/progress state where needed, but the exact mechanism is an architecture decision, not a promise of a background queue.

### Run statuses

Use conceptual statuses such as:
- Preparing/validating.
- Running.
- Completed.
- Completed with qualifications.
- Blocked by required prerequisites.
- Failed.

The exact persisted/API enum values belong to the Data Contract. Do not show “Completed” if persistence or required calculations failed.

### Required states

- Identity unresolved: block finalized analysis and route user to identity review.
- No reviewed inputs: explain what to add; no invented initial results.
- Missing optional data: allow a qualified/partial report if requirements permit.
- Missing required formula inputs: that formula is blocked with a named reason; unrelated valid calculations may still run.
- Conflict affecting a calculation: block or qualify that output and link to conflict review.
- Invalid period/unit: block the affected calculation and explain why.
- No applicable formulas: do not manufacture an overall score; show that analysis is currently unavailable/limited.
- Run failure: show error reference and retry; do not delete prior runs.
- Case changed since preflight: require refreshing readiness or explicitly reconfirming the new snapshot.
- Storage failure: do not claim a run is saved if the run/result snapshot was not persisted.

### Acceptance checks

- FR-030–FR-033 and FR-062–FR-064.
- A run is tied to a known cutoff, input snapshot and formula/rule versions.
- Each triggered rule refers to its supporting input/evidence.
- Missing/invalid data produce visible states, not fabricated outputs.
- A failed new run does not erase the prior successful run.
- Reopening a run does not rerun the analysis.

---

## 5.7 RUN-01 — Analysis Results and Findings

### Purpose

Let the user investigate calculated metrics and cross-indicator relationships rather than merely consume a score.

### Primary sections

1. Run summary and information cutoff.
2. Data quality/coverage and readiness limitations.
3. Financial/offer metrics calculated by the enabled formula register.
4. Cross-check findings.
5. Conflicting or disconfirming evidence.
6. Risks and unresolved questions.
7. Scenario navigation.
8. Report-preview action.
9. Run input snapshot, formula/rule versions and history details.

Only render result sections for calculations/rules that are actually implemented. A placeholder catalogue indicator must not appear as if calculated.

### Finding interaction

Each material finding should show:
- What relationship/check was triggered.
- Which values and periods were compared.
- Links to supporting facts/evidence locators.
- Rule/formula ID and version as available.
- Why it matters for this issuer and listing-day objective.
- Counter-evidence or plausible alternative explanations where available.
- Severity/relevance rationale where assigned.
- Whether the issue is resolved, unresolved, stale or not testable.

A rule trigger is an analytical finding, not proof of fraud, causation or a guaranteed market result.

### Results status language

- “Calculated” means deterministic arithmetic executed successfully from eligible inputs.
- “Not calculated” means the prerequisites were not satisfied or the metric is not enabled.
- “Not applicable” means the metric does not apply, with rationale where needed.
- “Unavailable” means the necessary evidence/input was not obtained.
- “Conflicting” means competing evidence remains unresolved.
- “Unverified” means the supporting fact has not met the validation policy.
- “Scenario” means the result depends on explicit assumptions.

Never convert unavailable/not-applicable to zero or neutral.

### Acceptance checks

- Findings can be traced to source facts and/or calculation traces.
- Positive and negative findings are both visible.
- Each displayed number includes sufficient units/period/as-of context.
- User can navigate from finding to input/source, then return to the same run without losing position.
- The run is read-only historical evidence; corrections create future state/new run rather than silently modifying it.

---

## 5.8 SCEN-01 — Listing-Day Scenarios

### Purpose

Calculate transparent return outcomes from user-defined assumptions, not manufacture forecasts.

### MVP scenario input

User supplies a scenario:
- Scenario label/name.
- Reference issue price from a validated fact or explicitly entered value with status.
- Scenario/exit price or percentage change as supported by the final scenario-input design.
- Optional share/lot quantity.
- Optional cost/charge assumptions only if net return is being calculated.
- Notes/assumptions and their provenance.
- Information cutoff/run association.

Whether the UI accepts price, percentage change or both as the canonical entry method must be settled during the UI and Data Contract steps. If both are supported, define one unambiguous conversion path and test it. The app must not maintain two contradictory authoritative inputs for the same scenario.

### Arithmetic

For issue price Pi and scenario/exit price Ps:

Gross return percentage = ((Ps − Pi) / Pi) × 100

The calculation runs only when the inputs are valid and Pi is positive. Per-share or per-lot gross profit is shown only when quantity is known. Net return is unavailable/incomplete unless the cost components and assumptions required for it are defined and supplied.

### Scenario comparison

Show scenarios side by side or in a compact comparison list, with:
- Scenario label.
- Explicit assumed price/change.
- Calculated gross return.
- Quantity-based gross profit only if applicable.
- Net return only if fully supported.
- Main assumptions and input status.
- Missing costs/inputs.
- Source/observation distinction.

The app must not imply that Bull/Base/Bear percentages were estimated by a validated model if the user entered them. The PRD requires uncertainty/adverse scenarios where adequate inputs exist; it does not authorize an unvalidated prediction engine.

### Required states

- Invalid/non-positive issue price: block return arithmetic.
- Missing scenario price/change: cannot calculate.
- Quantity missing: show return percentage; omit per-lot/quantity profit with explanation.
- Costs missing: gross return may be shown, but net return must not be invented.
- Scenario is assumption-only: visibly label it.
- Observed price: show evidence source and observation time, distinct from a typed assumption.
- Price or issue data changed after scenario was saved: indicate that the result is based on the associated run/snapshot and offer a new calculation/run where appropriate.
- Duplicate scenario names: distinguish scenarios by stable identity; do not overwrite silently.

### Acceptance checks

- FR-040–FR-043.
- Known-answer test confirms return formula.
- Quantity-based profit appears only when quantity is known.
- Gross and net returns are never confused.
- Return conditional on allotment is separated from allotment probability.
- Scenario prices are not shown as forecasts or real observations without evidence.

---

## 5.9 REPT-01 — Report Preview, Export and History

### Purpose

Let the user inspect and export a report derived from a saved analysis run, with evidence lineage and limitations intact.

### Report sections

Where supported by evidence and implemented scope:
- Executive assessment and evidence sufficiency.
- Issue identity and offer structure.
- Evidence inventory, versions and data-quality warnings.
- Financial trends and formulas.
- Earnings quality and cash-flow/working-capital analysis.
- Company-specific dependencies/concentration.
- Governance/legal/regulatory findings.
- Valuation and peer caveats.
- Subscription/GMP/market context only when valid observations exist.
- News/attention only when evidence exists; neither is a P0 dependency.
- Cross-indicator contradiction matrix.
- Material risks and counter-thesis.
- User-defined listing-day scenarios and assumptions.
- Data gaps, unresolved questions and confidence rationale.
- Sources, locators, timestamps, cutoff and methodology.

If a report section is unsupported or out of scope, show a limitation or “not assessed” status. Do not fabricate a generic paragraph to make the report appear comprehensive.

### Preview workflow

1. User selects a saved run.
2. User requests report preview/generation.
3. Report builder creates a structured report model based on that run.
4. The UI displays the report and its data-quality/limitation summary.
5. Material claims link to their evidence locator or calculation trace, or clearly show that the claim is a hypothesis/unresolved item.
6. User can return to the run without starting a new analysis.

### Export workflow

1. User selects Export.
2. UI shows the supported formats actually implemented.
3. User chooses a format and confirms export.
4. Export uses the saved report model; it does not silently fetch sources or rerun the analysis.
5. The generated artifact is saved locally and associated with the originating report/run.
6. Success is shown only after the file is generated and persisted successfully.
7. If export fails, the saved run and report preview remain available, and the user can retry.

The PRD recommends DOCX as the first polished export, with PDF potentially following, but the exact MVP export choice remains an open decision. App-flow should stay format-aware without claiming PDF is available before it is implemented and tested.

### Report history

- List prior reports/runs for the case.
- Display the run identifier, cutoff/time, status and export availability.
- Reopen prior report without rerunning it.
- If case inputs have changed since the saved run, display a stale-relative-to-current-case banner while preserving the original report.
- Generating a new report from a new run creates a new artifact and does not overwrite a prior report.
- If a report file is missing/corrupt, show an integrity error and allow regeneration from the saved run only if the underlying report model/history is available.

### Acceptance checks

- FR-060–FR-064.
- Material facts and calculations remain traceable.
- Uncertainty, data limitations, conflicts and scenario labels survive export.
- Report uses the correct run snapshot and information cutoff.
- Prior runs and reports remain available after a new analysis.
- Export failure does not erase the run or preview.

---

## 5.10 SET-01 — Minimal Settings and Local Data

### Purpose

Offer only essential local operational settings, if they are needed for the first release.

Possible content:
- Local data/storage location information.
- Version/runtime diagnostics useful for troubleshooting.
- Backup and restore instructions/action, once implemented and tested.
- Optional provider configuration status only if an approved optional adapter exists.

Do not create:
- User accounts or profile management.
- Billing/subscription pages.
- Cloud sync settings.
- Analytics dashboards.
- A provider marketplace.
- Configuration forms for unapproved providers.

### Required safety behaviour

- Never display secret API keys in plaintext after they are saved.
- Core app status must not fail just because an optional provider has no key.
- Backup/restore actions must explain what will be copied/replaced and must not overwrite user data without explicit confirmation and preflight checks.
- Do not present a backup action as successful until the backup file is verified and the manifest/contents are complete.

---

## 6. End-to-end workflow maps

### 6.1 Main research path

~~~mermaid
flowchart TD
    A[Open app] --> B{Existing case?}
    B -- No --> C[Create Mainboard IPO case]
    B -- Yes --> D[Open saved case]
    C --> E{Issue identity confirmed?}
    D --> E
    E -- No --> F[Resolve identity or register evidence]
    F --> E
    E -- Yes --> F2[Attempt approved source acquisition]
    F2 --> G[Review case and acquisition status]
    G --> H[Register sources and documents or supplement missing signals]
    H --> I[Review retrieved candidates and enter/review facts]
    I --> J[Resolve or explicitly retain conflicts]
    J --> K[Check analysis readiness]
    K --> L{Run prerequisites met?}
    L -- No --> M[Show blockers and next actions]
    M --> H
    M --> I
    M --> J
    L -- Yes or qualified partial run allowed --> N[Create saved analysis run]
    N --> O[Deterministic formulas and cross-checks]
    O --> P[Inspect results and findings]
    P --> Q[Enter user-defined scenarios]
    Q --> R[Preview report]
    R --> S[Export and save report]
    S --> T[Reopen prior run/report later]
~~~

The “qualified partial run” path is permitted only where the PRD's requirements and formula prerequisites allow it. An identity error or another mandatory prerequisite must not be bypassed simply to produce a report.

### 6.2 Evidence review path

~~~mermaid
flowchart TD
    A[Add evidence] --> B{Input mode}
    B -- Local file --> C[Validate file and store original]
    B -- Manual observation/source --> D[Enter value and source metadata]
    C --> E[Register metadata and integrity status]
    D --> E
    E --> F{Extraction requested and available?}
    F -- No --> G[Manual fact entry/review]
    F -- Yes --> H[Create candidate values with locators]
    H --> I[User reviews each candidate]
    G --> J[Validate unit, period, source and status]
    I --> K{Review decision}
    K -- Accept --> J
    K -- Correct --> L[Save corrected value with history]
    L --> J
    K -- Reject --> M[Keep rejected history; exclude from trusted inputs]
    K -- Unresolved --> N[Keep as pending; do not trust]
    J --> O{Conflict or validation issue?}
    O -- Yes --> P[Show warning / conflict resolution]
    O -- No --> R[Eligible for applicable rules]
    P --> R
~~~

### 6.3 Analysis-run lifecycle

~~~mermaid
stateDiagram-v2
    [*] --> Preflight
    Preflight --> Blocked: Required prerequisites missing
    Preflight --> Ready: Preconditions satisfied
    Preflight --> Qualified: Partial/qualified execution is allowed
    Ready --> Running
    Qualified --> Running
    Running --> Completed: Persisted results are valid
    Running --> CompletedWithQualifications: Results saved with limitations
    Running --> Failed: Execution or persistence failed
    Blocked --> [*]
    Completed --> [*]
    CompletedWithQualifications --> [*]
    Failed --> [*]
~~~

These are conceptual lifecycle states. Exact persisted values and transitions are finalized in the Data Contract. A run that fails must preserve diagnostics and must not be presented as completed. A new run never mutates a completed historical run.

---

## 7. Cross-screen state consistency

This section prevents common “fix one page, break another” loops.

### 7.1 One saved case context

The identity, evidence inventory, fact statuses, run history and report list must come from one persisted case. Each frontend screen must not hold a separately invented copy of the case state as its authority.

After a successful change:
- The affected view reflects the persisted result.
- The case overview updates its readiness summary.
- Analysis readiness is invalidated/recomputed when relevant inputs change.
- The prior run/report remains unchanged but is labeled as based on its original snapshot.
- Any cached frontend display is refreshed or marked stale according to a documented strategy.

### 7.2 Case changed after analysis

Examples that change the current case include:
- New evidence registered.
- A fact accepted/corrected/rejected.
- A source conflict resolved.
- A relevant manual observation changed.
- A new scenario input saved when scenarios are tied to a run.

When an analysis-relevant input changes:
1. Mark the case as changed since its latest run.
2. Do not rewrite the latest saved run or report.
3. Recompute the readiness/preflight view from the current accepted state.
4. Offer the user a new analysis run when appropriate.
5. Make it clear which report reflects which snapshot/cutoff.

Do not automatically rerun a potentially expensive operation in the background just because a user edits a fact.

### 7.3 Server is authoritative for persisted status

The frontend can give immediate field-level feedback, but the backend validates all persistent/domain changes. The UI must reconcile to the returned saved state.

Examples:
- A frontend dropdown cannot make an unresolved candidate trusted if the server rejects that transition.
- A disabled Run Analysis button is helpful, but the backend must independently reject invalid requests.
- A status badge must reflect the server's state, not only local button-click state.
- If the response is lost, refresh the relevant persisted resource before retrying operations that could duplicate records.

### 7.4 Avoid inconsistent meanings

The same concept must not be renamed or interpreted differently across screens:
- “Source observation” is not automatically a verified fact.
- “Candidate extracted” is not “accepted”.
- “Unavailable” is not “zero”.
- “Not applicable” is not “bad”.
- “Scenario” is not “prediction”.
- “Report saved” is not “analysis rerun”.
- “API healthy” is not “data complete”.
- “New case created” is not “issue identity verified”.

Exact names and enum strings will be centralized later in the Data Contract.

---

## 8. Global error and recovery behaviour

### 8.1 Error categories

The interface should handle, at minimum:
- Invalid form input.
- Ambiguous/unconfirmed issue identity.
- Unsupported file type/size.
- Corrupt/unreadable/encrypted document.
- Source metadata unavailable.
- Candidate extraction failed.
- Fact unit/period/status invalid.
- Conflicting values.
- Stale observation.
- Missing prerequisites.
- Analysis execution failure.
- Database unavailable/corrupt.
- Filesystem permission/disk-full/file-missing errors.
- Report generation/export failure.
- Optional provider unavailable/rate-limited/not configured.
- Unknown case/run/report.
- Unexpected internal error.

The final API error envelope is a Data Contract decision; the screen behaviours are defined here.

### 8.2 Recovery rules

- State what failed in user-readable language.
- Explain whether user input/data was saved or not saved, based on actual operation outcome.
- Offer a safe next action: retry, correct fields, register evidence manually, open case, resolve conflict, or contact the local log/diagnostic view.
- Do not expose stack traces, secrets, unnecessary local file paths or full private source text.
- Never clear the only copy of a user's unsaved form values merely because a request failed.
- Do not suggest buying an API or enabling paid billing as a recovery path.
- If an optional integration fails, continue to the manual path.
- If database/file persistence cannot be confirmed, do not show Saved/Completed.
- If the application cannot distinguish whether an operation succeeded after a connection/response failure, first reconcile persisted state and then offer retry.

### 8.3 Error message pattern

Each actionable error should communicate:
1. **What happened** — e.g. “The PDF text could not be extracted.”
2. **Impact** — e.g. “No facts were automatically accepted.”
3. **Next step** — e.g. “Enter the value manually or register a readable version.”
4. **Data status** — e.g. “The original file is still saved” only if verified.

Avoid generic “Something went wrong” when a more precise safe message is available. For unexpected errors, a generic message plus diagnostic reference is acceptable.

---

## 9. Accessibility and interaction quality

Accessibility applies to every flow, including errors and review queues.

- All inputs have visible labels and helpful descriptions for units/periods.
- Validation messages are associated with the input that needs correction.
- Keyboard navigation reaches all controls and dialogs.
- Focus order follows the task sequence; focus is returned to the triggering control after a modal closes.
- Use accessible text for status; colour/icon alone is insufficient.
- Use appropriate headings, buttons, form controls and table headers.
- Screen-reader announcements should communicate save success, validation errors and long-running operation completion.
- Tables remain understandable at narrow sizes; provide a usable stacked/scrollable alternative where necessary.
- Avoid dense screens with every technical field expanded by default; show essential facts first and detailed provenance on demand.
- Confirm before destructive operations; do not place destructive actions beside common primary actions without separation.
- Respect browser zoom and keyboard-only navigation.

Accessibility testing is part of the P0 acceptance suite, not a cosmetic follow-up.

---

## 10. Data integrity and user trust rules for the UI

The UI must preserve the evidence model defined by the Indicator Catalogue.

1. Every material number displays or links to source, period, unit, validation state and locator where available.
2. Raw sourced value and normalized/calculated value are distinguishable.
3. A fact correction does not erase the old value or its source history where history is required.
4. Source conflicts remain inspectable.
5. Publication time, event time, observation time, retrieval/capture time and analysis cutoff are not represented by one ambiguous date.
6. Stale values are visibly dated and excluded/down-weighted only under a documented rule.
7. Not-applicable indicators are not treated as missing evidence or negative findings.
8. Candidate extraction does not become trusted without a visible validation path.
9. A calculated result identifies its formula/rule and material input lineage.
10. A scenario displays its assumptions and is not worded as a forecast.
11. A user-entered unverified observation is labeled as such.
12. A generated report reflects a saved run, not a silently refreshed state.
13. If citation metadata is missing, the report should state the missing locator instead of manufacturing it.
14. Overall assessment/confidence must explain evidence coverage and limitations rather than provide an arbitrary confidence percentage.

---

## 11. Requirement traceability to the PRD

This mapping ensures the flow covers approved requirements instead of becoming an independent wish list. Requirement IDs are from the current PRD; implementation should confirm the exact current PRD wording before a feature is built.

| PRD requirement | Flow sections that cover it | Required acceptance evidence |
|---|---|---|
| FR-001 — create/save/reopen/rename case | HOME-01, CASE-01, CASE-02 | Case persists through restart and can be reopened/renamed. |
| FR-002 — issue identity and ambiguity | CASE-01, CASE-02, ANAL-01 | Ambiguous identity is visible/correctable and cannot silently produce a finalized report. |
| FR-003 — cases vs analysis runs | CASE-02, ANAL-01, RUN-01, REPT-01 | A new run does not overwrite older run/report. |
| FR-010 — register files/manual evidence | EVID-01, FACT-01 | Material inputs link to evidence or are explicitly user-supplied/unverified. |
| FR-011 — source metadata and locators | EVID-01, FACT-01 | Unknown metadata remains unknown; timestamps/periods are distinct. |
| FR-012 — preserve original/version | EVID-01 | Same-name/version uploads do not rewrite evidence used by old reports. |
| FR-013 — coverage and missing expected evidence | CASE-02, EVID-01, REPT-01 | Missing evidence is visible and the expectation basis is explainable. |
| FR-014 — conflict handling | FACT-01, ANAL-01, RUN-01 | Conflicts remain visible with sources and resolution status. |
| FR-015 — core acquisition orchestrator and approved connectors | CASE-01, CASE-02, section 8 | After identity confirmation, supported connectors are attempted; per-source outcomes/fields/timestamps/limitations persist; failures fall back to manual entry. |
| FR-020 — fact semantics | FACT-01, section 10 | Values have unit/period/source/method/status or visible unknowns. |
| FR-021 — candidate review | FACT-01 | Candidate can be accepted/corrected/rejected/unresolved; manual entry remains. |
| FR-022 — missingness states | All data screens, especially FACT-01 and ANAL-01 | Missing/stale/conflicting/unverified/invalid/N/A remain distinct. |
| FR-023 — type/unit/period/reconciliation validation | FACT-01, ANAL-01 | Invalid inputs are rejected/flagged with actionable guidance. |
| FR-024 — source/calculation lineage | RUN-01, REPT-01 | Material claim navigates to source or calculation trace. |
| FR-030 — deterministic financial measures | ANAL-01, RUN-01 | Only enabled, validated formulas execute with testable output. |
| FR-031 — offer structure | RUN-01, REPT-01 | Disclosed facts are separate from interpretations; unavailable fields are listed. |
| FR-032 — earnings quality | RUN-01, REPT-01 | Findings contain formula/rule and inputs, or state the limitation. |
| FR-033 — initial cross-checks | ANAL-01, RUN-01 | Triggered rules explain the relationship and identify supporting inputs. |
| FR-034 — deeper sector-specific checks (P1) | Deferred/P1; RUN-01 when implemented | Checks are applied only when appropriate and explain their applicability; not required for the P0 flow. |
| FR-016 — critical-signal connector feasibility and coverage | CASE-01, CASE-02, section 8, section 13 | A dated representative-IPO source benchmark records field coverage, permissions/terms, cost, timestamp quality and failures; unresolved critical gaps require explicit scope resolution before release. |
| FR-040 — acquired and manually supplied time-sensitive observations | CASE-02, EVID-01, FACT-01, SCEN-01 | Source, time, status, freshness and provenance are displayed for both retrieved and manual observations. |
| FR-041 — user-defined scenarios | SCEN-01 | Assumptions, reference price, cutoff and missing prerequisites are clear. |
| FR-042 — return conditional on allotment | SCEN-01 | Known-answer return test; no conflation with allotment probability. |
| FR-043 — uncertainty/adverse scenarios | SCEN-01, REPT-01 | Relevant downside is not hidden when adequate inputs exist. |
| FR-044 — synchronize available time-sensitive signals | CASE-02, FACT-01, ANAL-01, RUN-01 | Core signal comparisons use compatible timestamps/cutoffs and flag stale/asynchronous/missing data. Richer time-series visualizations can be staged, but core interconnection is P0. |
| FR-045 — historical outcomes/model calibration | Deferred/P2 | Must be leakage-controlled before any predictive claim. |
| FR-046 — IPO-name-triggered acquisition summary | CASE-01, CASE-02 | User sees candidate identity, acquisition attempts and per-source outcomes; ambiguity must be resolved, and failed/unavailable source states remain explicit. |
| FR-050 — record news items (P1) | EVID-01 and deferred news flow | If implemented, retain publisher, URL, publication/event/retrieval time and verification status; manual source registration remains available. |
| FR-051 — duplicate/syndicated story handling (P1) | Deferred/P1 | If implemented, repeated coverage must not be presented as independent corroboration; it is not a P0 dependency. |
| FR-052 — news classification (P1) | Deferred/P1 | If implemented, distinguish official fact, reporting, allegation, opinion and unverified claim; sentiment alone never verifies a claim. |
| FR-053 — search attention/Google Trends (P2) | Deferred/P2 | Only consider after access and value are evaluated; absence never blocks the core MVP. |
| FR-060 — structured qualified report | REPT-01 | Report states evidence sufficiency, limitations and qualified assessment. |
| FR-061 — citations/calculation traces | RUN-01, REPT-01 | Citation validation catches missing/unresolved references before export. |
| FR-062 — cutoff/run/formula versions | ANAL-01, RUN-01, REPT-01 | Report links to the exact saved run and cutoff. |
| FR-063 — export and local retention | REPT-01 | Export preserves citations/tables/statuses and reopens correctly. |
| FR-064 — prior run history | CASE-02, RUN-01, REPT-01 | Prior run/report remains available and unchanged. |

### Non-functional requirements

The flow also supports the PRD's privacy/security, reliability, accessibility, performance and maintainability goals:
- Local-only data and no mandatory external service.
- Safe uploads and visible failures.
- Accessible labels, keyboard flow and non-colour status signals.
- Consistent API validation and saved-state reconciliation.
- Reproducible run/report history.
- No user data sent to AI services as a hidden side effect.

---

## 12. Acceptance-test scenarios before implementation is considered complete

The following are required end-to-end scenarios. They are designed to catch integration defects across multiple screens, not merely verify individual buttons.

### AT-01 — First-use manual case

1. Launch the app without internet or provider credentials.
2. Create a Mainboard IPO case with only a name.
3. Confirm source status clearly states that online acquisition is unavailable/offline/not attempted as appropriate, and that manual entry remains available.
4. Confirm the case persists after refresh/restart.
4. Register an official offer PDF from local storage.
5. Enter key data manually.
6. Complete a formula whose approved prerequisites are satisfied.
7. Produce an HTML preview and the approved export format.
8. Reopen the case/report.

**Pass when:** the local/manual fallback path completes with no external API, paid service or AI requirement; the UI does not pretend live source retrieval succeeded when offline.

### AT-02 — Ambiguous identity

1. Create a case with a name that is not sufficient to identify one issue.
2. Attempt to run analysis.
3. Review the blocking message and next action.
4. Register supporting evidence and confirm/correct identity.
5. Return to analysis readiness.

**Pass when:** the app never silently chooses an issuer or treats a case as resolved simply because a string exists.

### AT-03 — SME issue outside scope

1. Attempt to create/analyse an issue identified as SME.
2. Confirm the app explains Mainboard-only scope.
3. Confirm it does not create a supported SME analysis path.

**Pass when:** no SME toggle, rule set or report claim appears.

### AT-04 — Bad file and upload recovery

1. Try an unsupported file type.
2. Try a corrupt or unreadable PDF.
3. Test a same-name file with different contents.
4. Simulate a storage failure where possible.
5. Retry safely.

**Pass when:** original data is not overwritten, error is specific, unsupported parsing does not masquerade as success, and no false evidence record remains.

### AT-05 — Extracted value review

1. Produce an extraction candidate with source locator.
2. Confirm it remains untrusted before review.
3. Correct it and save.
4. Open history and check the original candidate still exists.
5. Run an affected formula.

**Pass when:** the calculation uses only the approved value and traces it to the source and correction process.

### AT-06 — Conflicting values

1. Register two values that disagree for the same fact/period/basis.
2. Open Facts & Review.
3. Confirm both sources and values are visible.
4. Leave unresolved and attempt analysis.
5. Resolve the conflict with a recorded rationale and rerun.

**Pass when:** unresolved conflict blocks or qualifies the affected calculation; values are never averaged/overwritten silently.

### AT-07 — Missing/invalid input

1. Leave one required formula input missing.
2. Enter an incompatible unit/period.
3. Enter an invalid denominator/issue price where relevant.
4. Run preflight.

**Pass when:** the affected calculation is blocked with a useful reason; unrelated valid work may continue only where the rules permit; nothing is converted to zero.

### AT-08 — Scenario arithmetic

1. Enter a known issue price and scenario price.
2. Verify the return against an independently computed known answer.
3. Omit share quantity.
4. Omit transaction costs.

**Pass when:** gross return is correct, quantity-based profit is not invented, net return is not shown as if complete, and scenario assumption is labeled.

### AT-09 — Saved run immutability

1. Complete and save run A and report A.
2. Correct a fact or add evidence.
3. Return to run A/report A.
4. Start run B.
5. Compare A with B.

**Pass when:** A remains reproducible and unchanged; B reflects the new snapshot; the UI indicates which run the report describes.

### AT-10 — Report and export integrity

1. Generate report from a saved run containing a conflict, missing field and scenario assumption.
2. Export the report.
3. Reopen the export and compare it with preview.
4. Follow a citation/calculation reference.

**Pass when:** qualifications, timestamps, missingness, conflicts, assumptions and provenance survive export. No polished formatting hides a limitation.

### AT-11 — Local storage failure

1. Simulate database unavailable/corrupt or evidence-file missing.
2. Open Home, a case and a saved report.
3. Try an action that writes data.
4. Recover/restore test data.

**Pass when:** data errors are not displayed as empty results; the app never claims a write succeeded when it did not; recovery guidance is safe.

### AT-12 — Contract integration

After the Data Contract is approved:
1. Generate/verify TypeScript types from OpenAPI.
2. Run backend schema validation.
3. Change a test response field/type intentionally.
4. Run contract/build tests.

**Pass when:** incompatible field names/types/nullability cannot merge silently and the developer gets a specific test/build failure.

### AT-13 — Keyboard/accessibility

1. Complete the core case flow using keyboard only.
2. Cause a form validation error.
3. Review a candidate and conflict.
4. Inspect save/error/status messaging with accessibility tools.

**Pass when:** controls are reachable, errors are associated with fields, focus order is sensible and meaning is not communicated by colour alone.

### AT-14 — Prior history and deleted/missing IDs

1. Open an unknown case/run/report route.
2. Delete or move a test artifact through the supported workflow, if deletion is implemented.
3. Reopen a previous case and report.

**Pass when:** a clear not-found/integrity state is shown and the app never opens a different case by name similarity.

---

### AT-15 — IPO-name-triggered source acquisition and signal interconnection

1. Use a representative Mainboard IPO with an unambiguous identity and run the acquisition workflow online.
2. Confirm the system attempts every enabled/approved connector configured for that source benchmark and persists the attempt/result status.
3. Inspect QIB, NII, retail subscription and named unofficial GMP results where the tested connectors return them; verify source, category/definition, value/unit, observation/publication/retrieval times and freshness.
4. Force one connector to fail or return partial data; verify the result is marked failed/partial/unavailable rather than zero or successful.
5. Run the enabled cross-signal checks linking available subscription/GMP inputs with valuation, fundamentals, issue/free-float context and market/company-event signals.
6. Remove or stale one input; rerun preflight and verify the affected relationship is qualified/skipped with a specific reason while unrelated valid checks can run.
7. Manually enter or import the missing observation and verify it keeps its provenance/status and is included only under the agreed validation policy.

**Pass when:** acquisition outcomes are observable and reproducible; supported signal relationships are actually evaluated from time-aligned validated inputs; no missing, stale, unofficial or failed-source value is presented as verified or predicted. The test report records actual source coverage and never claims universal automation from one successful sample.



## 13. Dependencies and decisions that must be settled before coding each flow

This flow document is intended to reduce avoidable rework, but it must not pretend that every technical dependency is already approved. Before implementing the relevant screen, confirm the following decisions:

| Decision | Required before | Owner document / gate |
|---|---|---|
| Exact request/response fields, property casing, IDs, status enums and error schema | API-backed screen implementation beyond the minimal scaffold | Data Contract in Technical Design |
| Final identity identifiers and identity-resolution rules | Full case identity workflow | PRD + Data Contract; Mainboard-only rule is fixed |
| Supported upload formats, size limits and parser behaviour | Evidence upload implementation | Technical Design; representative-file test |
| Exact fact field schema and permitted status transitions | Fact entry/review | Data Contract + Database Schema |
| Which formulas are enabled in P0 and their golden fixtures | Analysis screen claiming specific metrics | Approved formula register from Indicator Catalogue |
| Default analysis cutoff behaviour | Analysis preflight | Technical Design/PRD decision before analysis implementation |
| Whether partial runs are allowed and what blocks a report | Analysis/report finalization | PRD requirements + explicit readiness policy |
| Scenario canonical input method (price, percentage change or both) | Scenario form | PRD and Data Contract; inputs must be unambiguous |
| Net-return cost components/rounding | Any screen showing net return | Formula register; absent components mean net result unavailable |
| Initial export format and offline generation path | Report export | PRD recommends DOCX first; decision and export test required |
| Backup/restore UX and supported OS | Before valuable user data is stored | Technical Design and local restore test |
| Optional external adapters and source terms | Any automated retrieval screen | Data Source & Feasibility Audit approval gate |

The product must not block all coding while every future/P1/P2 choice is decided. Build the minimal scaffold and the first vertical slice, but do not implement a feature whose required decision remains open.

---

## 14. P0 versus deferred experience

### P0 — required for a useful MVP

- Create, save, reopen and rename a case.
- Confirm a specific Mainboard IPO identity or visibly block final analysis while ambiguous.
- Register original source files and manual evidence with provenance.
- Display expected/missing evidence without implying every possible source is mandatory.
- Manually enter/review facts, including units/periods and validation state.
- Preserve and resolve or explicitly retain conflicting values.
- Run an approved, limited deterministic formula/rule set.
- Show readiness, missing prerequisites and partial limitations.
- Display explainable findings and supporting evidence.
- Enter user-defined listing-day price scenarios and calculate supported gross-return arithmetic.
- Generate, preview, export and retain a structured report with citations/limitations.
- Preserve prior runs/reports and reopen a case.
- Keep manual data entry, local calculations and reporting usable without internet, AI APIs or paid services. The intended online workflow also attempts acquisition through approved connectors; no source is claimed operational without feasibility evidence.
- From a confirmed IPO identity, expose retrieved/unavailable signal coverage and interconnect available fundamentals, valuation, QIB/NII/retail subscription, GMP and market/company-event inputs.

### P1 — expanded coverage after the core path works

- Additional connector coverage beyond the critical source categories; broader historical and multi-provider history.
- Richer event/news discovery, deduplication and classification where compliant coverage is verified.
- More expansive time-series visualizations; timestamp-aligned core comparisons are already P0.
- Deeper sector-specific rules and a broader dependency graph.
- Improved extraction and local OCR after representative accuracy testing.

### P2 — later/conditional

- Google Trends/search-attention integration, only if feasible and evaluated.
- Historical listing outcome backtesting, model calibration and predictive scoring, only after suitable point-in-time data and leakage-controlled out-of-sample evaluation.
- Any automated scenario range or probability feature requiring a separate methodology decision.

Deferred features must not appear as if operational in the MVP. Do not build non-functional placeholders that imply the feature exists.

---

## 15. Definition of done for an app-flow feature

A screen or journey is complete only when:

- It maps to one or more approved PRD requirements or a documented prerequisite.
- Its primary, empty, loading, validation, error and partial states are specified and implemented where applicable.
- Its data inputs are captured through the UI or a clearly documented supported fallback.
- The backend validates the operation independently of frontend button state.
- The success message reflects persisted success, not an optimistic assumption.
- The user can recover from errors without losing already saved evidence.
- Its output can be traced into case status, analysis and report flows.
- Prior runs/reports remain immutable.
- Keyboard and accessibility behaviour is tested.
- Contract, unit/integration and relevant end-to-end tests pass.
- The feature does not introduce a paid dependency or required live source.
- A code reviewer can tie the implementation back to requirement IDs and the current canonical documents.

---

## 16. Implementation order derived from this flow

Build only the current phase's working path; do not create all screens at once.

1. **Shell and case list:** local app startup, health status, error handling, create/open case route.
2. **Issue identity and source benchmark:** stable issue identity plus a dated benchmark for candidate subscription, GMP and official event/disclosure routes.
3. **Source registry and acquisition orchestrator:** approved connector interface, attempt/result/status history, timestamps, coverage/freshness diagnostics, and safe failure handling.
4. **Evidence registry and manual fallback:** original-file preservation, source metadata, uploads/import and manual observations.
5. **Manual facts/review and candidate acquisition review:** units, periods, source links, validation states, conflicts, and review/verification of retrieved candidate values.
6. **First Data Contract and persistence schema:** finalize for this vertical slice, including acquisition attempts and time-stamped observations.
7. **Formula register and cross-signal rules:** approve a small P0 set with independent fixtures; include subscription/GMP-versus-valuation/fundamentals/market context relationships where inputs exist.
8. **Analysis preflight and run:** deterministic results with saved snapshot, acquisition diagnostics and run history.
9. **Finding review:** source/input links, cross-signal explanations and unresolved states.
10. **Scenarios:** user-defined inputs and tested gross return.
11. **Report model and export:** HTML preview plus the approved/export-tested format.
12. **Backup/restore and end-to-end reliability:** validate recovery before real data becomes irreplaceable.

A phase is not complete merely because its route or screen exists; it must pass its defined acceptance checks.

---

## 17. Definition of readiness to begin substantive implementation

The flow is implementation-ready when the team has:

- Reviewed the main route map and case workspace structure.
- Agreed identity, evidence, manual-entry, preflight, analysis, scenario and report journeys.
- Accepted the explicit handling for missing, invalid, conflicting, stale and not-applicable values.
- Confirmed P0/P1/P2 boundaries.
- Identified each open dependency in Section 13 and assigned it to the correct later decision.
- Agreed the first end-to-end vertical slice and its test fixture.
- Confirmed that the Technical Design's local-first architecture can support the flows.
- Approved the first Data Contract and database schema only for the vertical slice before implementing their dependent endpoints/storage.
- Approved the first formula register before enabling those calculations.

**This is not a claim that the app will have zero defects.** It is a way to prevent known requirement gaps, missing UI paths, mismatched assumptions and untestable success states from being discovered one at a time during coding. The flow must be reviewed against the actual built application and kept aligned through tests.

---

## 18. Coding-agent instructions

Any agent implementing the app flow must:

1. Read AGENTS.md and the linked canonical project documents first.
2. Treat Mainboard-only, ₹0, local-first/manual-first and evidence integrity as binding.
3. Follow this document for user-visible journeys and states; follow Technical Design for architecture; follow the Data Contract for exact API fields once approved.
4. Never invent API payloads, database fields, formula definitions or statuses that have not been agreed.
5. Implement each feature with loading/empty/error/partial states, not only its happy path.
6. Make the backend enforce constraints independently from the UI.
7. Never show Saved/Completed until persistence succeeds.
8. Never silently replace missing data with zero, resolve conflicts by guessing, or promote unreviewed extraction.
9. Never mutate old run/report history when evidence or current case data changes.
10. Add/run tests from Section 12 and the relevant PRD criteria; report tests actually executed.
11. Keep changes scoped to the current milestone and inspect the diff.
12. Update this canonical app-flow.md in place if agreed behaviour changes. Do not create versioned duplicates.
13. If an implementation requirement is unclear or conflicts with the PRD/Technical Design, record the specific conflict and ask for a decision before encoding an irreversible assumption.

---

## 19. Flow sign-off checklist

Before the Data Contract and full screen implementation begin, review:

- [ ] Case creation, approved source discovery, identity-resolution and post-confirmation acquisition behaviour.
- [ ] Mainboard-only enforcement and SME out-of-scope state.
- [ ] Case workspace navigation and persisted status.
- [ ] Evidence registration, original-file preservation and source metadata.
- [ ] Source acquisition result/history, per-source status, timestamp/freshness display and manual fallback.
- [ ] Manual facts, optional extraction review and conflict workflow.
- [ ] Analysis preflight, cutoff and blocked/qualified execution semantics.
- [ ] Analysis run/history immutability.
- [ ] Scenario inputs, gross/net return distinction and labels.
- [ ] Report preview/export/history and citation preservation.
- [ ] Storage/API/parser/export error recovery.
- [ ] Keyboard/accessibility acceptance.
- [ ] P0/P1/P2 boundaries.
- [ ] First vertical slice acceptance test.

Record unresolved decisions in the relevant existing canonical document, then resolve them before the dependent implementation step. Do not create another document just to restate this checklist.

---

## 20. Current recommendation

**Recommended next action:** review this flow as the product's behaviour contract, then move to UI/UX design. Do not finalize every API field or database column here. Keep the next design tasks aligned:

- **app-flow.md:** screens, user journeys, transitions, prerequisites, visible statuses and failure recovery.
- **design.md:** visual layout, wireframes, reusable components, interactions and accessibility presentation.
- **TECHNICAL_DESIGN.md:** architecture, module ownership, storage and testing strategy.
- **database-schema.md:** proposed v0.1 persisted entities/relationships/constraints; validate and align it with the first Data Contract before migrations are implemented.
- **Data Contract:** exact API and module input/output structures, before dependent endpoint implementation.
- **implementation-plan.md:** build order and measurable delivery gates.

The objective is a coherent, testable end-to-end product—not a stack of disconnected documents or screens.


---

# Addendum A — Consolidated end-to-end website journey and integration handoff

> This addendum expands the user journey described above into one continuous, easy-to-follow path. It is additive: the preceding sections remain unchanged. This is still an **application-flow specification**, not the final Data Contract. Names below such as `case_id` and `evidence_id` are conceptual identifiers to help frontend/backend planning; their exact types, property names, nullability and wire representations must be agreed in the Data Contract.

## A1. The full journey, from opening the website to seeing results

### Step 1 — Home / My Research Cases

The user opens the local application and sees **Home / Cases**. This is the starting screen, not a market dashboard. It lists saved IPO research cases and provides a clear **New IPO Case** action. Each saved item should show the best-known issue name, identity state, last activity, latest analysis/report state and outstanding warnings.

If the user is returning, they open an existing case and continue where they left off. Opening a case restores saved state; it does not re-fetch data or re-run analysis automatically. If the local database cannot be read, show a storage error—not a falsely empty list.

### Step 2 — Enter the IPO name

The user selects **New IPO Case** and enters the IPO/issuer name, plus any optional identifier or known issue detail that helps distinguish it. A ticker is not mandatory. At this point the user has supplied a search phrase, **not a confirmed issue identity**.

The application searches/discovers candidates only through a source or local workflow actually available and allowed by the source audit. If no compliant discovery connector is enabled, say so and allow the user to continue with local/manual identification. Do not invent search results or imply that the internet was checked when it was not.

### Step 3 — Confirm the exact issue before full analysis

Show the best available candidate details side by side so the user can verify that the correct issue was selected. Relevant details include:

- Issuer/legal name and issue/display name.
- Mainboard segment and the evidence supporting that classification.
- Issue/open/close dates when known.
- Price band and issue identifiers when known.
- Source name, source record identifier/link and the time information available from that source.
- Any conflicting candidate or identity details.

If multiple issues could match, leave identity **ambiguous/unresolved** and ask the user to choose or supply supporting evidence. Do not silently select the first string match. If the IPO is identified as an SME issue, explain that SME IPOs are out of scope and stop the supported analysis flow. If segment is unknown, do not guess Mainboard.

Full analysis is blocked while the issue identity is materially uncertain. Supporting evidence can still be registered while identity is unresolved, provided it is clearly marked as not yet confidently linked to the issue.

### Step 4 — Create/save the research case

After the user begins the case, persist a local research case with a stable conceptual `case_id`. Link it to a confirmed `issue_id` only after the issue has been resolved adequately. Preserve the original user-entered search text separately from the final confirmed issue identity.

The case becomes the home for evidence, facts/observations, acquisition attempts, analysis runs, findings, scenarios and reports. These are parts of the same case—not separate projects duplicated for each feature. The user can close the application and return later.

A successful save must be confirmed by the persistence layer before the UI says **Saved**. If saving fails, preserve the form where safe, show the specific error and allow retry. Do not accidentally create two cases if the first save succeeded but its response was lost.

### Step 5 — Try source acquisition and show exactly what happened

After identity is confirmed, the application may run the acquisition orchestrator for connector adapters that have actually been approved and enabled. It should attempt only the categories each adapter is known and permitted to supply. The screen should show, per source/category, whether it was attempted, the real outcome, returned fields, source link/identifier, known timestamps, freshness and limitations.

Use clear user-visible states such as **Found**, **Partial**, **Unavailable**, **Not enabled**, **Not attempted**, **Blocked by policy/terms**, **Failed**, **Stale** and **Conflicting**. These labels explain actual outcomes; they are not interchangeable. An adapter that is not approved must not be shown as having fetched data. An API/network error is not a zero value and is not proof that the source contains no data.

Acquisition is helpful but is not a prerequisite for creating or maintaining a case. The user's work must remain possible without internet, provider credentials, paid APIs or AI services. At the current audit state, **no external source connector is production-approved**; see Addendum C.

### Step 6 — Upload documents (after case creation, from Evidence)

**The user does not have to upload a file just to search for or identify an IPO.** Once the local case exists, the user can open **Evidence** and add documents at any point. The recommended first document is the official offer document/RHP/prospectus. Addenda, annual reports, exchange/company disclosures and other relevant evidence can be added as available.

For every uploaded file, the user chooses a local file and can optionally add its source URL, document/published date, description and document type. The application validates the file type and size against the supported implementation, saves the original locally, and records its metadata/checksum and any available page/locator information. It must not imply that an upload succeeded until the file and its metadata were persisted.

A local PDF parser may create **extraction candidates**, ideally with the page/section locator and enough context for review. Extracted text is not automatically an accepted fact. The user reviews each candidate, corrects it where needed, and explicitly accepts or rejects it under the implemented review flow. If parsing is inaccurate, unsupported or fails, preserve the original file and allow manual entry. A document upload should not be lost because extraction failed.

The user can upload documents later, in stages. Do not make every possible document mandatory before the user can proceed. The application must not send local files to ChatGPT or another external service implicitly.

### Step 7 — Review facts and enter missing observations manually

The **Facts & Review** area brings together accepted facts, user-entered observations, unreviewed extraction candidates, conflicting alternatives, stale values and missing required inputs.

When a source doesn't provide a needed fact, the user can enter it manually if that observation type is supported. For example, manually recorded subscription values or GMP observations should retain, as known:

- The publisher/source, source URL or evidence reference.
- The value as written by the source and its parsed/numeric representation.
- Category and definition (for example, QIB, NII or retail, or what a GMP figure refers to).
- Unit, currency and scale.
- Reporting/financial period when applicable.
- Source publication time/date, observation/as-of time and retrieval/entry time as separate fields when known.
- The user's review/verification state and a note where useful.

Unknown timestamps stay unknown/null; do not fill them from the time the app happened to fetch the data. Do not assume a feed-generation time is the observation time of every item in the feed. The app must preserve raw source meaning and should not combine data that represents different periods or definitions without an explicit approved rule.

Missing means missing—not zero. Conflicting observations remain visible with their sources. Do not silently overwrite, average, or choose a preferred value without the documented rule/user review. Corrections and superseded values should remain auditable where the model supports history.

### Step 8 — Analysis Readiness / Preflight

Before execution, the user opens **Analysis & Findings** and sees a readiness/preflight view. It should tell the user what is ready, what is missing, what conflicts, what is stale and exactly which calculations will be affected.

The readiness view should include:

- Issue identity and Mainboard status.
- Documents and evidence that have been registered.
- Facts/observations and candidates awaiting review.
- Coverage/status of source attempts for relevant categories.
- Financial and offer facts needed by the currently enabled formulas.
- QIB/NII/retail subscription and GMP coverage, if relevant to enabled rules.
- Conflicting, stale, invalid, unverified and missing inputs.
- The analysis cutoff/as-of policy that will apply to the run.
- The reason each blocked or skipped formula/rule cannot execute.

Identity ambiguity blocks full issue-specific analysis. Missing data for one formula should normally block or qualify **that formula**, not automatically prevent every unrelated valid calculation. A partial, explicitly qualified run/report may be allowed where the agreed readiness policy says it is useful. If the available evidence is too thin to produce a useful analysis, explain the needed inputs and do not manufacture a result.

### Step 9 — Run deterministic analysis

When the user selects **Run Analysis**, the backend validates the input/evidence snapshot and executes only formulas and rules that are in the approved register. Core arithmetic is deterministic application code, not a mandatory AI answer. The run records which facts/evidence and formula/rule versions it used, the applicable cutoff, and the reason for any blocked/skipped check.

The planned analysis connects the applicable signals rather than displaying them as unrelated numbers. Depending on what is available and approved, relationships may include financial/business quality, offer and valuation, issue size/free float, QIB/NII/retail demand, unofficial GMP, and relevant market/company-event context. Use the Indicator Catalogue and approved formula/rule register to define the actual tests. If a required input is missing, stale, conflicting or not time-aligned, qualify or skip that relationship and say why.

A signal co-occurrence is not proof of causation, fraud or misconduct. Findings should describe the observed relationship, why it triggered, supporting and contradictory/context evidence, limitations and reasonable alternative explanations. Do not turn a single sample or unofficial signal into a guaranteed listing outcome.

Every new run creates a new immutable `analysis_run_id` and saved input/evidence snapshot. A later correction or added file may affect a new run, but it must not rewrite a previously saved run or report.

### Step 10 — Review results and scenarios

After the run is saved, open its results and clearly show which run/cutoff the user is looking at. The results page should contain these logical areas:

1. **Research summary:** issue identity, cutoff/as-of, evidence coverage and important qualifications.
2. **Business and financial quality:** only the approved, supported financial/business indicators and the sources/periods used.
3. **Offer, valuation and demand:** offer terms and enabled valuation/demand measures, including separate QIB/NII/retail categories where supported.
4. **Cross-signal findings:** the relationship tested, why it triggered, relevant evidence on both sides, and caveats/alternative explanations.
5. **Scenario calculator:** user-defined inputs and transparent arithmetic.
6. **Evidence, source status and limitations:** missing fields, stale/conflicting values, failed/unavailable sources and provenance.

Material claims must link back to the facts, source documents, page locators or observations that support them. If a value is unavailable, display it as unavailable or skipped with a reason; don't fill the space with an invented number.

The user may enter a listing/exit-price scenario. Label inputs as **assumptions**, not observations or predictions. Gross-return arithmetic can be shown when its prerequisites are met. Do not label a result as net return while fee/tax/slippage inputs and the approved net-return policy are absent. Allotment probability is a separate question from return conditional on receiving an allotment. Do not present guaranteed profit, a universal buy/avoid verdict or a prediction unsupported by validated methodology.

### Step 11 — Preview/export report and return later

The user generates a report from a saved run, previews it, and exports the formats actually implemented and tested. The preferred initial offline export path is DOCX after a representative-file test; HTML preview may also be available. Do not promise PDF export until a free, offline-compatible implementation has been verified.

A report must preserve evidence provenance, source-acquisition status, the run cutoff, data timestamps/unknown timestamps, missing inputs, conflicts, assumptions, skipped/blocked checks and limitations. Exporting a report must not silently re-run the analysis. The same saved report can be reopened later and should represent the same run snapshot.

If the user adds evidence or corrects a fact, show that the current case has changed since the previous run. The user can check readiness and run again; the new run/report is versioned separately and older reports remain unchanged.

## A2. Where each user action belongs

| User question/action | Where it happens | What must be saved or shown |
|---|---|---|
| “I want to analyse an IPO” | Home → New IPO Case | Create a case; no file upload required yet. |
| “Which IPO exactly?” | Issue discovery/identity confirmation | Candidate evidence and explicit confirmed/unresolved state. |
| “What did online sources return?” | Case Overview / Acquisition status | Real attempt outcomes, fields, times, freshness and limitations per source/category. |
| “I have the prospectus” | Case Workspace → Evidence | Preserve local original and metadata; extraction output remains a candidate until reviewed. |
| “This source is missing a value” | Facts & Review | Manual observation with source/meaning/unit/time where known and review state. |
| “Can I analyse this now?” | Analysis & Findings → Readiness | Prerequisites, conflicts, freshness, cutoff and formula-specific blockers. |
| “What does it tell me?” | Saved analysis run → Results/Findings | Deterministic calculations, qualified findings and traceable evidence. |
| “What if listing price is ₹X?” | Scenarios | Clearly labeled assumptions and supported gross-return calculation. |
| “I need a file/shareable report” | Reports & History | Preview/export from the selected immutable saved run. |
| “I changed a value; what now?” | Facts/Evidence → Readiness → New Analysis Run | New snapshot/run; older runs and reports remain unchanged. |
| “Something failed” | The same screen that initiated it | Specific failure/recovery action; preserve already persisted work and never claim a failed save succeeded. |

## A3. Data lifecycle: candidate → reviewed evidence → analysis → report

Use this sequence as the mental model shared by frontend and backend:

1. **Candidate discovery:** a name, a source row or extracted text suggests an issue/fact but is not yet necessarily accepted.
2. **Identity confirmation:** the user confirms the exact Mainboard issue with sufficient supporting details.
3. **Evidence registration:** save source document/URL/source response metadata and retain its provenance.
4. **Fact/observation review:** parse or enter the value, preserve its definition/period/unit/time, and record whether it is accepted, unverified, conflicting, stale, rejected or superseded.
5. **Readiness evaluation:** determine which approved formulas/rules have the necessary valid, time-appropriate inputs.
6. **Immutable analysis run:** evaluate only enabled rules and record its evidence/input/version snapshot.
7. **Finding review and scenario calculation:** show why each finding exists and keep scenario assumptions separate from observations.
8. **Saved report/export:** render from the selected saved run and preserve provenance, unknowns and limitations.
9. **Re-run after changes:** create a new run/report; do not mutate history.

If parsing, source retrieval, or one calculation fails, the application should preserve valid work from other stages and show exactly where the pipeline stopped. The user should not need to start the entire case again.

## A4. Integration identifiers and responsibilities (intended, not final API names)

These identifiers are conceptual anchors for the first frontend/backend vertical slice. Final API shapes, database fields and status enums are deliberately deferred to the Data Contract and schema alignment.

| Conceptual identifier/object | Created or updated when | Purpose |
|---|---|---|
| `case_id` | Research case is saved | Stable identifier for the user's case workspace. |
| `issue_id` | Issue identity is confirmed/linked | Stable issue reference distinct from user-entered search text. |
| `identity_status` | Candidate matching/review changes | Expresses confirmed, unresolved/ambiguous, out-of-scope or other agreed identity states. |
| `acquisition_attempt_id` | A source/category attempt starts or completes | Audits what was tried, when, and its actual outcome. |
| `evidence_id` | File, URL, source capture or supporting evidence is registered | Connects facts/findings/report claims to their evidence. |
| Fact/observation identifier | A value is entered/imported/extracted and recorded | Tracks one sourced statement with its meaning, unit, period, timestamps and review state. Exact property names remain for the Data Contract. |
| `analysis_run_id` | Analysis snapshot is successfully saved | Selects an immutable run and its cutoff, input snapshot and formula/rule versions. |
| `finding_id` | A rule emits a finding for a run | Connects the finding to trigger logic and supporting/contradicting evidence. |
| `report_artifact_id` | A report model or export is successfully saved | Identifies the report linked to a particular saved run. |

Frontend responsibility: gather user intent, show explicit source/review/readiness states, validate basic form input for usability and navigate through stable identifiers. Backend responsibility: enforce validation and scope, manage acquisition, persist provenance and snapshots, run deterministic formulas/rules, and return explicit statuses/errors. A disabled button is not a substitute for backend validation, and a success toast is not proof of persistence.

Do not invent endpoint names, API payload casing or exact database properties from this table. Define them in the Data Contract after the interaction flow is accepted.

## A5. Source-feasibility snapshot relevant to the flow (29 October 2026)

These are bounded smoke-test observations to inform honest UI states. They are **not** production approval, a guarantee of continued access or proof of repeatability.

| Candidate source | What was observed in the recorded tests | How the app-flow should treat it now |
|---|---|---|
| IPOS Markets | Combined script v0.2 returned HTTP 200 and matched all 10/10 target issues; all 10 matched detail records included QIB/NII/RII fields and an `as_of` value. One record (Bombay Coated) had `basis: "bids_only"` and `overall_times: null`; do not infer an overall-times value. | Priority subscription-data candidate, still unapproved. Any future adapter must preserve basis, null values, definition and observed/source time and pass repeatability/source-policy gates before being enabled. |
| GMP Today | The v0.2 test returned HTTP 200 and 3 items from 17 tracked; those per-item records had `updated_at: null`. The feed had `generated_at: 2026-10-29T10:00:40+05:30`. The observed medians differed between runs (BLS Polymers ₹48→₹51, Maxwell Engineering Solutions ₹33→₹43, Ajwa Projects ₹36→₹35). | Limited-sample GMP candidate, still unapproved. Do not treat the feed generation time as an item observation time, or claim the sample establishes comprehensive issue coverage. Preserve the source definition and unknown item timestamps. |
| Xflot directory | v0.2 directory test returned HTTP 200, 182 IPO records, 110 classified Mainboard. | Discovery candidate only; not a production-approved connector. |
| Xflot issue detail | The v0.1 BLS Polymers detail test returned Mainboard/OPEN, price band ₹142–₹150, last GMP ₹51, one GMP source and 11 history points; subscription fields were absent (`lastSubX: null`, `subs: []`). The combined v0.2 test did not re-test the individual detail endpoint. | Conditional issue/GMP detail candidate only; current evidence does not support using it for QIB/NII/retail subscription. Honour the documented 65-second minimum poll safeguard and required attribution/disclaimer. |

The v0.2 combined run is one run, not a strict same-version repeatability test. Do not invent a claim that repeatability has been proven. The audit permits work on the manual-first architecture and vertical slice to proceed without repeated smoke tests, but provider-specific enablement remains gated on source access/terms, repeatability and field-level validation. **No connector is production-approved at this snapshot.** Do not scrape NSE absent written permission. These external-source facts must stay aligned with the [Data Source & Feasibility Audit](IPO_Data_Source_and_Feasibility_Audit_v1.0.md); if that audit changes, update this snapshot rather than treating it as timeless.

## A6. Required error and recovery behaviour across the complete path

- **Discovery/source offline or blocked:** clearly mark not attempted, unavailable or policy-blocked as appropriate. Continue manual-first workflows.
- **Source response is partial or malformed:** preserve valid returned evidence as permitted, mark the source attempt partial/failed and reject invalid fields; never convert absent fields to zero.
- **Issue identity uncertain:** allow evidence gathering but block full issue-specific analysis until confirmed.
- **Unsupported/invalid file:** explain the file constraint, do not create a false successful evidence record, and keep the case open.
- **PDF extraction fails:** preserve the file and allow manual fact entry.
- **Save/database/disk failure:** never display “Saved”; retain user input where safe, give recovery guidance and permit retry/reconciliation.
- **Source disagreement:** show the competing values and provenance; require the defined resolution workflow or qualify the affected check.
- **Stale or unknown timestamps:** show unknown/stale status. Do not substitute retrieval time or current time for an unknown observation time.
- **One formula cannot run:** show its exact missing/invalid/conflicting prerequisites; unrelated eligible formulas may still complete.
- **A finding cannot be substantiated:** skip or qualify it rather than writing a definitive claim.
- **Unknown case/run/report ID:** show not-found and return navigation; never select another case because its name looks similar.
- **Export failure:** keep the saved run/report model, explain the failed export and allow retry. Export does not implicitly rerun analysis.
- **Evidence file later missing or corrupt:** show the integrity problem and a recovery/restore path; do not silently omit the supporting source from a report.
- **Backup/restore:** provide clear local backup/restore guidance and validate a restore before relying on backups for valuable research data.

## A7. End-to-end acceptance checklist for the first usable vertical slice

A vertical slice is usable only when the user can complete the following sequence without paid services, mandatory AI or a live connector:

- [ ] Start the local app and see a truthful Home/Cases state.
- [ ] Create a research case from an IPO name and distinguish that name from confirmed identity.
- [ ] Confirm a Mainboard issue, or see a clear ambiguity/SME out-of-scope block.
- [ ] Reopen the saved case after refresh/restart.
- [ ] Register a local offer PDF and retain its original even if extraction is unavailable or fails.
- [ ] Enter at least the required supported facts manually with their sources/units/periods and review status.
- [ ] See missing, stale, conflicting, invalid and unknown-time values distinctly from zero or verified values.
- [ ] See source attempts/coverage accurately, including disabled/unapproved adapters, without simulated-success claims.
- [ ] Run at least one approved deterministic calculation from valid prerequisites and see why any other enabled check was skipped.
- [ ] Inspect a finding and trace its supporting input/evidence; see limitations and alternative explanations where relevant.
- [ ] Enter a user-defined scenario and get only the arithmetic supported by its known assumptions.
- [ ] Save and preview a report that preserves the run cutoff, provenance, missingness, conflicts and caveats.
- [ ] Change evidence/facts, rerun, and confirm the previous run/report is unchanged.
- [ ] Simulate a failed save/source/file operation and verify that the UI reports the real failure and offers recovery.
- [ ] Confirm there is no required account, cloud hosting, paid API, external AI, broker/order execution or prohibited NSE scraping.

The first implementation should exercise this complete, minimal path before expanding provider coverage or adding advanced automation.



---

## Addendum B — Contract and file-structure decisions are now frozen

The previous sections describe the user journey and remain the source of truth for what the user sees and does. The P0 API fields/statuses and the target code file tree are now specified in [Implementation Blueprint & Data Contract](implementation-blueprint.md). This is an additive clarification to the conceptual references above, not a replacement for this flow document.

### B1. Which document controls what

- **app-flow.md:** screen order, user actions, prerequisites, visible states, error recovery and acceptance behaviour.
- **design.md:** approved visual presentation, palette, typography, responsive behaviour, accessibility and motion; the exact hero remains owner-controlled.
- **TECHNICAL_DESIGN.md:** architecture rationale, system boundaries and technical principles.
- **implementation-blueprint.md:** exact P0 frontend/backend stack, file tree and responsibilities, API methods/routes, camelCase JSON names, exact wire enums, request/response fields, decimal/timestamp rules, errors, configuration variables, local data-directory layout and contract change process.
- **database-schema.md:** SQLite entities/constraints/indexes and the migration alignment work needed to match the API contract.
- **implementation-plan.md:** delivery phases, gates, and what should be built/tested first.

### B2. Contract decisions relevant to the screens

- Browser route parameters are caseId, analysisRunId and reportId as defined in the blueprint; display names are not identifiers.
- API wire properties use camelCase. Do not use conceptual snake_case identifiers from earlier examples as literal JSON field names.
- IDs are backend-generated UUID strings. A case may exist with no confirmed issue; full issue-specific analysis remains blocked until identity is confirmed with evidence.
- Unknown numeric/time values are null with a status/reason, not zero or empty-string sentinels. Decimal values cross the API as decimal strings; money arithmetic belongs to Python Decimal.
- Core source/analysis statuses are defined in the blueprint and must be rendered as text as well as visual styling. A missing provider, a failed attempt and a successful source check are different states.
- File upload is to POST /api/v1/cases/{caseId}/evidence/files (PDF-only P0, 25 MiB default cap). Files are saved locally after the case exists; extraction yields candidates only and never silently accepts facts.
- Analysis readiness is read from GET /api/v1/cases/{caseId}/analysis/readiness. The effective informationCutoffAt returned by preflight is supplied to POST /api/v1/cases/{caseId}/analysis-runs.
- Reports are created from an immutable saved analysis run. POST report creation/export does not silently run analysis again.

### B3. Flow-to-contract integration gate

Before considering any screen implemented, verify that its action maps to the API route/response model in the blueprint, that its empty/loading/partial/error states are represented, that backend validation enforces the same constraints, and that the database schema/migration stores the required provenance. Update the blueprint, implementation models, generated TypeScript types and tests together if a product-approved behaviour change requires a contract change. Do not create a separate competing Data Contract file.
