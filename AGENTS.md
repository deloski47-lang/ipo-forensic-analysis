# AGENTS.md — Repository Operating Rules

## Read before changing anything

Read, in order: `README.md`, `docs/PROJECT_BRIEF.md`, `docs/PRD.md`, `docs/DATA_SOURCE_AUDIT.md` and `docs/INDICATOR_CATALOGUE.md`. Then identify the requirement IDs and indicator definitions affected by the proposed change.

## Binding project constraints

1. The total project budget is **₹0**. Do not introduce paid APIs, datasets, AI, hosting, software, upgrades, trials that require payment details, or paid fallbacks.
2. Never assume an API, data source, model, feature or free tier is free. Verify current pricing, terms, rate limits, attribution, historical access and failure behaviour before proposing an integration.
3. Scope is **Indian Mainboard IPOs only**. Do not implement or document SME IPO support.
4. Core operation is local-first and manual-first. Failure or absence of an optional integration must not block evidence entry, deterministic calculation or reporting.
5. AI is assistive only. It must never invent values, sources, citations, locators, timestamps, disclosures or missing data. Unknown is not zero.
6. Material financial calculations must be deterministic, input-traceable and covered by known-answer, missing-input and invalid-input tests.

## Documentation and decisions

- Canonical documents have stable names. Update the existing file; do **not** create numbered, dated or duplicate versions.
- Use Git history for previous states. Do not generate routine download copies.
- When a material product, data, architecture or methodology decision is made, record the decision, evidence, alternatives and consequences in the relevant canonical document (or an approved decision log) in the same change.
- If canonical documents conflict or a decision is missing, flag it. Do not silently choose the easiest implementation.
- Preserve source links, tables, requirement IDs and approved substance when consolidating documentation.

## Evidence, claims and review

- Prefer primary sources for material facts. Record publication/event/retrieval times, period, source identity and locator when available.
- Label observations as verified, extracted-review-required, user-entered-unverified, calculated, conflicting, unavailable, not-applicable, stale or invalid as appropriate.
- Preserve conflicts; never silently average or overwrite them.
- Verify externally changeable claims. Do not claim that a service is free, available, reliable or permitted without checking.
- SAWA lesson: Google Trends/pytrends did not work as expected; exact cause unknown. NewsAPI was tried as an alternative but is neither required nor an approved core dependency.

## Delivery discipline

- Keep changes scoped to the approved requirement IDs.
- Add and run relevant tests; report what actually ran and any limitations.
- Review diffs before committing. Never discard unrelated work.
- Do not promise listing gains or present an unvalidated prediction as a probability.
