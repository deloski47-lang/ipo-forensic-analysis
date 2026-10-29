---
title: IPO Forensic Analysis Engine — Data Source & Feasibility Audit
document_id: DSA-IPO-001
version: 1.0
status: Dated source/API screening completed; historical smoke-test evidence supports IPOS Markets, GMP Today and Xflot candidates, but no production connector is fully approved
last_updated: 29 October 2026
product_scope: Indian Mainboard IPOs only; local-first, single-user, manual-first, ₹0 budget MVP
canonical_source: Markdown
---

# IPO Forensic Analysis Engine
## Data Source & Feasibility Audit

**Document ID:** DSA-IPO-001  
**Version:** 1.0  
**Status:** Dated source/API screening performed — historical smoke-test evidence covers IPOS Markets, GMP Today and Xflot; broader coverage, repeatability and connector approval remain open
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
| Current subscription snapshots by category (QIB/NII/retail) | High for public-page visibility; lower for normalized, time-matched consistency | Historical IPOS Markets smoke-test evidence recorded HTTP 200 JSON, 9/10 target matches, and QIB/NII/RII plus `as_of` on all nine matched details; coverage, repeatability, timestamp semantics, accuracy and upstream rights remain unproven. Direct NSE scraping is prohibited absent written permission. | P0: IPOS Markets is the priority subscription candidate, subject to a current-version rerun and terms/provenance, freshness, accuracy and representative-coverage review. Until then use manual/user-driven capture for exchange pages. |
| Historical listing-day prices | Medium for manually sourced records; history/access terms require testing | Low/medium for free, unrestricted bulk backfill | Do not promise a complete backtest dataset |
| GMP | Non-official observation from named secondary publishers, not an exchange fact | Historical smoke-test evidence: GMP Today returned HTTP 200 JSON in about 489 ms, with 3 records from 18 tracked and CC-BY-4.0 attribution metadata; each returned record had `updated_at: null`. Xflot BLS Polymers detail returned valid JSON in about 705.2 ms with one GMP source and 11 GMP-history entries. Public-page quotes differ and timestamps are not aligned. | Keep GMP Today as a licensed limited-sample GMP candidate and Xflot as a quality-gated issue/GMP-detail candidate; neither is production-approved until coverage, timestamp semantics, rights and accuracy tests pass. Manual capture remains fallback. |
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

NSE's issue-information pages visibly publish category-wise offered/reserved quantities, bid counts, subscription multiples and update timestamps for specific issues. But the published NSE Terms of Use explicitly prohibit systematic or automated collection (including scraping and extraction) [S18]. Treat direct NSE pages as primary manual verification sources unless written permission is obtained. BSE/SEBI issue pages are useful source-discovery paths, but this screening did not verify a documented, no-cost, permitted first-party API for the required subscription fields. Do not infer that a page or underlying browser request is a licensed API. [S03–S04, S11, S18]

NSE's Data Sharing & Usage Policy describes agreements that specify permitted use and restrictions, including restrictions on redistribution. NSE's data-vending pages separately list EOD/historical products and tariffs; the official EOD/historical page describes downloadable product formats and directs interested parties to contact NSE Data for subscription. BSE's information-products tariff sheet also lists EOD, historical and corporate data offerings. [S06–S09]

**Implementation implication:** start with manual snapshots and official files where available. For any automation, separately verify the precise page/data product, access method, permitted local/personal use, storage/retention, costs, update cadence, rate limits, historical backfill and whether redistribution/export is allowed. Do not treat HTML page calls, undocumented JSON endpoints or a scraper that currently works as a supported integration contract.

**Critical distinction:** an end-of-day bar (open/high/low/close) cannot automatically substantiate every possible listing-day exit. If a later backtest models selling at listing/opening, define whether the outcome means official opening price, first trade, first executable quote, a time-bounded window or day close—and obtain a data source that actually contains that observation.

### 5.3 MCA — useful fallback, but not assumed free/bulk

The Ministry of Corporate Affairs' online help states that public company documents can include incorporation documents, annual returns and balance sheets, and that viewing public documents is fee-based and available through a logged-in workflow. [S05]

**Implementation implication:** use MCA as a fallback for a specific missing filing only after reviewing the required access/fee and comparing the value with an official offer document or issuer release. Do not base the MVP on automated bulk collection from MCA. The project should record when a source was accessed and preserve the document received.

### 5.4 Subscription — only useful with time and category context

Subscription totals are time-sensitive: a 12:00 PM snapshot is not the close-of-issue result. Store investor category, shares offered/reserved, bids or subscription multiple as published, timestamp/time zone if known, source and whether the issue was still open. Never replace the prior snapshot with a later number; retain each observation.

**Open limitation:** public visibility and visible timestamps are verified, but neither complete historical category coverage nor a permitted first-party automated exchange feed is established here. The free API documented by ipos.markets advertises category-wise subscription but its upstream rights/provenance and terms were not established in this review [S17]. Xflot's BLS Polymers single-issue endpoint passed one direct GET smoke test, but returned an empty `subs` list and `lastSubX: null`; it did not provide QIB/NII/RII rows in that sample. Its indexed page-level data also show internal consistency problems on the Zetwerk sample [S15]. Do not use Xflot for subscription data; keep ipos.markets as the unapproved category-subscription candidate pending direct response testing.

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
2. **Source screening benchmark completed (29 October 2026); close the live endpoint gate next.** The dated 10-IPO screening is recorded in Section 17. Next, run direct GET and repeatability tests for the documented candidates from a network-enabled development environment, verify each field/issue response and confirm current access/attribution terms. Do not repeat the page-level screen as if it were a successful API test.
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

This is an initial desk-based audit of official web pages and selected secondary methodology pages as reviewed on 29 October 2026, supplemented by historical JSON smoke-test reports. Those reports record successful point-in-time GETs but do not establish accuracy, repeatability, all-10-issue coverage, timestamp semantics or historical point-in-time validity. This audit did not conduct contractual/legal review, request data-provider quotes, measure large-scale extraction accuracy, exhaustively download historical exchange files, or verify every Indian Mainboard IPO. SME IPOs are outside this audit's scope. Web pages and tariffs can change. Accordingly, any untested point is marked unknown or conditional, not presented as a fact.

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

This is a dated source-screening benchmark for current, recently closed and historical Indian Mainboard IPOs. It combines public-page/documentation review with two uploaded historical smoke-test reports: `source-feasibility-run.json` and `xflot-detail-run.json`.

**Important interpretation:** both reports declare `script_version: 0.1`, while the current committed runner is version 0.2. They are therefore historical smoke-test evidence—not a claim of a reproducible current-script run. Preserve the reports' capture timestamps and response hashes in the test record where needed (including the Xflot detail SHA-256 below), and rerun the committed 0.2 script before using the results as a repeatability claim.

A successful GET establishes only that a particular endpoint responded with parseable JSON at that recorded time. It does **not** establish response accuracy, repeatability, complete 10-issue coverage, field/timestamp semantics, historical point-in-time validity, or upstream rights/terms approval. No connector is production-approved.

The benchmark distinguishes:

- **Historical smoke-test evidence:** a dated GET result recorded by the supplied report.
- **Candidate connector:** a route with relevant documented/public fields, still subject to validation.
- **Production-approved connector:** not achieved by any candidate. Approval requires a current-version repeat test, representative coverage, field/identity validation, timestamp semantics, accuracy comparison, and terms/provenance review.

Do not automate NSE page collection without written permission. Preserve Mainboard-only scope, the ₹0 constraint, deterministic calculations and complete manual/offline fallback.

### 17.2 Historical smoke-test results

| Candidate route | Historical result | What it supports | Decision as of 29 Oct 2026 |
|---|---|---|---|
| IPOS Markets subscription API | Index returned **HTTP 200 JSON**. Of 10 target issues, **9 matched**; all 9 matched detail records included **QIB, NII and RII** values and **`as_of`** timestamps. **Bombay Coated and Special Steels** was unmatched. | Strongest current evidence for a Mainboard subscription candidate with category fields and per-record timestamps. | **PRIORITY SUBSCRIPTION CANDIDATE; not production-approved.** The single unmatched target, all-10 coverage, meaning/freshness of `as_of`, accuracy, repeatability and upstream rights remain open. |
| GMP Today JSON API | Returned **HTTP 200 JSON** in about **489 ms**. It returned **3 records from 18 tracked** and exposed **CC-BY-4.0 attribution metadata**. Each returned record had **`updated_at: null`**. | Licensed, limited-sample GMP route; the licence/attribution must be retained. | **LIMITED-SAMPLE GMP CANDIDATE; not production-approved.** It cannot be the sole/full GMP connector. Null per-record update times mean freshness and observation semantics are unresolved. |
| Xflot IPO directory | Returned **HTTP 200 JSON** with **182 IPOs**, including **110 Mainboard** IPOs. | Directory discovery/identity candidate; directory presence is not proof that every target detail route or required field is available. | **CONDITIONAL ISSUE/GMP CANDIDATE; not a subscription source on current evidence.** Keep the publisher’s attribution/disclaimer and enforce at least a **65-second polling guard**. |
| Xflot BLS Polymers detail | Returned **HTTP 200 JSON** in about **705.2 ms**. It described a **Mainboard**, **OPEN** issue with price band **₹142–150**, **lastGmp ₹51**, **gmpSources 1** and **11 GMP-history entries**. Its subscription evidence was absent: **`lastSubX: null`** and empty **`subs`/`subscription_rows`**. The earlier recorded response was 2,173 bytes, captured 03:40:05–03:40:06 UTC on 29 Oct 2026, SHA-256 `1cf3f96744ede49540c7d4f9f80a0343af7d15896859e4e58f42d0cd7e7c6617`. | A point-in-time issue/GMP detail response, not category-subscription coverage. One GMP source also does not establish consensus quality. | **CONDITIONAL ISSUE/GMP-DETAIL CANDIDATE; not a subscription source.** Validate terms, field definitions/times, cross-source consistency and representative coverage before any approval. |

The results correct the earlier characterization that only Xflot had a live endpoint smoke test: the supplied historical reports also record successful IPOS Markets and GMP Today GETs. They do not alter the no-approval conclusion.

### 17.3 Representative ten-IPO coverage interpretation

The representative set remains useful for testing identity, null/applicability, interim/final status and point-in-time handling. The historical IPOS Markets run matched 9/10 targets and did **not** match Bombay Coated and Special Steels. That is not evidence that the issue has zero subscription or is invalid; it is a coverage/matching gap to preserve explicitly.

For all nine matched IPOS Markets details, QIB/NII/RII and `as_of` were present. This is encouraging field-availability evidence, not confirmation that values are correct, current, final, temporally compatible with other sources, or valid for a historical as-of replay. Do not replace an unknown/missing field with zero, and do not infer historical availability from a later `as_of` display.

The Xflot BLS sample confirms the opposite distinction: a detail endpoint can be healthy and carry issue/GMP fields while returning no category-subscription rows. Therefore Xflot must not supply QIB/NII/RII data unless future, independently validated evidence changes that conclusion.

### 17.4 Controls and remaining gates

Before a connector can be approved:

1. Rerun the committed **0.2** smoke-test script and retain the UTC capture times, HTTP status/content type, latency, response hash and parser result. Compare with the historical 0.1 reports; do not call them current-script proof.
2. Resolve each of the ten named Mainboard issues by stable identity and record per-issue success, failure, ambiguity and null/applicability states. A directory count does not prove all-detail coverage.
3. Validate exact fields and semantics: QIB/NII/RII definitions and status; `as_of` versus publication/observation/retrieval time; GMP units/value/range/source count; `updated_at: null`; and interim versus final data.
4. Compare a small set of observations with permitted user-driven/manual exchange references at the closest available time. Do **not** scrape NSE absent written permission.
5. Repeat after documented cache/refresh intervals and on a later sample. Treat schema changes, missing IDs, stale/untimed data, contradictions and silent fallbacks as fail/partial outcomes.
6. Review current provider terms, attribution, disclaimer, rate limits, storage/retention, intended use and upstream provenance. For Xflot, retain attribution/disclaimer and keep at least 65 seconds between polls.
7. Keep manual entry/import and local deterministic analysis fully functional. No source failure may fabricate a zero or a successful refresh.

### 17.5 Benchmark verdict

**No connector is production-approved.** IPOS Markets is the **priority subscription candidate** based on HTTP 200 JSON, nine matched representative details, and QIB/NII/RII plus `as_of` field presence; its unmatched Bombay Coated and Special Steels case and all remaining validation gates are material. GMP Today is a **limited-sample GMP candidate** based on its successful, attributed CC-BY-4.0 response, but 3/18 coverage and null per-record `updated_at` prevent it from being a full/freshness-qualified feed. Xflot is a **conditional issue/GMP-detail candidate**, with a healthy directory and BLS detail response, but current evidence makes it **not a subscription source**.

The product should proceed with the source-neutral acquisition workflow only for reviewed candidates, while maintaining Mainboard-only scope, ₹0 constraints, deterministic calculation, attribution/disclaimers, polling limits and complete manual fallback. The test run alone establishes none of accuracy, repeatability, all-ten coverage, timestamp semantics/historical point-in-time validity, or upstream rights/terms approval.


## 18. Final recommendation

Proceed with the **core signal-acquisition workflow and source-neutral evidence architecture**, while preserving the local/manual fallback and ₹0 constraint. Section 17 records historical smoke-test evidence for IPOS Markets, GMP Today and Xflot, but the reports are version 0.1 while the committed runner is 0.2; rerun the current script before claiming repeatability. Prioritise IPOS Markets for category subscription validation; treat GMP Today as a licensed limited-sample GMP candidate; and use Xflot only as a conditional issue/GMP-detail candidate with attribution/disclaimer and a 65-second polling guard—never as a subscription source on current evidence. No connector is production-approved until representative coverage, timestamp semantics, source rights/attribution, accuracy and repeatability checks pass. Do not purchase market data or automate prohibited NSE-page scraping. If a critical category still has no free/permitted route after the direct tests, present the evidence and trade-off for an explicit product-owner decision before release.

The product's competitive value is the combination of trustworthy source acquisition, traceable evidence and interconnected reasoning—not the number of APIs it connects to.
