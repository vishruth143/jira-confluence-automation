# Module 08 Completion Report

## Tracked Files
project_spec.md

## Spec Commit History
914fb4a (HEAD -> master) Initial Commit

## project_spec.md Contents
# Weekly Status Report Generator

## 1. Purpose

Create a manually triggered weekly status report generator for the Quality Engineering Manager of the Cotality-Australia project. The tool will retrieve delivery and quality data from Jira, combine it with weekly team capacity/context supplied by the manager, and produce a concise Markdown report for senior leadership and client stakeholders.

The report is intended to reduce manual status collation, make risks visible, and provide traceable evidence for the reported numbers.

## 2. Goals

- Generate a consistent Monday-to-Sunday weekly status report.
- Summarize progress, quality health, automation, capacity, risks, blockers, and trends for a 20-person team.
- Make the report suitable for senior leadership and Cotality-Australia stakeholders.
- Support a draft, review, and approval workflow before distribution.
- Link reported metrics and notable items back to Jira evidence where practical.
- Preserve dated Markdown reports so the team can review historical status.
- Fail clearly when Jira data is unavailable, incomplete, or inconsistent.

## 3. Non-goals for version 1

- Automatic email, Teams, Slack, Confluence, or PowerPoint distribution.
- A web dashboard or browser-based editing experience.
- Automatic inference of individual performance or productivity ratings.
- Replacing Jira as the system of record.
- Fully automated capacity, leave, or allocation calculations.
- Pulling data from CI/CD, test-management, incident, or leave systems until their interfaces are confirmed.

## 4. Users and stakeholders

### Primary user

- Quality Engineering Manager, responsible for a 20-person team on the Cotality-Australia project.
- Runs the generator, supplies weekly context/capacity inputs, reviews the draft, and approves the final report.

### Report audience

- Senior leadership: needs concise delivery confidence, quality posture, risks, and decisions needed.
- Cotality-Australia client stakeholders: needs transparent progress, quality status, commitments, dependencies, and upcoming work.

Individual performance metrics must not be presented. Team data should be aggregated by project, squad, or role unless an explicit business need and privacy approval exist.

## 5. Recommended v1 solution

Build a Python command-line application that:

1. Accepts a reporting date or derives the previous completed Monday-to-Sunday week.
2. Loads configuration and secure Jira credentials from the local environment.
3. Queries Jira Cloud through its REST API using an API token.
4. Normalizes Jira issues, sprint data, history, links, and configured custom fields.
5. Prompts for or loads weekly manual capacity and context inputs.
6. Calculates validated metrics and week-over-week comparisons.
7. Renders a Markdown draft from a versioned template.
8. Writes the draft to a dated output directory for review and approval.
9. Optionally finalizes the approved draft as the canonical report.

This keeps the first release simple to operate while leaving clear adapters for future delivery channels and data sources.

## 6. Reporting period and time zone

- Default reporting window: Monday 00:00 through Sunday 23:59.
- Default run behavior: report the most recently completed reporting week.
- The reporting date/window must be overrideable from the CLI for historical regeneration.
- The user answered `IST`; this specification assumes India Standard Time (`Asia/Kolkata`) because the manager may operate from India. This must be confirmed before implementation. All Jira timestamps must be converted to the configured report time zone before date-based calculations.
- The configured time zone must be stored in configuration, not scattered through code.

## 7. Jira scope and data contract

### Access

- Target Jira deployment: Jira Cloud.
- Authentication: API token associated with a dedicated service or manager account.
- Credentials must come from environment variables or an approved local secret store and must never be committed to the repository or report output.

### Configurable scope

Because the project key and board structure were not supplied, v1 must support configuration for:

- One or more Jira project keys.
- One or more board IDs.
- Optional saved filter IDs.
- Optional base JQL expression.
- Sprint selection rules.
- Issue types, statuses, labels, components, and custom fields used by the project.

The configuration must define one authoritative selection strategy and reject ambiguous configurations. A recommended default is project key plus a configurable JQL filter, with board and sprint data used for delivery metrics.

### Required Jira fields

- Issue key and URL.
- Summary.
- Issue type.
- Status and status category.
- Priority.
- Assignee and configured team/squad field, where available.
- Reporter.
- Created, updated, resolved, and due dates.
- Labels and components.
- Sprint membership and sprint state, where available.
- Story points or the configured estimation field, when present.
- Fix version/release and target milestone, when present.
- Parent/epic relationship.
- Issue links and blocker/dependency relationships.
- Configured defect severity field for bug issues.
- Configured test/automation fields, if Jira stores them.

The tool must identify missing fields and report them as data-quality warnings rather than silently treating missing values as zero.

## 8. Report content

The Markdown report must contain these sections in this order:

### Executive summary

- Overall status indicator: Green, Amber, or Red.
- One-paragraph delivery and quality narrative.
- Key accomplishments.
- Top risks or blockers.
- Decisions or support needed from stakeholders.

### Delivery progress

- Work completed during the reporting period.
- Work in progress at period end.
- Planned or committed work for the next period.
- Sprint or milestone status.
- Throughput and scope change compared with the previous period.
- Overdue work and aging items.

### Quality health

- Defects opened, resolved, and remaining during the period.
- Defects grouped by severity and status.
- Reopened or escaped defects when the source data supports the calculation.
- Test execution status when available.
- Quality trend and notable concerns.

### Automation health

- Automation coverage when available.
- Automated test pass/fail rate when available.
- Pipeline or test-suite health when an approved source is connected.
- Flaky-test signal when an approved source is connected.

For v1, unavailable automation metrics must be labeled `Not available from configured Jira data`; they must not be fabricated.

### Risks and blockers

For each significant item:

- Title and Jira link.
- Impact.
- Owner or responsible team.
- Age and due date.
- Mitigation or next action.
- Escalation/support required.

### Capacity and allocation

- Aggregated team capacity for the period.
- Leave or availability adjustments supplied manually.
- Allocation by squad or work category when supplied.
- Capacity risks affecting next-period commitments.

Manual inputs are aggregated and must not become individual performance scores.

### Next period plan

- Top priorities.
- Expected deliverables.
- Planned testing and automation work.
- Known dependencies and assumptions.

### Stakeholder asks

- Explicit decisions required.
- Approvals required.
- External dependencies requiring action.
- Requested date and owner for each ask.

### Appendix

- Metric definitions and reporting window.
- Jira scope/JQL used.
- Data-quality warnings.
- Source links for notable issues and metrics.
- Generation timestamp and tool version.

## 9. Metric definitions

Metric definitions must be implemented in one documented module and displayed in the appendix.

- **Completed work:** issues entering a configured completed status category during the reporting window.
- **Opened work:** issues created during the reporting window.
- **In progress:** issues not completed and in a configured in-progress status at period end.
- **Overdue:** unresolved issues whose due date is before the report period end.
- **Throughput:** completed issue count and, when consistently populated, completed story points.
- **Defect backlog:** unresolved issues classified as defects at period end.
- **Defect escape/reopen rate:** calculated only when the required Jira history or linked source data is configured; otherwise marked unavailable.
- **Scope change:** additions/removals to the configured sprint or commitment scope after the period began.
- **Aging:** elapsed time from issue creation or configured start event to the period end.
- **Trend:** current-period metric compared with the immediately preceding equivalent reporting period.

The report must distinguish counts from story-point totals and must not compare them as interchangeable measures.

## 10. Manual input model

The first version should accept a small YAML or JSON input file, with an interactive CLI prompt as a convenience. The input should support:

- Team total capacity.
- Leave or availability adjustment.
- Squad-level capacity/allocation, if applicable.
- Manual quality or automation context unavailable in Jira.
- Next-period priorities.
- Risks, mitigations, asks, and stakeholder notes.
- Overall status override and rationale.

The input file must identify the reporting window and must be validated before Jira queries or report generation proceed.

## 11. Configuration and output

Recommended repository layout:

```text
weekly-status-report/
  src/
    report_generator/
      cli.py
      config.py
      jira_client.py
      metrics.py
      inputs.py
      renderer.py
      models.py
  config/
    report.example.yaml
    team.example.yaml
  templates/
    weekly_status.md.j2
  reports/
    YYYY/
      YYYY-MM-DD_to_YYYY-MM-DD/
        draft.md
        inputs.yaml
        metadata.json
  tests/
```

The current workspace is a learning repository, so implementation may use a smaller layout initially. The generated report must not contain API tokens or raw private credentials.

Suggested CLI commands:

```text
python -m report_generator generate
python -m report_generator generate --week-ending 2026-09-06
python -m report_generator validate-inputs --file inputs.yaml
python -m report_generator finalize --draft reports/.../draft.md
```

Exact command names may be adjusted during implementation, but historical regeneration and draft/final distinction are required.

## 12. Draft and approval workflow

1. The manager runs generation for the default or selected week.
2. The tool validates configuration and manual inputs.
3. The tool retrieves Jira data and writes a draft Markdown report.
4. The tool prints a short generation summary, warnings, and output path.
5. The manager reviews and edits the draft if needed.
6. The manager explicitly finalizes the report, preserving the original generated metadata.
7. Distribution to stakeholders is manual in v1.

Generation must be repeatable for the same reporting window. A metadata file should record configuration version, source scope, generation time, and data retrieval status.

## 13. Error handling and data quality

- Retry transient Jira API failures with bounded exponential backoff.
- Respect Jira rate limits and pagination.
- Fail with a non-zero exit code for authentication failure, invalid configuration, or unavailable required scope.
- Continue with warnings for optional fields that are missing.
- Never silently convert API errors or missing values into zero-valued metrics.
- Include a data-quality section in every report, even when there are no warnings.
- Log diagnostic details locally without exposing tokens or sensitive request headers.

## 14. Security and privacy

- Use least-privilege Jira access, limited to the required projects and fields.
- Store the API token outside source control, preferably through environment variables or the organization-approved secret manager.
- Add secret patterns and generated reports to appropriate ignore rules where reports are not intended for version control.
- Sanitize logs and error messages.
- Aggregate team data and exclude individual performance rankings.
- Define retention and repository access rules before reports are committed to shared storage.
- Confirm whether client data may be stored in the repository or must remain on an approved internal system.

## 15. Testing strategy

- Unit tests for reporting-window calculation, time-zone conversion, metric definitions, trend calculation, input validation, and status classification.
- Jira client tests using mocked API responses for pagination, authentication errors, rate limiting, missing fields, and empty results.
- Contract fixtures for representative issue, sprint, history, link, and custom-field payloads.
- Snapshot or golden-file tests for Markdown rendering.
- Integration test against a non-production Jira project or approved test fixture, never against production by default.
- Security tests confirming tokens do not appear in logs or generated files.
- Acceptance test: a manager can generate, review, and finalize a complete report for a selected week.

## 16. Acceptance criteria for v1

- A user can configure Jira scope and generate a report for the previous completed week.
- A user can regenerate a selected historical week.
- The report includes all mandatory sections listed in this specification.
- Delivery and defect metrics reconcile with the configured Jira query and are traceable through links or appendix evidence.
- Missing optional data produces visible warnings.
- Manual capacity/context input is validated and reflected in the report.
- The output is concise, readable Markdown suitable for senior leadership and client review.
- Draft output can be reviewed and explicitly finalized without losing provenance.
- No secrets or individual performance rankings appear in output.
- Automated tests cover the core calculations and representative failure modes.

## 17. Open decisions and assumptions

The following require confirmation before implementation is considered production-ready:

1. Is `IST` India Standard Time (`Asia/Kolkata`), or another time zone?
2. What are the Jira project keys, board IDs, saved filters, and authoritative JQL scope?
3. Which Jira custom fields represent squad/team, severity, story points, test status, automation, and release/milestone?
4. What status names and status categories represent completed, blocked, deferred, and in-progress work?
5. What are the 20-person team’s squads, ownership mappings, and aggregate capacity rules?
6. Should report history be committed to Git, kept locally, or stored in an approved shared system?
7. What approval and distribution process is required after v1: email, Confluence, Teams, or another channel?
8. Which external systems provide authoritative test execution, automation, incident, leave, and release data?
9. What retention, client-data, and hosting policies apply?
10. What launch date and acceptable report-generation time are expected?

## 18. Recommended implementation phases

### Phase 1: Foundation

- Establish Python package, CLI, configuration schema, logging, and secret handling.
- Implement reporting-window and time-zone behavior.
- Add fixture-driven tests.

### Phase 2: Jira and metrics

- Implement Jira Cloud client with pagination, retries, and scope validation.
- Normalize issue data and implement delivery, quality, risk, and trend metrics.
- Add data-quality warnings and source links.

### Phase 3: Inputs and rendering

- Implement manual capacity/context input validation.
- Add Markdown template and mandatory report sections.
- Add draft metadata and historical output paths.

### Phase 4: Acceptance and hardening

- Run against approved non-production or fixture data.
- Validate report content with the manager and representative stakeholders.
- Document operating procedures, access controls, and unresolved open decisions.

## 19. Success measures

- The manager can produce a reviewed weekly report without manually collecting the core Jira metrics.
- Stakeholders can identify current delivery confidence, quality posture, top risks, and required decisions quickly.
- Report numbers are reproducible for a selected reporting window.
- The process exposes missing or unreliable source data rather than hiding it.
- The report remains maintainable as the project’s Jira configuration and delivery channels evolve.