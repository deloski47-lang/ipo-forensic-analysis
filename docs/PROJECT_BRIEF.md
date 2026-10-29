# Project Brief — IPO Forensic Analysis Engine

**Status:** Canonical  
**Version:** 1.0.1  
**Scope:** Indian Mainboard IPOs only  
**Mode:** Local-first, single-user, manual-first research application

## Product definition

The IPO Forensic Analysis Engine helps a user investigate an Indian Mainboard IPO for a possible listing-day exit. It turns offer documents, disclosures and time-sensitive observations into an auditable research report that shows evidence, calculations, risks, contradictions, gaps and conditional scenarios.

It is not a trading system, a promise of listing gains, a generic IPO listing site or a machine that converts incomplete information into certainty.

## The problem

IPO research is scattered across offer documents, financial statements, exchange material, subscription observations, unofficial GMP reports, news and market context. Sources may be incomplete, stale, inaccessible, inconsistent or poorly defined. A polished summary or score can hide those weaknesses.

The engine therefore asks: what is known; what supports it; what is missing or contradictory; which financial and business risks matter; and what conditional listing-day outcomes remain plausible at a stated information cutoff?

## Binding constraints

| Constraint | Meaning |
|---|---|
| ₹0 total budget | No paid APIs, data, AI, hosting, software, upgrades or paid fallbacks. Free tiers are optional only after verification; no service is presumed free. |
| Market scope | Indian **Mainboard IPOs only**. SME IPOs are excluded. |
| Local-first | Cases, evidence, calculations and reports must work on the user's machine without mandatory cloud infrastructure. |
| Manual-first | User-supplied files and documented manual entries are a complete core path; automation is optional. |
| Evidence-first | Material claims need evidence or an explicit unresolved/hypothesis label. |
| No invented values | AI and extraction may produce candidates, never unlabelled truth. Missing means missing. |
| Deterministic finance | Material calculations use specified formulas, validated inputs and tests. |
| Honest scenarios | A scenario is conditional, not a prediction or recommendation. Allotment likelihood and return conditional on allotment stay separate. |

## MVP outcome

A user can create and reopen an IPO case, register documents and manual observations, review extracted candidates, validate core inputs, run selected deterministic metrics and contradiction checks, and export an auditable qualified report. The report preserves citations, data status, calculations, assumptions, limitations and adverse cases.

MVP does not require automated news, Trends, subscription, GMP or exchange integrations. It also does not execute orders, guarantee gains, claim predictive accuracy, require cloud hosting or support multiple users.

## Research integrity

Every material record should retain source identity, source type, URL/local reference, relevant period, publication/event/retrieval time, version/locator, input method and validation/conflict status. Conflicting values are findings; they are never silently merged.

AI may help navigate, extract candidates, classify, summarise and explain evidence. It may not fabricate a source, number, locator, timestamp or disclosure. Material arithmetic belongs in deterministic code, not free-form model prose.

## Source strategy

Primary sources are preferred: offer documents, regulator filings, exchange disclosures, audited statements and official company announcements. Secondary reporting can be a lead, not sole proof of a material claim when verification is possible. GMP is unofficial and must remain labelled as such.

A source integration is admitted only after the feasibility audit confirms its field definitions, access method, cost/terms, coverage, time semantics, historical availability and manual fallback.

## Recorded lesson

In earlier SAWA work, Google Trends/pytrends did not work as expected; the exact cause was not established. NewsAPI was tried as an alternative. Neither is a required dependency for this project; any future attention/news integration remains optional and must pass the audit.

## Canonical document map

- `PROJECT_BRIEF.md`: product intent, scope and boundaries.
- `PRD.md`: approved measurable requirements and acceptance criteria.
- `DATA_SOURCE_AUDIT.md`: source feasibility and integration gates.
- `INDICATOR_CATALOGUE.md`: indicator meanings, inputs, status and calculation rules.

## Open decisions

Technology stack, local storage layout, initial formula set, document extraction approach, report format, source adapters and any predictive evaluation approach remain open. They require evidence and a documented decision before implementation.
