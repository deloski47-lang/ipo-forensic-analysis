# AGENTS.md — Repository Operating Rules

## Read before changing anything

Read, in order: `README.md`, `docs/IPO_Forensic_Analysis_Project_Brief_v1.0.md`, `docs/IPO_Forensic_Analysis_PRD_v1.0_APPROVED.md`, `docs/IPO_Indicator_Catalogue_and_Data_Dictionary_v1.0.md`, `docs/IPO_Data_Source_and_Feasibility_Audit_v1.0.md`, `docs/app-flow.md`, `docs/design.md`, and `docs/TECHNICAL_DESIGN.md`, then read `docs/implementation-blueprint.md` and `docs/implementation-plan.md`. The Implementation Blueprint is authoritative for the target file tree, fixed P0 API routes/wire fields/enums/configuration, and frontend/backend boundaries; the Implementation Plan defines delivery phases. Then identify affected requirement IDs and indicator definitions before changing implementation.

The filenames above are the actual existing canonical files in this repository. Preserve their full content and update them in place; do not create more numbered, dated, or duplicate copies as part of routine changes. Use Git history for previous states. Renaming the current historical filenames is a separate, deliberate repository change and must update every reference in the same change.

## Binding project constraints

1. The total project budget is **₹0**. Do not introduce paid APIs, datasets, AI, hosting, software, upgrades, trials that require payment details, or paid fallbacks.
2. Never assume an API, data source, model, feature or free tier is free. Verify current pricing, terms, rate limits, attribution, historical access and failure behaviour before proposing an integration.
3. Scope is **Indian Mainboard IPOs only**. Do not implement SME IPO support.
4. Core operation is local-first with a complete manual/offline fallback. **IPO-name-triggered source-acquisition orchestration and the first interconnected signal checks are P0 product requirements.** Individual source connectors are enabled only after free/permitted-use, coverage, timestamp and failure behaviour are verified. Connector failure must not block manual evidence entry, unrelated valid calculations or reporting, and must never be represented as successful retrieval.
5. AI is assistive only. It must never invent values, sources, citations, locators, timestamps, disclosures or missing data. Unknown is not zero.
6. Material financial calculations must be deterministic, input-traceable and covered by known-answer, missing-input and invalid-input tests.
7. The core workflow must not require a paid service, a hosted database, public deployment, AI API or a single external data provider. Do not interpret this as permission to omit the acquisition orchestrator: implement source discovery/status/history plus approved connectors for signal categories that pass the feasibility gate. If a critical signal has no free/permitted route, record and escalate the scope decision before release.
8. For UI/frontend/animation tasks in Claude Code, use the Anthropic-verified Frontend Design plugin/skill (https://claude.com/plugins/frontend-design). If unavailable, disclose that fact; never claim it was used if it was not.
9. The hero source is 21st.dev, but the product owner selects the exact component. Do not implement it before the source URL/code is supplied. Check the specific licence/current terms, do not incur costs, do not copy protected marketplace preview media, and add a visible link to the original component page/author as required.
10. Preserve the product owner's exact colour palette and typography. Use readable high-contrast combinations, respect reduced motion, and use only free/open-source Motion—not Motion+ or private paid packages.

## Documentation and decisions

- Update the existing canonical file; do **not** create numbered, dated or duplicate versions for routine edits. `docs/implementation-blueprint.md` is the authority for the exact P0 Data Contract and target code layout; do not invent a competing API schema or rename its fields per screen.
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
- Never silently downgrade source acquisition or interconnected QIB/NII/retail, GMP, company/offer and market-signal analysis to manual-only because a provider has not been found; report the feasibility gap and seek an explicit decision.
- Before frontend implementation, follow `docs/design.md` and use the required Frontend Design skill in Claude Code; do not improvise around the owner's hero decision.
