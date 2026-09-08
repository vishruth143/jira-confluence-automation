# Render Weekly Report

- Follow the shared rules in `./instructions/report-writing-constraints.agent.md`.
- Input format: structured data object with project name, reporting period, summary, accomplishments, quality metrics, blockers, capacity, next-period plan, and stakeholder asks.
- Processing steps:
  + Validate required sections are present.
  + Assemble content in the required order: Accomplishments, Blockers, Next Week, or the larger project template if used.
  + Convert structured data into concise Markdown bullet lists.
  + Keep statements factual, brief, and stakeholder-appropriate.
  + Preserve evidence links and metric notes when provided.
- Output format: Markdown only, with bullet lists and no tables or long narrative paragraphs.
- Constraints:
  + Maximum 20 lines total for a concise status report.
  + Include only material blockers and only the most important next-week actions.
  + No raw credentials, no invented numbers, and no unsupported claims.
