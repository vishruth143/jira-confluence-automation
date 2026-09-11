# Jira/Confluence Automation Constitution

## Purpose

This constitution governs the Jira/Confluence automation web application. The system must make delivery and quality reporting more consistent, traceable, and safe for managers and stakeholders.

## Technology Standards

- Frontend: React 18 with Vite and TypeScript.
- Backend: Node.js with Express and TypeScript.
- Database: PostgreSQL 15, run locally through Docker.
- API style: JSON over versioned HTTP endpoints under `/api`.
- Shared contracts: frontend and backend data shapes must be defined in reusable TypeScript types or schemas.

## Core Principles

### 1. Evidence Before Inference

- Jira and Confluence remain systems of record.
- Metrics must be traceable to source records, queries, or documented manual inputs.
- Missing or inconsistent data must produce explicit warnings or unavailable states.
- The system must never fabricate values or silently convert missing values to zero.

### 2. Privacy and Least Privilege

- Credentials and tokens must be supplied through environment variables or an approved secret store.
- Secrets must never be committed, logged, returned by APIs, or written to reports.
- Team reporting must be aggregated by project, squad, or role; individual performance scoring is prohibited.
- External integrations must request only the permissions required for their operation.

### 3. Explicit Reporting Workflow

- Reports must support draft, review, approval, and finalized states.
- Finalization must preserve the original draft, source inputs, reporting period, and metadata.
- Every generated report must identify its reporting window, data scope, generation time, and data-quality warnings.

### 4. Deterministic and Auditable Metrics

- The reporting period defaults to the completed Monday-to-Sunday week and supports historical override.
- All timestamps must be normalized to the configured reporting timezone before date-based calculations.
- Counts, story points, rates, and durations must remain distinct units.
- Metric definitions must be documented and implemented in tested backend services.

### 5. Validated Boundaries

- Validate configuration and manual inputs before querying Jira or generating a report.
- Reject ambiguous Jira project, board, filter, sprint, or JQL selection strategies.
- Validate API request bodies at the backend boundary and return clear client-safe errors.
- Do not expose raw third-party errors, credentials, stack traces, or private source data to users.

### 6. Maintainable Web Architecture

- Keep React presentation, frontend state, API access, and feature logic separated.
- Keep Express routing, controllers, validation, integration clients, domain services, and persistence separated.
- Prefer small, focused modules over broad shared abstractions.
- Keep Jira and Confluence integrations behind adapters so the domain logic can be tested independently.

### 7. Testable Delivery

- Every metric definition and validation rule must have automated tests.
- API integration tests must cover authentication failures, incomplete data, invalid input, and report lifecycle transitions.
- Frontend tests must cover report creation, warning display, draft review, and approval flows.
- Database behavior must be tested against PostgreSQL-compatible schemas and migrations.

## Data and Storage Rules

- PostgreSQL stores report metadata, workflow state, normalized inputs, and audit references.
- Generated Markdown reports and input snapshots must be retained with a dated, reproducible identifier.
- Database schema changes require reviewed migrations.
- Development data must be synthetic or appropriately sanitized.

## Review Requirements

A change is ready for review only when it:

- Follows the technology standards and architectural boundaries.
- Includes validation and tests appropriate to its risk.
- Documents changes to API contracts, metric definitions, configuration, or report format.
- Demonstrates that secrets and individual performance data are not exposed.
- Records any unavailable source data instead of presenting unsupported conclusions.

## Governance

This constitution is the source of truth for architectural and quality decisions. Deviations require a written rationale in the change description and explicit review approval. Amendments must preserve evidence-based reporting, privacy, deterministic metrics, and validated boundaries unless the constitution is formally revised.
