# Implementation Plan: Weekly Jira/Confluence Status Reporting

**Specification**: `spec/specification.md`
**Constitution**: `spec/constitution.md`
**Clarifications**: `spec/clarify.md`
**Target stack**: React 18 + Vite + TypeScript, Node.js + Express + TypeScript, PostgreSQL 15 via Docker
**Delivery model**: incremental vertical slices with a working, testable milestone at the end of each phase

## Delivery Principles

- Resolve clarification blockers before implementing dependent behavior.
- Deliver a thin end-to-end slice before adding secondary metrics or integrations.
- Keep Jira and Confluence behind adapters and keep domain calculations provider-independent.
- Treat missing data as an explicit state or warning, never as an invented value.
- Keep generated reports, source references, inputs, and state transitions auditable.
- Keep each milestone deployable or demonstrably runnable locally.

## Phase 0: Decisions and Contract Freeze

**Goal**: remove ambiguity that would cause rework or incompatible implementations.

### Work

- Confirm that the React/Node web application supersedes the Python CLI, or explicitly retain both as separate products.
- Decide whether Confluence is active in version 1. If active, define read/search/write scope; otherwise mark it as a future adapter.
- Define authentication, roles, report visibility, manager/reviewer/stakeholder permissions, and separation-of-duties rules.
- Freeze the lifecycle enum and transitions: `draft`, `under-review`, `approved`, and `finalized`.
- Decide whether PostgreSQL or dated file/object storage is authoritative for rendered Markdown and define recovery behavior.
- Define finalization/versioning rules for regeneration of an already finalized period.
- Confirm `Asia/Kolkata`, the timezone owner, and blocking behavior before confirmation.
- Freeze reporting-period input shape, inclusive/exclusive boundaries, and partial-week behavior.
- Define status mappings, defect classification, story-point completeness threshold, overdue logic, aging, scope change, trend, empty-result, and unavailable-data behavior.

### Milestone M0: Approved contracts

- Decision record exists for every item above.
- Canonical API, database, lifecycle, configuration, manual-input, and metric schemas are approved.
- `spec/specification.md` and `spec/clarify.md` are updated to remove superseded alternatives.

### Gate

No feature implementation proceeds with unresolved choices affecting data ownership, permissions, report states, or metric definitions.

## Phase 1: Repository and Local Platform Foundation

**Goal**: establish a runnable monorepo and repeatable local development environment.

### Work

- Define npm workspaces for `apps/web`, `apps/api`, and shared packages.
- Configure TypeScript, Vite, Express, linting, formatting, and test runners.
- Add Docker Compose for PostgreSQL 15 with a named volume, health check, non-production credentials, and documented port.
- Add environment validation and `.env.example` without real secrets.
- Add database migration tooling and the first migration for a health-checkable schema.
- Add API health and readiness endpoints.
- Add a minimal React shell with route placeholders and API connectivity check.
- Add CI checks for type checking, linting, unit tests, and migration validation.

### Milestone M1: Runnable skeleton

- `docker compose up` starts PostgreSQL 15 with a passing health check.
- API starts and exposes health/readiness responses.
- Web app starts through Vite and can reach the API health endpoint.
- Workspace commands run consistently from a clean checkout.

### Gate

A clean-machine setup test passes without committed secrets or manual file edits.

## Phase 2: Identity, Configuration, and Data Contracts

**Goal**: establish safe access and validated boundaries before external data retrieval.

### Work

- Implement the chosen authentication and session/token strategy.
- Implement roles and authorization for manager, reviewer, stakeholder, and administrator actions.
- Define TypeScript/shared schemas for report requests, manual inputs, normalized Jira records, metrics, warnings, sources, and API errors.
- Implement configuration storage and validation for project keys, boards, filters, JQL, sprint rules, statuses, issue types, labels, components, custom fields, and timezone.
- Enforce exactly one authoritative Jira selection strategy.
- Implement manual-input JSON schema and safe YAML parsing if YAML uploads remain in scope.
- Add validation for reporting-window consistency, ranges, lengths, maximum collection sizes, and status overrides.
- Add secret redaction utilities and safe error mapping.

### Milestone M2: Validated configuration boundary

- Authorized users can save and validate configuration and manual inputs.
- Invalid configuration and inputs return stable field-level errors before any Jira request.
- Shared schemas are consumed by both frontend forms and backend handlers.
- Automated tests cover authorization, invalid input, ambiguous scope, secret redaction, and period mismatch.

### Gate

No external integration or report generation endpoint accepts unvalidated configuration or manual input.

## Phase 3: Jira Retrieval Adapter

**Goal**: retrieve a complete, paginated, normalized source dataset safely.

### Work

- Implement the Node.js Jira adapter with typed methods for issue search, boards, sprints, issue history, links, and custom fields.
- Implement authentication using the approved service or user-account model.
- Add request timeouts, bounded exponential backoff, retryable status handling, rate-limit handling, pagination, and cancellation.
- Implement field mapping for required standard and configured custom fields.
- Normalize timestamps to the confirmed reporting timezone.
- Preserve source identifiers, URLs, query scope, retrieval timestamp, page counts, and partial-data status.
- Return explicit warnings for missing optional fields and block on missing required scope according to the approved policy.
- Implement Confluence adapter only if Phase 0 keeps it in version 1; otherwise keep a tested adapter interface without a live client.

### Milestone M3: Reproducible source snapshot

- A configured test scope produces a typed normalized snapshot from fixture data.
- Pagination and transient-failure tests pass.
- Authentication failures, partial results, rate limits, and missing fields map to documented safe errors/warnings.
- No credential or private request header appears in logs, snapshots, or API responses.

### Gate

Metrics services consume normalized fixtures and adapter interfaces, not raw third-party response shapes.

## Phase 4: Reporting Period and Metrics Engine

**Goal**: implement deterministic, tested calculations independent of the UI.

### Work

- Implement completed, opened, in-progress, overdue, throughput, defect backlog, aging, scope-change, trend, and story-point calculations.
- Implement historical status reconstruction using Jira history where required.
- Implement configured status and defect mappings.
- Implement explicit availability states for missing source data and zero-value distinction.
- Implement current/prior-period comparison with defined zero-baseline and rounding behavior.
- Implement data-quality warning aggregation with source references.
- Add metric definitions and units to each metric snapshot.

### Milestone M4: Golden metric results

- Representative fixtures produce approved expected results for each metric.
- Boundary tests cover period start/end, timezone conversion, late completion, missing due dates, empty results, missing story points, status changes, and unavailable history.
- Counts, story points, rates, and durations remain distinct in types and output.
- Unit and property tests pass for period and metric services.

### Gate

Metric definitions and expected outputs are approved before report layout work depends on them.

## Phase 5: Report Generation and Persistence

**Goal**: create a complete, traceable Markdown draft and persist its artifacts.

### Work

- Implement PostgreSQL migrations and repositories for reports, manual inputs, metric snapshots, source references, warnings, and audit events.
- Implement report versioning, uniqueness, concurrency protection, and finalized-artifact preservation.
- Implement the report renderer with the required section order and unavailable-data wording.
- Include source scope, definitions, warnings, generation timestamp, timezone, tool version, and links in the appendix.
- Persist dated Markdown, input snapshots, metadata, and database records using the approved authority model.
- Implement generation idempotency and safe retry behavior.
- Add sanitization for Markdown rendering and safe handling of user-authored content.

### Milestone M5: Draft report artifact

- A fixture-backed generation request creates a `draft` report and all required artifacts.
- A generated report contains all required sections in the required order.
- A reviewer can trace every displayed metric to a fixture/source reference, manual input, or unavailable state.
- Failed generation leaves no misleading finalized artifact.

### Gate

Golden-file report tests pass and secret/privacy scans find no credentials or individual performance data.

## Phase 6: React Reporting Workflow

**Goal**: expose the core reporting workflow through the web application.

### Work

- Build report-generation form with period selection, configuration status, manual context entry, and upload support if approved.
- Build validation and error presentation with field-level messages and stable error codes.
- Build generation progress, empty, partial-data, failure, unauthorized, and session-expired states.
- Build report detail view with section navigation, metric tables, trends, warnings, definitions, source links, and metadata.
- Build draft review actions and explicit approval/finalization confirmation.
- Build historical report list with period/state filters and detail navigation.
- Ensure keyboard navigation, semantic headings, focus states, accessible status messaging, and responsive layouts.

### Milestone M6: End-to-end manager workflow

- An authorized manager can enter context, generate a draft, review warnings, approve, and finalize a report from the UI.
- Stakeholders can view only reports permitted by their role.
- Finalized reports cannot be overwritten through normal UI actions.
- Frontend component and workflow tests pass against API fixtures.

### Gate

A browser-based acceptance test completes the primary P1 user stories without direct database manipulation.

## Phase 7: History, Confluence, and Operational Integrations

**Goal**: add approved secondary capabilities without weakening the core reporting path.

### Work

- Implement report history search, filtering, pagination, and version display.
- Add Confluence read/search or publication workflows only if approved in Phase 0.
- Add source-link permission handling and inaccessible-source presentation.
- Add operational audit history and report regeneration/version comparison.
- Add optional connectors only after their source contracts and permissions are approved.

### Milestone M7: Controlled integration release

- Historical browsing and source references work for authorized users.
- Any active Confluence workflow has adapter, permission, conflict, and failure tests.
- Optional integrations produce explicit unavailable states when disconnected.

### Gate

Secondary integrations cannot block core Jira report generation unless explicitly configured as required dependencies.

## Phase 8: Security, Reliability, and Performance Hardening

**Goal**: validate the system against production-like failure and abuse cases.

### Work

- Run security tests for authentication, authorization, secret leakage, SSRF, Markdown/XSS, YAML safety, injection, and unauthorized report access.
- Add structured logs, correlation IDs, health/readiness endpoints, redaction, metrics, and alert conditions.
- Decide synchronous versus asynchronous generation based on measured scope; implement job status, polling, cancellation, and idempotency if needed.
- Load-test Jira pagination, database queries, report rendering, and concurrent generation/finalization.
- Add database backup/restore procedures, retention/cleanup, migration rollback guidance, and disaster-recovery checks.
- Test Docker startup ordering, unavailable database behavior, and external-service outages.

### Milestone M8: Release candidate

- Security, accessibility, performance, reliability, migration, and restore checks meet approved thresholds.
- Generation meets the defined percentile latency target for the approved normal scope.
- Concurrent requests cannot overwrite or corrupt finalized reports.
- Operational runbook covers configuration, credentials, failures, backups, and support escalation.

### Gate

Release is blocked by unresolved critical security issues, data-integrity failures, secret exposure, or unexplained metric discrepancies.

## Phase 9: Documentation and Release

**Goal**: make the system operable and maintainable by the intended team.

### Work

- Update README with local setup, Docker, environment variables, migrations, and workspace commands.
- Document API schemas, authentication/authorization, Jira configuration, manual-input schema, metric definitions, report lifecycle, and retention.
- Provide sanitized fixture data and examples for development and testing.
- Document known unavailable metrics and approved future integrations.
- Publish a release checklist and rollback plan.
- Review the constitution for any approved amendments and update the specification after implementation decisions.

### Milestone M9: Version 1 handoff

- A new developer can start the stack and run the test suite from documentation.
- A manager can generate, review, approve, finalize, and retrieve a report using documented workflows.
- Stakeholders can understand report confidence, warnings, source scope, and metric definitions.
- Release artifacts, migrations, runbook, and decision records are versioned.

## Cross-Phase Milestones

| Milestone | Outcome | Primary evidence |
|---|---|---|
| M0 | Decisions and contracts approved | Updated spec, schemas, decision records |
| M1 | Local stack runs | Docker health, API health, Vite app |
| M2 | Inputs and access are validated | Schema and authorization tests |
| M3 | Source data is normalized | Adapter fixtures and failure tests |
| M4 | Metrics are deterministic | Golden metric tests |
| M5 | Draft artifacts are traceable | Golden reports and persistence tests |
| M6 | Manager workflow works in browser | End-to-end UI acceptance tests |
| M7 | Approved secondary integrations work | Integration and permission tests |
| M8 | Release candidate is hardened | Security, load, accessibility, recovery evidence |
| M9 | Version 1 is operable | Documentation and handoff checklist |

## Definition of Done

The implementation is complete when:

- All approved Phase 0 decisions are reflected in the specification and code.
- React 18/Vite, Node.js/Express, and PostgreSQL 15 run through the documented local workflow.
- Authorized managers can generate and finalize a report for the default or historical period.
- Jira data, manual inputs, metrics, warnings, sources, and report metadata are traceable.
- Missing and unavailable data is explicit and never fabricated.
- Draft, review, approval, and finalization rules are enforced and audited.
- No individual performance scoring, credentials, or unauthorized private data is exposed.
- Unit, integration, browser, security, migration, accessibility, performance, and recovery tests pass at approved thresholds.
