# Feature Specification: Weekly Jira/Confluence Status Reporting

**Feature Branch**: `001-weekly-status-report`
**Created**: 2026-09-11
**Status**: Draft
**Input**: Module 08 weekly status report specification

## Constitution Alignment

- Frontend: React 18, Vite, and TypeScript.
- Backend: Node.js, Express, and TypeScript.
- Database: PostgreSQL 15 running through Docker.
- Jira and Confluence remain external systems of record.
- Reports must be evidence-based, privacy-preserving, deterministic, and auditable.

## Overview

Build a manually triggered web application for the Quality Engineering Manager of the Cotality-Australia project. The application retrieves delivery and quality data from Jira, combines it with manager-provided weekly context, calculates validated metrics, renders a Markdown report, and supports draft, review, approval, and finalization.

The application must make missing, unavailable, or inconsistent data visible. It must not infer individual performance or fabricate metrics.

## User Scenarios & Testing

### User Story 1 - Generate a weekly report (Priority: P1)

As a Quality Engineering Manager, I want to generate a report for the most recently completed Monday-to-Sunday period so that stakeholders receive a consistent status update.

**Acceptance scenarios**:

1. Given valid configuration and manual inputs, when the manager selects Generate, then the system retrieves Jira data, calculates metrics, and creates a draft report.
2. Given no selected period, when the manager selects Generate, then the system uses the most recently completed reporting week.
3. Given a historical week, when the manager selects that week, then the system generates a report for the selected period without changing the current default.
4. Given Jira authentication or required-scope failure, when generation starts, then no report is finalized and the UI shows a clear actionable error.

### User Story 2 - Review data and warnings (Priority: P1)

As a report reviewer, I want to see source scope, metric definitions, and data-quality warnings so that I can assess confidence in the report.

**Acceptance scenarios**:

1. Given a generated draft, when the reviewer opens it, then the report shows the reporting window, Jira scope, generation timestamp, and tool version.
2. Given a missing optional Jira field, when metrics are calculated, then the report contains a warning and does not silently substitute zero.
3. Given unavailable automation data, when the report is rendered, then the metric is labeled `Not available from configured Jira data`.
4. Given a metric, when the reviewer inspects its source link or definition, then the relationship to Jira data or manual input is visible.

### User Story 3 - Supply weekly context (Priority: P1)

As a Quality Engineering Manager, I want to enter team capacity, risks, and next-period priorities so that the report includes context Jira cannot provide.

**Acceptance scenarios**:

1. Given a valid manual-input form or JSON/YAML upload, when the manager saves it, then the system validates the reporting window and required fields.
2. Given missing required manual input, when validation runs, then the system identifies the field and blocks report generation.
3. Given capacity or allocation data, when it is rendered, then it is aggregated by team, squad, or work category and never presented as individual performance.

### User Story 4 - Review and finalize a report (Priority: P1)

As a manager, I want to review and explicitly finalize a draft so that distribution only occurs after approval.

**Acceptance scenarios**:

1. Given a generated draft, when the manager reviews it, then its state is `draft` and the original generated content is preserved.
2. Given a draft, when the manager finalizes it, then its state changes to `finalized` and its metadata and source inputs remain available.
3. Given a finalized report, when a user views it, then the system prevents accidental replacement of the finalized artifact.

### User Story 5 - Browse historical reports (Priority: P2)

As a stakeholder, I want to browse dated reports so that I can compare delivery and quality trends over time.

**Acceptance scenarios**:

1. Given multiple reports, when a user opens report history, then reports are listed by reporting window and state.
2. Given a report, when a user opens its appendix, then the metric definitions, warnings, source scope, and generation metadata are available.

### Edge Cases

- The selected end date precedes the start date.
- The selected period is not a complete Monday-to-Sunday window.
- Jira returns no matching issues.
- Jira pagination returns partial data or a rate-limit response.
- Required Jira fields are missing or contain inconsistent dates.
- A manual input file identifies a different reporting window.
- A report is regenerated for an already finalized period.
- A user lacks permission to view a report or source link.
- PostgreSQL is unavailable during generation or finalization.

## Functional Requirements

### Reporting periods

- **FR-001**: The system MUST default to the most recently completed Monday 00:00 through Sunday 23:59 period.
- **FR-002**: The system MUST accept a historical reporting period override.
- **FR-003**: The system MUST store the configured timezone, defaulting to `Asia/Kolkata` only after explicit confirmation.
- **FR-004**: The system MUST normalize Jira timestamps to the configured timezone before date-based calculations.
- **FR-005**: The system MUST calculate the immediately preceding equivalent period for trend comparisons.

### Jira integration

- **FR-006**: The backend MUST authenticate to Jira Cloud using credentials from environment variables or an approved secret store.
- **FR-007**: The backend MUST support one or more project keys, board IDs, saved filter IDs, base JQL, sprint rules, issue types, statuses, labels, components, and configured custom fields.
- **FR-008**: The system MUST reject ambiguous selection configurations before querying Jira.
- **FR-009**: The Jira adapter MUST support pagination, bounded retries for transient failures, rate-limit handling, and clear authentication errors.
- **FR-010**: The system MUST retrieve, where available, issue key and URL, summary, issue type, status and category, priority, assignee, team or squad, reporter, dates, labels, components, sprint data, story points, fix version, parent or epic, issue links, blocker/dependency links, defect severity, and configured test or automation fields.
- **FR-011**: The system MUST keep Jira integration code behind an adapter so domain services can be tested without Jira access.

### Manual inputs

- **FR-012**: The system MUST accept validated JSON or YAML manual inputs and may provide an interactive web form as a convenience.
- **FR-013**: Manual inputs MUST support team capacity, leave or availability adjustment, squad allocation, manual quality or automation context, next-period priorities, risks, mitigations, stakeholder asks, status override, and rationale.
- **FR-014**: Manual inputs MUST identify their reporting window.
- **FR-015**: The system MUST validate manual inputs before Jira queries or report generation.
- **FR-016**: The system MUST aggregate team context and MUST NOT produce individual performance scores or rankings.

### Metrics

- **FR-017**: The system MUST calculate completed work as issues entering a configured completed status category during the reporting period.
- **FR-018**: The system MUST calculate opened work as issues created during the reporting period.
- **FR-019**: The system MUST calculate in-progress work as issues not completed and in a configured in-progress status at period end.
- **FR-020**: The system MUST calculate overdue work as unresolved issues whose due date is before the period end.
- **FR-021**: The system MUST calculate throughput as completed issue count and completed story points when consistently populated.
- **FR-022**: The system MUST calculate defect backlog, defect counts by severity and status, aging, scope change, and trend when required source data is available.
- **FR-023**: The system MUST label defect escape, reopen, quality, and automation metrics unavailable when required Jira history or source data is not configured.
- **FR-024**: The system MUST keep counts, story points, rates, and durations as separate units.
- **FR-025**: The system MUST emit data-quality warnings for missing fields and MUST NOT silently convert missing values to zero.

### Report content

- **FR-026**: Every report MUST contain sections in this order: Executive Summary, Delivery Progress, Quality Health, Automation Health, Risks and Blockers, Capacity and Allocation, Next Period Plan, Stakeholder Asks, and Appendix.
- **FR-027**: The executive summary MUST include overall status, delivery and quality narrative, accomplishments, top risks or blockers, and stakeholder decisions needed.
- **FR-028**: Delivery Progress MUST include completed work, in-progress work, next-period commitments, sprint or milestone status, throughput, scope change, overdue work, and aging.
- **FR-029**: Quality Health MUST include defects opened, resolved, remaining, severity/status breakdowns, and supported reopen or escape signals.
- **FR-030**: Automation Health MUST show configured coverage, pass/fail, pipeline, and flaky-test signals, or explicit unavailable labels.
- **FR-031**: Risks and Blockers MUST include title, Jira link, impact, owner or team, age, due date, mitigation, and escalation need when available.
- **FR-032**: The Appendix MUST include metric definitions, reporting window, Jira scope or JQL, data-quality warnings, source links, generation timestamp, and tool version.
- **FR-033**: Reports MUST not contain API tokens, raw credentials, or unauthorized private data.

### Workflow and persistence

- **FR-034**: A report MUST support `draft`, `under-review`, `approved`, and `finalized` states.
- **FR-035**: Finalization MUST preserve the original draft, normalized inputs, reporting period, source scope, warnings, and metadata.
- **FR-036**: The system MUST persist report metadata, workflow state, normalized inputs, and audit references in PostgreSQL 15.
- **FR-037**: The system MUST retain generated Markdown reports and input snapshots using a dated, reproducible identifier.
- **FR-038**: Schema changes MUST use reviewed database migrations.
- **FR-039**: Regeneration MUST be repeatable for the same period and source configuration, subject to source-data changes being recorded.

## API Contract

All endpoints are versioned under `/api/v1` and use JSON.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/reports` | List reports by period and state |
| `POST` | `/reports/generate` | Validate inputs, retrieve data, calculate metrics, and create a draft |
| `GET` | `/reports/:id` | Retrieve report metadata and rendered content |
| `GET` | `/reports/:id/metrics` | Retrieve metrics, comparisons, warnings, and definitions |
| `POST` | `/reports/:id/validate` | Re-run validation without finalizing |
| `POST` | `/reports/:id/approve` | Move a draft to approved after review |
| `POST` | `/reports/:id/finalize` | Create the immutable finalized artifact |
| `GET` | `/reports/:id/sources` | Retrieve permitted source references |

Error responses MUST include a stable error code, safe user-facing message, field errors where applicable, and a correlation ID. Raw tokens, request headers, stack traces, and unfiltered third-party responses MUST NOT be returned.

## Frontend Requirements

- The React application MUST provide period selection, manual context entry or upload, configuration status, generation progress, and actionable validation errors.
- The report view MUST provide readable sections, metric tables, trend comparisons, warning states, source links, and draft workflow actions.
- The report history view MUST support filtering by reporting period and lifecycle state.
- The UI MUST distinguish unavailable metrics from zero values.
- The UI MUST not display individual performance rankings or sensitive credentials.
- Loading, empty, error, unauthorized, and finalized states MUST be represented explicitly.

## Data Model

### Report

- `id`
- `period_start`
- `period_end`
- `timezone`
- `state`
- `overall_status`
- `rendered_markdown`
- `source_scope`
- `generation_timestamp`
- `tool_version`
- `created_at`
- `updated_at`
- `finalized_at`

### ManualInput

- `id`
- `report_id`
- `period_start`
- `period_end`
- `capacity_payload`
- `risk_payload`
- `priority_payload`
- `stakeholder_ask_payload`
- `status_override`
- `override_rationale`
- `validation_warnings`

### MetricSnapshot

- `id`
- `report_id`
- `metric_name`
- `value`
- `unit`
- `availability`
- `definition`
- `source_references`
- `warning`

## Non-Functional Requirements

- **NFR-001 Performance**: For a normal configured scope, the UI MUST show generation progress and the backend SHOULD return a draft within 60 seconds, excluding external outages.
- **NFR-002 Reliability**: A failed generation MUST not create a misleading finalized report or lose an existing finalized report.
- **NFR-003 Security**: Secrets MUST be externalized, logs sanitized, and integration permissions limited to required scope.
- **NFR-004 Privacy**: No individual performance metrics or rankings may be stored or rendered.
- **NFR-005 Auditability**: A reviewer MUST be able to identify the period, source scope, inputs, warnings, definitions, and generation metadata for every report.
- **NFR-006 Accessibility**: The frontend MUST support keyboard navigation, visible focus, semantic headings, readable contrast, and accessible status/error messaging.
- **NFR-007 Maintainability**: Jira/Confluence adapters, domain services, API handlers, persistence, and React presentation must remain separately testable.
- **NFR-008 Compatibility**: Local development MUST run with React 18/Vite, Node.js/Express, PostgreSQL 15, and Docker.

## Out of Scope for Version 1

- Automatic email, Teams, Slack, Confluence, or PowerPoint distribution.
- Automatic inference of individual performance or productivity ratings.
- Replacing Jira as the system of record.
- Fully automated capacity, leave, or allocation calculations.
- CI/CD, test-management, incident, or leave-system integrations until interfaces are approved.

## Success Criteria

- **SC-001**: A manager can generate a valid report for the most recently completed Monday-to-Sunday period from the web UI.
- **SC-002**: A manager can regenerate a historical period without changing the default period behavior.
- **SC-003**: Every displayed metric is traceable to Jira source data, a manual input, or an explicit unavailable state.
- **SC-004**: Missing fields and unavailable sources appear as warnings or `Not available` labels and are never silently treated as zero.
- **SC-005**: A report can move through draft, review, approval, and finalization while preserving source inputs and metadata.
- **SC-006**: Team capacity and context are aggregated without exposing individual performance data.
- **SC-007**: Invalid configuration and manual inputs block generation before Jira queries or report persistence.
- **SC-008**: The application passes unit, API integration, frontend workflow, database migration, and security tests defined by the constitution.
