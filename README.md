# IPO Forensic Analysis Engine

A local-first, evidence-driven research tool for analysing **Indian Mainboard IPOs** and preparing auditable, company-specific listing-day research reports.

## Non-negotiable constraints

- **₹0 total budget:** no paid APIs, data, AI, hosting, software, upgrades or paid fallback services.
- **Mainboard IPOs only:** SME IPOs are out of scope.
- **Local-first with a complete manual fallback:** offline research, calculations and reporting work from saved/user-supplied evidence. For an identified IPO, the app must also attempt acquisition through approved source connectors and show per-source outcomes; no provider is assumed until free/permitted access and coverage are verified.
- **Evidence over fluency:** AI never invents values, sources, pages, timestamps or citations.
- **Deterministic finance:** material calculations are reproducible, documented and tested.
- **No unvalidated prediction claims:** scenarios are conditional calculations unless a model is validated on appropriate out-of-sample data.

## Start here

Read the canonical documents in this order:

1. [Project Brief](docs/IPO_Forensic_Analysis_Project_Brief_v1.0.md)
2. [Product Requirements Document](docs/IPO_Forensic_Analysis_PRD_v1.0_APPROVED.md)
3. [Indicator Catalogue & Data Dictionary](docs/IPO_Indicator_Catalogue_and_Data_Dictionary_v1.0.md)
4. [Data Source & Feasibility Audit](docs/IPO_Data_Source_and_Feasibility_Audit_v1.0.md)
5. [Application Flow](docs/app-flow.md)
6. [UI/UX Design Specification](docs/design.md)
7. [Technical Design](docs/TECHNICAL_DESIGN.md)
8. [Database Schema — proposed v0.1](docs/database-schema.md)
9. [Implementation Plan](implementation-plan.md)
10. [Agent rules](AGENTS.md)

The repository Markdown files are the source of truth. Update the existing file when a decision changes; use Git history rather than creating numbered copies or routine download files. Existing historical filenames are preserved for now, and every link must use their actual paths.

## Current status

The detailed product requirements, evidence-source baseline, application flow, UI/UX design baseline, proposed technical architecture and proposed SQLite database schema are recorded. The database-schema document defines a concrete v0.1 persistence baseline, but its migrations have not been implemented or tested, and its field/API alignment must be finalized against the first Data Contract. These documents are specifications, not evidence that the application has been implemented or tested. Before substantive feature development, validate the local technical scaffold, finalize the first Data Contract for the initial vertical slice, approve the initial MVP formula register, and define representative test fixtures. Implementation must remain usable without paid services, a single external provider or AI. Source-acquisition orchestration and core interconnection of available company/offer fundamentals, valuation, QIB/NII/retail subscription and GMP signals are required product capabilities; individual connectors must be supported by dated feasibility evidence.
