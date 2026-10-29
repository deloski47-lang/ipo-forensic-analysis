# IPO Forensic Analysis Engine
## Product Requirements Document (PRD)

**Document ID:** PRD-IPO-001  
**Version:** 1.0 (approved scope baseline; review amendments incorporated 29 October 2026)  
**Status:** Approved MVP scope baseline — technical and data-source decisions remain open  
**Last updated:** 29 October 2026  
**Product mode:** Local-first, single-user research application  
**Primary market:** Indian IPOs  
**Primary use case:** Evidence-based research for a possible listing-day exit

> **Document purpose:** Define what the first useful version of the IPO Forensic Analysis Engine must do, how success will be judged, and what is deliberately outside scope. This document locks the product scope and expected behaviour for the MVP; it does not lock the technology stack, database schema, document extraction method, or external data providers. Approval of this PRD is not approval of technical design or a claim that all data sources are feasible.

---

## 1. Executive summary

The IPO Forensic Analysis Engine is a local-first research application for analysing Indian IPOs, with particular emphasis on the risks and possible returns of a listing-day exit. It should help one user assemble evidence, validate facts, examine the issuer's business and financial risks, compare market signals, detect contradictions, and produce an auditable report.

The product is not intended to be a generic IPO listing page, a promotional summary generator, an automated trading system, or a machine that promises listing gains. Its output should be a structured, source-cited research report that makes evidence gaps, conflicts, assumptions, scenarios, and uncertainty visible.

The first release will be **manual-first and scenario-based, not a validated prediction engine**: the user can provide official documents and manually enter time-sensitive data when reliable automated retrieval is unavailable. MVP scenarios are transparent conditional calculations, not model-generated forecasts. Automated source discovery may be added only where feasibility and source quality have been demonstrated. Lack of an API must never prevent the core research workflow from operating.

The product's defining capability is not a single score. It is the ability to link evidence across financials, offer structure, governance, business dependencies, valuation, subscription, grey-market premium (GMP), news and market context—and then explain where those signals agree or conflict.

## 2. Problem statement

IPO research is fragmented across offer documents, financial statements, exchange pages, subscription data, unofficial GMP reports, company disclosures, news coverage and peer-company information. These sources differ in reliability, freshness, format and availability. A user can easily overlook risks, compare incompatible periods, rely on stale data, double-count repeated news, or treat a plausible narrative as a verified fact.

A simple score or sentiment summary can conceal those problems. In particular, high subscription, positive news, or a reported GMP does not by itself prove that a listing-day exit will be profitable.

The application must help the user answer:

1. What is actually known about this IPO, and which sources support each important fact?
2. How strong is the issuer's financial and business position, and what risks are material for this particular company?
3. Do the offer structure, valuation, demand indicators, GMP observations, news and wider market conditions support or contradict one another?
4. What plausible listing-day outcomes and downside scenarios follow from the available evidence and stated assumptions?
5. What is missing, stale, conflicting, or still unverified—and how much should that reduce confidence in the analysis?

## 3. Product vision and principles

The application should behave like a skeptical research analyst: it must try to disprove an initial thesis, not merely assemble support for it.

### 3.1 Non-negotiable principles

- **Evidence before narrative.** Every material factual claim must be linked to its supporting evidence or explicitly labelled unsupported/unresolved.
- **No invented numbers.** Missing values remain missing. Unknown is not zero, and an estimate must never be disguised as an observed fact.
- **Auditable arithmetic.** Financial calculations use deterministic, tested code. Important calculated outputs retain their input values, units, periods, formula/version and rounding rules.
- **Contradictions are findings.** Conflicting values or signals must be preserved and explained; they must not be silently averaged away.
- **Timestamp discipline.** Publication time, event time, retrieval time and the analysis information cutoff are distinct fields.
- **Company-specific analysis.** Applicable checks should adapt to business model and sector. Inapplicable metrics must be marked not applicable, not treated as missing evidence.
- **Uncertainty is explicit.** Separate facts, calculated metrics, interpretations, hypotheses and scenarios.
- **No guaranteed outcomes.** Listing-day results are uncertain. The product must not imply that a scenario or score is a reliable probability unless validated appropriately.
- **Local-first and cost-aware.** The first release should work locally without requiring paid APIs, cloud hosting or a cloud database.
- **Manual fallback.** A source integration failure must not silently block the user from supplying a documented value or file.
- **No look-ahead leakage.** Any historical evaluation must use only information available at the simulated decision timestamp.

## 4. Target user and usage context

### 4.1 Primary user

One individual researching Indian IPOs for personal decision support, with a limited initial budget and a preference for local operation and transparent reasoning.

### 4.2 User needs

The user needs to:

- work from official IPO documents and other source files;
- see what the application extracted and correct errors before relying on them;
- enter manually collected data when automated collection is unavailable;
- understand the origin and freshness of each material fact;
- identify issuer-specific risks instead of receiving the same generic checklist for every company;
- see both positive and negative evidence, including contradictions;
- evaluate possible listing-day outcomes with transparent assumptions;
- export and revisit a detailed report without losing the evidence trail.

### 4.3 Usage assumptions

- Single-user, local-first operation is the default for the initial release.
- Internet access may be available for optional research but is not assumed to be reliable for every source.
- Data may be incomplete; the system must still produce a qualified report where possible.
- The user retains responsibility for reviewing evidence and making financial decisions.

## 5. Product goals and non-goals

### 5.1 Goals

| ID | Goal | Definition of success |
|---|---|---|
| G-01 | Produce an auditable IPO report | A report can be traced from material claims to source evidence and calculation inputs. |
| G-02 | Make missingness visible | Unavailable, stale, conflicting and unverified data are labelled rather than silently omitted or fabricated. |
| G-03 | Make calculations reproducible | Core calculations can be independently reproduced from stored inputs and versioned formulas. |
| G-04 | Find cross-signal contradictions | The system surfaces relevant relationships between financial, governance, valuation and market indicators. |
| G-05 | Focus on listing-day decisions | The report addresses possible listing-day outcomes and downside, conditional on the available evidence. |
| G-06 | Work without paid data services | A user can complete the core workflow using uploaded documents and manual data entry. |
| G-07 | Preserve analysis integrity | Re-running or reviewing an analysis makes its sources, cutoff and assumptions identifiable. |

### 5.2 Non-goals for the initial release

- Automatically placing, modifying or selling market orders.
- Guaranteeing a listing gain or outputting an unvalidated probability as if it were calibrated.
- Long-term portfolio construction as the primary workflow.
- Public SaaS launch, public accounts, teams, social features or multi-user collaboration.
- Mandatory cloud hosting, managed cloud database or paid subscription APIs.
- Building a general-purpose financial research platform for every asset class.
- Treating AI sentiment or a single GMP observation as a standalone buy/sell signal.
- Claiming predictive performance before a valid historical backtest demonstrates it.
- Forcing all indicator modules into the first release merely because they appear in the catalogue.

## 6. Scope and release boundaries

The first release must be useful as a manual-first research tool before the project invests in fragile automation. The stages below describe product scope, not a commitment to a specific technology.

### 6.1 MVP: manual-first forensic report

The MVP must support:

1. Create and identify an IPO research case.
2. Add offer documents and evidence files, and record source metadata.
3. Enter or confirm key issue details and time-sensitive observations manually.
4. Allow manual entry of facts as a complete fallback. If extraction is implemented, treat extracted values as candidates and show them for user review before they become trusted inputs.
5. Record source locators such as document version, page, section or table.
6. Compute a selected set of applicable financial and offer metrics deterministically.
7. Show data quality, completeness, freshness, conflicting values and unresolved questions.
8. Run a first set of high-value cross-check rules.
9. Create a listing-day scenario section where inputs permit it, clearly separating verified observations from assumptions.
10. Generate and export a structured report with citations, findings, limitations and an overall qualified assessment.
11. Reopen a saved research case and review its source evidence and latest report.

The MVP must not require automated news, Trends, subscription, GMP, exchange APIs, paid AI APIs, or AI-based document extraction to function. Those values may be manually entered with their source and timestamp. AI-assisted extraction is optional and must fail safely to manual entry.

### 6.2 Follow-on release: market-signal enrichment

After the MVP works reliably, consider:

- timestamped subscription observations by investor category;
- timestamped GMP observations from clearly labelled unofficial sources;
- curated peer IPO records and comparable-company measures;
- market/sector context and a more developed listing-day scenario engine;
- replaceable news-provider adapter(s), deduplication and event classification;
- improved source discovery and extraction automation.

Any source integration is conditional on a data-source feasibility review. An integration must not be described as reliable until coverage, field definitions, timestamps, access terms, failure behaviour and historical availability are tested.

### 6.3 Later scope: validation and advanced analysis

- Historical backtesting with immutable as-of snapshots and leakage controls.
- Calibration and evaluation of scenario or prediction models, if data volume and quality support it.
- Expanded sector-specific analysis, richer dependency graphs and advanced contradiction rules.
- Optional search-attention signals such as Google Trends, only if access is practical and the signal has a clear evaluation plan.

## 7. Primary user journeys

### Journey A: Start a research case

1. User opens the application and chooses to create an IPO case.
2. User enters the issuer/issue name and any available identifiers or issue details.
3. Application records the case and clearly flags identity ambiguity rather than analysing a potentially incorrect issuer.
4. User adds the offer documents and other evidence, or begins with manual data entry.
5. Application displays the evidence inventory and highlights missing expected documents.

**Required behaviour:** The user must be able to correct the issuer/issue identity before running the full analysis.

### Journey B: Add and verify evidence

1. User uploads or registers an evidence file, or enters an observation manually.
2. Application records source type, source title or URL, publisher, relevant dates, retrieval date, document version and locator where available.
3. Any extraction creates candidate facts, not automatically trusted facts.
4. User reviews candidate values, units, periods and supporting locators; user can accept, correct, reject or mark a value unresolved.
5. Conflicting values remain visible with their sources and resolution status.

**Required behaviour:** The application must not promote a low-confidence extraction into a trusted factual input without a visible validation path.

### Journey C: Analyse and investigate

1. User starts an analysis run against a known information cutoff.
2. Application validates required inputs, units and periods.
3. Deterministic calculations run only for applicable metrics with valid inputs.
4. Cross-check rules produce findings with the related inputs and rule explanation.
5. User inspects material findings, counter-evidence and unresolved questions.
6. The application generates a listing-day scenario view when its prerequisites are met.

**Required behaviour:** Missing or invalid input must create a visible status or blocked calculation, not a fabricated output.

### Journey D: Review and export report

1. User opens the report preview.
2. Report distinguishes facts, calculated metrics, interpretation, hypotheses, scenario assumptions and unknowns.
3. User can navigate from a material claim to its source locator and, where applicable, calculation trace.
4. User exports the report and can return to the case later.

**Required behaviour:** Export must preserve citations, limitations and scenario labels; a polished layout must not conceal missing data.

## 8. Functional requirements

Priority definitions: **P0** = required for MVP; **P1** = follow-on; **P2** = later/conditional.

### 8.1 Case and issue identity

| ID | Priority | Requirement | Acceptance condition |
|---|---|---|---|
| FR-001 | P0 | Create, save, reopen and rename an IPO research case. | A case can be closed and reopened without losing registered evidence or analysis history. |
| FR-002 | P0 | Store the issue identity and available identifiers separately from user-entered search text. | An ambiguous identity is flagged and can be corrected before final reporting. |
| FR-003 | P0 | Distinguish IPO cases and analysis runs. | A new run does not silently overwrite the record of an earlier run. |

### 8.2 Evidence and source registry

| ID | Priority | Requirement | Acceptance condition |
|---|---|---|---|
| FR-010 | P0 | Register uploaded files and manually entered observations as evidence. | Every material input can be traced to a source record or explicitly marked as user-supplied without a verified external source. |
| FR-011 | P0 | Store available source title, publisher/source type, URL or local file reference, publication date, event date, retrieval time, data period, version and locator. | Unknown metadata stays unknown; the application does not invent a date or page reference. |
| FR-012 | P0 | Preserve original uploaded evidence and document version identity. | Replacing a file does not silently change what supported an earlier report. |
| FR-013 | P0 | Display document coverage and expected-but-missing evidence. | The report shows material gaps and the basis for required-document expectations. |
| FR-014 | P0 | Preserve conflicting sources and allow resolution status/notes. | Conflicts are not silently overwritten or averaged. |
| FR-015 | P1 | Support source adapters for verified, useful automated retrieval. | Each adapter has documented coverage, source terms, timestamp rules and graceful failure behaviour. |

### 8.3 Fact extraction and validation

| ID | Priority | Requirement | Acceptance condition |
|---|---|---|---|
| FR-020 | P0 | Represent a fact with value, unit, currency if applicable, period, source locator, extraction/input method and validation status. | A fact without a reliable unit or period cannot silently enter an incompatible calculation. |
| FR-021 | P0 | If fact extraction is implemented, label extracted values as candidates until reviewed or validated under an explicit rule. | The user can inspect, correct, accept or reject a candidate fact. Manual entry remains available whether extraction succeeds or fails. |
| FR-022 | P0 | Represent unavailable, not applicable, stale, conflicting, unverified and invalid states distinctly. | These states are visible in the interface and report; none is automatically converted to zero. |
| FR-023 | P0 | Validate basic data types, units, periods, ranges and arithmetic reconciliations where applicable. | Invalid inputs are rejected or flagged with an actionable explanation. |
| FR-024 | P0 | Retain source and calculation lineage for report claims. | A reviewer can inspect the input evidence behind a material claim. |

### 8.4 Financial and offer analysis

| ID | Priority | Requirement | Acceptance condition |
|---|---|---|---|
| FR-030 | P0 | Calculate a defined set of core financial measures from validated inputs. | Each calculation uses a documented formula, input periods, units, rounding rule and automated test cases. |
| FR-031 | P0 | Analyse offer structure, including fresh issue/OFS, intended use of proceeds, issue size, dilution and selling-supply considerations where data are disclosed. | The report separates disclosed facts from interpretation and lists unavailable fields. |
| FR-032 | P0 | Assess selected earnings-quality signals, such as PAT versus operating cash flow, other income and one-off effects where the required data exist. | A finding includes its formula/rule and supporting inputs; unavailable inputs produce a limitation instead of a guess. |
| FR-033 | P0 | Run initial cross-checks across selected financial, offer, governance and market indicators. | Every triggered rule produces an explainable finding and identifies its evidence/input records. |
| FR-034 | P1 | Add deeper sector-specific checks, related-party/dependency mapping and expanded valuation comparisons. | A check is applied only where relevant and its applicability rationale is recorded. |

### 8.5 Listing-day research and scenarios

| ID | Priority | Requirement | Acceptance condition |
|---|---|---|---|
| FR-040 | P0 | Support manually entered market observations with source and timestamp, including subscription and GMP where available. | Each observation shows whether it is official or unofficial, its time and its provenance. |
| FR-041 | P0 | Present user-defined listing-day price scenarios and downside where adequate inputs are available. | Each scenario records the assumed listing price or percentage change, reference issue price, information cutoff, assumptions and missing prerequisites; the report does not present user-entered scenarios as predictions. |
| FR-042 | P0 | Calculate listing return conditional on allotment separately from allotment probability. | For a valid issue price and scenario price, the system calculates gross return percentage as (scenario price − issue price) / issue price and shows the formula and inputs. Per-share/lot profit is shown only when the applicable share/lot quantity is known. Allotment probability remains a separate field and is not inferred by the return calculation. |
| FR-043 | P0 | Show uncertainty and material adverse scenarios alongside positive cases. | The report cannot show only an upside case when an applicable downside scenario is available. |
| FR-044 | P1 | Provide time-series views for subscription/GMP and synchronize them with news and attention observations. | Different publication/retrieval times are retained; missing observations are not interpolated without a visible rule. |
| FR-045 | P2 | Evaluate historical listing outcomes and model calibration. | Any published performance claim is based on a documented, leakage-controlled evaluation. |

### 8.6 News and attention signals

| ID | Priority | Requirement | Acceptance condition |
|---|---|---|---|
| FR-050 | P1 | Allow news items to be recorded with publisher, URL, publication/event/retrieval timestamps, topic and verification status. | Material news claims can be traced to the item and, where possible, a primary source. |
| FR-051 | P1 | Detect repeated/syndicated stories to avoid treating duplicates as independent corroboration. | Duplicate or near-duplicate items are grouped or flagged. |
| FR-052 | P1 | Classify news as a discovery lead, verified fact, allegation, opinion or unverified claim. | Sentiment alone cannot promote a claim to verified fact. |
| FR-053 | P2 | Add search-interest/Google Trends if current access and data quality are workable. | This remains optional and cannot block the core analysis when absent. |

### 8.7 Report generation and auditability

| ID | Priority | Requirement | Acceptance condition |
|---|---|---|---|
| FR-060 | P0 | Generate a structured report containing findings, evidence, limitations and a qualified overall assessment. | A completed report never hides critical missing data or material contradictions. |
| FR-061 | P0 | Include source references for material factual claims and calculation traces for material computed metrics. | Citation validation detects missing or unresolved references before export. |
| FR-062 | P0 | Include analysis timestamp/information cutoff, run identifier and relevant formula/rule versions. | The report can be tied to the version of evidence and rules used. |
| FR-063 | P0 | Export a readable report document and preserve a local copy. | Citations, tables, uncertainty labels and limitations survive export and reopen. |
| FR-064 | P0 | Allow the user to review prior report runs. | A new run does not erase the prior report or silently mutate its input snapshot. |

## 9. Required report structure

The report template should support the following sections. For the MVP, each section must either contain evidence-backed analysis, be marked unavailable/not applicable with a reason, or be explicitly deferred from the MVP template. The existence of a section in this list does not require a full advanced analysis module in the MVP:

1. **Executive assessment:** concise summary of the strongest supporting evidence, strongest risks, confidence/data quality and unresolved issues. No guaranteed prediction.
2. **IPO identity and issue mechanics:** issue details, fresh issue/OFS split, intended proceeds, dilution and potential supply considerations.
3. **Evidence coverage and data quality:** available/missing documents, source quality, freshness, extraction validation and conflicts.
4. **Financial performance:** revenue, margins, earnings, cash conversion, working capital and relevant balance-sheet measures supported by available data.
5. **Earnings quality and accounting:** recurring versus non-recurring effects, other income, audit observations and reconciliation checks where relevant.
6. **Business model and company-specific risks:** customer/supplier/product/geographic concentration, operations, contracts, competition and sector risks where disclosed.
7. **Governance, related parties and legal/regulatory risks:** distinguish verified findings from allegations or unresolved reports.
8. **Valuation and peers:** compatible measures, peer-selection rationale, differences in periods/definitions and valuation limitations.
9. **Demand and listing setup:** subscription observations, GMP history, likely supply/free-float context, market regime and timestamps, when available.
10. **News and attention context:** only when data are available; distinguish primary-source confirmation from reported or unverified claims.
11. **Cross-indicator findings:** links between indicators, contradictions, competing explanations, and counter-evidence.
12. **Listing-day scenarios and downside:** assumptions, conditional return calculations, plausible adverse cases and missing prerequisites.
13. **Unresolved questions and next evidence to collect.**
14. **Methodology and audit appendix:** sources, source cutoffs, formulas, calculation traces, rule/model versions and relevant limitations.

The report must not force a numeric overall score. If a summary rating is later introduced, its meaning, calibration and validation evidence must be documented. An overall assessment may remain qualitative and conditional.

## 10. Data quality, provenance and status rules

The application must clearly distinguish at least the following states:

- **Verified:** reviewed and supported by a suitable source or a documented validation rule.
- **Extracted — review required:** candidate value produced by parsing or AI extraction but not yet confirmed.
- **User-entered — unverified:** manually entered value with insufficient external verification.
- **Calculated:** result produced by deterministic code from identified inputs.
- **Conflicting:** credible sources or inputs disagree and no final resolution has been established.
- **Unavailable:** sought but not available from the sources currently in the case.
- **Not applicable:** metric or check does not fit the issuer or current context, with a reason.
- **Stale:** value exists but falls outside the defined freshness rule for that signal.
- **Invalid:** value fails required type, unit, period or consistency validation.

Status must be represented as data, not only by colour. The interface must not imply that a value is reliable merely because it has been extracted successfully or generated fluently by an AI model.

Every important evidence record should distinguish, where applicable:

- publication timestamp;
- event timestamp;
- retrieval timestamp;
- financial/reporting period;
- analysis information cutoff;
- source identity and type;
- document/version identity and locator;
- input/extraction method;
- validation and conflict status.

## 11. AI behaviour and financial integrity requirements

AI may assist with document navigation, extraction of candidate facts, classification, summarisation, hypothesis generation and explanation of verified findings. It is not the source of truth for numeric financial data.

### Mandatory guardrails

1. Never invent missing numbers, source URLs, document pages, company disclosures, peer values or citations.
2. Never treat an absence of evidence as evidence of zero, no risk or no event.
3. Never perform material financial arithmetic only in free-form model text when the result can be computed by deterministic code.
4. Never silently resolve conflicting values. Preserve both sources and flag the discrepancy.
5. Never combine incompatible units, currencies, reporting periods, share counts or accounting bases without explicit validated transformation rules.
6. Never present allegations, opinion, social-media rumours or unverified reporting as established fact.
7. Never use future information in a historical as-of analysis.
8. Every AI-generated material factual claim must be tied to source evidence or clearly labelled as an unverified hypothesis.
9. AI-generated explanations must be limited by what the stored evidence supports. Confidence language must not be based solely on the model's self-reported confidence.
10. If a required input is missing or ambiguous, ask for review when needed or produce an explicit limitation; do not guess to complete the report.

## 12. Non-functional requirements

| ID | Area | Requirement |
|---|---|---|
| NFR-01 | Local-first | The core case, evidence, calculations and reporting workflow must operate on the user's machine without mandatory cloud hosting. |
| NFR-02 | Cost | MVP operation must not depend on a paid data provider or paid AI API. Optional provider/API costs must be disclosed before adoption. |
| NFR-03 | Integrity | Material calculations must be deterministic for a fixed set of validated inputs and formula versions. |
| NFR-04 | Traceability | A material report claim must be linked to evidence, calculation lineage or an explicit hypothesis/scenario label. |
| NFR-05 | Reproducibility | A run must record its information cutoff, input snapshot and applicable calculation/rule versions. |
| NFR-06 | Resilience | Failure of a source adapter or optional AI service must not corrupt saved evidence or erase an existing report. |
| NFR-07 | Maintainability | Indicator rules and source integrations should be modular enough to add, disable or replace without rewriting the entire application. |
| NFR-08 | Security/privacy | Local files and any secrets must not be exposed in source control or sent to external services without an explicit, documented reason. |
| NFR-09 | Validation | High-impact calculations and data transformations require automated tests, including invalid and missing-input cases. |
| NFR-10 | Usability | The user can see why an analysis is limited and what evidence would resolve the limitation. |
| NFR-11 | Export | The report must remain readable, navigable and auditable in the exported format. |
| NFR-12 | Accessibility | Status must not rely on colour alone; text, tables and controls should remain legible and operable. |

Exact performance targets and supported file-size limits will be set during technical design after sample documents and an implementation environment are tested. Do not invent targets in advance.

## 13. Acceptance criteria for MVP release

The MVP is acceptable only when all P0 requirements are implemented and the following end-to-end criteria pass:

- **AC-01 — Evidence-first case:** A user can create one IPO case, register the relevant offer documents and manually enter market observations.
- **AC-02 — Identity safety:** An ambiguous issuer/issue identity is flagged before a final report is produced.
- **AC-03 — Reviewable extraction:** Candidate extracted facts show their source locator and can be accepted, corrected or rejected.
- **AC-04 — Missingness:** Deliberately omitted critical inputs remain unavailable; they are not filled with zero or invented estimates.
- **AC-05 — Deterministic math:** Every metric enabled in the MVP formula register has a documented formula, units, input periods, rounding rule, missing/invalid-input behaviour, at least one known-answer test, and invalid-input tests. The release gate is 100% passing tests for all enabled MVP formulas; no metric may be enabled merely because its implementation exists.
- **AC-06 — Source traceability:** A reviewer can move from a material report claim to its source evidence or calculation trace.
- **AC-07 — Contradiction handling:** Conflicting values or signals appear as a finding and are not silently reconciled.
- **AC-08 — Scenario honesty:** Listing scenarios state their assumptions and do not imply an unvalidated probability of gain. Given a valid issue price and user-entered scenario price, the system reproduces the documented gross-return formula to the agreed rounding tolerance.
- **AC-09 — Conditional returns:** Listing-return calculations and allotment-probability assumptions are kept separate.
- **AC-10 — Export integrity:** Exported output retains citations, limitations, data-quality indicators and scenario qualifications.
- **AC-11 — Run history:** A subsequent run does not silently overwrite the source snapshot and report from a previous run.
- **AC-12 — Offline/manual core:** With local files and manual inputs available, the core case, calculation and report workflow completes without an online data provider, paid API, or AI service.
- **AC-13 — Failure handling:** Failure of optional source retrieval or AI extraction leaves original evidence intact and gives the user a clear message.
- **AC-14 — No unsupported predictive claim:** No accuracy claim is shown unless a documented, leakage-controlled historical evaluation supports it.

## 14. Success metrics

Initial success should be measured by research quality and workflow reliability, not by whether an IPO happens to list at a premium.

| Metric | Initial target/measurement approach |
|---|---|
| Traceability coverage | 100% of material factual claims in a release-acceptance test are linked to evidence or explicitly labelled unresolved/hypothesis. |
| Calculation reproducibility | 100% of agreed core calculation test cases pass, including known-answer and invalid-input cases. |
| Missing-data integrity | 100% of deliberately omitted critical values remain visibly missing in test cases. |
| Conflict visibility | 100% of seeded conflicts appear in the evidence-quality view or findings list. |
| Export consistency | All required report sections and qualifications persist in DOCX/PDF or other selected export format. |
| Manual-first usability | A test case can be completed using uploaded documents and manual inputs without a paid API. |
| Prediction quality | Not claimed at MVP. Evaluated only after sufficient timestamped historical data and a valid methodology exist. |

The first targets are acceptance-test criteria, not a claim that extraction will be perfect on every real-world document.

## 15. Risks and mitigations

| Risk | Why it matters | Required mitigation |
|---|---|---|
| Incomplete or inaccessible source data | The report could appear complete while missing key evidence. | Manual fallback, visible coverage, source feasibility checks and limitation disclosure. |
| Extraction/OCR errors | A wrong number can distort every downstream calculation. | Candidate/review status, source locators, arithmetic reconciliation and deterministic tests. |
| Stale market signals | Subscription/GMP/news can change quickly. | Timestamp every observation and apply signal-specific freshness rules. |
| GMP quality | GMP is unofficial, noisy and can be copied across websites. | Label unofficial status, preserve source/time/history and avoid treating duplicated reports as independent evidence. |
| AI overconfidence | Fluent text can conceal unsupported claims. | Evidence-bound claim schema, citation validation and explicit unknown/hypothesis states. |
| False peer comparability | Multiples can be misleading across different businesses or periods. | Record peer rationale, compatible periods and definitions, and comparability limitations. |
| Look-ahead leakage | Backtest results can be unrealistically optimistic. | Immutable as-of snapshots, hard cutoff enforcement and leakage tests. |
| Scope creep | Too many integrations can delay a useful first product. | Manual-first MVP, staged priorities and acceptance gates. |
| API/provider dependency | Coverage, licensing, price or field availability may change. | Provider-agnostic interfaces and no core dependence on a single external API. |
| Unsupported performance claims | Users may mistake a report for a proven predictor. | No prediction-accuracy claims before valid evaluation and calibration. |

## 16. Dependencies and assumptions

- The user can obtain or supply at least some IPO offer documents and supporting data.
- Source availability and permissions vary and must be evaluated; no specific news, market-data or Trends provider is approved by this PRD.
- Primary sources should be preferred for material facts: offer documents, exchange disclosures, audited financial information, regulator records and official company announcements.
- Secondary reporting may help discover leads but should not independently establish a material adverse claim where verification is possible.
- GMP is unofficial and must be labelled as such.
- The initial app is for personal research, not order execution or a public multi-user product.
- The indicator catalogue is a research framework; not every indicator is required or applicable in the MVP.

## 17. Open decisions intentionally deferred

These are not accidental omissions; they belong in later planning documents and must be resolved with evidence before implementation:

1. Exact frontend/backend framework versions and dependency list.
2. Exact local database, file storage layout and backup strategy.
3. Final API contracts and module boundaries.
4. Supported document formats, maximum file size and extraction methods.
5. Initial list of core formulas and the exact formula specifications/test fixtures.
6. News provider selection, historical search coverage, licensing, rate limits and pricing.
7. Availability and terms for reliable subscription/GMP/history sources.
8. MVP report export format (recommend DOCX first; PDF may follow) and detailed visual design.
9. The quantitative method for listing-day scenario ranges and the peer cohort rules.
10. Whether and when a predictive model is justified by historical data quality and sample size.
11. Exact MVP formula register and golden test fixtures; these must be approved before those formulas are implemented.
12. Whether the MVP export is DOCX-only initially or DOCX plus PDF; recommended default is DOCX first.
13. Backup/restore procedure and supported local operating systems; resolve during technical design before storing irreplaceable research cases.

No coding agent may silently make one of these decisions and present it as already approved. It must propose the decision, rationale, alternatives and consequences for review, unless the decision has already been made in the project decision log.

## 18. Relationship to other project documents

This PRD must be read together with:

- **Project Brief:** canonical working copy: `IPO_Forensic_Analysis_Project_Brief_v1.0.md`; DOCX is the polished reading copy.
- **Indicator Catalogue & Data Dictionary:** canonical working copy: `IPO_Indicator_Catalogue_and_Data_Dictionary_v1.0.md`; DOCX is the polished reading copy.
- **This PRD:** `IPO_Forensic_Analysis_PRD_v1.0.md` is the canonical product-requirements source; this DOCX is its reading copy.
- **Future Data Source & Feasibility Document:** source coverage, accessibility, reliability, historical depth, terms, costs and manual fallbacks.
- **Future App Flow Document:** detailed screen-by-screen behaviour.
- **Future UI/UX Design Brief:** visual and interaction patterns.
- **Future TRD/Architecture Document:** approved technical stack and component behaviour.
- **Future Database Schema Document:** persistent entities, fields and relationships.
- **Future Implementation Plan:** ordered tasks and release gates.
- **Future agent instructions:** root-level `CLAUDE.md` and `AGENTS.md`, plus a concise project decision log, must direct coding agents to the canonical Markdown documents and prevent unapproved design changes.

**Documentation rule:** Markdown in Git is the source of truth for project requirements and technical decisions. DOCX versions are generated reading/sharing copies; do not edit them independently and let the two versions drift.

### Document authority rule

If documents conflict, do not silently choose whichever is easier to implement. Record the conflict, identify the affected requirements and propose a resolution. The approved PRD defines product behaviour; the approved TRD/architecture defines technical decisions; the schema defines storage structure; the indicator catalogue defines indicator meaning. A documented, reviewed decision can amend any of them.

## 19. Instructions for coding and review agents

Every coding agent must:

1. Read this PRD and the project rules before implementation.
2. Read the relevant indicator and data definitions before changing analytical logic.
3. Identify the requirement IDs covered by a proposed change.
4. Keep calculation logic deterministic, testable and separate from AI-generated prose.
5. Never invent a missing number, citation, source, timestamp or requirement.
6. Ask for a decision or raise an explicit unresolved item when instructions conflict; do not silently make product decisions.
7. Implement only the agreed scope for the current milestone.
8. Add tests for successful, missing, conflicting, stale and invalid-input cases where relevant.
9. Report actual files changed, commands run, tests passed/failed and known limitations. Never claim to have tested something that was not run.
10. Keep docs and code aligned; propose changes to this PRD when implementation exposes a real requirement gap.

## 20. Definition of done for a feature

A feature is not done merely because the screen or endpoint exists. A feature is done only when:

- its behaviour matches an approved requirement;
- its inputs, outputs and failure states are defined;
- validation and relevant tests exist and have been run;
- data provenance and missingness are preserved where applicable;
- user-facing limitations are clear;
- source code and tests are reviewed;
- relevant documentation is updated;
- no known critical defect is concealed by a successful-looking report.

---


## 21. Approval status and decisions

**PRD scope status:** Approved as the MVP product-scope baseline, subject to the explicitly open decisions below. This approval authorizes planning and feasibility work; it does not authorize implementation of undecided technical choices.

### Approved for MVP

- Local-first, single-user Indian IPO research.
- Manual-first case creation, evidence registration and time-sensitive observation entry.
- Source provenance, visible missingness/conflicts, reviewable facts, deterministic calculations and report traceability.
- A first set of documented financial/offer calculations and explainable cross-checks, with the exact enabled formula register approved before implementation.
- User-defined listing-day scenarios with transparent arithmetic; no claim of calibrated predictive power.
- Export and retention of report/run history without silently mutating prior evidence.

### Explicitly not approved as MVP requirements

- Mandatory live news, Google Trends, GMP, subscription or exchange APIs.
- Paid AI/API dependency or automatic document extraction as a prerequisite.
- Automatic trading/order execution, public SaaS, multi-user accounts or cloud database.
- A universal numeric IPO score or unvalidated probability of listing gain.
- Full implementation of all indicator catalogue modules or all advanced report sections.

### Open decisions that block the affected implementation

| Decision | Current status | Required next action |
|---|---|---|
| Data-source availability, access terms and historical depth | Open | Complete Data Source & Feasibility Audit before selecting integrations. |
| Exact MVP formula register and golden test data | Open | Select a small core set from the Indicator Catalogue and approve formulas/tests before implementation. |
| Supported document formats and extraction approach | Open | Test representative IPO documents; keep manual entry as fallback. |
| Local database, storage, backup/restore and OS support | Open | Decide in the TRD/architecture document before persistence implementation. |
| MVP export format | Open; DOCX first recommended | Confirm during app-flow/report design. |
| Scenario-price input method and any later scenario-range method | Partly defined | MVP accepts transparent user-defined scenarios; any automated range methodology requires a separate documented decision. |
| News provider, Trends and automated market-data providers | Not selected | Evaluate only after the feasibility audit. |
| Predictive modelling and calibration | Deferred | Require sufficient timestamped historical data and leakage-controlled evaluation before any performance claims. |

## 22. Review amendments incorporated

This approved baseline tightens the previous draft in five ways:

1. Clarifies that the MVP is a manual-first research and scenario-calculation tool, not a validated prediction engine.
2. Makes AI-assisted extraction optional and preserves manual entry as a complete fallback.
3. Makes the scenario-return formula and its inputs explicit and testable.
4. Replaces the vague “at least one agreed set of metrics” acceptance criterion with a formula-register release gate.
5. Clarifies that advanced report sections may be marked unavailable or deferred rather than forcing all modules into the MVP.

## Appendix A. Core terminology

| Term | Meaning in this project |
|---|---|
| IPO case | A saved research workspace for one identified issuer/issue. |
| Evidence record | A source document, disclosure, market observation or manually supplied item registered for analysis. |
| Fact | A factual value or statement tied to source evidence, period and validation state. |
| Calculated metric | A value produced by deterministic code from identified inputs and a defined formula. |
| Interpretation | An evidence-based explanation that goes beyond directly reported data. |
| Hypothesis | A plausible explanation that has not been established as fact. |
| Scenario | A conditional outcome based on stated inputs and assumptions; not a promise or necessarily a probability. |
| GMP | Grey market premium: an unofficial observation, not an official exchange price. |
| Information cutoff | The exact time after which information is excluded from a particular as-of analysis or backtest decision. |
| Look-ahead leakage | Use of information that was not available at the simulated decision timestamp. |
| Listing return conditional on allotment | Return calculation assuming an application received an allotment; distinct from the chance of allotment. |

## Appendix B. Minimum issue-case inputs for a useful report

The application should request or identify the following where applicable. The list is not a reason to fabricate values; unavailable fields must remain visibly unavailable.

- Issuer and issue identity, issue type and relevant dates.
- Price band/issue price, lot size, issue size and share-count basis where available.
- Fresh issue versus offer-for-sale split and stated use of proceeds.
- Offer-document financial periods and corresponding income statement, balance sheet and cash-flow data.
- Auditor qualifications, material contingent liabilities and disclosed related-party information where relevant.
- Subscription observations with investor category and timestamp, if available.
- GMP observation(s) with source and timestamp, clearly marked unofficial, if supplied.
- Peer observations and market context only when source, period and comparability are documented.
- User's intended analysis/decision cutoff, where time-sensitive evidence is involved.

## Appendix C. One-sentence product definition

**A local-first, evidence-driven Indian IPO research engine that builds auditable, company-specific forensic reports and transparent listing-day scenarios without inventing missing facts or overstating predictive certainty.**
