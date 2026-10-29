# Data Source & Feasibility Audit

**Status:** Canonical v1.0.1  
**Scope:** Indian Mainboard IPOs only

> **Binding constraints:** Total budget is **₹0**: no paid APIs, data, AI, hosting, software or upgrades; never assume a service or free tier is free. Scope is Indian Mainboard IPOs only, never SME. Core operation is local-first and manual-first. AI must never invent values, sources or citations. Material financial calculations must be deterministic and tested.  
**Decision:** The core workflow must operate without any automated external data source.

## Audit rule

A source is not an approved dependency merely because it has a website, endpoint, trial or free tier. Before integration, verify its current terms, price, limits, licensing/attribution, fields, coverage, timestamps, historical availability, automation permission and failure behaviour. Record the verification date and a manual fallback.

## Source matrix

| Need | Preferred source / link | MVP access | Status | Manual fallback |
|---|---|---|---|---|
| Offer documents (DRHP/RHP/prospectus) | [SEBI Public Issues filings](https://www.sebi.gov.in/filings/public-issues.html) | Browser/download and user-supplied file | Core evidence source; no API assumed | User registers a local copy and records URL, version and locator. |
| Issue summary / offer material | [BSE Issue Summary](https://www.bseindia.com/markets/PublicIssues/Issuesummary.aspx), issuer/merchant-banker material | Browser/manual | Discovery/verification candidate | User enters fields with document/source reference. |
| Official exchange disclosures and listing facts | Relevant BSE/NSE issuer or public-issue page | Browser/manual | Candidate; exact access/coverage not yet approved | User registers official disclosure or manually records observation with timestamp. |
| Financial statements, risks, proceeds, offer structure | DRHP/RHP/prospectus and audited documents | Document extraction + review | Core | Manual transcription with page/section locator. |
| Subscription observations | Official exchange/registrar publication when available | Manual only until audited | Optional | User-entered observation with category, source and event/retrieval time. |
| GMP | Public reports; no official primary source | Manual only | Optional, unofficial, noisy | User-entered observation marked unofficial; preserve source/time. |
| Peer valuation and market context | Company filings/exchange data and documented user research | Manual only | Optional | Record period, definition, source and comparability note. |
| News | Primary source first; secondary reporting for leads | Manual only | Optional | Save URL, publisher and timestamps; label verification status. |
| Search attention / Trends | Google Trends or pytrends only if later proven usable | Not approved | Optional research only | Omit signal; do not block analysis. |

The SEBI public-issues page exposes categories for draft offer documents, RHPs and final offer documents. This confirms it as a valuable document-discovery source, not an API guarantee or a blanket automation permission.

## Reliability and interpretation rules

1. Offer documents and audited disclosures take priority for issuer facts.
2. A source may establish a lead without establishing a material claim.
3. Subscription and GMP are observations, not proof of listing performance.
4. Duplicated or syndicated news is not independent corroboration.
5. Record publication time, event time and retrieval time separately where known.
6. Unknown coverage, field definition or historical availability means the integration is unapproved.
7. No source integration may write over saved user evidence or prevent manual entry on failure.

## Cost and operational feasibility

The project budget is **₹0**. Therefore:

- No paid service can be adopted.
- A nominal “free” plan needs current verification; payment details, usage caps, commercial restrictions, attribution requirements and continuity risk all matter.
- Core functionality cannot depend on a free tier, because free terms and access may change.
- Local storage and user-supplied files form the baseline; optional connectors must fail gracefully.

## SAWA integration lesson

Google Trends/pytrends previously did not work as expected during SAWA work. The exact cause remains unknown, so it is not safe to assume the same method will work here. NewsAPI was tried as an alternative, but it is **not** a required dependency. Neither source is needed for the MVP.

## Integration approval checklist

Before adding a connector, document:

- exact source URL and owner;
- intended fields and their definitions;
- Mainboard-only coverage and exclusion handling for SME IPOs;
- access method and automation permission;
- current cost, terms, rate limits and attribution;
- timestamp semantics and historical depth;
- a sample validation against primary evidence;
- stale/missing/error behaviour;
- manual fallback and source-removal plan;
- tests demonstrating no fabricated values or silent overwrites.

Until every applicable item is verified, retain the source as **manual-only** or **not approved**.
