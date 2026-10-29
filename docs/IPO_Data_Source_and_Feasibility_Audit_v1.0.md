---
title: IPO Forensic Analysis Engine — Data Source & Feasibility Audit
document_id: DSA-IPO-001
version: 1.0
status: Dated source/API screening completed; direct raw-endpoint smoke tests remain open; no production connector fully approved
last_updated: 29 October 2026
product_scope: Indian Mainboard IPOs only; local-first, single-user, manual-first, ₹0 budget MVP
canonical_source: Markdown
---

# IPO Forensic Analysis Engine
## Data Source & Feasibility Audit

**Document ID:** DSA-IPO-001  
**Version:** 1.0  
**Status:** Dated source/API screening performed — promising documented routes identified; direct raw-endpoint smoke tests remain open  
**Research snapshot:** 29 October 2026  
**Companion documents:** Approved PRD v1.0; Project Brief v1.0; Indicator Catalogue & Data Dictionary v1.0

> **Purpose.** Determine whether the approved MVP can acquire the evidence it needs, from which sources, under what access and quality constraints, and what must remain manual until feasibility is demonstrated. This document is an audit and implementation gate, not a provider commitment or legal opinion.

## 1. Executive decision

### Verdict

**The current evidence does not establish a dependable, universal, free automated data pipeline—but that is a source-feasibility gap to resolve, not a reason to omit the product's acquisition workflow.** The product requirement is that entering an IPO name triggers issue/source discovery and an acquisition attempt for approved connectors, then connects the resulting observations through the cross-indicator engine. Source-specific availability, permissions, freshness and coverage must be tested before promising automatic retrieval for a field.

This audit must separate three conclusions:
1. **The source-acquisition orchestrator is a core MVP capability.** It tracks attempted connectors, retrieved fields, timestamps, partial results, missing categories and failure reasons.
2. **Each source connector is conditional on evidence.** A public webpage does not automatically imply an unrestricted API, permission to scrape it, permanent historical availability or rights to store/reuse the data. Do not use prohibited or undocumented endpoints or evade access controls.
3. **The user must have a complete fallback.** Manual entry, document upload/import, and local analysis remain usable when a source is unavailable. A missing signal must be visibly missing; the app must not pretend it refreshed successfully.

Official offer documents remain the main evidence foundation. For time-sensitive listing signals, the initial source benchmark must explicitly test category-wise subscription (QIB/NII/retail), named unofficial GMP publishers, and the company/exchange/regulatory event context required by the signal relationships. If no compliant free acquisition path exists for a critical category, record that as an explicit product-owner release decision; do not silently downgrade it to a manual-only intended product or claim full automation.

### Feasibility at a glance

| Area | MVP feasibility | Automation confidence | Recommendation |
|---|---|---|---|
| Offer documents and issue facts | High, manual-first | Medium/unknown until link and PDF tests pass | Primary evidence pack; manual registration is the fallback |
| Audited financials, risks, offer structure and governance disclosures | High for disclosures present in the offer documents | Medium/low for zero-review extraction | Manual verification; extracted values are candidates only |
| Local calculations and report generation | High; internal deterministic code | High once formulas and tests are specified | Build without external service dependencies |
| Current subscription snapshots by category (QIB/NII/retail) | High for public-page visibility; lower for normalized, time-matched consistency | Two keyless API candidates are documented, but raw GET, upstream rights, 10-IPO response coverage and field mapping are not yet independently verified; direct NSE scraping is prohibited by published NSE terms absent permission | P0: smoke-test the documented APIs and approve only after access terms, provenance, freshness, accuracy and representative coverage pass. Until then use manual/user-driven capture for exchange pages. |
| Historical listing-day prices | Medium for manually sourced records; history/access terms require testing | Low/medium for free, unrestricted bulk backfill | Do not promise a complete backtest dataset |
| GMP | Non-official observation from named secondary publishers, not an exchange fact | Xflot documents an API with explicit attribution/polling/disclaimer conditions; gmptoday.in documents a CC-BY-4.0 API but only a three-live-issue sample. Current public-page values disagree and have different timestamps. Neither raw JSON endpoint passed a direct GET in this environment. | Treat Xflot as a quality-gated candidate; gmptoday.in as a licensed but incomplete cross-check candidate. Do not approve either as a complete production connector until direct endpoint, timestamp and coverage tests pass; manual evidence remains fallback. |
| News/event evidence | High for manual source registration; automated coverage unproven | Unknown until provider rights, history and timestamps are verified | P0 source-discovery feasibility for events relevant to IPO case analysis; attempt approved routes, preserve provenance and fall back to manual evidence |
| Allotment status | Available through official exchange/registrar lookup flows | Low for durable historical research dataset | Not needed for MVP analysis; do not collect personal application data |
| Google Trends | Medium for documented manual snapshots; signal has interpretation limits | API currently presented as limited alpha access | P2 only; never an MVP blocker |
| Historical model calibration/backtesting | Not validated by this audit | Requires a point-in-time dataset and outcome definitions | Later scope, with no leakage and no performance claims beforehand |

## 2. Scope and assumptions

This audit follows the approved PRD and focuses on source feasibility for the MVP's P0 requirements: IPO-name-triggered source discovery/acquisition attempts, source metadata and timestamps, offer-document evidence, validated financial/offer inputs, category-wise subscription and GMP observations where a compliant retrieval path can be established, first interconnected cross-checks, scenario inputs, report citations and saved analysis history.

It does **not** assume that every module in the Indicator Catalogue must be implemented in the first release. Broad news coverage, search-attention signals, a large peer-IPO database, full historical/intraday market-data backfill and predictive modelling are not MVP prerequisites. The acquisition orchestrator and core relationships between available subscription/GMP signals and company/offer/valuation fundamentals are P0; individual connectors must pass feasibility review.

### Binding MVP scope: Mainboard only and ₹0 budget

The product owner's explicit decision and the repository's binding rules limit this MVP to **Indian Mainboard IPOs only**. SME IPOs are out of scope and must not be added to case-identity rules, source adapters, sample fixtures or acceptance tests. This resolves the earlier broad wording in the PRD and planning brief; it is no longer an open scope question.

The total project budget is **₹0**. Do not introduce paid market-data subscriptions, datasets, AI APIs, hosting, databases, software upgrades or paid fallbacks. A free provider may be used only after its current access terms, limits, and permitted use are verified. A connector is a provider choice, not proof of the whole signal category; if no compliant free route exists for a critical signal, record the gap and obtain an explicit product-owner decision before release. The local/manual fallback must always work.


### What counts as verified

A source is “verified for integration” only after a recorded test confirms the exact required fields, source identity, update timing, historical depth, format stability, failure behaviour, access conditions and permitted use. A browser page existing is not enough. This audit is an initial web research pass; it has not tested APIs, automated downloads, account-based access, contractual permissions, or the completeness of a historical dataset.

## 3. Evidence trust model

The application should grade **the evidence item and what claim it can support**, not attach one blanket quality score to an entire website.

| Evidence class | Examples | Default treatment |
|---|---|---|
| A — Regulatory / official filing | SEBI filing page; filed RHP/prospectus; regulator-issued order | Preferred source for disclosed issue terms, filings and regulatory/legal records. Preserve document date/version and page/section. |
| B — Official exchange / issuer source | NSE/BSE issue page; exchange filing; issuer investor-relations release | Preferred for exchange-published bid snapshots, listing notices, market records and company announcements, subject to exact field/date verification. |
| C — Official registrar / process result | Registrar's basis-of-allotment or application-status page | Relevant to the particular allotment process or application. Not a general signal of likely listing performance. |
| D — Secondary publication | News article, financial portal, data aggregator | Useful for discovery/context; important facts should be checked against primary documents where practical. Preserve publication time and article URL. |
| E — Unofficial market observation | GMP posts or broker-market chatter | Explicitly unofficial, source-attributed, timestamped and low-confidence. Never presented as an exchange-confirmed price or probability. |
| F — User input / AI candidate | Manual value, OCR/LLM extraction awaiting review | User-entered data remains attributed as such; extracted values remain candidates until accepted. Preserve correction/rejection history. |
| G — Derived result | Formula output, scenario result, cross-check finding | Reproducible only from known source inputs, formula version, units, rounding and calculation trace. Never label as an observed fact. |

These classes are not a universal numeric score. A value from a primary document can still be stale or refer to a different period. The system should preserve source quality, data freshness, applicability, validation status and conflict status separately.

## 4. Data-source matrix

“Acquisition attempted” means the core app initiates retrieval through a reviewed/approved connector; it does not imply universal coverage or that an API exists. Every connector must pass a documented source/terms/coverage/timestamp test. Manual entry is a complete fallback and offline workflow—not a reason to omit acquisition attempts from the intended product.

| Data need | Candidate source(s) | What can reasonably be obtained | Feasibility and constraints | MVP treatment |
|---|---|---|---|---|
| Issue identity, issue type, price band/price, dates, issue size, fresh issue/OFS, lot size, registrar, listing venue | SEBI Public Issues filings [S01]; NSE IPO page [S03]; BSE Public Issue summary [S04]; RHP/prospectus | Core identity, dates and offer terms when disclosed | Strong manual path. Page layouts, links and availability vary; no stable public API verified in this audit. Use identifiers and document evidence to disambiguate similarly named issues. | P0 manual capture + evidence attachment; source adapter only after tests |
| Offer documents: DRHP/RHP/prospectus and addenda | SEBI Public Issues [S01]; issuer and exchange issue pages | Original offer documents and updates; official filings are grouped by document stage | Strong as primary-source path, but multiple versions/addenda must not be merged invisibly. Extraction from complex PDF tables needs review. | P0; preserve original file, URL, retrieved date, version and page/section locators |
| Historical/restated financial statements, cash flows, financial notes and auditor information | RHP/prospectus; issuer annual reports; MCA View Public Documents [S05] | Financial statements and disclosures available in the relevant document sets | High disclosure availability for filed IPO docs; low confidence in fully automatic extraction without review. MCA's public-document guidance says viewing company documents is a fee-based service and requires login for the paid viewing workflow. | P0 manual verification; extracted numbers are untrusted candidates until reconciled |
| Risk factors, business model, customer/supplier concentration, related parties, promoter/shareholding, litigations, indebtedness, objects of issue | RHP/prospectus [S01–S02]; issuer filings; exchange corporate disclosures | Disclosures and context available at the document date | Content-heavy and company-specific; some facts are described in prose or tables. Not all indicators apply to every issuer. Later litigation/news changes need separate event sources. | P0 curated evidence with page/section locators; applicable/not-applicable states |
| Valuation and peer comparisons | RHP/prospectus peer tables and valuation disclosures; official peer filings; annual reports | Issue price, disclosed EPS/financial ratios and issuer-selected peers where disclosed | Definitions/periods may differ; issuer-picked peers are not automatically comparable. Live peer-price history and comparable ratios may be licensed or third-party sourced. | P0 compute only from validated inputs; label peer selection and as-of date; avoid automatic peer feed |
| Subscription by investor category | NSE IPO page [S03]; exchange issue pages | Current issue pages may show offered/reserved quantities, bids and category subscription | Useful for a dated snapshot; persistence of complete historical category data was not proven. Refresh timing and final-vs-interim status must be captured. | Optional P0 manual observation, source + observed/captured time + category definitions |
| GMP | Secondary IPO sources such as the methodology description on IPOtick [S13]; other explicitly named publishers | A reported unofficial grey-market indication, often with publisher-specific conventions | No official NSE/BSE/SEBI GMP feed was identified. Values may be crowdsourced, inconsistently defined, stale or incomparable. Historical observations may be incomplete; capture rights/terms separately. | Attempt acquisition from an approved named publisher when a free/permitted route is verified; otherwise show unavailable and allow manual snapshot with publisher, exact quote/context, currency/unit, timestamp and unofficial flag. Never treat missing GMP as zero or official fact |
| Listing-day outcome and daily OHLCV | NSE daily reports/bhavcopy [S10]; official NSE EOD/historical products [S07–S08]; BSE data products [S09] | Daily OHLC, close/volume and other exchange-defined fields depending on file/product; listing day can be joined only after identity/date validation | A public daily-report page is not proof of unrestricted bulk historical reuse. NSE explicitly offers paid EOD/historical data products and tariffs; BSE also lists paid market-data products. A day-level open is not necessarily the first executable trade/price at the exact simulated exit time. | P0 scenarios use user-entered price scenarios; verified market price may be manually recorded. Backtesting data is a separate later feasibility gate |
| Real-time/intraday listing price or order/trade-level prices | Official exchange data products [S07–S09] | Potentially detailed market observations under defined licensed products | More costly and contractual/technical than manual MVP. Not demonstrated as free public API in this audit. Required only if the product later promises intraday-exit simulations. | Out of MVP; do not imply first-trade or executable-price accuracy from end-of-day fields |
| Company disclosures and post-filing events | NSE/BSE corporate announcements; issuer investor-relations pages; SEBI notices/orders | Primary announcements, results and regulatory events | High value but fragmented. Coverage must be tested by issuer and period; timestamps and subsequent corrections/addenda matter. | Acquisition candidates are tested as part of the P0 source benchmark; approved connectors are attempted by the orchestrator, with manual evidence registration as fallback |
| News and event context | Original issuer/exchange/regulator announcements first; reputable news publishers second | Events, reporting and interpretation | No single news provider was verified here as covering required India IPO topics with acceptable cost, historical depth, licensing and stable timestamps. Article full text reuse and redistribution may be restricted. | Benchmark event/news discovery routes for P0 usefulness and terms; use approved connectors only, keep article claims traceable, and allow manual registration with headline, publisher, URL and separate publication/event/capture times |
| Allotment/bid status | NSE bid/allotment verification [S11]; registrar pages such as MUFG Intime [S12]; BSE investor lookup [S11–S12, S17] | A specific issue's bid or allotment status through an investor-facing lookup flow | Useful for an investor application, not a general IPO-quality dataset. NSE states bid information is available through 10 days after issue closure; this is not a long-term historical archive guarantee. Personal identifiers are unnecessary for the analysis engine. | Out of MVP. Do not store PAN, bank details, application numbers or DP/client IDs for this product's research workflow |
| Google Trends/search attention | Google Trends UI/FAQ [S14]; official Trends API alpha page [S15] | Relative, normalized interest observations; UI values depend on query, geography and time range | Trends explains values are normalized and not a scientific poll. Its API documentation currently describes an alpha and invites limited early-access applications; API access must not be presumed. | P2 only. If used later, record exact term/topic, geography, date range, capture date and scaling method |
| Sector/macro market context | Official exchange index/market reports; issuer/sector official releases | Dated broad-market or sector context | Can enrich the report, but definition and time alignment must be explicit. Avoid adding a broad market feed before core IPO evidence works. | Manual if materially relevant; automation after source checks |

## 5. Source-specific findings

### 5.1 SEBI and offer documents — primary foundation

SEBI's Public Issues page lists three key document stages: draft offer documents filed with SEBI, red-herring documents filed with ROC, and final offer documents filed with ROC. The documents can support a large part of the forensic report: risk factors, business description, capital structure, proceeds, restated financial statements, promoter/management disclosures, related-party matters and legal disclosures. [S01–S02]

**Implementation implication:** an evidence pack should register the document as a versioned object, not merely store a URL. Store at least the issuer/issue identity, document type, date shown on the document, source URL, retrieval timestamp, local filename, file hash, page count if available, and locators for every accepted fact. A later RHP, addendum or final prospectus must create a new evidence version and must not rewrite prior analysis runs.

**Limitation:** an offer document reports what was disclosed at a particular time; it is not a guarantee of current conditions. Later events require later evidence. PDF tables and notes may need manual review even if extraction technology is used.

### 5.2 Exchanges — strong for official market/issue evidence, not an assumed free API

NSE's issue-information pages visibly publish category-wise offered/reserved quantities, bid counts, subscription multiples and an update timestamp for specific issues. But the published NSE Terms of Use explicitly prohibit systematic or automated collection (including scraping and extraction) absent express written consent [S14]. Treat direct NSE pages as primary manual verification sources unless written permission is obtained. BSE/SEBI issue pages are useful source-discovery paths, but this screening did not verify a documented, no-cost, permitted first-party API for the required subscription fields. Do not infer that a page or underlying browser request is a licensed API. [S03–S04, S11, S14–S15]

NSE's Data Sharing & Usage Policy describes agreements that specify permitted use and restrictions, including restrictions on redistribution. NSE's data-vending pages separately list EOD/historical products and tariffs; the official EOD/historical page describes downloadable product formats and directs interested parties to contact NSE Data for subscription. BSE's information-products tariff sheet also lists EOD, historical and corporate data offerings. [S06–S09]

**Implementation implication:** start with manual snapshots and official files where available. For any automation, separately verify the precise page/data product, access method, permitted local/personal use, storage/retention, costs, update cadence, rate limits, historical backfill and whether redistribution/export is allowed. Do not treat HTML page calls, undocumented JSON endpoints or a scraper that currently works as a supported integration contract.

**Critical distinction:** an end-of-day bar (open/high/low/close) cannot automatically substantiate every possible listing-day exit. If a later backtest models selling at listing/opening, define whether the outcome means official opening price, first trade, first executable quote, a time-bounded window or day close—and obtain a data source that actually contains that observation.

### 5.3 MCA — useful fallback, but not assumed free/bulk

The Ministry of Corporate Affairs' online help states that public company documents can include incorporation documents, annual returns and balance sheets, and that viewing public documents is fee-based and available through a logged-in workflow. [S05]

**Implementation implication:** use MCA as a fallback for a specific missing filing only after reviewing the required access/fee and comparing the value with an official offer document or issuer release. Do not base the MVP on automated bulk collection from MCA. The project should record when a source was accessed and preserve the document received.

### 5.4 Subscription — only useful with time and category context

Subscription totals are time-sensitive: a 12:00 PM snapshot is not the close-of-issue result. Store investor category, shares offered/reserved, bids or subscription multiple as published, timestamp/time zone if known, source and whether the issue was still open. Never replace the prior snapshot with a later number; retain each observation.

**Open limitation:** public visibility and visible timestamps are verified, but neither complete historical category coverage nor a permitted first-party automated exchange feed is established here. The free API documented by ipos.markets advertises category-wise subscription but its upstream rights/provenance and terms were not established in this review [S17]. Xflot also documents category-wise subscription in a public API, but its indexed page-level data show internal consistency problems on the Zetwerk sample and the raw endpoint has not passed a direct GET test [S15]. Keep both as unapproved candidates pending direct response testing.

### 5.5 GMP — weak, non-official, optional evidence

No official exchange/regulator GMP feed was identified in this research. GMP should remain an unofficial, source-attributed observation. Two public APIs surfaced: Xflot documents a no-key combined IPO/GMP API with attribution, no-more-than-once-per-minute polling and a required disclaimer; gmptoday.in documents a no-key feed under CC BY 4.0 with attribution, but its API response is explicitly a three-live-issue sample rather than the site's full tracked board [S15–S16]. The Xflot issue pages also display source/time disagreement and, in at least one sample, internal conflicts; therefore technical availability and source terms do not by themselves confer data-quality approval.

**Implementation implication:** treat GMP only as a dated, attributed market observation. Do not infer a probability of listing gains from it; do not substitute missing GMP with a value from another site; do not combine providers without preserving each reported observation. Store the publisher's wording/definition and the timestamp at which the claim was observed. If the publisher does not disclose a timestamp or method, mark that limitation explicitly.

### 5.6 News and issuer events — manual evidence first

For high-impact events, prefer the original issuer, exchange or regulator announcement and use news coverage as secondary context. The MVP needs the ability to register a URL and key metadata, not an automated news firehose. Any eventual provider must be compared on India IPO coverage, issuer/market coverage, original publication timestamps, historical search, duplicate syndication, API limits, price, terms for retaining article text, and whether processed summaries can be exported. None of those items should be assumed solved by a generic “news API.”

### 5.7 Trends — do not design around API access

Google Trends says its index is normalized against total search volume for the selected geography and time range; it reflects search interest, is not a scientific poll, and should be one signal among others. The official API page continues to describe an alpha/early-access path and invites applications for limited tester access. [S14–S15]

**Implementation implication:** leave Trends out of MVP. If the user captures a UI value later, record search term/topic, geography, time range, retrieval date and the displayed normalization context. Do not call the index “number of searches,” and do not build a mandatory API integration based on the current alpha page.

## 6. Proposed source capture contract

The exact database schema remains open; this is the minimum data contract the future design should preserve. It must be mapped into the approved PRD and data dictionary before implementation.

### 6.1 For every source/evidence item

- Stable local `source_id` and `evidence_id`.
- Source class/trust category; publisher/source name; source title.
- URL or local file reference; original filename; content type; file hash for stored files.
- Document/observation version or revision where identifiable.
- Publication time/date, event time/date, retrieval/capture time, and effective period stored as separate fields. Unknown values remain unknown.
- Source locator: page, section, table, paragraph, announcement ID or precise URL fragment where available.
- Capture method: manual, file upload, import, or verified adapter; adapter/version for automated retrieval.
- Data terms/access note if relevant; do not infer permission from mere accessibility.
- Validation status: unreviewed, confirmed, corrected, rejected, unresolved, stale, conflicting, or not applicable as appropriate.
- Change history for accepted/corrected/rejected values; preserve prior report versions.

### 6.2 For every fact/observation

- Value plus explicit unit, currency and period/date where applicable.
- Related issuer/issue/security identity and identifier used to join it.
- Evidence/source link and locator; no “source URL” field that points only to a generic homepage when a specific document/page exists.
- Observation time and capture time for market snapshots.
- State: observed, calculated, user-entered, extracted candidate, interpretation, hypothesis or scenario assumption.
- Conflict references where two sources disagree.
- No default of zero when a field is missing or unavailable.

### 6.3 For every calculated metric or scenario output

- Formula identifier and version; named inputs with source/evidence IDs; units/periods; rounding rule; exact calculation timestamp and analysis information cutoff.
- Validation and applicability prerequisites; deterministic output or an explicit blocked/unavailable state.
- Test reference from the formula register, plus calculation trace in the report or drill-down view.
- Clear distinction between observed market price and user-entered scenario price. Scenario price is an assumption, not an externally verified forecast.

## 7. Information-time and point-in-time integrity

The central question for an IPO listing-day tool is not only “what number was later recorded?” It is “what evidence could the user have known by the chosen cutoff?” This distinction is mandatory if historical backtesting is added.

For each time-sensitive input, preserve as distinct concepts:

1. **Publication time** — when the publisher made the information public, if known.
2. **Event time** — when the reported event occurred.
3. **Observation time** — the time a market snapshot is supposed to represent.
4. **Capture time** — when the application/user retrieved or recorded it.
5. **Analysis cutoff** — the latest information allowed in a given analysis run.

A late edit to a news article, a final subscription number recorded after issue close, or a later corrected document must not leak into a replay of an earlier decision. If a historic observation has no reliable timestamp, the backtest must exclude it or classify it under a clearly defined missing-time rule; it must not assume the value was available earlier.

## 8. Main risks and recommended controls

| Risk | Why it matters | Control / release condition |
|---|---|---|
| Confusing a working website with a stable API | Source markup/endpoints can change, be rate-limited, or be restricted by terms | No integration without repeatable test, documented fields, terms review and graceful failure |
| Treating visible data as free to republish | Market-data contracts can restrict use and redistribution | Record intended use; check current exchange/source terms; obtain provider confirmation before redistribution or public release |
| Missing historical data mistaken for no event | Historical subscription/news/GMP pages may expire or omit old snapshots | Explicit coverage status per issuer/date; never silently backfill from memory or unrelated sources |
| Wrong issuer/security join | Company names, symbols and issue names may vary; symbols can change | Resolve identity using multiple identifiers where available; flag ambiguity and preserve alias history |
| Mixed financial periods or standalone/consolidated accounts | Ratios can be materially wrong despite correct arithmetic | Store period, statement basis, units and currency; block invalid joins; reconciliation tests |
| PDF extraction errors | Tables, footnotes, signs, commas and units can be misread | Candidate facts require review; attach page/table locators; reconcile totals and test known values |
| Stale or untimed GMP | Gives false precision to a non-official market observation | Optional only, timestamped and source-attributed; freshness warning; no silent averaging |
| News duplicates or revised timestamps | Repeated syndication can be mistaken for independent signals | Manual first; later use canonical URL/story/event IDs and preserve publication/capture times |
| Look-ahead leakage in backtesting | Makes historical results look better than real-time decisions | Immutable as-of snapshots; exclude later-published observations; tests must simulate actual cutoff |
| Overbuilding around P1/P2 signals | Consumes time before the core report is auditable | MVP gate requires manual-first success and P0 acceptance before source adapters |
| Unclear Mainboard/SME scope | Source fields, exchange segments and outcome definitions differ | Approve scope boundary and include representative cases in the source test corpus |

## 9. What is feasible now versus not yet proven

### Feasible now for the MVP

- Store official PDFs and other user-supplied evidence locally.
- Create a source registry with provenance, dates, locators and source-quality classes.
- Manually enter and verify issue terms, financial figures and time-sensitive observations.
- Mark evidence missing, stale, conflicting, unverified, invalid or not applicable.
- Calculate selected metrics with deterministic, tested code.
- Let users set listing-price scenarios; calculate conditional return from issue price and scenario price only when inputs are valid.
- Produce an auditable report that identifies missing and unsupported material claims.

### Not yet proven; do not promise it

- A stable, documented, free API spanning all required NSE/BSE IPO fields.
- Complete historical subscription-by-category snapshots for all IPOs.
- A reliable official GMP history (no official source identified in the reviewed materials).
- A licensed, low-cost, comprehensive historical/intraday listing-price feed suitable for any chosen exit-time definition.
- A free news API with adequate historical India-IPO coverage and acceptable retention/reuse rights.
- General availability of the Google Trends API beyond the alpha/early-access programme.
- Any calibrated probability of listing gains or validated predictive performance.

## 10. Recommended implementation sequence

1. **Preserve fixed scope and analytical intent:** Mainboard-only and ₹0. The intended experience is IPO-name-triggered acquisition attempts plus interconnected analysis of company/offer fundamentals, valuation, category-wise subscription (QIB/NII/retail), GMP and relevant market/company-event signals. Do not re-open these product goals simply because provider feasibility is uncertain.
2. **Run the source benchmark early, before promising integration coverage.** Test candidate routes for current issue identity/terms, QIB/NII/retail subscription, named unofficial GMP publishers, official company/exchange/regulatory events and any market/news context that the cross-signal rules require. Record sample IPOs, fields, exact definitions, observed/publication/retrieval timestamps, freshness, history, access/usage terms, cost/quotas, stability and failure behaviour.
3. **Define source-neutral evidence and acquisition contracts.** Preserve the source/evidence/fact/observation/calculation lineage and status model; put per-source mapping behind connector interfaces. Do not hard-code one vendor into the domain model.
4. **Implement the source-acquisition orchestrator and complete fallback together.** After IPO identity is confirmed, trigger approved connectors, persist source-attempt outcomes and show returned/missing/stale/conflicting categories. Manual entry/import and local case/report workflow must still work offline.
5. **Implement a working vertical slice with interconnection.** One IPO case should pass through identity confirmation, acquisition attempts, manual supplement, validation, an approved formula set, selected cross-indicator findings, scenario calculations and a traceable report/run history.
6. **Run and preserve the acceptance-test log.** Test source success, partial success, missing data, stale data, ambiguous identity, denied/unavailable source and offline fallback. Preserve actual dated pass/fail results in Git; never mark an unrun test as passed.
7. **Resolve critical-source gaps explicitly before release.** If no lawful/free source path exists for a critical required signal, present the evidence and trade-off to the product owner. Do not silently relabel a manual-only product as the intended automated signal-interconnected product; no paid provider is to be added without a product-owner decision that changes the ₹0 constraint.
8. **Only then expand historical backtesting.** Approve outcome definition, point-in-time history and permitted dataset access before claiming calibration/prediction performance.

## 11. Source feasibility test plan

These tests are the next concrete work items. All tests should be logged against named IPO cases, not just marked “tested” in general.

| Test ID | Test | Acceptance condition | Priority |
|---|---|---|---|
| DSA-T01 | Offer-document retrieval across selected issues | For each sample, locate the appropriate filed offer document, verify issuer/issue identity and document date/version; retain local copy and direct source URL | P0 |
| DSA-T02 | Version/addendum handling | For at least one issue with a later addendum/final document, show both versions without silently replacing earlier evidence | P0 |
| DSA-T03 | Core fact locator test | Manually verify issue price/price band, issue size, fresh issue vs OFS, a financial statement value and one material risk against explicit page/section/table locators | P0 |
| DSA-T04 | Financial-period/unit validation | Confirm statement basis (standalone/consolidated), period, units and sign conventions for sample financial inputs; calculate a known-answer metric independently | P0 |
| DSA-T05 | Subscription acquisition benchmark (QIB/NII/retail) | On a representative set of recent and older Mainboard IPOs, test a documented/approved route for category definitions, shares offered/reserved, bids/multiples, observed/publication/retrieval time, interim/final status, coverage, limits/terms and failure behaviour | P0 source-feasibility gate; connector cannot be claimed before results are recorded |
| DSA-T06 | Listing-day price definition | Write a precise outcome definition (e.g., official opening price vs first trade vs day close), source fields required and whether the tested files actually contain that measure | P0 decision before historical backtest; not a blocker for manual scenarios |
| DSA-T07 | Historical data depth and rights | Check multi-year coverage for intended issue universe; capture current data tariff/terms, intended-use restrictions, formats and written clarification if needed | P1 / before automation |
| DSA-T08 | GMP acquisition and evidence benchmark | Test named candidate publishers across representative IPOs. Record source-access method/terms, quote convention/units, timestamps, freshness, historical gaps, copied/duplicated values and failures. Preserve two differently timed/source observations independently. | P0 source-feasibility gate for the intended listing-signal analysis; GMP remains explicitly unofficial |
| DSA-T09 | News/announcement provenance | Register a primary announcement and one secondary story; preserve URLs and separate publication/event/capture times; check whether duplicate reporting is identified as separate coverage rather than independent events | P0 registry capability; provider automation later |
| DSA-T10 | Failure and manual fallback | Disable network or use a missing/dead source; complete core data entry, calculations and report creation with missingness labelled | P0 release gate |
| DSA-T11 | Historical cutoff integrity | Construct a sample where a value is published after the analysis cutoff; prove that it is excluded from that run and does not rewrite an earlier report | P0 architecture/test gate for any backtest; foundational timestamp behaviour in MVP |
| DSA-T12 | Source identity collision | Use issues with similar names or changed symbols; confirm ambiguity is surfaced and facts cannot attach to the wrong issue silently | P0 |
| DSA-T13 | Source terms / automation gate | Before writing a live adapter, document allowed method, rate limits, storage/retention, personal/non-commercial use, reuse/export, attribution and costs from current source terms or written response | P1 before each adapter |

| DSA-T14 | IPO-name-triggered acquisition orchestrator | For named representative Mainboard IPOs, verify that identity resolution precedes attaching observations, approved connector attempts are recorded, returned fields and separate timestamps persist, and failed/blocked/unavailable outcomes remain visible. Test ambiguous identity and offline operation. | P0 |
| DSA-T15 | Cross-signal synchronization smoke test | With validated company/offer/valuation inputs and time-stamped QIB/NII/retail and GMP observations, verify the specified first relationships run only on compatible inputs/cutoffs, preserve competing sources and counter-evidence, and mark missing/stale/asynchronous prerequisites instead of inventing a result or claiming causation. | P0 |

### Minimum sample design

Use at least 10 **Indian Mainboard IPO** cases for the first feasibility sample: a mix of recent and older issues, different issue sizes/sectors, relevant exchange/registrar paths, and both clean and difficult documents. SME IPOs are out of scope and must not be included in the MVP benchmark. The sample is for source availability and extraction reliability, not for claiming predictive performance.

## 12. Provider-selection scorecard (use before approving any adapter)

Rate each candidate only after evidence is collected. Use “unknown” rather than a guessed score.

| Criterion | Evidence required |
|---|---|
| Field coverage and definitions | Field list, units, category definitions, identifier system and sample output |
| Source authority | Primary/official vs secondary; underlying source cited? |
| Freshness and timestamp quality | Publication/observation times, time zone, update cadence, correction behaviour |
| Historical depth and completeness | Earliest available date, gaps, revised history, retention/deletion behaviour |
| Format and technical stability | Documented API/file format, version policy, pagination, rate limits, failure modes |
| Permitted use | Personal/non-commercial use, local storage, caching, derived metrics, export and redistribution rights |
| Total cost | Free tier restrictions, subscription fee, overage, taxes, per-user/per-medium limits, contract minimums |
| Provenance | Direct source URLs, source timestamps and audit trail preserved |
| Fallback behaviour | Manual entry, last-good data clearly marked stale, no fabricated values |
| Practical value | Does the data materially improve an approved P0 requirement, or is it only “nice to have”? |

**Approval rule:** a source adapter is not approved merely because it is technically possible. The decision must show that its data quality and rights support a defined requirement and that the manual fallback remains complete.

## 13. Open decisions and recommended answers

| Decision | Current state | Recommendation |
|---|---|---|
| Mainboard vs SME coverage | Fixed product decision: Indian Mainboard IPOs only | Keep SME IPOs out of the MVP source benchmark, case identity, adapters and acceptance fixtures |
| Historical outcome definition | Open; scenarios are MVP, backtest is later | For MVP, use explicit user-entered scenario prices. Before backtesting, define open/first-trade/close and transaction assumptions separately |
| Acquisition workflow vs provider selection | Acquisition orchestration and initial signal interconnection are required P0 product capabilities; individual providers remain unapproved until tested | Implement the provider-neutral orchestrator; benchmark and approve free/permitted routes for critical subscription (QIB/NII/retail) and unofficial GMP signals. If a critical category has no compliant route, obtain an explicit product-owner release decision rather than silently defaulting to manual-only |
| Subscription/GMP/news/Trends source providers | Not selected; source feasibility is not yet demonstrated | Test candidates early for permitted access, cost, category/field coverage, timestamps, freshness, historical depth and failure behaviour; manual observation remains fallback. Google Trends remains P2 |
| Paid market-data access | No budget/provider approved | Assume zero external data spend in MVP; do not access/redistribute licensed datasets without terms approval |
| AI extraction | Optional and not required | Defer until manual workflow and validation are sound; extracted candidates must be user-reviewable |
| Data persistence and backup | Technical decision remains open | Preserve original files and run history; select local storage only after architecture review |
| Historical backtest dataset | Not yet validated | Treat as a separate feasibility project, with as-of data and an explicit missingness policy |

## 14. Definition of “data-source feasible” for MVP

The MVP passes this audit's practical gate when:

- IPO-name entry initiates the core acquisition workflow for approved connectors, with source attempts/outcomes and missing categories visible.
- A representative dated source benchmark exists for critical listing-signal families, especially QIB/NII/retail subscription and named unofficial GMP sources; every connector claimed as working has actual coverage, terms, timestamp and failure evidence.
- No critical signal category with no free/permitted retrieval route is silently treated as solved; the product owner has explicitly resolved any such release trade-off.
- A user can complete the local core workflow without paid providers or AI, and manual entry/upload remains a complete fallback.
- A representative sample of offer documents can be registered with source metadata and locators.
- Core inputs have verified units, periods, issue identity and status; unresolved items remain visibly unresolved.
- Every enabled formula has known-answer and invalid-input tests, as required by the PRD.
- The report correctly distinguishes evidence, calculation, interpretation and scenario assumption.
- Offline/manual fallback works and source failure does not create fabricated values.
- No external adapter is treated as approved until data terms, fields, timestamps, historical coverage, failure handling and costs have been documented.

This gate validates an evidence-driven manual-first tool. It does **not** validate predictive power or guarantee a profitable listing-day exit.

## 15. Research limitations

This is an initial desk-based audit of official web pages and selected secondary methodology pages as reviewed on 29 October 2026. It did not conduct contractual/legal review, request data-provider quotes, test live API endpoints programmatically, measure large-scale extraction accuracy, exhaustively download historical exchange files, or verify every Indian Mainboard IPO. SME IPOs are outside this audit's scope. Web pages and tariffs can change. Accordingly, any untested point is marked unknown or conditional, not presented as a fact.

The findings should be refreshed before a source adapter or commercial/public deployment is approved. Intended use matters: private local research, internal tools and public redistribution may be treated differently by a data provider.

## 16. Reference sources

The links below are the source trail for this audit. Official/regulatory/exchange sources are prioritised; third-party sources are used only where they document an unofficial category or help describe an access workflow. **Accessed/reviewed:** 29 October 2026.

- **[S01] SEBI — Public Issues filings.** Lists draft offer documents filed with SEBI, red-herring documents filed with ROC, and final offer documents filed with ROC. [Open source](https://www.sebi.gov.in/filings/public-issues.html)
- **[S02] SEBI — Guide to understand an Offer Document.** Describes the information commonly disclosed in offer documents, including risk factors, financial statements, capital structure, objects of the issue, business, promoters, legal information and offering information. [Open source](https://www.sebi.gov.in/sebi_data/docfiles/20612_t.html)
- **[S03] NSE — IPO / All Upcoming Issues.** Current issue page includes issue dates/status and offered/reserved, bids and subscription fields. [Open source](https://www.nseindia.com/market-data/all-upcoming-issues-ipo)
- **[S04] BSE — Issue Summary Document: IPO/FPO.** Public issue summary page with company search, date filters and issue/listing-stage links; page access may vary by automated client. [Open source](https://www.bseindia.com/markets/PublicIssues/Issuesummary.aspx)
- **[S05] MCA — MCA21 online help, document-related services.** States public documents may include annual returns and balance sheets; viewing them is a fee-based logged-in service. [Open source](https://www.mca.gov.in/MCA21/dca/WebHelp/Help_MCA21_English.pdf)
- **[S06] NSE — Data Sharing & Usage Policy.** Sets out market-data use, access and redistribution conditions and subscription agreements. [Open source](https://www.nseindia.com/static/market-data/nse-data-policy)
- **[S07] NSE — Data and Information Vending.** Describes NSE Data & Analytics' market-data products and current product/tariff resources. [Open source](https://www.nseindia.com/static/nse-data-and-analytics/data-information-vending)
- **[S08] NSE — Paid End-of-Day / Historical Data.** Describes EOD/historical products, formats, subscription inquiry and associated tariff resources. [Open source](https://www.nseindia.com/static/market-data/eod-historical-data-subscription)
- **[S09] BSE — Information Products Domestic Tariff Sheet.** Lists market-data, EOD, historical and corporate-data products. Verify current tariff and intended-use terms before use. [Open source](https://www.bseindia.com/downloads1/Information_Products_Pricing_Sheet.pdf)
- **[S10] NSE — All Reports.** Current exchange report page includes downloadable daily reports such as bhavcopy/security-deliverable data; current availability does not prove unrestricted historical bulk access. [Open source](https://www.nseindia.com/all-reports)
- **[S11] NSE — Verify IPO Bid / Allotment Details.** Describes bid verification and says bid information is available through 10 days after issue closure; allotment information is provided as supplied by the registrar. [Open source](https://www.nseindia.com/invest/check-trades-bids-verify-ipo-bids)
- **[S12] MUFG Intime — Public Issues / Application Status.** Official registrar investor-facing lookup page. [Open source](https://in.mpms.mufg.com/Initial_Offer/public-issues.html)
- **[S13] IPOtick — IPO Data Sources & Methodology.** Third-party methodology page explicitly describes GMP as unofficial and not published/verified by NSE, BSE or SEBI. This is not an official regulator statement. [Open source](https://ipotick.in/about)
- **[S14] Google Trends Help — FAQ about Google Trends data.** Describes normalization and warns that Trends is not scientific polling data. [Open source](https://support.google.com/trends/answer/4365533?hl=en)
- **[S15] Google for Developers — Google Trends API alpha.** Current documentation describes a rolling five-year window and an alpha/early-access application path; general API availability was not assumed. [Open source](https://developers.google.com/search/apis/trends)
- **[S16] SEBI — Approach to securities-market data access and terms of usage.** Circular dated 25 February 2022 on access and terms for securities-market data sources. [Open source](https://www.sebi.gov.in/legal/circulars/feb-2022/approach-to-securities-market-data-access-and-terms-of-usage-of-data-provided-by-data-sources-in-indian-securities-market_56420.html)
- **[S17] Zerodha Support — IPO bid/allotment status guide.** Secondary procedural guide naming exchange and registrar lookup paths; use official portals for actual verification. [Open source](https://support.zerodha.com/category/trading-and-markets/ipo/ipo-application/articles/check-ipo-status)


## 17. Dated source/API benchmark — 29 October 2026

### 17.1 Scope and evidentiary status

This is a dated **source-screening benchmark**, conducted before the implementation plan, focused on current and recently closed Indian Mainboard IPOs. It checks visible field coverage, timestamp semantics, documented endpoint contracts, stated usage conditions and cross-source consistency.

**Important limit:** the web research interface and the available execution environment could not complete direct HTTP GET requests to the raw JSON endpoints. The API routes and conditions below are documented by their publishers, and related public issue pages can be inspected, but no raw endpoint is marked as having passed a live request from this benchmark. The source audit therefore distinguishes:
- **Documented candidate:** the publisher documents a free endpoint and fields/terms.
- **Public-page observed:** information is visible on a published issue page or search-indexed page with a source/time context.
- **Production-approved connector:** not yet achieved by any candidate in this benchmark. Approval requires a direct GET smoke test, repeatability, 10-IPO coverage and source/usage review.

The research environment's inability to call a raw endpoint must not be interpreted as evidence that the provider endpoint itself is down. It means the direct-GET test remains open. Do not put any of these APIs into production code as a proven integration based on this document alone.

### 17.2 Provider screening results

| Candidate route | What its public documentation/page establishes | Free/permitted-use screening | Data-quality / coverage finding | Decision as of 29 Oct 2026 |
|---|---|---|---|---|
| NSE issue-information pages | Visible category-wise reserved/offered shares, bids, multiples and an update timestamp on issue pages. A sample page for Paras Healthcare displays QIB/NII/retail values as at 21 Oct 2026 12:00. [S03, S14] | NSE Terms of Use explicitly prohibit systematic or automated collection, including scraping and extraction, without express written consent. [S18] | Strong primary manual verification source; the retrieved page/snapshot does not establish complete post-close historical coverage or a permitted free automation interface. | **NO-GO for a direct scraper** unless written permission is obtained. Manual/user-driven verification remains usable. |
| BSE / SEBI public-issue pages | SEBI's curated market-data page links to NSE and BSE primary-market issue resources. [S04] | No documented no-key BSE category-subscription API with clearly applicable free automation terms was verified in this screening. | Use as primary document/issue discovery and independent comparison; page accessibility is not API permission. | Manual/source-registration route only pending a specific, documented, permitted API/access path. |
| Xflot public Market Data API | Documentation describes GET /api/public/market/ipos and a per-IPO endpoint with reported GMP, subscription, category-wise subscription, timestamps/history, contributing-source count, spread and gmpDisputed flag. [S19] | The published API terms require attribution with a link, polling no more than once per minute, and preservation of the disclaimer. No key/sign-up is required per its documentation. [S19] | Promising combined-feed candidate, but not approved. Its public Zetwerk issue page updated 28 Oct contains contradictions: issue chronology says it closes on 19 Oct despite the issue having listed on 23 Oct; different sections show different issue sizes; and its headline subscription summary conflicts with the detailed category table. [S22] The Xflot monthly page's visible last-updated time was 24 Oct, five calendar days before this snapshot. [S23] Raw API payloads, upstream rights and ten-issue API coverage remain unverified here. | **CONDITIONAL CANDIDATE; FAIL quality sign-off for now.** Direct GET, freshness and consistency tests must pass before enabling it. Use source-level reconciliation, not trust in the API's existence. |
| gmptoday.in JSON API | Documentation describes /api/gmp.json, a no-key static JSON feed advertised as hourly, with median/range/source-count data and timestamps. [S24] | The publisher explicitly documents CC BY 4.0, including commercial use, with attribution/link required. [S24] | The API response is explicitly a sample of the three live issues with the strongest grey-market signal; the site displays a broader board. Its home page timestamp from this screen was 28 Oct 2026, 19:29 IST, not the current morning of 29 Oct; use response-level timestamps and do not assume the advertised refresh always occurred. | **LICENSED LIMITED-SAMPLE CANDIDATE; direct GET remains untested.** Not adequate as the sole/full GMP connector. |
| ipos.markets subscription API | Documentation advertises a free, keyless REST API for current/final QIB/NII/retail subscription, overall multiples and category book fields, with JSON/CSV and a five-minute edge cache. The publisher explicitly states that its curation is MIT-licensed and asks for attribution. [S25] | The publisher's published licence/attribution terms are clearer than the exchange webpage route. The publisher says the data are republished from official NSE/BSE books; the upstream source's own redistribution agreement was not independently verified in this screening. | **Strongest subscription API candidate.** The API docs specify board/status, as-of, source, final/interim basis, denominator semantics and category books. Raw GET, current-IPO category coverage, repeatability and cross-check accuracy remain untested here. | **PRIORITY CANDIDATE; not yet runtime-approved.** Confirm current licence, test direct GET and run the representative-IPO field/consistency checks before enabling it. |
| IPO Watch web pages | Public page displays GMP for open/recent IPOs. The reviewed 28 Oct page shows multiple Mainboard IPOs and values. [S24] | Its Terms of Use grant a personal, non-commercial access licence and restrict copying, reproduction, distribution, republication and downloading except where stated. [S24] | Useful as a user-opened secondary reference, but no permitted API route was established. GMP is unofficial and timestamps/definitions are publisher-specific. | **NO-GO as an automated adapter under the terms reviewed.** Keep as a manual reference unless permission or a published API licence says otherwise. |
| InvestorGain web pages | Homepage advertises a two-hour refresh interval and issue/GMP/subscription fields. [S25] | A Terms & Conditions page is linked, but its full terms were not successfully reviewed here; no explicit API use grant was verified. | Visible values can support manual comparison, but publisher-level update timing is not the same as each quote's observation time. | **NOT APPROVED** until exact terms, source attribution, historical coverage and an actual API/response are verified. |
| Groww / InvestKraft / IPO Premium public pages | Public subscription pages expose category-wise data; a sample BLS page from IPO Premium has category figures and a 28 Oct 20:58:12 update timestamp; an InvestKraft SFC page exposes categories and GMP snapshots with timestamps. [S22–S23] | No documented free category-subscription API plus explicit automated-reuse terms were verified for these page routes in this review. | Good manually inspected comparison/reference pages. Same-page views can differ by tab/source (for example, InvestKraft SFC has both consolidated and NSE-labelled tables) and must be mapped explicitly. | **MANUAL COMPARISON ONLY** unless a separate API and permitted-use terms are verified. |

### 17.3 Ten-IPO representative screening set

This is a **public-page/API-documentation screening**, not a claim that the JSON connectors passed live GET. The ten cases deliberately mix active/current issues, recently closed/listed issues, and older completed Mainboard IPOs.

| Mainboard IPO | Subscription evidence | GMP evidence | Feasibility finding |
|---|---|---|---|
| BLS Polymers (active; bidding 27–29 Oct 2026) | NSE's issue-information page confirms symbol, Mainboard issue period and issuer identity. gmptoday.in's 27 Oct subscription page explicitly said category-wise splits were not yet published by its relayed source. The ipos.markets API documentation claims coverage of all issues and specifies QIB/NII/RII category objects, but the raw endpoint has not been tested for this symbol. [S03, S21, S28] | gmptoday.in's current board listed a ₹46 median, ₹38–50 range and 12 trackers in its 28 Oct 19:29 IST snapshot; Xflot's current indexed homepage showed ₹51 without a comparable timestamp in the snippet. [S19, S20, S23] | **Strong current identity/GMP discovery; category-split coverage still needs live API verification.** GMP providers differ and timestamps are not aligned. |
| SFC Environmental Technologies (active; bidding 27–29 Oct) | gmptoday.in's 27 Oct 08:00 IST page explicitly said QIB/NII/retail split had not yet been published by the source it relays. ipos.markets is the documented subscription candidate; direct GET is pending. [S21, S27] | gmptoday.in's 28 Oct board displayed ₹16, range ₹13–20, with 12 trackers; Xflot's current indexed homepage showed ₹13. [S19, S20, S27] | **GMP coverage exists but provider values differ.** Need category subscription from a verified source; do not fill missing categories from overall subscription. |
| EAAA India Alternatives (closed 28 Oct; awaiting listing) | Public issue pages showed overall final subscription; its category-level API response was not directly fetched. The documented ipos.markets schema includes the relevant category fields, but this specific issue remains unverified at endpoint level. [S21, S29] | gmptoday.in's 28 Oct board displayed a median ₹15, range ₹9–25, and 11 trackers; Xflot/other third-party pages showed different values at different times. [S20, S23, S29] | **Useful timestamp, spread and contradiction test.** Capture a final-subscription status and separate every GMP source/time. |
| M.K. Sons Fine Jewels (active; bidding 28–30 Oct) | IPO-calendar/issue pages establish the Mainboard issue, but this screen did not verify a raw category-wise subscription response. Because the issue was still open, an absent snapshot must remain unavailable, not zero. [S27] | gmptoday.in displayed ₹10, range ₹8–13, 13 trackers, on its 28 Oct snapshot. [S20, S23] | **Current GMP candidate; category-wise live retrieval pending.** |
| Bombay Coated and Special Steels (upcoming; bidding 29 Oct–2 Nov) | The issue calendar shows a future/opening issue; a subscription value before bidding has started is not applicable/not yet published, not a zero-demand signal. [S27] | gmptoday.in displayed ₹9 with a range ₹8–9; the public board showed 12 trackers. [S20, S23] | **Pre-bidding test for applicability and null semantics.** |
| Jio Platforms (closed 23 Oct; awaiting listing) | NSE issue-information confirms the issue period and symbol; the final category-wise payload was not directly fetched. [S08, S21] | gmptoday.in displayed a ₹247 median and ₹232–250 range on its recent closed-issue board, with five trackers in the indexed snapshot. [S20, S30] | **Recent closed issue.** Need exact category data, final/interim state and source timestamps for an end-to-end pass. |
| Paras Healthcare (closed 23 Oct; awaiting listing) | NSE's public issue-information page shows category-wise subscription with an update timestamp of 21 Oct 2026, 12:00 IST—an interim snapshot during the bidding window, not a final close-of-issue result. [S31] | gmptoday.in displayed ₹13 with a range ₹8–13, six trackers, on its recent closed-issue board. [S20, S31] | **Explicit interim-versus-final temporal-integrity test.** The connector must retain the 21 Oct snapshot rather than relabel it final. |
| Zetwerk Manufacturing Businesses (listed 23 Oct) | Xflot's public page displayed QIB/NII/retail detail but conflicted with its headline overall subscription and issue-size/chronology fields. An NSE listing circular confirms that trading started 23 Oct. [S22, S24] | The inspected Xflot page reported no GMP for this issue. [S26] | **FAIL for unreviewed single-source ingestion.** Preserve source evidence and block/flag inconsistent fields; the API/page must not be treated as ground truth. |
| Data Patterns (India) (historical Mainboard IPO, listed Dec 2021) | ipos.markets' public historical issue page displays QIB/NII/RII final multiples, offer/issue terms and listing outcome. Its page labels a subscription table "as of 10 Oct 2026" despite the IPO having completed in 2021; that timestamp must be interpreted/validated rather than assumed to be the original bid-book timestamp. [S29] | A trustworthy, point-in-time pre-listing GMP series was not established in this screen. The gmptoday accuracy feed is an accuracy/backtest record, not necessarily a full historical GMP quote archive. [S20, S25] | **Historical subscription outcome coverage visible; historic GMP history not proven.** Exclude unsupported historical GMP from backtests. |
| Burger King India (historical Mainboard IPO, listed Dec 2020) | ipos.markets' public historical page displays category-wise final subscription and first-day listing outcome; its subscription table also labels the snapshot "as of 10 Oct 2026", which is not the IPO's actual issue-period date and should not be reused as the original market-information timestamp. [S30] | No complete timestamped pre-listing GMP series was established from the reviewed sources. [S20, S26] | **Second historical subscription outcome check.** Useful for testing category mapping and listing-outcome records, but not evidence of historical GMP availability. |

### 17.4 Preliminary sample-screen totals

- **10/10 issue identities** were discoverable through a public source/page route or exchange issue reference. This is identity/page discovery, not direct API coverage.
- **7 current or recently closed Mainboard IPOs** (BLS Polymers, SFC Environmental Technologies, EAAA India Alternatives, M.K. Sons Fine Jewels, Bombay Coated and Special Steels, Jio Platforms and Paras Healthcare) had a visible GMP quote/range or an explicitly recorded no-quote condition in the indexed/public publisher pages reviewed. Published quote timestamps differ; no cross-source same-time accuracy claim is made.
- **2 historical Mainboard IPOs** (Data Patterns and Burger King India) had publicly visible final category subscription and listing outcome information on ipos.markets pages. These page renderings do not prove that an original point-in-time timestamp or full historical GMP series is available.
- **At least 2 current-open issues** (BLS Polymers and SFC Environmental Technologies) had a secondary publisher explicitly state that it had not yet received category-wise splits as of its stated timestamp. This is why the app needs per-field source coverage and cannot assume all public pages contain QIB/NII/RII values.
- **At least 1 source page** (Zetwerk on Xflot) showed internal inconsistency across issue status, issue size and overall/category subscription fields. It is not safe to ingest a single normalized summary without reconciliation.
- **0 raw JSON endpoints passed a live GET in this screening environment.** The web research interface could retrieve API documentation and indexed source pages but refused direct raw JSON endpoint fetches; local execution also had no DNS/network access. This is a benchmark-execution limitation, not proof that each provider API is down.
- **No connector is yet production-approved.** Current conclusion: ipos.markets is the strongest documented category-wise subscription API candidate; gmptoday.in is an explicitly CC-BY-licensed but limited-sample GMP cross-check; Xflot is an explicitly documented free API whose per-issue data quality needs a strict fail-closed validation gate. The exact current terms and source-field accuracy must be checked again at implementation time.

### 17.5 Next required test to close the benchmark

Before approving a connector, execute the following against all ten named issues from the application developer environment or another network environment that can reach the documented URLs:

1. Call the provider's documented endpoint directly, record UTC start/end time, HTTP status, content type, response hash, latency, and parser result. Do not store secrets in the test log.
2. Resolve each issue by stable identifier/slug. Confirm the response is Mainboard-only, and record per-issue coverage rather than counting the directory endpoint as proof of every issue.
3. Validate exact required fields: QIB, NII (including any small/big NII definitions), retail, offered/reserved quantity where available, overall multiple, GMP value/range, source-count/dispute flag, issue identity, source attribution, observed/published/retrieved times and null semantics.
4. Compare a small set of API observations against the exchange's published page at the closest available information time, preserving differing timestamps. Do not fetch or scrape NSE automatically without written permission; use a permitted user-driven/manual reference capture for this comparison.
5. Repeat after the published cache/refresh interval and on a later sample. Fail or mark partial on stale data, missing issue IDs, schema changes, internal contradictions, missing timestamps where required, or silent fallback.
6. Confirm the exact provider terms and provenance/upstream data rights. Store a dated copy/link of the terms reviewed, the attribution wording and rate-limit/disclaimer requirements.
7. Only then mark the candidate connector passed. Until then, the orchestrator should report the candidate as unverified/unavailable and retain manual evidence entry.

### 17.6 Benchmark verdict

The screen has identified **a strong documented subscription API candidate (ipos.markets), an explicitly CC-BY-licensed but limited-sample GMP API (gmptoday.in), and a free documented combined-data API (Xflot) whose output requires strict reconciliation**. It has **not** established an approved, end-to-end production pipeline because raw GET tests, per-issue live coverage, repeatability and response-level consistency checks remain incomplete. The next gate is direct endpoint testing from a network-enabled development environment; direct automated collection from NSE pages remains prohibited by its published terms absent permission.



- **[S18] NSE — Terms of Use.** Prohibits systematic or automated data collection, including scraping, mining and extraction, on or in relation to the website/mobile application. [Open source](https://www.nseindia.com/static/nse-terms-of-use)
- **[S19] Xflot — Free IPO & Market Data API documentation.** Documents public JSON endpoints, board/status and IPO/GMP/subscription fields; requires attribution, polling at most once per minute, and retention of the disclaimer. The page itself says API documentation updated 25 Sep 2026; this is not a verified live response timestamp. [Open source](https://www.xflot.com/api-docs)
- **[S20] gmptoday.in — IPO GMP API documentation and live board.** Documents /api/gmp.json, a three-issue sample under CC BY 4.0 with attribution, median/range/source counts and timestamp fields; live board indexed with data timestamp 28 Oct 2026, 19:29 IST. [API docs](https://gmptoday.in/api/) · [Live board](https://gmptoday.in/)
- **[S21] ipos.markets — IPO subscription API documentation.** Advertises keyless JSON/CSV endpoints for category-wise current/final QIB/NII/RII subscription, board/status, as-of/final/basis fields and a five-minute cache; states MIT-licensed curation and asks for attribution. Direct endpoint tests remain pending. [Open source](https://ipos.markets/api-docs)
- **[S22] Xflot — Zetwerk Manufacturing Businesses issue page.** The inspected indexed page was used as a consistency-failure example. [Open source](https://www.xflot.com/ipo/zetwerkmanufacturingbusinesses)
- **[S23] Xflot — IPO homepage.** Indexed current page with Mainboard calendar and GMP values for open/current issues; per-field observation timestamps require endpoint validation. [Open source](https://xflot.com/)
- **[S24] NSE — Listing of Equity Shares of Zetwerk Manufacturing Businesses Limited.** Exchange circular states trading commenced 23 Oct 2026. [Open source](https://noticeblue.com/circulars/5d0a64fe-34d9-475c-b8ad-a9f133643129)
- **[S25] ipos.markets — Data Patterns (India) Limited IPO page.** Public historical issue page with category-wise subscription, offer terms and listing-day outcome; its displayed subscription table timestamp requires interpretation before point-in-time use. [Open source](https://ipos.markets/ipo/data-patterns-india-limited)
- **[S26] ipos.markets — Burger King India Limited IPO page.** Public historical issue page with category-wise subscription and listing-day outcome; its displayed subscription table timestamp requires interpretation before point-in-time use. [Open source](https://ipos.markets/ipo/burger-king-india-limited)
- **[S27] gmptoday.in — SFC Environmental Technologies subscription page.** States category splits were not available at its 27 Oct 2026 08:00 IST snapshot. [Open source](https://gmptoday.in/ipo/sfc-environmental-technologies/subscription/)
- **[S28] gmptoday.in — BLS Polymers subscription page.** States category splits were not available at its 27 Oct 2026 08:00 IST snapshot. [Open source](https://gmptoday.in/ipo/bls-polymers/subscription/)
- **[S29] gmptoday.in — EAAA India Alternatives live GMP board/page.** Current indexed listing with median/range/tracker count at the stated observation time. [Open source](https://gmptoday.in/ipo/eaaa-india-alternatives/)
- **[S30] gmptoday.in — Jio Platforms live GMP board/page.** Current indexed listing with median/range/tracker count at the stated observation time. [Open source](https://gmptoday.in/ipo/jio-platforms/)
- **[S31] NSE — Paras Healthcare issue-information page.** Public category-wise subscription snapshot updated 21 Oct 2026, 12:00 PM IST; this was during the 21–23 Oct bidding period and is interim. [Open source](https://www.nseindia.com/market-data/issue-information?series=EQ&symbol=PARASHLTH&type=Active)
- **[S32] Xflot — Free IPO & Market Data API documentation, terms section.** API use conditions are part of the publisher's documentation. [Open source](https://www.xflot.com/api-docs)

## 18. Final recommendation

Proceed with the **core signal-acquisition workflow and source-neutral evidence architecture**, while preserving the local/manual fallback and ₹0 constraint. Do not purchase market data, use prohibited scraping, or promise a provider's coverage before testing it. The next engineering work must benchmark candidate sources against representative Mainboard IPOs, then build the acquisition orchestrator to record per-source attempts, returned fields, timestamps, partial coverage and failures. Connectors that pass the access/terms/data-quality gate can be enabled; unresolved critical free/permitted source gaps must be presented for an explicit product-owner decision before release.

The product's competitive value is the combination of trustworthy source acquisition, traceable evidence and interconnected reasoning—not the number of APIs it connects to.
