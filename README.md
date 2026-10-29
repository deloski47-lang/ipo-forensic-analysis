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
8. [Database Schema — proposed v0.2](docs/database-schema.md)
9. [Implementation Blueprint & Data Contract](docs/implementation-blueprint.md)
10. [Implementation Plan](docs/implementation-plan.md)
11. [Agent rules](AGENTS.md)

The repository Markdown files are the source of truth. Update the existing file when a decision changes; use Git history rather than creating numbered copies or routine download files. Existing historical filenames are preserved for now, and every link must use their actual paths.

## Current status

The project requirements, evidence-source baseline, application flow, UI/UX design, technical architecture, proposed SQLite schema, and implementation plan are recorded in the canonical Markdown documents. The [Implementation Blueprint & Data Contract](docs/implementation-blueprint.md) now fixes the P0 frontend/backend stack, target file tree, API paths, JSON fields, nullability, enums, error envelope, configuration variables, local storage layout and build gates. These are specifications, not evidence that the application has been implemented or tested. Before feature development, validate the local scaffold, align docs/database-schema.md and migration 0001 with the blueprint, approve the initial P0 formula register and define representative fixtures. Implementation must work without paid services, a single external provider or AI. Source-acquisition orchestration and interconnection of available fundamentals, valuation, QIB/NII/retail subscription and GMP signals remain required; connectors need dated feasibility evidence before enablement.


## Local development — Phase 0 scaffold

The working scaffold is being built on branch build/phase-0-scaffold. It is not merged into main yet.

### Prerequisites

- Python 3.11 or newer.
- Node.js 22.22 or newer (the chosen React Router v8 release requires Node.js 22.22+; the current Vite release also has a minimum Node.js version).
- Git.

### Start the backend (Windows PowerShell)

    cd backend
    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -e ".[dev]"
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

The initial GET /api/v1/health endpoint should respond. It intentionally reports the database as not initialized until the schema/migration milestone is implemented.

### Start the frontend (a second terminal)

    cd frontend
    npm install
    npm run dev

Open http://127.0.0.1:5173. The screen should show whether the local API is reachable. From the frontend folder, run npm run typecheck, npm run lint and npm test. From the backend folder, run pytest.

### Important current limitation

This scaffold is only the first build foundation. Case creation, persistent SQLite models/migrations, evidence upload, manual fact entry, acquisition orchestration, analysis runs, scenario calculations and reports are not implemented by the scaffold commit. Do not enter real research data until persistence and backup/restore have been implemented and tested.
