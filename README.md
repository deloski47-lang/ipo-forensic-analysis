# IPO Forensic Analysis Engine

A local-first, evidence-driven research tool for analysing **Indian Mainboard IPOs** and preparing auditable, company-specific listing-day research reports.

## Non-negotiable constraints

- **₹0 total budget:** no paid APIs, data, AI, hosting, software, upgrades or paid fallback services.
- **Mainboard IPOs only:** SME IPOs are out of scope.
- **Manual-first and local-first:** the core workflow works from user-supplied documents and manual observations; integrations are optional.
- **Evidence over fluency:** AI never invents values, sources, pages, timestamps or citations.
- **Deterministic finance:** material calculations are reproducible, documented and tested.
- **No unvalidated prediction claims:** scenarios are conditional calculations unless a model is validated on appropriate out-of-sample data.

## Start here

Read the canonical documents in this order:

1. [Project Brief](docs/IPO_Forensic_Analysis_Project_Brief_v1.0.md)
2. [Product Requirements Document](docs/IPO_Forensic_Analysis_PRD_v1.0_APPROVED.md)
3. [Data Source & Feasibility Audit](docs/IPO_Data_Source_and_Feasibility_Audit_v1.0.md)
4. [Indicator Catalogue & Data Dictionary](docs/IPO_Indicator_Catalogue_and_Data_Dictionary_v1.0.md)
5. [Technical Design](docs/TECHNICAL_DESIGN.md)
6. [Agent rules](AGENTS.md)

The repository Markdown files are the source of truth. Update the existing file when a decision changes; use Git history rather than creating numbered copies or routine download files. Existing historical filenames are preserved for now, and every link must use their actual paths.

## Current status

The detailed product requirements and research baseline are recorded. The Technical Design is a **proposed architecture**, not an implemented application or proof of successful runtime tests. Before substantive feature development, validate the local technical scaffold, agree the first Data Contract for the initial vertical slice, approve the initial MVP formula register, and define representative test fixtures. Implementation must remain usable without paid services, live data APIs or AI.
