---
document: IPO Forensic Analysis Engine — Project Brief
version: 1.0
status: Planning brief; scope and architecture require approval before implementation
source: IPO_Forensic_Analysis_Project_Brief.docx
converted_on: 2026-10-29
---

# IPO FORENSIC ANALYSIS ENGINE

*Project Scope, Core Vision & Technical Brief*

A local-first, evidence-driven research system for evaluating Indian Mainboard IPOs primarily for listing-day exits.

**Status:** Planning brief — agree on requirements and architecture before further implementation.

**Intended user:** Single user / personal research. Local hosting first; no public product or cloud deployment required for the initial version.

---


> **CORE PRINCIPLE**
> AI must not guess, invent missing numbers, fabricate sources, or perform financial arithmetic without independent validation. Every material conclusion must trace to evidence, a reproducible calculation, or an explicitly labelled hypothesis.


## Binding Scope and Budget

The product owner's binding constraints for this project are:

- **Coverage:** Indian Mainboard IPOs only. SME IPOs are outside the MVP and must not be implemented.
- **Total budget:** ₹0. No paid API, dataset, AI service, hosting, software, upgrade, or paid fallback may be introduced.
- **Operation:** Local-first and manual-first. Core research must work from user-provided documents and manual observations without requiring live source APIs or AI.
- **Integrity:** Unknown is not zero; every material claim must be evidence-backed, a deterministic calculation, or explicitly identified as an interpretation/hypothesis.

These constraints supersede any broader wording elsewhere in this planning brief.

# 1. Executive Summary


The IPO Forensic Analysis Engine is a personal research application where the user enters an IPO name and receives a detailed, source-cited report focused on the likelihood and risk of a profitable listing-day exit. It is not a conventional IPO dashboard, generic listing page, or long-term investing recommendation tool.

It should collect and organize evidence, read offer documents, calculate financial and valuation measures, examine business-specific risks, compare indicators against one another, investigate contradictions, incorporate time-sensitive market signals, and produce a report with uncertainty and unresolved questions clearly stated.

- Primary objective: improve disciplined listing-day IPO decisions when capital cannot remain tied up for long.

- Primary output: a forensic research report, not a simplistic score or unqualified BUY/AVOID label.

- Initial mode: local-first; verified free sources where possible, with manual document/data upload as fallback.

- Longer-term goal: build and validate a historical model using only information available before each IPO listed.


# 2. Core Vision



> **THE VISION**
> Enter an IPO name. The system investigates available evidence, checks whether indicators agree, finds material risks and inconsistencies, tests plausible explanations, and produces a comprehensive listing-day decision report with citations, confidence limits and explicit unknowns.

The system should behave like a skeptical financial research analyst rather than a promotional IPO summary generator. It should actively search for reasons its initial thesis may be wrong.


## What success looks like


- Explain not only what each metric says, but how it connects to other metrics.

- A positive headline cannot outweigh contradictory underlying facts without explanation.

- Company-specific checks adapt to business model, sector, revenue structure and supply chain.

- Every important claim traces to a page, table, filing, dated data point or reproducible calculation.

- Missing, stale, conflicting or unverifiable data lowers confidence and is shown plainly.

- Listing outcomes are scenarios and distributions, not promised predictions.


# 3. Primary Use Case and Boundaries



## Primary workflow


1. User searches for an IPO by issuer name, symbol or identifier.

1. System resolves the correct issuer/issue and collects or accepts documents and market data.

1. System extracts facts, records source/date and validates values.

1. Deterministic calculation layer computes financial, valuation, demand and market measures.

1. Cross-indicator analysis tests relationships, inconsistencies, concentration and risk scenarios.

1. System produces a detailed listing-day report with scenarios, unresolved questions and qualified final assessment.


## Out of scope for the initial version


- Long-term portfolio selection as the primary objective.

- Automated placing, modifying or selling of market orders.

- Public accounts, multi-user features, social features or public SaaS launch.

- Cloud hosting, paid data subscriptions or expensive infrastructure before the local workflow proves useful.

- Assuming every source can be automatically accessed; manual uploads and review remain supported.

- Guaranteeing listing gains or presenting an unvalidated heuristic as a reliable probability.


# 4. Evidence Ingestion and Source Management


Build an evidence file for every IPO. Gather evidence automatically when reliable access exists, or accept user-supplied documents and data.


## Expected evidence categories


- DRHP, RHP, final prospectus, addenda and amendments; preserve document version and publication date.

- Audited financial statements, restated financial information, interim statements and auditor reports.

- Exchange issue information, price band, lot size, issue size, issue timetable and final subscription figures.

- Subscription time series by QIB, NII/HNI and retail categories where available, with timestamp and source.

- Anchor allocation and disclosed investor details where applicable.

- GMP observations from clearly labelled unofficial sources, with timestamp, source and history—not a lone snapshot.

- Peer-company filings, prices, valuation measures and business-model comparables.

- Company announcements, credible news, regulatory notices, litigation disclosures and relevant sector news.

- Market and sector context: index returns, volatility, recent comparable IPOs and broader risk appetite.

- Google Trends/search-interest data and other attention signals, subject to access and availability.


## Source-quality requirements


- Prioritize primary sources: offer documents, exchange disclosures, audited filings, regulator records and official company announcements.

- Use secondary reporting to discover leads or provide context; verify material claims against primary evidence where possible.

- Store URL/file reference, publisher, title, page/table, publication timestamp, retrieval timestamp and data period.

- Distinguish publication time, event time and retrieval time.

- Keep conflicting source values; document how conflicts were resolved or leave them unresolved.

- Track source reliability, completeness, freshness and whether values are extracted, manually entered, calculated or inferred.

- Do not treat undocumented endpoints as guaranteed APIs; adapters must fail gracefully.

- If issuer, issue, document version or reporting period is uncertain, ask for clarification rather than analyze the wrong entity.


# 5. Forensic Analysis Framework


Analysis must be modular and adaptive. Not every metric applies to every issuer; explain when a measure is not applicable, unavailable or unreliable.


## 5.1 Offer structure and IPO mechanics


- Fresh issue versus OFS, use of proceeds, debt repayment, general corporate purposes, issue size, post-issue shares, dilution, promoter/early-investor selling, pre-IPO transactions, lock-ins and upcoming supply unlocks.

- Check whether the stated purpose of the issue fits the balance sheet, growth plans and funding needs.


## 5.2 Earnings quality and accounting


- Revenue growth, gross margin, EBITDA/operating margin, PAT, tax rate, other income, exceptional items, non-recurring gains, expense capitalization and accounting-policy changes.

- Operating cash flow versus PAT, free cash flow where meaningful, receivables, inventory, payables, working-capital days, write-offs, provisions, contingent liabilities and auditor qualifications.

- Test whether profit improvement is recurring, cash-supported and consistent with operations.


## 5.3 Revenue, customer and supplier concentration


- Major customer concentration, contract renewals, supplier concentration, single-source raw materials, related-party counterparties, geography, product, channel and key-employee dependence.

- Where disclosed, quantify revenue, purchases, receivables or production tied to concentrated counterparties; never invent undisclosed names.

- Stress-test loss of a major customer, supplier interruption, input-price shock, contract non-renewal and reduced bargaining power.


## 5.4 Business model and sector-specific checks


- Adapt checks to the issuer: inventory/receivables for manufacturing and distribution; order book/execution for EPC; retention/utilization for services; regulatory/approval risks for relevant healthcare; credit quality and asset-liability risk for financial companies.

- Investigate unit economics, capacity utilization, seasonality, cyclicality, raw-material exposure, churn, pricing power, technological substitution and barriers to entry when relevant.


## 5.5 Governance, promoters and related parties


- Promoter background/ownership, pledges where applicable, related-party transactions/balances, litigation, regulatory actions, auditor changes, qualifications, remuneration, loans/guarantees, capital restructuring and unusual transactions.

- Separate verified adverse findings from allegations, disclosed risks and unproven hypotheses.


## 5.6 Valuation and comparable companies


- Calculate appropriate P/E, P/B, EV/EBITDA and price/sales only where meaningful, using compatible definitions and periods.

- Use post-issue share count and issue price consistently; compare growth, margins, return ratios, leverage and business mix.

- Identify weak/cherry-picked peer sets, unjustified premiums and non-comparable data.


## 5.7 Demand, market structure and listing setup


- Subscription progression by category, anchor allocation where relevant, issue size, likely free float, expected selling supply, market/sector sentiment, recent comparable IPOs and volatility.

- Track GMP as unofficial and noisy, with timestamps; never present it as an official price or guaranteed forecast.

- Check whether demand is broad-based or concentrated, and whether demand signals conflict with valuation or market conditions.


## 5.8 Legal, regulatory and external risks


- Material litigation, regulatory approvals, tax disputes, environmental/operating permits, export/import exposure, geopolitical and supply-chain risks, customer contracts and sector-specific regulation.

- Track events known before listing and distinguish disclosed facts from speculative scenarios.


## 5.9 News, sentiment and investor attention


- Search issuer, promoter, product, sector and relevant counterparty names. Prefer primary statements and credible sources; label opinion, rumor and unverified social posts.

- Measure news volume, source quality, recency, sentiment, topic, novelty and repeated syndicated stories.

- Google Trends/search interest indicates attention, not truth or buy demand. Check query ambiguity, baseline, geography and abnormal spikes.


# 6. Cross-Indicator Synchronization and Contradiction Detection


This is the defining capability and a core product requirement—not merely a later enhancement. Connect indicators and evaluate competing explanations instead of merely listing metrics or summing independent scores. The initial analysis must relate available company/offer fundamentals and valuation to category-wise subscription demand (QIB, NII and retail), GMP observations, market/sector context, relevant company events/news and comparable IPO outcomes where those signals are available. The system must show which relationships were tested, which inputs were unavailable or stale, and which relationships contradict one another.

**Acquisition requirement:** entering an IPO name initiates issue/source discovery; once the issue is sufficiently identified, the system attempts retrieval through approved source connectors for supported signal categories. Manual entry and evidence upload remain required fallbacks and must work offline. “Manual-first” means evidence can always be supplied manually—it does not mean that the product should default to making the user find every time-sensitive signal herself/himself. No provider is considered usable until its access method, permitted use, field definitions, coverage and timestamp quality are tested. If no free and permitted retrieval route exists for a critical signal, that is a visible release-blocking product decision, not a silent scope reduction.


| Relationship | Required investigation |
| --- | --- |
| Profit growth vs cash flow | If PAT rises but operating cash flow does not, inspect receivables, inventory, payables, other income, one-off gains, tax effects and working-capital movements. |
| Sales growth vs receivables | If receivables grow faster than sales, examine debtor days, overdue balances, customer concentration, credit terms and subsequent collections if disclosed. |
| Margin expansion vs business drivers | Test input prices, product mix, utilization, discounts, subsidies, exceptional items, capitalized costs and sustainability. |
| Customer vs supplier concentration | Stress-test simultaneous dependence on a few customers and a single critical supplier; assess interruption and bargaining power. |
| High subscription vs valuation | Demand may be strong despite stretched valuation. Analyze category mix, market conditions, issue size and comparable outcomes. |
| High GMP vs weak fundamentals | Treat as conflicting evidence; verify GMP freshness/source, then examine demand, valuation, float and sentiment. |
| Growth vs one-off contracts | Check repeatability, contract duration, customer dependence, order-book quality and whether growth is recurring. |
| Positive news vs primary disclosures | Compare claims with RHP, audited figures, exchange filings and company clarifications; flag unresolved differences. |
| Search spike vs actual demand | Check whether attention is accompanied by subscription and credible news or driven by viral controversy, confusion or promotion. |
| OFS vs growth narrative | Examine who is selling, proportion sold, stated reason, post-issue holdings and how any fresh-issue proceeds are used. |


## How synchronization should work


1. Extract facts with source, date, unit, period and page/table reference.

1. Normalize units and periods; do not mix standalone/consolidated figures or incompatible reporting windows.

1. Run deterministic calculations and domain-specific checks.

1. Link related indicators and flag relationships that do not hold.

1. Generate plausible explanations and test them against evidence.

1. Rate findings by severity, evidence strength, listing-day relevance and unresolved uncertainty.

1. Present confirming and disconfirming evidence. Do not declare fraud from an anomaly alone.

1. If a contradiction cannot be resolved, label it unresolved and lower confidence.


> **NON-NEGOTIABLE AI RULE**
> AI must not invent missing numbers, fabricate citations, silently fill gaps, or perform financial arithmetic without independent validation. Financial calculations must be performed by deterministic, testable code or verified calculation tools. AI may explain results, identify hypotheses and request missing evidence, but must label assumptions and never turn an unknown into a fact.


# 7. Listing-Day Decision Model


The target is return from offer price to an executable listing-day exit, not long-term company performance.


## Required outputs


- Bull, base, bear and severe-downside scenarios with explicit assumptions and supporting evidence.

- Estimated gross/net return where defensible; disclose brokerage, taxes, charges, slippage and assumed exit price/time.

- Potential downside and loss scenarios, not only upside.

- Separate business/offer quality from listing-day demand and sentiment.

- State whether data support a numerical estimate or only a qualitative assessment.

- Show main scenario drivers and what new evidence would change the view.

- Base confidence on evidence completeness and model validation, not an arbitrary percentage.

- Separate probability of allotment from listing-day return conditional on allotment.

- Do not call outputs probabilities until calibration is tested out of sample.


## Historical backtesting requirements


- Build historical IPO data including poor outcomes where available, not only winners.

- Use only information available at the historical decision time; prevent look-ahead bias and leakage.

- Store timestamped GMP, subscription, search and news observations; do not use final values for earlier dates.

- Measure calibration, error, profitable-trade rate, average/median net return, downside/tail loss and results by market regime/IPO segment.

- Compare against simple baselines and test whether each added signal improves out-of-sample results.

- Maintain a paper-trading log before trusting model outputs with capital.


# 8. Google Trends and News: Recommended Treatment


Include investor attention and news as a separate, time-sensitive signal family. It should affect analysis only through explicit, testable relationships with other evidence.


## Google Trends


- Track issuer and relevant keyword search interest where a reliable access route exists, with geography/date windows appropriate to Indian IPO investors.

- Use change from baseline, unusual spikes and time-series shape, not a single index value.

- Resolve ambiguous company names and generic terms; store the exact queries used.

- Compare search spikes with news timestamps, subscription progression, GMP observations and market sentiment.

- Access caveat: Google's official documentation describes a Trends API alpha with limited tester access. Do not assume general API access; use it only if access is granted, otherwise choose a compliant, tested fallback.


## News and sentiment


- Search company, promoter, product, sector and relevant disclosed counterparty names.

- Deduplicate repeated/syndicated stories and identify the original source.

- Classify items as official filing/announcement, credible reporting, opinion, rumor or unverified social content.

- Capture publication time, event time, source, topic, sentiment, novelty, evidence links and confirmation status.

- Seek negative as well as positive news; news volume is not the same as credibility.

- Do not treat headlines or AI summaries as verified facts without checking the underlying source.

Research note: academic studies have found associations between online search attention and IPO pricing or initial returns in some markets. Results depend on market conditions and study design; this justifies testing attention as a feature, not treating it as a standalone predictive rule.


# 9. Report Format and Required Sections


- Executive verdict for listing-day objective, including whether evidence is sufficient.

- Issue identity, dates, price band, lot size, issue structure and offer mechanics.

- Evidence inventory: sources obtained, versions, timestamps, missing documents and data-quality warnings.

- Financial trends with source/page references and reproducible calculations.

- Earnings-quality review and accounting/working-capital checks.

- Customer, supplier, product, geography and operational concentration analysis.

- Promoter, governance, related-party, legal and regulatory findings.

- Valuation and peer-comparability caveats.

- Subscription progression, anchor data, GMP history, float/supply and market context.

- News and investor-attention review, including Google Trends where available.

- Contradiction matrix: signal A, signal B, conflict, explanations tested, evidence and unresolved status.

- Material risks ranked by severity, likelihood where estimable, time horizon and listing-day relevance.

- Bull/base/bear/severe-downside scenarios and net-return assumptions.

- Counter-thesis: strongest reasons not to apply even if the main thesis is positive.

- Data gaps, questions for manual review, confidence rationale and analysis timestamp.

- Source bibliography with links, document page/table references and retrieval timestamps.


# 10. Data Integrity, Auditability and Safety


- Every material number has provenance: source, date/period, units, extraction method and confidence.

- Keep raw source values separate from normalized values and calculated outputs.

- Use explicit metric definitions and versioned formulas.

- Use precision-aware financial arithmetic; test rounding, units and signs.

- Validate extracted values against source tables and reconcile totals where possible.

- Never silently substitute zero for missing values.

- Mark stale/incomplete data and prevent stale signals from appearing current.

- Store the information cutoff used for every report so it can be reproduced.

- Treat uploaded documents and web pages as untrusted input; extracted text must not override system rules or trigger arbitrary actions.

- Do not claim to detect every fraud or hidden relationship; investigate only risks supported by available evidence and implemented checks.


# 11. Proposed Local-First Technical Architecture


Keep the first version simple enough for one person to operate and debug. Separate ingestion, extraction, calculations, cross-checking and report generation.


| Layer | Responsibility |
| --- | --- |
| User interface | Small local web app: search/select IPO, upload documents, view evidence status, run analysis, inspect/export report. |
| Backend/orchestration | Python FastAPI service to coordinate ingestion, validation, calculations and report assembly. |
| Document processing | PDF text/table extraction, page references, OCR fallback for scanned pages, structured extraction schemas and human correction. |
| Evidence store | Local SQLite for metadata, extracted facts, sources, timestamps, observations and report versions; local files for originals. |
| Calculation engine | Deterministic Python modules with unit tests, metric definitions and versioned formulas. |
| Cross-indicator engine | Explicit rules/dependency graph for financial relationships, concentration, contradictions and sector-specific checks. |
| AI layer | Document interpretation, disclosure retrieval, summarization, hypothesis generation and evidence-grounded narrative synthesis. |
| Report output | Detailed HTML and DOCX/PDF export with citations, tables, scenarios, data gaps and caveats. |
| Data adapters | Isolated official-source/news/search connectors with tests, timestamps, rate limits and graceful failure. |
| Testing | Formula unit tests, document fixtures, report regression tests, citation validation and time-leakage tests. |


# 12. Implementation Phases

The phases below must not postpone the defining cross-signal capability or hide unverified source access. Source feasibility is tested early; automated adapters are implemented only for sources that pass the explicit acceptance gate.

## Phase 0 — Requirements and source-feasibility gate

Finalize the signal relationships, report claims, data/evidence model and time-cutoff rules. Test a representative set of Mainboard IPOs against candidate sources for issue identity/terms, QIB/NII/retail subscription observations, named unofficial GMP observations, company disclosures/news and relevant market context. Record actual fields, observation timestamps, historical depth, access terms, cost, failure modes and coverage. A source must not be called feasible based only on a webpage existing.

## Phase 1 — IPO discovery, signal acquisition and evidence-first core

Implement the IPO-name entry/discovery flow and a source-acquisition orchestrator for approved connectors. The orchestrator attempts supported lookups after identity resolution, records per-source outcomes and timestamps, and shows unavailable/unsupported/stale/conflicting states. Preserve manual entry and document upload as complete fallbacks. A draft case and the core app must still work offline.

## Phase 2 — Core interconnected forensic analysis

Ship a tested first set of cross-indicator checks as part of the core analysis, not as a separate optional product. Include financial quality vs cash flow, revenue vs receivables/concentration, valuation vs fundamentals/peers, and listing-demand relationships such as QIB/NII/retail subscription vs valuation, GMP, offer size/free float and market/sector conditions. Findings must preserve confirming and disconfirming evidence, timestamps, limitations and missing prerequisites.

## Phase 3 — Expand approved time-sensitive source integrations

Improve coverage and freshness for subscription, unofficial GMP, official company/exchange events, news and market/sector context where a tested, free/permitted route exists. Add time-series views, source disagreement handling, deduplication and richer refresh behaviour. Do not make Google Trends or any one external provider a dependency.

## Phase 4 — Historical dataset and backtesting

Build point-in-time history that includes weak and poor listings, not only winners. Enforce information cutoffs and evaluate whether each added signal contributes out-of-sample value. No probability/accuracy claim before proper validation.

## Phase 5 — Broader validated automation

Automate additional source retrieval and document extraction only when reproducibility, source permissions, coverage and error handling are demonstrated. Retain manual correction and evidence review; never make an extraction result authoritative merely because it was automated.

# 13. Initial MVP Acceptance Criteria


- [ ] Create a Mainboard IPO case by name, resolve/confirm the correct issuer/issue, and attempt acquisition through approved source connectors after identity confirmation.

- [ ] Show a per-source acquisition summary: attempted/succeeded/partial/unavailable/blocked, returned fields, source and observation/publication/retrieval timestamps, freshness, and manual fallback. Never imply a source was checked when it was not.

- [ ] Interconnect the first validated financial/offer/valuation checks with available QIB/NII/retail subscription and named unofficial GMP observations; show missing, stale, conflicting or asynchronous signal limitations rather than inventing values.

- [ ] Upload a prospectus and supporting files without live data access.

- [ ] Every extracted financial fact has a source/page reference or is marked unverified.

- [ ] Financial ratios are calculated in code and unit-tested.

- [ ] Missing values remain missing; the engine does not guess or fill gaps silently.

- [ ] Report contains listing-day-specific analysis, not only long-term quality commentary.

- [ ] Initial cross-indicator checks explain the relationship tested.

- [ ] Contradictions are surfaced with competing explanations and unresolved status.

- [ ] Report includes sources, timestamps, confidence rationale, assumptions, gaps and counter-thesis.

- [ ] Analysis can be rerun with stored information cutoff and versioned logic.

- [ ] Data-access failures do not fabricate values or block manual completion.

- [ ] No broker execution, cloud deployment or paid API is required for the local MVP.


# 14. Key Risks and Open Questions


- Some exchange/provider data may be difficult to access reliably or may require registration, permission or payment.

- Prospectuses contain tables, footnotes and scanned pages that can break automated extraction.

- Unusual metrics can have legitimate explanations; risk flags need context.

- Undisclosed relationships or unavailable data cannot be reliably detected.

- Language models can produce plausible but unsupported explanations unless constrained and validated.

- Survivorship bias, look-ahead leakage, sparse data and regime changes can make a backtest misleading.

- Google Trends API access may be limited; it must remain optional and not block core analysis.

- Confirm source licensing and website terms before automated ingestion.

- 'Everything' is not literally achievable; target a broad, explicit, auditable checklist with sector-specific expansion and visible coverage gaps.


# 15. Product Principles / Non-Negotiables


- Evidence over confidence.

- Primary sources over summaries wherever practical.

- Calculations in deterministic code; AI explains, cross-checks and investigates.

- Unknown means unknown—not zero or an estimate disguised as fact.

- Every important claim is traceable.

- Contradictions are first-class findings, not noise to average away.

- Company-specific analysis rather than one rigid checklist.

- Listing-day return and downside are the target; company quality is an input, not the whole answer.

- Investor attention and sentiment are context signals, not proof of value.

- Local-first, manual fallback, low recurring cost.

- Backtesting before claiming predictive accuracy.

- Never promise a listing gain or treat an unvalidated score as a reliable probability.


# 16. Selected References and Source Starting Points


- Google Trends API alpha documentation — https://developers.google.com/search/apis/trends
Official documentation; confirms alpha access is limited.

- Google Trends API announcement — https://developers.google.com/search/blog/2025/07/trends-api
Official announcement and description of the alpha.

- NSE issue information — https://www.nseindia.com/market-data/issue-information
Starting point for issue information; verify fields and access constraints.

- SEBI — https://www.sebi.gov.in/
Regulatory rules, filings and notices.

- Research: Google searches and IPO pricing — https://www.sciencedirect.com/science/article/pii/S0378720624000545
Study of retail online activity and IPO pricing using U.S. IPO data.

- Research: Investor attention and IPO returns in India — https://doi.org/10.1108/JEAS-03-2022-0075
Study of investor attention and IPO returns in Indian markets.


## Project Documentation Status (maintained update — 2026-10-29)

- Project Brief: source document converted to this Markdown working copy.
- Indicator Catalogue & Data Dictionary: companion document exists; conversion to canonical Markdown remains pending.
- Product Requirements Document (PRD): draft v1.0 created and awaiting product-scope review.
- Recommended next step: review the PRD, then audit data-source feasibility before finalizing architecture, API providers or database schema.

# 17. Final Project Definition



> **ONE-SENTENCE DEFINITION**
> A local-first, evidence-grounded IPO forensic research engine that analyzes Indian Mainboard IPOs primarily for listing-day exits by combining offer-document research, verified financial calculations, company-specific risk checks, cross-indicator synchronization, time-sensitive demand/attention signals, historical backtesting and a detailed source-cited report—without inventing missing information or promising outcomes.

**Historical planning note (superseded):** The original DOCX recommended creating the indicator catalogue next. That catalogue has since been created; converting it into canonical Markdown remains pending.

**Current next step:** Review and approve the PRD, then audit data-source feasibility before committing to API providers, technical architecture or database schema.
