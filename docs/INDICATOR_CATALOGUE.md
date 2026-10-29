# Indicator Catalogue & Data Dictionary

**Status:** Canonical v1.0.1  
**Scope:** Indian Mainboard IPOs only

> **Binding constraints:** Total budget is **₹0**: no paid APIs, data, AI, hosting, software or upgrades; never assume a service or free tier is free. Scope is Indian Mainboard IPOs only, never SME. Core operation is local-first and manual-first. AI must never invent values, sources or citations. Material financial calculations must be deterministic and tested.  
**Use:** Research framework, not a promise, scorecard or mandatory checklist.

## Data-status vocabulary

| Status | Meaning |
|---|---|
| Verified | Reviewed against a suitable source or explicit validation rule. |
| Extracted — review required | Candidate derived from document parsing or AI; not trusted yet. |
| User-entered — unverified | Manual value with inadequate external verification. |
| Calculated | Deterministic result with identified formula and inputs. |
| Conflicting | Credible inputs disagree; no final resolution. |
| Unavailable | Sought but absent from evidence. |
| Not applicable | Does not fit this issuer/context; reason required. |
| Stale | Exists but violates the signal's freshness rule. |
| Invalid | Fails type, unit, period or reconciliation checks. |

Unknown is never zero. An inapplicable metric is not missing. A calculation must retain inputs, units, periods, formula/rule version and rounding rule.

## Indicator catalogue

| ID | Area | Indicator / question | Typical input(s) | Output / rule | MVP priority |
|---|---|---|---|---|---|
| IND-01 | Identity | Is issuer/issue identity unambiguous? | Issuer, identifiers, dates, offer document | Flag ambiguity before final report | P0 |
| IND-02 | Offer | Fresh issue vs OFS mix | Offer structure | State shares/value and disclosed implications; no automatic judgement | P0 |
| IND-03 | Offer | Use of proceeds | Offer document proceeds section | Disclosed allocation, gaps and interpretation separately | P0 |
| IND-04 | Offer | Issue size, price band, lot and share-count basis | Offer document | Validated facts; retain period/version | P0 |
| IND-05 | Financial | Revenue growth | Compatible-period revenue | `(current / prior - 1) × 100`; block invalid/incompatible periods | P0 |
| IND-06 | Financial | EBITDA / operating margin | Validated operating figures | Explicit formula and accounting basis | P0 |
| IND-07 | Financial | PAT margin | PAT and revenue | `PAT / revenue × 100` | P0 |
| IND-08 | Financial | Operating-cash-flow conversion | CFO and PAT | `CFO / PAT` where meaningful; explain period and sign | P0 |
| IND-09 | Financial | Debt / leverage and liquidity | Debt, cash, equity/current liabilities | Defined metric only when compatible inputs exist | P0 |
| IND-10 | Earnings quality | Other income / one-off effects | Financial statements and notes | Identify disclosed non-core/recurrent distinction; do not infer | P0 |
| IND-11 | Earnings quality | PAT vs cash-flow consistency | PAT, CFO, working-capital evidence | Finding with traceable inputs; limitation if unavailable | P0 |
| IND-12 | Governance | Auditor qualifications / changes | Audit report, offer document | Verified disclosure with locator; unresolved claims stay labelled | P0 |
| IND-13 | Governance | Related parties / contingent liabilities | Notes and offer documents | Disclosed facts, applicable trend/relationship checks | P0 |
| IND-14 | Business risk | Customer, supplier, product or geography concentration | Risk factors and notes | Company-specific dependency finding | P0 where disclosed |
| IND-15 | Business risk | Contracts, competition, regulation and operations | Risk factors/business section | Evidence-linked risk, not generic boilerplate | P0 where material |
| IND-16 | Valuation | Peer comparable multiples | Peer values, period, definition, rationale | Comparison only with documented compatibility limitations | P1 |
| IND-17 | Demand | Subscription by category and time | Official/manual observation | Time-stamped observation; no predictive claim | P0 manual entry |
| IND-18 | Demand | GMP level/change/source | Manual report observation | Label unofficial; preserve history/source/time | P0 manual entry |
| IND-19 | Context | Market/sector regime | Dated source/observation | Context, not causal proof | P1 |
| IND-20 | News | Material event / catalyst / adverse report | URL, publisher, timestamps, verification | Lead, verified fact, allegation or unresolved status | P1 |
| IND-21 | Attention | Search-interest observation | Audited attention source | Optional context only; omit if unavailable | P2 |
| IND-22 | Cross-check | Contradiction between signals | Referenced indicators | Explain relation, evidence and competing explanations | P0 |
| IND-23 | Scenario | Listing return conditional on allotment | Issue price, scenario/listing price, assumptions | `(scenario price - issue price) / issue price × 100`; never merge with allotment probability | P0 |
| IND-24 | Scenario | Downside case | Explicit adverse assumptions | Labelled conditional scenario with prerequisites/gaps | P0 |

## Input field dictionary

| Field | Meaning | Required provenance |
|---|---|---|
| `value` | Literal reported or calculated value | Source or calculation trace |
| `unit` / `currency` | Measurement and currency | Never inferred if uncertain |
| `period_start`, `period_end` | Reporting/observation period | Required for comparisons/calculation |
| `publication_time` | When source was published | Preserve if known |
| `event_time` | When observation/event occurred | Separate from publication/retrieval |
| `retrieval_time` | When user/system obtained source | Required for external observation when possible |
| `source_type` | Official filing, exchange, issuer, manual, secondary media, etc. | Required |
| `source_locator` | URL, local reference, document version/page/section/table | Required for material claims when available |
| `method` | User entry, extraction, import or calculation | Required |
| `status` | One defined status from this document | Required |
| `formula_version` | Calculation/rule version | Required for calculated outputs |
| `analysis_cutoff` | Latest information permitted for a run | Required for time-sensitive/historical work |

## Calculation and interpretation rules

- Financial arithmetic is implemented in deterministic tested code, never only in AI prose.
- Validate units, currencies, periods, share-count basis and zero/negative denominators before calculation.
- Keep the formula and rounding policy with each calculated result.
- Every cross-check finding names its inputs and rule; no opaque score is required.
- Separate fact, calculated metric, interpretation, hypothesis and scenario in storage and reports.
- Preserve counter-evidence and conflicting values.
- Historical work uses only information available at the recorded cutoff; no look-ahead leakage.

## Out of scope

This catalogue does not require every indicator in every case. It does not authorize SME support, paid data, automatic trading, unvalidated predictive claims or an AI-generated number without evidence.
