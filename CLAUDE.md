# CLAUDE.md

Claude Code: follow [AGENTS.md](AGENTS.md) before taking any repository action.

The detailed requirements and research references live in [docs/](docs/):

- [Project Brief](docs/IPO_Forensic_Analysis_Project_Brief_v1.0.md)
- [Approved PRD](docs/IPO_Forensic_Analysis_PRD_v1.0_APPROVED.md)
- [Indicator Catalogue & Data Dictionary](docs/IPO_Indicator_Catalogue_and_Data_Dictionary_v1.0.md)
- [Data Source & Feasibility Audit](docs/IPO_Data_Source_and_Feasibility_Audit_v1.0.md)
- [Application Flow](docs/app-flow.md)
- [UI/UX Design Specification](docs/design.md)
- [Technical Design](docs/TECHNICAL_DESIGN.md)

The linked existing Markdown files are the canonical sources for their content. Update them in place and preserve their full substance; do not create versioned duplicates for routine changes. The binding constraints are ₹0 total budget, Mainboard IPOs only, local-first/manual-first operation, no AI-invented values, and deterministic tested financial calculations.

The Technical Design is a proposed technical baseline. The Application Flow specifies user-visible journeys and states. Respect each document's decision status: resolve required decisions and validate recommendations before implementing dependent features. Never claim tests or integrations work without actually testing them.

## Required UI/UX workflow

For any frontend, visual design, responsive layout, or animation task, use Anthropic's verified **Frontend Design** plugin/skill for Claude Code: https://claude.com/plugins/frontend-design. Apply it before implementation and use its design-planning/critique workflow. If it is not installed or unavailable in the current Claude Code environment, do not claim to have used it; tell the product owner and request it be enabled before implementing the visual UI.

The skill must obey `docs/design.md`. The product owner owns the hero component: its source is 21st.dev, but do not choose or implement the exact component until the owner supplies its URL/code. Preserve the exact palette and typography, the zero-budget constraint, contrast guidance, reduced-motion/accessibility rules, and free/open-source Motion-only constraint. Before integrating a 21st.dev component, verify its actual author licence and current terms; use no paid items and include a visible link to the original component page/author as required by the applicable terms.