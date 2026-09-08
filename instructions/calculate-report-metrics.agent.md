# Calculate Report Metrics

- Input format: structured Jira issue data or a normalized issue list with fields for status, priority, dates, story points, labels, severity, and team information.
- Processing steps:
  + Filter issues into the configured reporting window.
  + Separate completed, in-progress, open, and overdue work by status category.
  + Aggregate counts and story points for each metric.
  + Compare current-period values with the prior equivalent period.
  + Flag missing fields as data-quality warnings instead of guessing values.
  + Distinguish counts from story points and never compare them as interchangeable units.
- Output format: Markdown summary or structured JSON with metric names, current values, previous values, trend, and notes.
- Constraints:
  + Use exact definitions for completed work, opened work, overdue work, backlog, throughput, and aging.
  + Mark unavailable metrics as `Not available` when the required source data is missing.
  + Do not fabricate automation or defect metrics from incomplete data.
  + Keep results evidence-based and traceable to Jira source fields.
