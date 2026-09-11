# Implementation Tasks: Weekly Jira/Confluence Status Reporting

**Source plan**: `spec/plan.md`
**Source specification**: `spec/specification.md`
**Task status values**: `Not started`, `In progress`, `Blocked`, `Done`

## Phase 0: Decisions and Contract Freeze

### T001 - Resolve product scope

- **Priority**: P0
- **Dependencies**: None
- **Outcome**: Confirm the React/Node web application as the v1 product and decide whether the Python CLI is retained separately.

**Acceptance criteria**:

- A decision record names the products included in v1.
- All obsolete Python CLI references are removed or explicitly labeled as a separate product.
- `spec/specification.md` and `spec/plan.md` use consistent product terminology.

### T002 - Decide Confluence scope

- **Priority**: P0
- **Dependencies**: T001
- **Outcome**: Decide whether Confluence is an active v1 integration or a future adapter.

**Acceptance criteria**:

- The decision identifies read, search, write, and publication behavior.
- If active, required spaces, page permissions, conflict behavior, and failure handling are documented.
- If deferred, Confluence is represented only as a tested adapter boundary and is excluded from the v1 acceptance path.

### T003 - Define identity and roles

- **Priority**: P0
- **Dependencies**: T001
- **Outcome**: Define authentication, authorization, report visibility, and role permissions.

**Acceptance criteria**:

- Authentication provider and session/token strategy are documented.
- Manager, reviewer, stakeholder, and administrator permissions are mapped to actions.
- Unauthorized and forbidden behavior is defined for API and UI flows.

### T004 - Freeze report lifecycle

- **Priority**: P0
- **Dependencies**: T003
- **Outcome**: Establish canonical states and legal transitions.

**Acceptance criteria**:

- The canonical states are `draft`, `under-review`, `approved`, and `finalized`.
- A transition table defines actor permissions, required fields, and invalid-transition responses.
- Finalized reports cannot be overwritten through normal operations.

### T005 - Decide storage authority and versioning

- **Priority**: P0
- **Dependencies**: T004
- **Outcome**: Define database/file authority, report versions, regeneration, and recovery behavior.

**Acceptance criteria**:

- The authoritative location for rendered Markdown is documented.
- A uniqueness/versioning rule exists for period, scope, and configuration.
- Regeneration after finalization preserves the finalized artifact and creates a defined new version or draft.

### T006 - Freeze period and timezone rules

- **Priority**: P0
- **Dependencies**: T001
- **Outcome**: Define date input, timezone confirmation, boundaries, and partial-week behavior.

**Acceptance criteria**:

- The canonical API period shape is documented.
- `Asia/Kolkata` confirmation ownership and blocking behavior are documented.
- Inclusive/exclusive boundaries and most-recently-completed-week behavior are covered by examples.

### T007 - Freeze metric and input contracts

- **Priority**: P0
- **Dependencies**: T002, T005, T006
- **Outcome**: Approve status mappings, defect rules, trend rules, input schemas, and unavailable-data semantics.

**Acceptance criteria**:

- Completed, in-progress, unresolved, defect, overdue, aging, scope-change, trend, and story-point rules are defined.
- Manual-input fields, types, requiredness, ranges, and collection limits are defined.
- A decision record identifies behavior for empty data, partial data, and missing history.

## Phase 1: Repository and Local Platform Foundation

### T008 - Configure npm workspaces

- **Priority**: P0
- **Dependencies**: T001
- **Outcome**: Create workspace scripts for `apps/web`, `apps/api`, and shared packages.

**Acceptance criteria**:

- A clean checkout can install dependencies from the repository root.
- Workspace scripts can target frontend, backend, shared packages, and all tests.
- No application package contains implementation code outside its declared workspace boundary.

### T009 - Configure TypeScript, Vite, Express, linting, and tests

- **Priority**: P0
- **Dependencies**: T008
- **Outcome**: Establish consistent build, lint, format, and test commands.

**Acceptance criteria**:

- Web and API type checks complete successfully.
- Lint and formatting commands are documented and deterministic.
- Unit and integration test commands run from the root workspace.

### T010 - Add PostgreSQL Docker Compose environment

- **Priority**: P0
- **Dependencies**: T008
- **Outcome**: Run PostgreSQL 15 locally through Docker.

**Acceptance criteria**:

- `docker compose up` starts PostgreSQL 15 with a named volume.
- A health check reports readiness.
- Ports and non-production credentials come from documented environment configuration.
- No real credentials are committed.

### T011 - Add environment validation

- **Priority**: P0
- **Dependencies**: T003, T010
- **Outcome**: Validate runtime configuration and provide a safe `.env.example`.

**Acceptance criteria**:

- Required variables and allowed formats are defined.
- Missing required configuration fails with safe, actionable messages.
- Logs and errors redact credential values.

### T012 - Add database migration foundation

- **Priority**: P0
- **Dependencies**: T010
- **Outcome**: Establish migration scripts and a health-checkable initial schema.

**Acceptance criteria**:

- Migrations run against PostgreSQL 15 from a clean database.
- Migration status can be checked from a documented command.
- A rollback or recovery policy is documented.

### T013 - Add API health and readiness endpoints

- **Priority**: P1
- **Dependencies**: T010, T012
- **Outcome**: Expose service and dependency health.

**Acceptance criteria**:

- Health reports process availability without requiring external services.
- Readiness reports PostgreSQL dependency state.
- Responses use documented JSON shapes and status codes.

### T014 - Add React application shell

- **Priority**: P1
- **Dependencies**: T009, T013
- **Outcome**: Provide the initial route shell and API connectivity check.

**Acceptance criteria**:

- Vite starts the React 18 application.
- The shell has placeholder routes for generation, report detail, and history.
- The UI distinguishes API available, unavailable, loading, and error states.

### T015 - Add CI foundation

- **Priority**: P1
- **Dependencies**: T009, T012, T013, T014
- **Outcome**: Automate type checks, lint, tests, and migration validation.

**Acceptance criteria**:

- CI runs on pull requests.
- Failures identify the failing check and do not expose secrets.
- A clean-machine setup test is documented and reproducible.

## Phase 2: Identity, Configuration, and Data Contracts

### T016 - Implement authentication

- **Priority**: P0
- **Dependencies**: T003, T009
- **Outcome**: Authenticate web users and establish secure sessions or tokens.

**Acceptance criteria**:

- Unauthenticated requests cannot access protected report endpoints.
- Session expiration and logout behavior are defined and tested.
- Tokens and identity claims are not logged or returned unnecessarily.

### T017 - Implement role authorization

- **Priority**: P0
- **Dependencies**: T016, T004
- **Outcome**: Enforce manager, reviewer, stakeholder, and administrator actions.

**Acceptance criteria**:

- Each protected endpoint checks the required role.
- UI actions are hidden or disabled when the role cannot perform them.
- Authorization tests cover allowed, unauthorized, and forbidden cases.

### T018 - Define shared TypeScript schemas

- **Priority**: P0
- **Dependencies**: T007, T008
- **Outcome**: Share validated contracts across web, API, and domain services.

**Acceptance criteria**:

- Schemas exist for report requests, manual inputs, normalized source records, metrics, warnings, sources, and errors.
- Frontend and backend use the same contract definitions.
- Invalid values produce field-level errors without unsafe coercion.

### T019 - Implement configuration persistence and validation

- **Priority**: P0
- **Dependencies**: T007, T012, T018
- **Outcome**: Store and validate Jira scope, mappings, statuses, and timezone.

**Acceptance criteria**:

- Valid configurations can be saved and retrieved by authorized users.
- Ambiguous project/board/filter/JQL selection is rejected before retrieval.
- Configuration changes are versioned or auditable.

### T020 - Implement manual-input validation

- **Priority**: P0
- **Dependencies**: T007, T018
- **Outcome**: Validate JSON/YAML uploads and web-form payloads.

**Acceptance criteria**:

- Required fields, ranges, lengths, list sizes, and reporting-window equality are checked.
- YAML parsing is safe and rejects unsupported or malformed content.
- Validation runs before Jira retrieval or report generation.

### T021 - Implement safe error and secret handling

- **Priority**: P0
- **Dependencies**: T011, T016, T018
- **Outcome**: Standardize safe API errors and redaction.

**Acceptance criteria**:

- Error responses include stable codes, safe messages, field errors, and correlation IDs.
- Tokens, headers, stack traces, and raw third-party payloads are excluded from responses and logs.
- Secret-leak tests pass for normal and failure paths.

## Phase 3: Jira Retrieval Adapter

### T022 - Implement typed Jira adapter

- **Priority**: P0
- **Dependencies**: T007, T018, T019, T021
- **Outcome**: Provide typed issue, board, sprint, history, link, and custom-field retrieval.

**Acceptance criteria**:

- Adapter methods and response types are defined.
- Raw Jira response shapes do not leak into domain services.
- Fixture-backed tests cover every required retrieval method.

### T023 - Implement Jira authentication and scope selection

- **Priority**: P0
- **Dependencies**: T019, T022
- **Outcome**: Authenticate using the approved service/user model and apply one authoritative scope.

**Acceptance criteria**:

- Credentials are loaded only from approved secret sources.
- Valid scope produces the expected JQL and source-scope record.
- Invalid or ambiguous scope fails before a data snapshot is created.

### T024 - Implement pagination, retries, rate limits, and cancellation

- **Priority**: P0
- **Dependencies**: T022
- **Outcome**: Make external retrieval bounded and resilient.

**Acceptance criteria**:

- Pagination retrieves all permitted pages up to the configured maximum.
- Retryable failures use bounded exponential backoff and non-retryable failures stop immediately.
- Rate-limit responses expose retry timing safely.
- Cancellation stops pending retrieval without creating a misleading report.

### T025 - Implement field mapping and normalization

- **Priority**: P0
- **Dependencies**: T006, T007, T022
- **Outcome**: Convert Jira records to the canonical normalized model.

**Acceptance criteria**:

- Required standard and configured custom fields map to shared types.
- Timestamps are converted to the configured timezone.
- Missing optional fields create warnings; missing required data follows the approved blocking policy.

### T026 - Implement source snapshots and provenance

- **Priority**: P1
- **Dependencies**: T023, T024, T025
- **Outcome**: Preserve query scope, source identifiers, retrieval time, pages, and partial-data state.

**Acceptance criteria**:

- A snapshot records scope, query/configuration version, retrieval timestamp, page count, and completeness.
- Every normalized record retains a source identifier.
- Snapshot fixtures are deterministic and contain no secrets.

### T027 - Implement optional Confluence adapter

- **Priority**: P2
- **Dependencies**: T002, T022
- **Outcome**: Add approved Confluence read/search/write behavior or a tested deferred boundary.

**Acceptance criteria**:

- If active, spaces, permissions, versions, conflicts, and failures are tested.
- If deferred, no live Confluence call is required for the v1 acceptance path.
- Confluence failures cannot silently invalidate Jira-only reports unless configured as required.

## Phase 4: Reporting Period and Metrics Engine

### T028 - Implement reporting-period service

- **Priority**: P0
- **Dependencies**: T006, T018
- **Outcome**: Calculate current and prior periods consistently.

**Acceptance criteria**:

- Default and historical periods match approved boundary examples.
- Timezone conversion and Monday/Sunday boundaries are tested.
- Invalid or incomplete periods return documented errors or warnings.

### T029 - Implement status and defect classification

- **Priority**: P0
- **Dependencies**: T007, T025
- **Outcome**: Apply configured status and defect mappings.

**Acceptance criteria**:

- Case and alias behavior is defined and tested.
- Unknown statuses and severities are surfaced as warnings.
- Classification behavior is deterministic for the same configuration.

### T030 - Implement core delivery metrics

- **Priority**: P0
- **Dependencies**: T028, T029
- **Outcome**: Calculate completed, opened, in-progress, overdue, throughput, and backlog.

**Acceptance criteria**:

- Each metric matches approved fixture results.
- Late completion, missing due dates, empty results, and boundary dates are tested.
- Counts and story points remain separate typed values.

### T031 - Implement defect, aging, scope, and trend metrics

- **Priority**: P1
- **Dependencies**: T028, T029, T030
- **Outcome**: Calculate secondary metrics when required data exists.

**Acceptance criteria**:

- Defect backlog and severity/status breakdowns match fixtures.
- Aging start event, scope baseline, trend formula, zero baseline, and rounding are documented and tested.
- Missing history produces explicit unavailable states.

### T032 - Implement metric availability and warning aggregation

- **Priority**: P0
- **Dependencies**: T025, T030, T031
- **Outcome**: Represent unavailable metrics and data-quality warnings safely.

**Acceptance criteria**:

- Missing values are not silently converted to zero.
- Each warning identifies the affected field, metric, or source where possible.
- Zero, unavailable, partial, and blocked states are distinguishable in shared output types.

### T033 - Create golden metric fixtures

- **Priority**: P1
- **Dependencies**: T029, T030, T031, T032
- **Outcome**: Lock approved expected outputs for representative source data.

**Acceptance criteria**:

- Fixtures cover normal, empty, partial, invalid, and historical cases.
- Golden outputs are reviewed and versioned.
- Unit and property tests pass against the fixture set.

## Phase 5: Report Generation and Persistence

### T034 - Create database schema and repositories

- **Priority**: P0
- **Dependencies**: T005, T012, T018, T032
- **Outcome**: Persist reports, inputs, metrics, sources, warnings, and audit events.

**Acceptance criteria**:

- Tables have documented types, keys, nullability, indexes, and foreign keys.
- Repository tests run against PostgreSQL 15.
- Sensitive values are excluded or encrypted according to the approved policy.

### T035 - Implement report versioning and concurrency control

- **Priority**: P0
- **Dependencies**: T004, T005, T034
- **Outcome**: Protect finalized reports and concurrent generation/finalization.

**Acceptance criteria**:

- Concurrent requests cannot overwrite a finalized artifact.
- Duplicate generation behavior is idempotent or creates a documented new version.
- Conflicts return a stable API error and preserve existing data.

### T036 - Implement Markdown report renderer

- **Priority**: P0
- **Dependencies**: T030, T031, T032, T033
- **Outcome**: Render all required sections and appendix data.

**Acceptance criteria**:

- Sections appear in the required order.
- Metrics, warnings, unavailable labels, source scope, definitions, and metadata render correctly.
- User-authored content is sanitized against Markdown/XSS threats.

### T037 - Persist dated report artifacts

- **Priority**: P0
- **Dependencies**: T005, T034, T035, T036
- **Outcome**: Save Markdown, input snapshots, metadata, and database records.

**Acceptance criteria**:

- Artifact identifiers include period and reproducible version information.
- Original drafts and finalized artifacts remain retrievable.
- Failed generation does not create a misleading finalized artifact.

### T038 - Implement generation orchestration

- **Priority**: P0
- **Dependencies**: T020, T023, T026, T028, T030, T031, T034, T036
- **Outcome**: Coordinate validation, retrieval, calculation, rendering, and persistence.

**Acceptance criteria**:

- Generation validates inputs before external requests.
- Successful fixture-backed generation creates a draft and related provenance records.
- Partial and failed retrieval states follow approved semantics.
- A generation summary includes state, warnings, period, and output identifier.

### T039 - Add report lifecycle service

- **Priority**: P0
- **Dependencies**: T004, T035, T037
- **Outcome**: Enforce review, approval, and finalization transitions.

**Acceptance criteria**:

- Valid transitions succeed for authorized actors.
- Invalid transitions fail without changing state.
- Finalization records actor, timestamp, reason if required, and immutable artifact reference.

## Phase 6: React Reporting Workflow

### T040 - Build report-generation form

- **Priority**: P0
- **Dependencies**: T014, T017, T018, T020, T038
- **Outcome**: Collect period and manual context and start generation.

**Acceptance criteria**:

- Form supports default/historical periods and approved manual-input fields.
- Client-side errors match shared schemas without replacing server validation.
- Submit state prevents accidental duplicate generation.

### T041 - Build progress and error states

- **Priority**: P0
- **Dependencies**: T021, T038, T040
- **Outcome**: Show generation progress, warnings, empty data, partial data, failures, and session expiry.

**Acceptance criteria**:

- Each state has an actionable user-facing message.
- Warnings are distinct from blocking errors.
- Tokens, raw third-party responses, and stack traces never appear in the UI.

### T042 - Build report detail view

- **Priority**: P0
- **Dependencies**: T036, T039, T041
- **Outcome**: Present report sections, metrics, sources, warnings, and workflow actions.

**Acceptance criteria**:

- Required sections and appendix are navigable and readable.
- Zero and unavailable values are visually and semantically distinct.
- Source references and metric definitions are available to permitted users.

### T043 - Build review and finalization actions

- **Priority**: P0
- **Dependencies**: T017, T039, T042
- **Outcome**: Support under-review, approval, and finalization from the UI.

**Acceptance criteria**:

- Actions are role-aware and require confirmation where appropriate.
- Finalized reports show immutable state and cannot be overwritten.
- Transition failures leave the displayed report state consistent with the server.

### T044 - Build report history

- **Priority**: P1
- **Dependencies**: T034, T042
- **Outcome**: Browse reports by period, state, and version.

**Acceptance criteria**:

- History supports approved period/state filters and pagination.
- Reports display state, period, version, and generation time.
- Unauthorized reports are absent or safely rejected according to the access policy.

### T045 - Apply accessibility and responsive behavior

- **Priority**: P1
- **Dependencies**: T040, T041, T042, T043, T044
- **Outcome**: Make the workflow usable with keyboard and supported browsers.

**Acceptance criteria**:

- Semantic headings, labels, focus states, and accessible status/error messaging are present.
- Keyboard-only navigation covers generation and lifecycle actions.
- Approved WCAG target and browser matrix pass automated and manual checks.

## Phase 7: History, Confluence, and Operational Integrations

### T046 - Add source-link permission handling

- **Priority**: P1
- **Dependencies**: T026, T042
- **Outcome**: Render accessible Jira/Confluence sources safely.

**Acceptance criteria**:

- Inaccessible sources are labeled without exposing private data.
- URLs are validated and cannot create SSRF behavior in the backend.
- Source identifiers and display URLs remain auditable.

### T047 - Add operational audit history

- **Priority**: P1
- **Dependencies**: T005, T034, T039
- **Outcome**: Expose state and generation events to permitted reviewers.

**Acceptance criteria**:

- Audit events include actor, action, timestamp, previous/new state, and correlation ID.
- Audit history cannot be altered through normal UI actions.
- Retention and visibility rules are enforced.

### T048 - Add approved secondary integrations

- **Priority**: P2
- **Dependencies**: T002, T027, T046
- **Outcome**: Add only integrations with approved contracts and permissions.

**Acceptance criteria**:

- Each integration has an adapter, configuration, permission, failure, and unavailable-state test.
- Disconnected optional integrations do not block core Jira generation.
- Integration data is attributed to its source and retrieval time.

## Phase 8: Security, Reliability, and Performance Hardening

### T049 - Complete security test suite

- **Priority**: P0
- **Dependencies**: T016, T017, T021, T036, T046
- **Outcome**: Validate the application against common web and integration threats.

**Acceptance criteria**:

- Tests cover authentication, authorization, secret leakage, SSRF, Markdown/XSS, YAML safety, injection, and unauthorized access.
- Critical and high findings are resolved or formally accepted with rationale.
- Security tests run in CI.

### T050 - Add observability and operational controls

- **Priority**: P1
- **Dependencies**: T013, T021, T038
- **Outcome**: Provide safe logs, correlation, health, metrics, and alerts.

**Acceptance criteria**:

- Logs are structured and redact secrets and sensitive payloads.
- Correlation IDs cross API, generation, integration, and audit records.
- Health/readiness and failure alerts cover API, database, Jira, and report generation.

### T051 - Choose and implement generation execution model

- **Priority**: P1
- **Dependencies**: T038, T050
- **Outcome**: Use synchronous generation or an asynchronous job model based on measured scope.

**Acceptance criteria**:

- The decision records expected scope, latency, concurrency, and cancellation needs.
- If asynchronous, job creation, status, progress, cancellation, retry, and idempotency are implemented.
- If synchronous, timeout and safe failure behavior are tested.

### T052 - Load and concurrency test the system

- **Priority**: P1
- **Dependencies**: T035, T038, T051
- **Outcome**: Verify performance and data integrity under approved workload.

**Acceptance criteria**:

- Test workload defines issue count, database size, report size, and concurrent users.
- Latency and throughput meet approved percentile targets.
- Concurrent generation and finalization preserve report integrity.

### T053 - Add backup, restore, and recovery procedures

- **Priority**: P1
- **Dependencies**: T034, T037
- **Outcome**: Protect PostgreSQL data and report artifacts.

**Acceptance criteria**:

- Backup frequency, retention, RPO, and RTO are documented.
- A restore test recovers report metadata, artifacts, and lifecycle state.
- Migration rollback and Docker/database outage procedures are documented.

## Phase 9: Documentation and Release

### T054 - Document local development

- **Priority**: P1
- **Dependencies**: T010, T012, T014
- **Outcome**: Enable a new developer to run the stack and tests.

**Acceptance criteria**:

- README documents Node/npm setup, Docker, environment variables, migrations, and workspace commands.
- No real secret is required for fixture-backed development.
- Troubleshooting covers database, Jira, and configuration failures.

### T055 - Document contracts and operations

- **Priority**: P1
- **Dependencies**: T018, T019, T030, T039, T050
- **Outcome**: Publish API, metric, configuration, lifecycle, retention, and security documentation.

**Acceptance criteria**:

- Every API endpoint has request, response, status-code, and error examples.
- Metric definitions and unavailable-data rules are documented.
- Role permissions, report retention, source scope, and secret handling are documented.

### T056 - Prepare release and rollback checklist

- **Priority**: P0
- **Dependencies**: T049, T052, T053, T054, T055
- **Outcome**: Prepare the version 1 handoff package.

**Acceptance criteria**:

- Checklist covers migrations, configuration, secrets, backups, tests, monitoring, and rollback.
- Release candidate evidence is linked to each success criterion.
- Known limitations and deferred Confluence/integration work are recorded.

### T057 - Run version 1 acceptance review

- **Priority**: P0
- **Dependencies**: T045, T047, T048, T056
- **Outcome**: Verify all P1 scenarios and constitutional requirements.

**Acceptance criteria**:

- Browser acceptance tests complete generation, review, approval, finalization, and history flows.
- Metrics, warnings, source provenance, privacy, and security checks pass.
- No unresolved critical data-integrity or secret-exposure issue remains.
- The release decision is recorded by an authorized reviewer.

## Milestone Mapping

| Milestone | Required tasks | Exit evidence |
|---|---|---|
| M0 | T001-T007 | Approved decision records and updated specification |
| M1 | T008-T015 | Clean setup, Docker health, API health, Vite shell, CI |
| M2 | T016-T021 | Auth, roles, schemas, validation, safe errors |
| M3 | T022-T027 | Typed source snapshots and adapter failure tests |
| M4 | T028-T033 | Golden metric fixtures and boundary tests |
| M5 | T034-T039 | Persisted, traceable draft and lifecycle tests |
| M6 | T040-T045 | Browser-tested manager workflow |
| M7 | T046-T048 | Controlled history, sources, and approved integrations |
| M8 | T049-T053 | Security, observability, performance, recovery evidence |
| M9 | T054-T057 | Documentation, release checklist, and acceptance sign-off |
