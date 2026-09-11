# Specification Review: Gaps and Clarifications

**Reviewed**: `spec/constitution.md`, `spec/specification.md`
**Review stance**: senior implementation review
**Status**: Clarifications required before production implementation

## 1. Contradictions

### C-001: Web application versus Python CLI

The constitution and specification require React 18/Vite plus Node.js/Express, but the source Module 08 specification still calls the recommended v1 solution a Python command-line application and lists Python module commands. Decide whether the web application supersedes the Python CLI, whether both are required, or whether the CLI is removed from scope. Update all examples and acceptance criteria consistently.

### C-002: Confluence named as a system of record but not specified as a feature

The constitution and specification refer to Jira and Confluence, but the requirements define only Jira retrieval and Jira source links. Decide whether Confluence is an active v1 integration, a future adapter, or simply project naming. If active, add use cases, permissions, fields, endpoints, failure behavior, and acceptance tests.

### C-003: Report lifecycle states are not aligned

The constitution requires `draft`, `review`, `approval`, and `finalized` states. The detailed specification uses `draft`, `under-review`, `approved`, and `finalized`. Define the canonical enum and allowed transitions, including whether `review` and `approval` are states or actions.

### C-004: Report storage is split between database and files

The constitution says PostgreSQL stores report metadata and workflow state while generated Markdown and input snapshots are retained as dated artifacts. The specification also includes `rendered_markdown` inside the `Report` model. Decide whether Markdown is authoritative in PostgreSQL, the filesystem/object store, or both, and define consistency and recovery rules.

### C-005: Finalized immutability is ambiguous

The specification says finalization creates an immutable artifact, but also requires regeneration for the same period. Define whether regeneration creates a new version, is forbidden after finalization, or creates a new draft while preserving the finalized version.

## 2. Scope and user authorization

### G-001: Authentication and authorization are missing

The specification does not define how users authenticate to the web app, how manager/reviewer/stakeholder roles are assigned, or which users may generate, review, approve, finalize, view, or download reports. Define identity provider, session/token strategy, role permissions, and tenant/project isolation.

### G-002: Approval permissions are missing

It is unclear whether the same person may generate, approve, and finalize a report, whether separation of duties is required, and whether approval requires a comment or reason. Define these rules and audit requirements.

### G-003: Jira identity mapping is missing

Define how the authenticated web user maps to a Jira account or service account, whether all users share a service account, and how source permissions are enforced when displaying issue links.

### G-004: Stakeholder access is undefined

The P2 historical-report user is called a stakeholder, but no read-only access model, invitation flow, or report visibility boundary is specified. Define whether reports are internal-only, project-scoped, or publicly shareable within the organization.

### G-005: Audit trail is underspecified

`audit references` and metadata are mentioned but no event model is defined. Specify which actions are recorded, actor identity, timestamp, source version, previous state, new state, reason, retention, and tamper protection.

## 3. Jira and Confluence integration

### G-006: Jira adapter contract is incomplete

Define adapter methods, request/response types, pagination limits, timeout values, retryable status codes, retry count, backoff policy, rate-limit handling, and cancellation behavior.

### G-007: Selection strategy rules are not concrete

The specification requires one authoritative selection strategy and rejects ambiguity, but does not define valid combinations or precedence among project keys, boards, filters, base JQL, sprint rules, issue types, labels, and components. Define the schema and examples of valid and invalid configurations.

### G-008: Jira field mappings are not configurable enough

The required fields include story points, team, severity, testing, and automation fields, but their Jira custom-field IDs and fallback behavior are unspecified. Define field mapping configuration, type validation, missing-field handling, and whether a run can proceed when a configured field is absent.

### G-009: Historical issue state calculation is unclear

Metrics such as in-progress-at-period-end, defect backlog, scope change, aging, and overdue work require historical state or event data. Define which Jira history events are required, how status at the period boundary is reconstructed, and what happens when history is unavailable.

### G-010: Confluence contract is absent

If Confluence remains in scope, define spaces/pages to read, CQL or equivalent queries, page version handling, links, permissions, write operations, conflict behavior, and whether reports are ever published there. If it is out of scope, remove it from the product name and constitution references or mark it as a future adapter.

### G-011: Third-party API version and integration mechanism are absent

Specify whether the backend uses the Jira/Confluence REST APIs directly or an MCP server, the supported API versions, required scopes, and local versus hosted integration configuration.

### G-012: Source link behavior is unclear

Define whether source links are stored as URLs, issue/page identifiers, or both; how inaccessible links are represented; and whether links are validated during generation or only rendered.

## 4. Reporting periods and time

### G-013: "Most recently completed" is ambiguous

Define behavior when the current time is during Sunday, at midnight Monday, or in a daylight-saving timezone. State whether the current incomplete week is excluded and which clock/timezone determines completion.

### G-014: Period input shape is inconsistent

The requirements accept a historical period override but do not define whether the API accepts `weekEnding`, `periodStart` and `periodEnd`, or a reference date. Define one canonical request shape and validation rules.

### G-015: Full-week validation is unclear

The edge cases mention an incomplete Monday-to-Sunday period, but the requirements do not say whether partial periods are rejected, allowed with warnings, or allowed only for historical data.

### G-016: Timestamp precision is unspecified

Define inclusive/exclusive boundaries, timestamp precision, handling of null dates, invalid dates, and dates without timezone offsets. Specify how Jira timestamps are converted before comparisons.

### G-017: Timezone confirmation is unresolved

The requirement says `Asia/Kolkata` is the default only after explicit confirmation, but there is no defined owner, confirmation mechanism, or fallback if confirmation has not occurred. Define the configuration state and blocking behavior.

## 5. Metric definitions

### G-018: Status categories are not defined

Define the exact configured values for completed, in-progress, unresolved, cancelled, reopened, and blocked statuses. Specify case sensitivity, status-name versus status-category matching, and how unmapped statuses are handled.

### G-019: Overdue logic conflicts with due-date wording

FR-020 defines overdue as unresolved issues with a due date before period end, while the earlier implementation and backlog imply completion by due date matters. Define whether an issue completed late remains overdue, whether due date equals period end, and how missing due dates are treated.

### G-020: Scope change has no source event definition

Define the commitment baseline, when it is captured, what additions/removals count, and how sprint changes or JQL changes affect the calculation.

### G-021: Aging has no start-event precedence

Define whether aging starts at creation, a configured status transition, sprint entry, or another event, and how missing history affects the result. Define units and rounding.

### G-022: Defect classification is incomplete

Define whether defect classification uses issue type, a configured label, project, or custom field. Define severity ordering, unknown severity, reopened defects, and defects moved between statuses during the period.

### G-023: Trend calculation is incomplete

Define the comparison output for zero baselines, unavailable prior data, percentage versus absolute change, rounding, and whether favorable direction differs by metric.

### G-024: Story-point completeness threshold is missing

The requirement says completed story points are used when consistently populated, but does not define “consistently.” Set a completeness threshold and behavior for mixed estimation systems or negative/non-numeric values.

### G-025: Empty data behavior is unspecified

Define whether a valid query returning zero issues produces a successful zero report, a warning, or a blocked generation. Distinguish no data from failed data retrieval.

### G-026: Manual overrides versus calculated metrics are unresolved

Define which fields may be overridden, whether overrides replace or annotate calculated values, who may override them, and how the original value and rationale are retained.

## 6. Manual inputs and validation

### G-027: Manual input schema is not defined

Provide a canonical JSON schema or TypeScript schema with field names, types, required/optional status, allowed ranges, maximum lengths, list sizes, and examples for capacity, leave, allocation, risks, priorities, asks, and status override.

### G-028: YAML support is unclear for a JSON API

The web API is JSON-based but manual inputs may be YAML uploads. Define upload content types, parser/library, size limits, duplicate keys, unsafe YAML features, and error reporting.

### G-029: Reporting-window consistency rule is missing

Define whether manual input dates must exactly equal the selected report period and how mismatches are surfaced. Specify whether a user can save inputs before selecting a period.

### G-030: Risk and stakeholder-ask structures are incomplete

Define required fields, ownership format, due-date rules, priority/severity values, status values, and maximum item counts for risks, blockers, mitigations, and asks.

## 7. API and frontend behavior

### G-031: API request and response schemas are missing

Endpoint names are listed, but request bodies, response shapes, pagination, filtering, sorting, status codes, validation errors, and idempotency behavior are not defined. Add versioned schemas and examples for every endpoint.

### G-032: Long-running generation behavior is unclear

A 60-second target is given, but no asynchronous job model, progress events, polling endpoint, cancellation, retry, or duplicate-generation behavior is specified. Decide between synchronous generation and a job resource.

### G-033: Error codes are not enumerated

Define stable codes for invalid input, invalid configuration, unauthorized, forbidden, Jira authentication failure, rate limiting, partial data, database failure, conflict, and unavailable metrics.

### G-034: Pagination and large result behavior are missing

Define maximum Jira results, backend page size, UI pagination or virtualization, memory limits, and whether reports include all matching records or a bounded subset.

### G-035: Frontend routing and state ownership are incomplete

Define required routes, URL state, query caching, form state, optimistic updates, refresh behavior, unsaved-change handling, and behavior after session expiration.

### G-036: Markdown rendering and editing are unclear

The manager is said to review and possibly edit a draft, but the UI does not define whether editing is supported, whether edits are stored separately from generated content, which Markdown is allowed, or how sanitization prevents script injection.

### G-037: Download and export behavior is absent

Define whether users can download Markdown, JSON metadata, or PDF; filename conventions; content disposition; and authorization checks.

### G-038: Accessibility and browser support lack measurable targets

The constitution requires accessibility, but the specification has no target standard or browser matrix. Define WCAG level, supported desktop/mobile browsers, and test tooling.

## 8. Database and operations

### G-039: Database schema is not relationally specified

The data model lists fields but not types, nullability, keys, indexes, foreign keys, uniqueness, JSONB usage, or migration tooling. Define the PostgreSQL schema and retention indexes.

### G-040: Report versioning and uniqueness are missing

Define uniqueness for period, scope, and configuration version; whether multiple drafts can coexist; and how report versions are numbered.

### G-041: Retention and cleanup are absent

The constitution requires retained artifacts, but no retention duration, archival policy, deletion workflow, or privacy deletion behavior is specified.

### G-042: Docker development contract is absent

Define the Docker Compose services, PostgreSQL volume, port, health check, migration startup order, credentials, seed data policy, and behavior when Docker is unavailable.

### G-043: Environment configuration is incomplete

List required environment variables, validation timing, secret source, development defaults, production restrictions, and configuration reload behavior. Never place example secrets in committed files.

### G-044: Observability is underspecified

Define structured logs, correlation IDs, metrics, tracing, health/readiness endpoints, redaction rules, and alert conditions for Jira, database, and generation failures.

### G-045: Concurrency and locking are missing

Define behavior when two users generate or finalize the same period concurrently, including database locks, idempotency keys, conflict responses, and preservation of finalized artifacts.

### G-046: Backup and recovery are absent

Define PostgreSQL backup frequency, report artifact backup, restore testing, recovery point objective, and recovery time objective.

## 9. Testing and acceptance

### G-047: Test fixtures and environments are undefined

Define sanitized Jira fixtures, manual-input fixtures, PostgreSQL test strategy, browser test environments, and whether external integration tests run against a sandbox or mocks.

### G-048: Security acceptance tests are incomplete

Add tests for authentication, authorization, secret leakage, SSRF through source URLs, Markdown/XSS, YAML parser safety, injection, rate limits, and unauthorized report access.

### G-049: Performance acceptance criteria are too vague

“Normal configured scope” and 60 seconds are not measurable. Define issue count, custom-field count, concurrent users, database size, percentile latency, and maximum report size.

### G-050: Failure semantics are incomplete

Define whether partial Jira data can produce a draft, how partial retrieval is labeled, when generation is blocked, and whether retries can create duplicate artifacts.

### G-051: Success criteria are not independently verifiable

Several success criteria use terms such as “valid,” “traceable,” and “appropriate” without testable thresholds. Add concrete assertions, fixture identifiers, expected response codes, and required UI states.

## Recommended decision order

1. Resolve the web-app versus Python-CLI scope and decide whether Confluence is active in v1.
2. Define identity, roles, report lifecycle transitions, finalization/versioning, and report visibility.
3. Freeze the reporting-period, manual-input, Jira field-mapping, and metric schemas.
4. Define API contracts, asynchronous generation behavior, persistence model, and Docker development contract.
5. Add measurable security, performance, accessibility, reliability, and acceptance tests.
