# Validate Weekly Inputs

- Input format: JSON or YAML object with required keys for reporting window, team capacity, leave, allocation, risks, stakeholder asks, and status override.
- Validate all required fields before any Jira query or report generation begins.
- Check that `reporting_window.start` and `reporting_window.end` are present and use a Monday-to-Sunday range.
- Check that team capacity is numeric or parseable, and that leave and allocation values are non-negative.
- Check that risks, asks, and next-week priorities are lists or objects with required fields when present.
- Reject incomplete or ambiguous data with a clear validation error that names the missing field and reason.
- Processing steps:
  + Parse the input file.
  + Normalize keys to a single schema.
  + Validate required fields and value ranges.
  + Validate date ordering and timezone consistency.
  + Return either a valid normalized payload or a blocked list of errors.
- Output format: structured validation result with `valid`, `errors`, and `warnings` fields.
- Constraints:
  + No silent defaults for missing required values.
  + No fabricated metrics or dates.
  + No raw secrets or credentials in output.
  + Keep output concise and machine-readable.
