---
document: IPO Forensic Analysis Engine — Indicator Catalogue and Data Dictionary
version: 1.0
status: Planning reference; formulas and sources require verification before implementation
source: IPO_Indicator_Catalogue_and_Data_Dictionary.docx
converted_on: 2026-10-29
---

# IPO Forensic Analysis Engine

## Indicator Catalogue & Data Dictionary

**Purpose:** Define the indicators, source requirements, calculation rules, caveats, cross-checks and report outputs for the Indian IPO forensic analysis engine.

**Critical rule:** AI must not invent missing values, fabricate citations, silently fill data gaps, or perform financial arithmetic without independent validation. Calculations belong in deterministic, tested code.

---

IPO INDICATOR  
CATALOGUE & DATA DICTIONARY

Specification for an evidence-grounded listing-day IPO research engine

Companion document to the IPO Forensic Analysis Engine — Project Scope, Core Vision & Technical Brief.

Purpose: define the indicators, source requirements, calculation conventions, cross-checks and output fields so another AI or developer can implement the project without losing essential context.


| CORE SAFEGUARD<br>AI must not invent missing numbers, fabricate sources, silently impute data, or perform financial arithmetic without independent validation. Calculations belong in deterministic, tested code. AI may interpret evidence and propose hypotheses only when clearly labelled and traceable. |
| --- |

Status: Version 1.0 — detailed working specification. Indicators are conditional: use only when relevant, disclosed, comparable and sufficiently supported.


# 1. How to Use This Document


- Treat this catalogue as the implementation specification, not a claim that every field is available for every IPO.

- Use the indicator ID as a stable identifier in code, test cases, reports and stored records.

- Every indicator needs: definition, source, as-of time, applicability, calculation method, limitations, dependencies and report placement.

- Separate observed facts, normalized facts, calculated metrics, model outputs and analyst hypotheses.

- An unavailable indicator is UNKNOWN or NOT_APPLICABLE—not zero and not automatically neutral.

- Do not create a single overall score by blindly adding all indicators. Correlated indicators can double-count the same underlying risk.

- Use company/sector-specific modules in addition to common modules; financial services, manufacturing, software, EPC and healthcare require different checks.


# 2. Indicator Record Contract


Each stored indicator observation should follow this logical record. A database schema can split the fields into normalized tables, but must preserve the semantics.


| Field | Type | Meaning | Rule |
| --- | --- | --- | --- |
| indicator_id | string | Stable ID, e.g. FIN_OCF_PAT | Required |
| issuer_id / issue_id | string | Canonical company and specific IPO issue identifiers | Required |
| indicator_name | string | Human-readable label | Required |
| value_raw | string/number/null | Original value exactly as sourced; preserve original units | Required where observed |
| value_normalized | number/string/null | Normalized value after documented conversion | Conditional |
| unit | string | INR, INR crore, %, days, shares, index points, category, etc. | Required where applicable |
| period_start / period_end | date/null | Period the observation describes, not when retrieved | Required for period metrics |
| event_time | datetime/null | When the event happened, if different from publication | When applicable |
| published_at | datetime/null | Source publication time | When available |
| retrieved_at | datetime UTC | When system acquired the source | Required for imported data |
| source_id | string | Foreign key to source/provenance record | Required |
| source_locator | string/null | URL, document page, section, table, row, paragraph or API field | Required for material facts |
| extraction_method | enum | manual, parsed_table, OCR, API, structured_feed, calculated | Required |
| validation_status | enum | verified, cross_checked, unverified, conflicting, stale, failed | Required |
| applicability | enum | applicable, not_applicable, unknown | Required |
| confidence | enum | high, medium, low; rationale stored separately | Required for interpreted/extracted facts |
| formula_version | string/null | Version of deterministic formula, if calculated | For derived metrics |
| information_cutoff | datetime | Latest time of information allowed into a particular report/backtest | Required per report |
| notes / limitations | string | Caveats, definition differences, assumptions and unresolved issues | As needed |


# 3. Source Registry and Evidence Provenance



| Field | Definition |
| --- | --- |
| source_id | Stable internal ID |
| source_type | official_exchange, regulator, issuer_filing, audited_report, official_company, news_provider, media_outlet, unofficial_gmp, market_data, search_attention, user_upload, analyst_note |
| publisher / author | Who published it; distinguish original publisher from syndicator |
| title | Exact source/document/headline title |
| url_or_file_path | Exact URL or local file reference |
| document_version | DRHP/RHP/final prospectus/addendum/version date |
| published_at / event_time / retrieved_at | Separate timestamps; never collapse them |
| page/table/section | Precise locator for PDF or document claims |
| source_quality | primary, reputable_secondary, unofficial, user_supplied, unknown |
| access_method | manual, documented_API, permitted_scrape, upload, other |
| license_or_terms_note | Any access/usage constraints identified |
| content_hash | Optional checksum to identify changed files |
| verification_notes | What was checked, cross-source agreement, unresolved conflicts |


| SOURCE HIERARCHY<br>Prefer SEBI/exchange filings, RHP/DRHP, audited financial statements and official company disclosures for company facts. Use reputable news to discover and contextualize events. Treat GMP as unofficial. Treat social posts and unsourced claims as leads, not facts. |
| --- |


# 4. Status, Missingness and Confidence Rules



| Status | Meaning | Required behavior |
| --- | --- | --- |
| VERIFIED | Primary source checked or value reconciled to source table | May be used with citation and cutoff. |
| CROSS_CHECKED | Two or more credible sources agree, or total reconciles | Record sources and reconciliation. |
| UNVERIFIED | Source/extraction has not been checked sufficiently | Label prominently; reduce confidence. |
| CONFLICTING | Credible sources disagree materially | Keep all values, explain conflict, do not silently pick one. |
| STALE | Value is too old for the decision context | Show timestamp; exclude or down-weight per explicit freshness rule. |
| MISSING | Expected data not found | Leave null; state effect on analysis. |
| NOT_APPLICABLE | Metric does not make sense for this issuer | Explain why; do not penalize. |
| FAILED | Retrieval or extraction failed | Show failure and offer manual upload/correction. |

Confidence is not a decorative percentage. Store a reason: source authority, extraction reliability, recency, cross-source agreement, coverage and relevance. Do not report numerical predictive probabilities until the model is calibrated on representative out-of-sample data.


# 5. Catalogue at a Glance



| Module | Area | IDs | Main sources | Purpose |
| --- | --- | --- | --- | --- |
| ISS | Issue structure and mechanics | ISS-01 to ISS-12 | RHP/DRHP, exchange | Capital structure, proceeds, OFS, dilution and selling supply |
| FIN | Financial performance and earnings quality | FIN-01 to FIN-22 | Restated financials, auditor reports | Growth, margins, cash conversion, working capital, one-offs |
| CON | Concentration and business dependencies | CON-01 to CON-12 | Offer documents, financial notes | Customer/supplier/product/geographic concentration |
| GOV | Governance, promoters and related parties | GOV-01 to GOV-14 | RHP, regulator/court filings | Ownership, related parties, litigation, auditor issues |
| VAL | Valuation and peer comparison | VAL-01 to VAL-12 | Issue price, financials, peer data | IPO valuation, peer quality, premium and downside sensitivity |
| DEM | Demand, subscription and market structure | DEM-01 to DEM-14 | Exchange/registrar/market data | Category demand, timing, float, supply and market regime |
| GMP | Grey-market premium observations | GMP-01 to GMP-06 | Unofficial sources | Freshness, source reliability, trend and disagreement |
| NEWS | News and event evidence | NEWS-01 to NEWS-12 | News API/provider, official announcements | Catalysts, negative events, credibility, novelty and confirmation |
| ATT | Search/investor attention | ATT-01 to ATT-06 | Google Trends if accessible or permitted alternative | Attention spike, baseline, ambiguity and relationship to demand |
| PEER | Comparable IPO and listing history | PEER-01 to PEER-10 | Exchange historical data, verified datasets | Similar issue outcomes, regime-aware base rates |
| RISK | Scenario, liquidity and net-return model | RISK-01 to RISK-12 | Derived from verified data | Listing-price scenarios, net return, downside and uncertainty |
| XCHK | Cross-indicator synchronization | XCHK-01 to XCHK-18 | Derived from multiple modules | Contradictions, causal hypotheses, concentration and interaction effects |
| DATA | Data coverage and model integrity | DATA-01 to DATA-10 | All source and processing logs | Completeness, freshness, citation coverage and look-ahead prevention |


# 6. Detailed Indicator Catalogue


The following catalogue is the planned first implementation set. “Formula” describes a calculation or test, not an automatic verdict. Thresholds should be sector-aware and calibrated; do not hard-code universal danger cutoffs without justification.


## 6.1 Issue Structure and Mechanics (ISS)



| ID | Indicator | Definition / required data | Primary source | Calculation / test | Why it matters | Cautions / red flags | Report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ISS-01 | Issue type | Fresh issue, OFS, or mixed | RHP/DRHP | Categorical classification; reconcile issue tables | Fresh issue funds the company; OFS proceeds go to selling shareholders | Misreading OFS as company fundraising | Issue summary |
| ISS-02 | Fresh issue / OFS split | Amount and % of total issue for each component | RHP / final prospectus | Component amount ÷ total issue size | Clarifies capital raised by company versus holders | Large OFS alone does not prove poor quality; inspect seller context | Issue summary |
| ISS-03 | Use of proceeds | Amounts/percent by stated use | RHP/DRHP | Reconcile stated allocation to fresh issue amount | Debt repayment, capex, acquisitions, working capital, general purposes | Vague use, large general-purpose allocation, mismatch with stated need | Offer structure |
| ISS-04 | Post-issue share count / market cap | Fully diluted post-issue shares and price-band market cap | Offer document, issue price | Post-issue shares × price; validate share basis | Core denominator for valuation and dilution | Wrong share count can distort all multiples | Valuation |
| ISS-05 | Dilution | Ownership change caused by issue | Shareholding tables | Compare pre/post holdings on compatible bases | Shows change in ownership/control | Check ESOPs, convertibles and fully diluted basis where disclosed | Ownership |
| ISS-06 | Promoter/early-holder selling | Shares and % offered for sale; seller identity | OFS/ownership tables | OFS shares ÷ pre-issue holding or total offered shares, clearly labelled | Incentives and supply context | Interpret with seller history, lock-in and remaining stake | Supply risk |
| ISS-07 | Lock-in expiry calendar | Date and quantity becoming eligible for sale | Applicable rules, offer document, exchange filings | Map lock-in schedule; verify applicable regulation | Potential future supply overhang | Eligibility to sell does not mean actual selling | Post-listing risk |
| ISS-08 | Pre-IPO transactions | Recent transfers, price, parties and dates where disclosed | RHP, share capital history | Timeline and price comparison; account for splits/bonuses | Detect unusual timing or large price gaps | Different rights/terms and illiquidity may explain price differences | Governance/valuation |
| ISS-09 | Debt repayment vs debt profile | Proceeds earmarked for debt versus total debt and maturity | RHP, financial statements | Compare proceeds with borrowings and maturities | Tests capital allocation and leverage effect | Does repayment solve risk or merely refinance it? | Balance sheet |
| ISS-10 | Issue size / free float estimate | Shares likely available for trading at listing, with assumptions | Issue terms, shareholding and lock-in rules | Document explicit free-float assumptions; avoid treating all shares as tradeable | Supply/demand context | Float estimates can be wrong if restrictions or categories misunderstood | Listing setup |
| ISS-11 | Price band and lot economics | Price range, lot shares, minimum application amount | Official issue terms | Upper price × lot size; validate application rules | Capital tied up and affordability | Do not confuse application amount with expected loss | Decision summary |
| ISS-12 | Offer-document version changes | Differences between DRHP, RHP, addenda and final filing | All versions available | Diff key sections/tables and dates | Can reveal changed terms, risks or financials | Version coverage may be incomplete | Evidence/changes |


## 6.2 Financial Performance and Earnings Quality (FIN)



| ID | Indicator | Definition / required data | Primary source | Calculation / test | Why it matters | Cautions / red flags | Report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FIN-01 | Revenue growth | Year-on-year and CAGR over disclosed periods | Restated financials | (Current/prior)-1; CAGR only across compatible periods | Growth context | Check acquisitions, discontinued operations, seasonality and period length | Financial trends |
| FIN-02 | Gross margin | Revenue less cost of goods/services, under consistent definitions | Financial statements | Gross profit ÷ revenue where meaningful | Pricing, input cost and mix signal | Definitions vary by sector and issuer | Margins |
| FIN-03 | Operating / EBITDA margin | Operating profit or EBITDA relative to revenue | Statements and reconciliation | Use disclosed/reconciled EBITDA definition; EBITDA ÷ revenue | Operating performance | EBITDA is not cash flow; inspect exclusions and capitalization | Margins |
| FIN-04 | PAT margin and growth | Profit after tax and margin trend | Restated statements | PAT ÷ revenue; period growth | Reported bottom-line performance | Check one-offs, tax, minority interests and other income | Earnings quality |
| FIN-05 | Other income dependency | Share of PBT/PAT supported by other income | Financial statements/notes | Other income ÷ PBT or relevant base; define denominator | Separates core operations from non-operating income | Other income may be recurring for some business models; inspect composition | Earnings quality |
| FIN-06 | Exceptional/non-recurring items | Material one-time gains/losses | Notes/auditor statements | Normalize only with disclosed line items; show reported and adjusted figures separately | Tests earnings sustainability | Never adjust without showing formula and rationale | Earnings quality |
| FIN-07 | Operating cash flow (OCF) | Cash generated by operating activities | Cash flow statement | Reported OCF; trend by period | Cash support for earnings | Check working-capital and one-off cash effects | Cash conversion |
| FIN-08 | OCF/PAT conversion | Operating cash flow relative to PAT | Cash flow and income statement | OCF ÷ PAT only when denominator is meaningful; show periods | Earnings-to-cash consistency | Negative/near-zero PAT makes ratio unstable; explain rather than force interpretation | Cross-check |
| FIN-09 | Free cash flow (FCF) | Operating cash flow less capex | Cash flow statement/capex notes | OCF − capital expenditure, with explicit capex definition | Internal funding capacity | Growth capex can depress FCF legitimately; not universal quality test | Cash flow |
| FIN-10 | Receivables growth vs sales | Trade receivables growth compared with revenue growth | Balance sheet/notes | Compare same period-end basis; calculate debtor days if inputs allow | Collection risk and potential revenue-quality issue | Acquisitions, seasonality and contract terms may explain gaps | XCHK |
| FIN-11 | Receivable days | Average trade receivables ÷ revenue × days | Statements/notes | Use average balances if available; disclose 365/period basis | Collection efficiency | Revenue including GST/tax and contract assets can affect comparability | Working capital |
| FIN-12 | Inventory growth / days | Inventory change and inventory days | Statements/notes | Average inventory ÷ cost of sales × days, when meaningful | Obsolescence, demand and working-capital risk | Not applicable to many asset-light/service businesses | Working capital |
| FIN-13 | Payable days and supplier financing | Trade payables relative to purchases/cost base | Statements/notes | Average payables ÷ eligible purchases × days | May explain OCF despite weak collection | Longer payable days may reflect bargaining power or stress | Working capital |
| FIN-14 | Working-capital cycle | Receivable days + inventory days − payable days | Derived from FIN-11 to FIN-13 | Only if component definitions/periods are comparable | Cash tied up in operations | Use sector-aware interpretation | Working capital |
| FIN-15 | Leverage | Debt, net debt, debt/equity, net debt/EBITDA where meaningful | Statements/notes | Define debt and cash components explicitly | Balance-sheet risk | Financial firms require different measures; EBITDA may be negative | Balance sheet |
| FIN-16 | Interest coverage | EBIT/interest expense or other defined coverage | Statements | Use consistent EBIT and interest definitions | Ability to service debt | Low/negative EBIT or capitalized interest complicates ratio | Balance sheet |
| FIN-17 | ROE / ROCE / ROA | Returns on equity, capital employed and assets | Statements | Define average vs closing balances and capital employed | Capital efficiency | IPO proceeds and restructuring can distort historical denominators | Returns |
| FIN-18 | Tax-rate anomalies | Effective tax rate trend and unusual credits/charges | Statements/notes | Tax expense ÷ pre-tax profit where meaningful | Tests whether earnings growth relies on tax effects | Loss years, deferred tax and incentives need context | Earnings quality |
| FIN-19 | Contingent liabilities/provisions | Disclosed obligations relative to scale | Notes/auditor report | Quantify where possible; distinguish contingent from recognized liabilities | Potential future cash/legal risk | Not every contingent liability crystallizes | Risk |
| FIN-20 | Auditor qualifications/emphasis | Qualified opinions, emphasis of matter, key audit matters | Audit reports | Extract exact wording and page; human verification for material findings | Potential reliability/estimation issues | KAM is not automatically a qualification or evidence of wrongdoing | Governance |
| FIN-21 | Capitalized costs / accounting changes | Changes that affect expense recognition or reported margins | Notes/auditor reports | Compare disclosed policy and amounts over time | Detect apparent improvement due to accounting treatment | Requires accounting expertise and source context | Earnings quality |
| FIN-22 | Related-party balances in financials | Receivables, loans, sales, purchases, guarantees to related parties | Notes/RHP | Quantify values and compare to revenue/assets/equity where useful | Potential conflict or concentration channel | Related-party status and arm's-length nature require evidence | Governance/XCHK |


## 6.3 Concentration and Business Dependencies (CON)



| ID | Indicator | Definition / required data | Primary source | Calculation / test | Why it matters | Cautions / red flags | Report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CON-01 | Top-customer concentration | Revenue share of largest customers | RHP/customer concentration disclosures | Use disclosed percentages and period; sum top-N only if data support it | Customer dependency | Do not infer identities if not disclosed | Business risk |
| CON-02 | Top-supplier concentration | Purchases or input dependence on largest suppliers | RHP/notes | Use disclosed share and period | Single-source exposure | Supplier disclosure may be incomplete | Supply risk |
| CON-03 | Single-source critical input | Critical material/component with few/no substitutes | RHP, sector evidence, disclosed contracts | Qualitative rating with cited evidence; quantify where possible | Production continuity risk | Must distinguish verified sole-source from analyst hypothesis | Supply risk |
| CON-04 | Product concentration | Revenue share by product/service line | Segment disclosures | Top product share and change over time | Dependence on product cycle | Segment definitions may change | Business risk |
| CON-05 | Geographic concentration | Revenue/assets by geography | Segment notes/RHP | Top geography share; currency/exposure mapping | Local market/regulatory/currency exposure | Only compare consistent geographic definitions | Business risk |
| CON-06 | Contract/order-book concentration | Dependence on major contracts, projects or renewals | RHP, official disclosures | Quantify disclosed order book and customer shares; assess expiry dates | Revenue visibility and cliff risk | Order book is not guaranteed revenue | Business risk |
| CON-07 | Customer churn/retention | Customer retention, repeat business, churn where disclosed | RHP/operating metrics | Use issuer-defined metric; record exact definition | Revenue durability | Do not compare incompatible company-defined metrics | Business quality |
| CON-08 | Pricing power / discount dependence | Discounting, rebates, incentives and price changes | RHP, notes, management discussion | Trend price/mix/margin and disclosed discount policy | Tests whether growth/margins are bought through discounting | Discount data may not be disclosed | XCHK |
| CON-09 | Raw-material exposure | Input costs as share of costs and sensitivity | RHP, notes, sector data | Quantify disclosed share; scenario-test input price changes | Margin volatility | Avoid false precision without quantities/contracts | Supply risk |
| CON-10 | Capacity utilization / operating leverage | Utilization, installed capacity and planned capex | RHP, operating data | Actual output ÷ capacity where both are comparable | Scalability and fixed-cost sensitivity | Capacity may be nameplate or effective; verify basis | Operations |
| CON-11 | Key-person dependence | Reliance on founders, key staff, licenses or relationships | RHP/governance disclosures | Qualitative, cited assessment | Continuity risk | Avoid speculative personality judgments | Governance |
| CON-12 | Dependency interaction scorecard | Combined customer, supplier, geography and product concentration | CON-01 to CON-11 | Rule graph; do not mechanically sum correlated risks | Compound fragility | Require explanation of each interaction and evidence strength | XCHK |


## 6.4 Governance, Promoters and Legal (GOV)



| ID | Indicator | Definition / required data | Primary source | Calculation / test | Why it matters | Cautions / red flags | Report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-01 | Promoter ownership and changes | Pre/post issue holdings and recent changes | RHP/shareholding tables | Reconcile percentages and share counts | Control/incentive context | Control can change with voting rights or shareholder agreements | Governance |
| GOV-02 | Pledged shares / encumbrances | Pledge/encumbrance where disclosed/applicable | RHP/exchange filings | Shares pledged ÷ relevant holdings; state denominator | Potential forced-sale/financing risk | Do not assume no pledge if disclosure is absent | Governance |
| GOV-03 | Related-party transactions | Sales, purchases, loans, guarantees and balances | RHP/financial notes | Quantify and trend; compare to scale and terms where disclosed | Conflicts of interest or dependency | Not all related-party transactions are improper | Governance |
| GOV-04 | Promoter/director litigation | Material cases and status | RHP, court/regulator sources | Record parties, forum, status, disclosed exposure and source date | Legal/reputation risk | Allegation is not finding of liability | Legal |
| GOV-05 | Regulatory actions | Orders, investigations, restrictions or notices | SEBI, RBI, MCA, sector regulator, exchange | Capture exact status and date; distinguish notice from final order | Potential business/market risk | Verify issuer/person identity carefully | Legal |
| GOV-06 | Auditor changes/qualifications | Auditor resignation/change and audit opinion history | RHP, filings, audit reports | Timeline and exact cited wording | Financial-reporting risk | Changes can have benign explanations; investigate facts | Financial quality |
| GOV-07 | Internal control / restatement signals | Restatements, control weaknesses and corrections | Audit report/RHP/filings | Document event, materiality and remediation | Reliability of reported figures | Do not infer fraud without evidence | Governance |
| GOV-08 | Promoter remuneration/loans/guarantees | Compensation and financial links with company | RHP/notes | Trend and compare to scale/terms | Potential extraction or conflict risk | Use sector and company context | Governance |
| GOV-09 | Shareholding and beneficial ownership complexity | Layered entities, trusts or shareholder agreements where disclosed | RHP/shareholding disclosures | Map disclosed control links | Control transparency | Do not infer beneficial ownership beyond records | Governance |
| GOV-10 | Capital restructuring history | Splits, bonuses, conversions, reclassification, buybacks | RHP/share capital history | Timeline and normalize historical per-share metrics | Context for pre-IPO ownership/prices | Adjust historical figures consistently | Ownership |
| GOV-11 | License/permit dependency | Critical approvals and renewal dates | RHP/regulator/official sources | List material approvals and status | Operational interruption risk | Only applicable to regulated/permit-dependent firms | Legal |
| GOV-12 | Environmental/safety claims | Material disclosed notices, accidents or compliance issues | RHP, regulator, official statements | Record verified event/status/exposure | Potential liability/continuity risk | Avoid extrapolating from unsupported reports | Risk |
| GOV-13 | Use-of-proceeds execution risk | Ability to deploy proceeds as stated | RHP and operating evidence | Compare proposed capex/timeline to track record and capacity | Execution risk | Plans are not achieved outcomes | Offer risk |
| GOV-14 | Governance evidence conflicts | Conflicting disclosures across filing, company statement and regulator record | All relevant sources | Maintain conflict record; request human review | Prevents silent reconciliation | Do not resolve without support | XCHK |


## 6.5 Valuation and Peers (VAL)



| ID | Indicator | Definition / required data | Primary source | Calculation / test | Why it matters | Cautions / red flags | Report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VAL-01 | Price-band market capitalization | Post-issue equity value at lower/upper band | Price band and post-issue shares | Price × post-issue shares; verify share basis | Size and valuation anchor | No incorrect pre-issue share count | Valuation |
| VAL-02 | P/E | Price or market cap divided by compatible earnings | Offer document and peer data | Market cap ÷ PAT, or price/EPS on consistent basis | Earnings valuation | Negative/near-zero PAT makes P/E not meaningful | Valuation |
| VAL-03 | P/B | Market cap ÷ equity book value | Financials/issue terms | Use appropriate equity and post-issue pro forma treatment | Asset-based valuation | Not suitable as standalone measure for many firms | Valuation |
| VAL-04 | EV/EBITDA | Enterprise value divided by compatible EBITDA | Financials, debt/cash, issue terms | EV = market cap + defined debt − defined cash; disclose definitions | Operating valuation | Not meaningful for negative/unstable EBITDA or financial firms | Valuation |
| VAL-05 | Price/sales | Market cap ÷ revenue | Financials/issue terms | Use same period and post-issue basis | Useful where earnings temporarily low | Margins and business mix must be considered | Valuation |
| VAL-06 | Peer-set quality | Similarity of selected listed peers | Peer filings/industry data | Document inclusion/exclusion and business comparability | Avoids cherry-picked comparisons | No peer set is perfectly comparable | Valuation |
| VAL-07 | Growth-adjusted valuation context | Compare valuation with growth, margins, returns and risk | Issuer and peers | No universal formula; use side-by-side normalized metrics | Checks whether premium is supported | Avoid false precision or unvalidated composite | Valuation |
| VAL-08 | Peer valuation percentile | Issuer multiple versus peer distribution | Verified peer dataset | Percentile only with sufficient comparable sample | Relative expensiveness | Small or biased peer set weakens conclusion | Valuation |
| VAL-09 | Post-issue capital effects | Effect of fresh cash/debt repayment on earnings and shares | Offer terms, pro forma data | Show reported historical and pro forma figures separately | Prevents denominator mismatch | Do not assume proceeds generate returns immediately | Valuation |
| VAL-10 | Valuation sensitivity | Effect of multiple compression or earnings miss | VAL-01 to VAL-09 | Scenario grid using explicit assumptions | Downside if market reprices the issue | Scenario is not a forecast | Risk model |
| VAL-11 | Peer operating quality comparison | Margins, growth, ROCE, leverage, concentration | Issuer/peer filings | Normalize period and definition; cite each peer fact | Premium quality check | Accounting differences may impair comparability | Valuation |
| VAL-12 | Price-band sensitivity | Change in valuation between lower and upper band | Offer terms and financials | Recalculate key multiples at each price-band endpoint | Shows how much price matters | Final price and issue structure must be verified | Decision summary |


## 6.6 Subscription, Demand and Market Structure (DEM)



| ID | Indicator | Definition / required data | Primary source | Calculation / test | Why it matters | Cautions / red flags | Report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DEM-01 | QIB subscription | Category subscription multiple/time series | Official exchange/verified source | Demanded shares ÷ offered shares under stated category rules | Institutional demand signal | Check whether anchor allocation is counted separately or excluded | Demand |
| DEM-02 | NII/HNI subscription | Category subscription multiple/time series | Official exchange/verified source | Use published category definition and timestamp | Non-institutional demand | High multiple can reflect leverage/large applications; not quality proof | Demand |
| DEM-03 | Retail subscription | Retail category multiple/time series | Official exchange/verified source | Use category rules and timestamp | Retail demand/attention | May be driven by sentiment or expected listing gains | Demand |
| DEM-04 | Employee/shareholder categories | Category-specific subscription where applicable | Issue data | Keep separate; document eligibility and denominator | Contextual demand | Not present in every IPO | Demand |
| DEM-05 | Subscription trajectory | Change over time and last-day acceleration | Timestamped category observations | Absolute change, relative change and time remaining | Demand momentum | Never use final figure as if known earlier in backtest | XCHK |
| DEM-06 | Anchor allocation quality | Disclosed anchor participants, amount and lock-in terms where relevant | Official anchor allocation | Describe investor type and concentration; no simplistic prestige score | Demand/ownership context | Allocation does not guarantee secondary-market buying | Demand |
| DEM-07 | Issue size and likely tradable float | Offer shares, existing holders, restrictions and expected float | RHP, shareholding and rules | Explicit assumptions; calculate ranges if uncertain | Supply at listing | Actual selling behavior is unknown | Listing setup |
| DEM-08 | Issue demand concentration | Distribution across categories/large applications where data exist | Official data | Only quantify if source provides data | Tests breadth of demand | Do not infer hidden application concentration | Demand |
| DEM-09 | Market regime | Index return, volatility, breadth and risk appetite | Verified market data | Predefine windows (e.g., 5/20/60 trading days); store cutoffs | Market backdrop | Window selection must be fixed before backtesting | Regime |
| DEM-10 | Sector momentum | Sector index/peer movement before listing | Market data | Predefined window and benchmark | Sector sentiment | Past movement not guarantee | Regime |
| DEM-11 | Comparable IPO performance | Recent listing returns in comparable cohort | Verified listing prices and offer prices | Cohort selection documented; report median/distribution | Base-rate context | Avoid selecting only successful peers | Peer |
| DEM-12 | Listing calendar congestion | Nearby large issues/events and market calendar | Official calendar/market data | List concurrent events; no universal formula | Potential competition for funds/attention | Interpret cautiously | Context |
| DEM-13 | Expected sell-side supply | OFS, pre-IPO holders, lock-in and float context | Offer docs/rules | Qualitative/range estimate, explicit assumptions | Potential listing pressure | Eligible shares do not equal actual sell orders | Risk |
| DEM-14 | Market event risk | Major macro/sector/issuer event before listing | Official calendar and credible news | Record event, time and scenario relevance | Volatility around listing | No prediction of event impact without evidence | Risk |


## 6.7 Grey-Market Premium (GMP) (GMP)



| ID | Indicator | Definition / required data | Primary source | Calculation / test | Why it matters | Cautions / red flags | Report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GMP-01 | GMP observation | Reported unofficial premium/discount | Named unofficial source | Store raw quoted amount and implied percentage only if price band known | Sentiment proxy | Not exchange-regulated official price; source can be unreliable | Demand |
| GMP-02 | GMP freshness | Age of observation at analysis cutoff | Source timestamp/retrieval time | Cutoff minus observation time | Stale values are less relevant | If source timestamp absent, freshness is unknown | Data quality |
| GMP-03 | GMP trend/volatility | Changes across time and source | Timestamped history | Change, range and dispersion; minimum observations required | Momentum/uncertainty signal | Sparse observations should not imply robust trend | XCHK |
| GMP-04 | Cross-source GMP disagreement | Difference between sources/time | Multiple sources | Compare same time basis; preserve all readings | Detects unreliable/noisy market signal | Sources may copy one another, not independent | Data quality |
| GMP-05 | GMP vs subscription divergence | Whether GMP and official demand move together | GMP + DEM series | Time-aligned comparison; no causal claim | Conflicting sentiment signals | Correlation does not establish cause | XCHK |
| GMP-06 | GMP implied listing premium | GMP divided by issue price reference | GMP and issue price | Clearly label implied estimate and basis | Communicates market expectation | Not a forecast or guaranteed return | Report |


## 6.8 News and Event Evidence (NEWS)



| ID | Indicator | Definition / required data | Primary source | Calculation / test | Why it matters | Cautions / red flags | Report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEWS-01 | News item provenance | Publisher, author, headline, URL, publication/event time | News API/provider and primary sources | Persist metadata and original link; deduplicate by canonical URL/content | Audit trail | News APIs may omit publishers or alter timestamps | News |
| NEWS-02 | Source credibility class | Official, reputable reporting, opinion, rumor, social/unverified | Source registry and human rules | Rule-based classification; retain rationale | Prevents rumor being treated as fact | Publisher category is not a truth guarantee | News |
| NEWS-03 | Event type/materiality | Earnings, order win/loss, regulation, litigation, management, product, financing, incident | News + issuer filings | Classify event and affected risk modules | Connects event to financial/business thesis | Classification requires human review for high-impact items | XCHK |
| NEWS-04 | Sentiment and direction | Positive/negative/mixed/neutral tone toward issuer/event | Text classifier + source text | AI classification with evidence span and review status | Contextual sentiment signal | Sentiment is not truth, materiality or price impact | Sentiment |
| NEWS-05 | Novelty / duplicate coverage | Whether story adds new facts or repeats prior report | Headline/body similarity and timestamps | Deduplication and event clustering | Avoid counting one event many times | Syndicated content may appear as many URLs | News |
| NEWS-06 | News volume abnormality | Change in number of distinct relevant stories | Timestamped news archive | Compare against issuer baseline and peer/sector baseline if available | Attention/event alert | Low historical coverage makes baseline unstable | ATT |
| NEWS-07 | Claim verification status | Whether material claim is confirmed by primary source | News item and filing/announcement | Confirmed, partly confirmed, contradicted, unverified | Evidence quality | No confirmation found is not proof of falsehood | Evidence |
| NEWS-08 | News-to-filing consistency | Consistency of media claim with RHP/filing/official statement | NEWS + official docs | Link claim to specific passage/value; flag discrepancy | Detect misleading or outdated narratives | Different reporting dates/definitions can explain differences | XCHK |
| NEWS-09 | Event timing vs issue/listing | Event occurred/published before or after relevant cutoff | News metadata | Use event_time and published_at separately | Correct historical information set | Late corrections must not rewrite historical prediction inputs | Backtest |
| NEWS-10 | Negative-news coverage | Relevant adverse events, disputes or correction stories | News + primary sources | Search with issuer aliases, promoters, products, key counterparties | Avoid one-sided research | Name ambiguity and false matches must be controlled | Risk |
| NEWS-11 | Catalyst tracking | Potential near-term event before listing | Official calendars/announcements | List event, source, time, scenario and uncertainty | Context for listing risk | Do not assign probability without a basis | Risk |
| NEWS-12 | News API coverage health | Coverage gaps, failed requests, provider/source limits | Provider logs | Track query, result count, last successful retrieval, errors and coverage caveats | Avoid interpreting no results as no news | Provider availability and licensing can change | Data quality |


## 6.9 Search / Investor Attention (ATT)



| ID | Indicator | Definition / required data | Primary source | Calculation / test | Why it matters | Cautions / red flags | Report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATT-01 | Search interest series | Relative search interest for issuer/query | Google Trends if available or approved alternative | Store exact query, geography, timeframe, retrieval time and normalized index | Attention context | Trends values are normalized/relative, not absolute search counts | Attention |
| ATT-02 | Search spike vs baseline | Abnormal change in search interest | ATT-01 time series | Predefined baseline and robust anomaly rule | Detect attention shocks | Small baselines and noisy terms create false alerts | XCHK |
| ATT-03 | Query ambiguity | Whether terms uniquely identify issuer/IPO | Query metadata/manual validation | Maintain exact terms and ambiguity note | Avoid unrelated searches | Company names can collide with common words | Data quality |
| ATT-04 | Attention/news synchronization | Alignment of search spike and news events | ATT + NEWS timestamps | Time-window join and event inspection | Distinguish event-driven attention from unexplained spike | Temporal alignment does not prove causation | XCHK |
| ATT-05 | Attention/subscription synchronization | Alignment of search interest and demand progression | ATT + DEM | Compare same windows and preserve cutoff | Tests whether attention corresponds to actual demand | Subscription data may update at different intervals | XCHK |
| ATT-06 | Attention source availability | Whether authorized/reliable access exists | Provider logs | Track method, failures and terms | Prevents silent substitution | Google Trends API access may be limited; optional feature | Data quality |


## 6.10 Comparable IPOs and Historical Base Rates (PEER)



| ID | Indicator | Definition / required data | Primary source | Calculation / test | Why it matters | Cautions / red flags | Report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PEER-01 | Comparable cohort definition | Rules for peer IPO selection | Issue metadata | Define sector, size, offer type, time window and exclusions before outcome analysis | Fair historical comparison | Avoid outcome-driven selection | Backtest |
| PEER-02 | Listing return distribution | Offer-to-listing return distribution for cohort | Verified prices | (listing reference price − issue price)/issue price; define opening/close separately | Base-rate evidence | Listing price may differ by opening vs close; fees excluded unless net model | Scenarios |
| PEER-03 | Downside frequency and tail | Share of cohort with negative listing outcomes and worst-tail outcomes | PEER-01/02 | Compute proportion and quantiles with sample size | Downside context | Small samples give unstable estimates | Risk |
| PEER-04 | Sector/market regime match | Similarity of market conditions | Market data | Tag regime and compare like periods | Context for base rates | Regime classification must be predefined | Backtest |
| PEER-05 | Issue-size match | Similarity of issue size and float | Offer documents | Bins or matching rule predeclared | Supply-demand comparability | Issue size alone insufficient | Backtest |
| PEER-06 | Subscription cohort match | Similar category subscription profile | Official subscription data | Compare categories and timing cutoffs | Demand analogues | Do not use final subscription for earlier-time predictions | Backtest |
| PEER-07 | Valuation cohort match | Similar valuation and financial quality | Issuer/peer metrics | Use transparent match variables | Valuation analogues | Missing peer data can bias cohort | Backtest |
| PEER-08 | Historical news/attention features | Past news and attention at decision cutoff | Archived data | Only use timestamped historical snapshots | Tests incremental signal value | Historical archive may be incomplete | Backtest |
| PEER-09 | Feature ablation results | Whether a feature improves predictive performance | Backtest runs | Compare baseline with/without feature on out-of-sample data | Prevent useless complexity | Requires enough data and repeated validation | Model validation |
| PEER-10 | Prediction calibration | Agreement between predicted probabilities and outcomes | Validated model outputs/outcomes | Brier score/calibration curve or suitable metrics when sample size supports | Assess probability quality | Do not publish probability claims before adequate validation | Model validation |


## 6.11 Listing-Day Scenarios and Returns (RISK)



| ID | Indicator | Definition / required data | Primary source | Calculation / test | Why it matters | Cautions / red flags | Report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RISK-01 | Offer price reference | Final issue price and its source | Final issue terms | Use final price, not assumed upper band if issue price differs | Return denominator | Flag if final price unavailable | Return |
| RISK-02 | Listing-price reference | Opening price and/or specified exit price | Verified exchange data | Define whether open, intraday, close or user-selected time | Return numerator | These are different outcomes; never mix them | Backtest |
| RISK-03 | Gross listing return | Return before costs | Issue/listing price | (exit price − issue price)/issue price × 100 | Core outcome | Scenario estimate must be separated from realized return | Report |
| RISK-04 | Net return after costs | Net outcome after fees/taxes/slippage assumptions | Broker fee schedule and applicable rules | Transparent calculation; jurisdiction/date-specific inputs | Decision relevance | Costs vary; show assumptions and update date | Report |
| RISK-05 | Scenario ranges | Bull/base/bear/severe downside assumptions | All modules | Evidence-linked scenario construction; range rather than false precision | Communicates uncertainty | Not a guarantee or probability unless validated | Report |
| RISK-06 | Scenario drivers | Most influential variables in each scenario | XCHK/VAL/DEM/NEWS | Sensitivity or structured narrative with links | Shows what changes outcome | Qualitative rankings must be labelled if not computed | Report |
| RISK-07 | Downside magnitude | Potential loss from issue price under downside scenarios | Scenario ranges | (downside exit − issue price)/issue price | Capital-risk framing | No claim that scenario is maximum possible loss | Risk |
| RISK-08 | Allotment probability | Chance of allotment under category/rules where estimable | Application category, valid applications and allotment rules/data | Use official process and historical/current counts; otherwise unknown | Separates allocation from return | Do not conflate oversubscription multiple with personal probability | Report |
| RISK-09 | Capital lock-up duration | Time from application debit/block to release/exit settlement | Issue/ASBA/broker rules | Date-based estimate with explicit assumptions | User capital constraint | Operational timing varies by application and broker/bank | Report |
| RISK-10 | Evidence coverage scorecard | Coverage by module and severity of missing evidence | DATA module | Coverage counts/weighted critical gaps; disclose formula | Shows how complete report is | Not the same as probability of success | Report |
| RISK-11 | Decision assessment | Consider / Cautious / Avoid / Insufficient evidence, with rationale | All relevant modules | Rule-governed, explainable synthesis; no unsupported certainty | Action-oriented summary | Must not hide contradictory evidence behind one score | Report |
| RISK-12 | What would change the view | New data or thresholds that could change assessment | Scenario/risk dependencies | List specific measurable triggers | Supports updates and re-analysis | Avoid vague statements | Report |


## 6.12 Cross-Indicator Synchronization (XCHK)



| ID | Indicator | Definition / required data | Primary source | Calculation / test | Why it matters | Cautions / red flags | Report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| XCHK-01 | PAT vs OCF divergence | Profit growth and operating cash flow diverge | FIN-04/07/08 | Flag material divergence using sector-aware historical context; investigate WC and non-cash items | Earnings quality | Divergence is a question, not proof of manipulation | Critical findings |
| XCHK-02 | Sales vs receivables divergence | Receivables outgrow sales or debtor days jump | FIN-01/10/11 | Compare same periods and acquisition effects | Collection/revenue quality | Check contract assets and seasonality | Critical findings |
| XCHK-03 | Margin vs cost-driver divergence | Margin rises without matching business driver | FIN-02/03/21 + CON-08/09 | Inspect mix, input prices, discounts, accounting and utilization | Sustainability of margins | Data may not reveal all drivers | Critical findings |
| XCHK-04 | Profit vs other-income divergence | Profit growth substantially supported by non-operating income | FIN-04/05/06 | Reconcile PBT/PAT components | Recurring earnings | Other income may be core for some sectors | Critical findings |
| XCHK-05 | Customer/supplier double concentration | Concentrated revenue and critical input source overlap | CON-01/02/03 | Build dependency map; quantify disclosed shares | Compound operational risk | Avoid assuming same counterparties without evidence | Risk map |
| XCHK-06 | Customer concentration vs receivables | Top customers and receivables both concentrated | CON-01 + FIN-10/11/22 | Link only when customer-level data disclosed | Potential collection cliff | Customer-level receivable data often unavailable | Risk map |
| XCHK-07 | Subscription vs GMP divergence | Official demand and unofficial premium diverge | DEM + GMP | Time-align observations and source quality | Conflicting sentiment | GMP data may be sparse or copied | Market synthesis |
| XCHK-08 | Subscription vs valuation divergence | High demand but stretched valuation | DEM + VAL | Present both signals; test cohort outcomes | Crowded/overpriced risk | Strong demand may still support listing premium | Market synthesis |
| XCHK-09 | Search/news vs subscription divergence | Attention/news grows without matching demand or vice versa | ATT + NEWS + DEM | Align timestamps, categories and query validity | Attention quality | Data update schedules differ | Market synthesis |
| XCHK-10 | News claim vs filing conflict | Headline claim differs from official disclosure | NEWS + source passages | Quote/locate both claims; classify conflict | Narrative integrity | Dates/definitions may differ | Evidence conflicts |
| XCHK-11 | OFS vs funding narrative | Large selling component alongside stated funding need | ISS-01/02/03/06 | Compare issue structure and proceeds | Incentive alignment | OFS may have valid reasons; not a verdict alone | Offer analysis |
| XCHK-12 | Valuation premium vs quality | Premium relative to peers without matching growth/returns/quality | VAL + FIN + CON/GOV | Compare normalized metrics and uncertainty | Downside sensitivity | No universal fair value formula | Valuation |
| XCHK-13 | Leverage vs use of proceeds | Debt remains high despite fundraising or planned repayment | ISS-03/09 + FIN-15/16 | Recalculate pro forma leverage where inputs support it | Balance-sheet risk | Use proceeds may be partly allocated to other needs | Financial risk |
| XCHK-14 | Related-party vs concentration | Material related-party trade and dependency concentration | GOV-03/22 + CON | Join disclosed counterparties and amounts | Conflict/dependency | Do not infer relationships not disclosed | Governance |
| XCHK-15 | Event/news vs business exposure | News event hits a key customer, supplier, regulator or product | NEWS + CON/GOV | Map event to disclosed exposure and scenario | Materiality assessment | Entity matching errors possible | Risk |
| XCHK-16 | Peer comparison integrity | Issuer and peers use incompatible accounting/periods/definitions | VAL + PEER | Validate basis before ranking | Prevents false comparison | May require manual normalization | Valuation |
| XCHK-17 | Time leakage check | Any input published after historical decision cutoff | DATA/NEWS/DEM/GMP/ATT | Hard reject from historical feature set or mark post-cutoff | Backtest validity | Do not overwrite historical snapshots with later data | Model integrity |
| XCHK-18 | Contradiction disposition | Track each contradiction to resolution or unresolved state | All modules | Status: open, explained, partly resolved, unresolved, rejected with evidence | Auditability | Unresolved material contradiction must lower confidence | Report |


## 6.13 Data Coverage and Model Integrity (DATA)



| ID | Indicator | Definition / required data | Primary source | Calculation / test | Why it matters | Cautions / red flags | Report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DATA-01 | Required document coverage | Presence/version/status of expected docs | Evidence registry | Checklist by issuer type and issue stage | Shows missing foundations | Required set varies by issuer and stage | Evidence status |
| DATA-02 | Critical-field completeness | Completeness of high-impact values | Indicator records | Count available critical fields / expected applicable fields; publish denominator | Coverage warning | Completeness does not mean correctness | Report |
| DATA-03 | Source freshness | Age of dynamic observations | Source records | Cutoff minus retrieved/published time with per-signal rule | Prevents stale demand/news/GMP use | Financial filings have different freshness rules than market signals | Report |
| DATA-04 | Citation coverage | Share of material claims with valid source locator | Report claims and source registry | Automated citation validation + manual audit | Traceability | A URL alone may not support the specific claim | Report |
| DATA-05 | Extraction confidence | Confidence/validation of parsed values | Extraction pipeline | Based on method, checks and manual review | Targets OCR/table errors | Do not rely on model self-confidence alone | Evidence |
| DATA-06 | Reconciliation checks | Totals, ratios, balance sheet/cash flow checks | Source tables/calculation engine | Run deterministic checks with tolerances | Catches extraction/unit errors | Accounting presentation can require exceptions | Data QA |
| DATA-07 | Unit/period consistency | Compatible units, currencies, periods and accounting basis | Facts/metrics | Schema validation and normalization rules | Prevents invalid calculations | Never silently convert ambiguous units | Data QA |
| DATA-08 | Duplicate/copy source detection | Repeated content and non-independent sources | Source registry/news archive | URL canonicalization and content similarity | Avoids false corroboration | Similar reports may still have independent verification | News QA |
| DATA-09 | Reproducibility/version | Formula, prompt, code and information cutoff versions | Run metadata | Persist run configuration and source snapshot IDs | Allows audit/re-run | Live sources may change; preserve snapshots when permitted | Audit |
| DATA-10 | Model performance monitoring | Out-of-sample metrics and drift | Backtest/paper log | Predefined performance metrics and review interval | Detects degradation | No validated performance until adequate sample exists | Model governance |


# 7. Cross-Module Dependency Map


Dependencies are directional analysis relationships, not proof of causality. Implement explicit edges and store why each edge exists.


| Starting indicator | Must cross-check with | Purpose |
| --- | --- | --- |
| FIN-01 Revenue growth | FIN-10/11 receivables; CON-01 customers; CON-08 discounts; FIN-02/03 margins | Growth quality, collection risk and discount-driven sales |
| FIN-04 PAT | FIN-05 other income; FIN-06 one-offs; FIN-07 OCF; FIN-18 tax; FIN-20 audit | Recurring and cash-supported earnings |
| FIN-03 margins | CON-08 discounting; CON-09 input costs; FIN-21 capitalization; FIN-17 returns | Margin source and sustainability |
| CON-01 customers | FIN-10/11 receivables; CON-06 contracts; NEWS events; GOV-03 related parties | Customer-loss and collection stress |
| CON-02/03 suppliers | CON-09 raw materials; NEWS events; DEM/market conditions | Supply interruption and input-price scenarios |
| ISS-02 OFS split | GOV-01 ownership; ISS-07 lock-in; DEM-07 float; RISK-13 supply | Seller incentives and potential supply |
| VAL-02/04 multiples | FIN growth/margins/returns; PEER cohort; DEM regime | Whether valuation premium has support |
| DEM subscription | GMP history; ATT search interest; NEWS event timeline; VAL multiples | Demand breadth, attention and price expectations |
| NEWS material event | CON exposures; GOV/legal; FIN sensitivity; event timing | Issuer-specific event materiality |
| ATT search spike | NEWS volume/novelty; DEM progression; query ambiguity | Attention versus actual demand |
| All inputs | DATA timestamps; XCHK-17 time leakage; source provenance | Prevent look-ahead bias and unsupported conclusions |


# 8. Formula and Normalization Standards


- Store raw sourced values before any normalization. Preserve the original unit and exact source context.

- Normalize currency and scale only when explicit: INR, lakh, crore, thousands, millions, shares, per-share values and percentages must never be inferred silently.

- Use consolidated versus standalone basis explicitly. Prefer consistent basis across periods; explain any unavoidable mismatch.

- Record fiscal-year labels and exact period-end dates. Do not compare a 9-month period directly with a full year without an explicit, defensible adjustment.

- Use average balance sheet values for ratios such as ROE/ROCE/receivable days when available; if only closing balances are available, label that limitation.

- Do not calculate ratios with zero, negative or near-zero denominators without a defined treatment. Return NOT_MEANINGFUL and explain why.

- Round only for display; retain precision internally. Displayed rounding must not alter downstream calculations.

- Do not use one fixed red-flag threshold for all industries. Store thresholds by sector, metric definition, historical distribution and validation status.

- Where adjusted/normalized metrics are used, show reported metric, adjustment line items, formula, rationale and resulting adjusted value side by side.

- Every formula requires unit tests, edge-case tests and at least one manually verified example.


# 9. News API Integration Requirements


News API is recommended as an ingestion option, not a source of truth and not necessarily a substitute for Google Trends. It supplies news coverage; search-interest data and news volume measure different things.

- Provider selection must consider Indian company/IPO coverage, source breadth, historical search, timestamps, deduplication, latency, rate limits, price and licensing.

- Store provider, query terms, request time, result count, pagination state and any provider coverage limitations.

- Search issuer aliases, legal entity name, promoter names where relevant, product/brand names, sector terms and material disclosed counterparties while controlling false matches.

- Deduplicate syndicated stories and link all copies to an event cluster so one event is not counted as many independent signals.

- Keep original headline, publisher, URL, published_at, event_time when known, retrieved_at, snippet/body only as permitted, and source credibility class.

- AI may classify topic/sentiment and summarize, but must attach an evidence span and source link. High-impact claims require primary-source verification or an explicit unverified label.

- Do not interpret zero API results as proof that no news exists. Record query failures, coverage limits and inaccessible publishers.

- Check provider terms before storing full articles or redistributing content. Prefer storing metadata, links and short permitted excerpts where appropriate.

- Use official company/exchange/regulator feeds alongside a news provider for material facts; a news API is a discovery and context layer.

- Provider/API choice remains an implementation decision after a small source-coverage test. Avoid committing to a specific paid service in the core design.


| SYNCHRONIZATION EXAMPLE<br>A news API detects a story claiming a major customer has ended a contract. The engine should identify the customer against disclosed customer concentration, check official company/exchange filings, estimate the revenue exposure only if disclosed data support it, examine search-interest and subscription/GMP changes after publication, and flag the story as unverified if no primary confirmation is found. It must not invent the customer's revenue share. |
| --- |


# 10. Report Claim and Finding Schema



| Field | Definition |
| --- | --- |
| claim_id | Stable ID for every material report claim |
| claim_text | Atomic statement; avoid bundling several facts into one claim |
| claim_type | observed_fact, calculated_metric, interpretation, hypothesis, scenario, unknown |
| supporting_indicator_ids | One or more catalogue IDs |
| source_ids_and_locators | Evidence links, pages/tables and exact source versions |
| calculation_trace | Inputs, formula version, output and rounding where calculated |
| counter_evidence | Relevant evidence that weakens or contradicts the claim |
| status | supported, partly_supported, disputed, unverified, unresolved, rejected |
| materiality | critical, high, medium, low; rationale required |
| listing_day_relevance | Direct, indirect, low, unknown; explain the pathway |
| confidence_rationale | Source quality, extraction checks, coverage and uncertainty—not a made-up confidence number |
| as_of_cutoff | Information cutoff for report or backtest |
| human_review_required | Boolean plus reason for critical extraction/conflict items |


# 11. Decision Synthesis Rules


- Do not average all indicators into one opaque score. Correlated measures (e.g., receivable growth and debtor days) can double-count one underlying issue.

- Separate issuer/business quality, offer valuation, demand/sentiment, supply/float, event risk, and evidence quality into distinct dimensions.

- Use critical red flags and unresolved contradictions as gates or explicit cautions, not as tiny score deductions hidden by positives.

- Distinguish positive evidence, negative evidence, mixed evidence and missing evidence. Missing is not neutral.

- Every conclusion should say: what was observed, why it matters for listing day, what could explain it, what evidence supports it, what contradicts it and what remains unknown.

- Do not label fraud, manipulation or deliberate deception unless supported by authoritative findings; describe anomalies and possible explanations carefully.

- Use categories such as CONSIDER, CAUTIOUS, AVOID, or INSUFFICIENT EVIDENCE only with explicit decision rules and caveats.

- Do not publish predicted probability of profit until backtesting and calibration support it. Before that, show qualitative scenarios and confidence in evidence coverage.


# 12. Historical Backtest Data Contract



| Field | Requirement |
| --- | --- |
| ipo_id | Canonical issuer and issue ID |
| decision_timestamp | Exact timestamp when a simulated decision is made |
| information_cutoff | Hard cutoff; any later-published/retrieved fact is excluded |
| feature_snapshot_ids | Immutable IDs for source and indicator observations available at cutoff |
| model_version | Code, rule, formula and prompt/model versions |
| decision_output | Assessment and scenario ranges recorded before outcome |
| application_category | If modeling allotment probability, the relevant category and assumptions |
| realized_opening_price | Verified exchange opening price and source |
| realized_close_price | Verified listing-day close and source |
| realized_exit_definition | Open, close, fixed time or other predeclared exit rule |
| net_return_assumptions | Costs, taxes, fees and slippage model version |
| outcome_timestamp | When actual outcome became known |
| exclusion_reason | Any excluded case and predeclared reason |


| ANTI-LEAKAGE RULE<br>Never use final subscription figures, post-listing news, corrected later filings, final GMP values, or any other information that was unavailable at the simulated decision timestamp. Keep historical snapshots immutable. Otherwise the backtest is invalid. |
| --- |


# 13. MVP Prioritization



| Priority | Scope | Reason / exit criterion |
| --- | --- | --- |
| P0 — required first | Evidence registry, upload/manual input, document/page citations, core financial calculations, missing-data states, report generation, first cross-checks | Can produce a useful, auditable report for one IPO without live APIs. |
| P1 — core listing signals | Issue mechanics, valuation, category subscription snapshots, GMP timestamp history, market regime, scenario output | Adds listing-day-specific context while preserving source timestamps. |
| P2 — news integration | News provider adapter, deduplication, event classification, primary-source verification workflow, news-to-indicator graph | Improves event discovery; provider chosen after coverage/cost test. |
| P3 — advanced forensic modules | Sector-specific checks, richer table extraction, related-party/dependency graph, more contradiction rules | Broadens coverage after data and core workflow are reliable. |
| P4 — validation and automation | Historical backtest, feature ablation, calibration, source adapters and monitoring | Only after sufficient timestamped data and repeatable outputs exist. |


# 14. Acceptance Tests for the Catalogue


- [ ] If PAT rises while OCF falls, the system flags the divergence, checks working capital/one-offs and does not automatically label fraud.

- [ ] If receivables grow much faster than sales, the report shows exact periods, formulas, source pages and alternative explanations.

- [ ] If a news API reports a serious event, the system stores the source/timestamps, checks official disclosures and labels it unverified until evidence supports it.

- [ ] If Google Trends is unavailable, the report says unavailable and continues; it does not fabricate search-interest values.

- [ ] If a metric is not relevant to a sector, it is marked NOT_APPLICABLE with a reason.

- [ ] If two sources conflict, both values and source metadata remain available for review.

- [ ] If a required field is missing, no silent zero or invented estimate appears.

- [ ] If an extraction lacks a reliable page/table locator, material claims are marked unverified or sent for human review.

- [ ] If a historical input is timestamped after the decision cutoff, the backtest pipeline rejects it.

- [ ] If the report gives a scenario, it identifies assumptions and does not call the scenario a guaranteed or calibrated probability.


# 15. Source and API Research Starting Points



| Resource | Location | Implementation note |
| --- | --- | --- |
| Google Trends API documentation | https://developers.google.com/search/apis/trends | Optional only; official access may be limited. Verify eligibility before planning around it. |
| Google Trends API announcement | https://developers.google.com/search/blog/2025/07/trends-api | Official announcement of the limited alpha. |
| NSE issue information | https://www.nseindia.com/market-data/issue-information | Starting point for issue terms/subscription data; confirm access and field definitions. |
| SEBI | https://www.sebi.gov.in/ | Official regulatory materials and disclosures. |
| News API provider documentation | Provider not selected yet | Compare coverage, historical access, timestamps, licensing, rate limits and cost using a small Indian IPO sample. |
| Official issuer/exchange disclosures | Per-IPO source registry | Use as primary verification layer for material events reported by news providers. |


# 16. Final Instruction to Any AI/Developer Continuing This Project



| IMPLEMENTATION CONTRACT<br>Read this document together with the Project Scope, Core Vision & Technical Brief before coding. Do not skip requirements because they are lengthy. First propose the data schema and an indicator-to-source coverage matrix. Implement in small tested phases. Do not silently narrow scope, invent data, claim unsupported API access, or generate a polished report that hides missing evidence. When a feature is unavailable, report the limitation and keep a manual fallback. |
| --- |

Next deliverable after this document: an implementation-ready schema/ERD and a source availability audit on a small sample of IPOs, followed by a prioritized MVP task breakdown.
