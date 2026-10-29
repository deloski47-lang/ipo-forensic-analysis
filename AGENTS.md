# AGENTS.md — Repository Operating Rules

## Read before changing anything

Read, in order: `README.md`, `docs/IPO_Forensic_Analysis_Project_Brief_v1.0.md`, `docs/IPO_Forensic_Analysis_PRD_v1.0_APPROVED.md`, `docs/IPO_Indicator_Catalogue_and_Data_Dictionary_v1.0.md`, `docs/IPO_Data_Source_and_Feasibility_Audit_v1.0.md`, `docs/app-flow.md`, and `docs/TECHNICAL_DESIGN.md`. Then identify the affected requirement IDs and indicator definitions before changing implementation.

The filenames above are the actual existing canonical files in this repository. Preserve their full content and update them in place; do not create more numbered, dated, or duplicate copies as part of routine changes. Use Git history for previous states. Renaming the current historical filenames is a separate, deliberate repository change and must update every reference in the same change.

## Binding project constraints

1. The total project budget is **₹0**. Do not introduce paid APIs, datasets, AI, hosting, software, upgrades, trials that require payment details, or paid fallbacks.
2. Never assume an API, data source, model, feature or free tier is free. Verify current pricing, terms, rate limits, attribution, historical access and failure behaviour before proposing an integration.
3. Scope is **Indian Mainboard IPOs only**. Do not implement SME IPO support.
4. Core operation is local-first and manual-first. Failure or absence of an optional integration must not block evidence entry, deterministic calculation or reporting.
5. AI is assistive only. It must never invent values, sources, citations, locators, timestamps, disclosures or missing data. Unknown is not zero.
6. Material financial calculations must be deterministic, input-traceable and covered by known-answer, missing-input and invalid-input tests.
7. The full core workflow must not require a paid service, a hosted database, a public deployment or an AI/data API.

## Documentation and decisions

- Update the existing canonical file; do **not** create numbered, dated or duplicate versions for routine edits.
- Use Git history for previous states. Do not generate routine download copies.
- When a material product, data, architecture or methodology decision is made, record the decision, rationale/evidence, alternatives and consequences in the relevant canonical document in the same change.
- If canonical documents conflict or a decision is missing, flag it. Follow the product owner's explicit binding decisions and do not silently choose the easiest implementation.
- Preserve source links, tables, requirement IDs and approved substance when editing documents.
- Do not treat a proposed recommendation as an approved or implemented decision unless its status says so.

## Evidence, claims and review

- Prefer primary sources for material facts. Record publication/event/retrieval times, period, source identity and locator when available.
- Label observations as verified, candidate awaiting review, user-entered-unverified, calculated, conflicting, unavailable, not-applicable, stale or invalid as appropriate.
- Preserve conflicts; never silently average or overwrite them.
- Verify externally changeable claims. Do not claim that a service is free, available, reliable or permitted without checking current authoritative sources.
- SAWA lesson: Google Trends/pytrends did not work as expected; exact cause unknown. NewsAPI was tried as an alternative but is neither required nor an approved core dependency.

## Delivery discipline

- Keep changes scoped to approved requirements or an explicitly documented prerequisite.
- Add and run relevant tests; report what actually ran and any limitations.
- Review diffs before committing. Never discard unrelated work.
- Do not promise listing gains or present an unvalidated prediction as a probability.
- Never claim the application or a test was verified unless it was actually run. A documentation/repository review is not a runtime test.
