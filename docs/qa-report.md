# QA Report

## Project
`jira-confluence-automation`

## Session Summary
This session covered environment startup, UI inspection, screenshot capture, and the main user flow of the application.

## Pages Visited
1. `http://localhost:5173/` — home page / report dashboard
2. Same page after generating a draft report
3. Same page after sending the report to review, approving it, and finalizing it

## Elements Tested
### Home Page
- Text: `COTALITY AUSTRALIA`
- Heading: `Weekly status desk`
- Status text: `Prototype API connected`
- Button: `Generate draft`
- Button: `Create first draft`
- Archive panel and report history count
- Empty-state copy in the workspace panel

### Draft Report State
- Archive item: `2026-08-31 to 2026-09-06 draft Amber`
- Heading: `DRAFT REPORT`
- Report title and status badge
- Metrics:
  - `COMPLETED`
  - `IN PROGRESS`
  - `THROUGHPUT`
  - `DEFECTS OPENED`
  - `DEFECT BACKLOG`
- Data quality note
- Report body text block
- Buttons:
  - `Send to review`
  - `Approve`
  - `Finalize`

### Workflow Actions Tested
- Generated a draft report
- Sent the report to review
- Approved the report
- Finalized the report

## Bugs Found
- No functional UI bugs were found in the tested flow.
- Docker Compose could not start because `docker` was not available on PATH in this environment.
- A Copilot rate-limit error occurred during one request, but it did not block the manual UI test flow.

## Fixes Applied
- Added the Chrome DevTools MCP server to `.vscode/mcp.json`.
- No application code changes were required during this session.

## Current Status
- Main user flow: **passing**
- Draft generation: **passing**
- Review / approve / finalize flow: **passing**
- Docker Compose startup: **blocked by missing Docker CLI in environment**

## Notes
- The app was tested at `http://localhost:5173/`.
- Backend server was running at `http://localhost:3001` during the session.
