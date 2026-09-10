# Use Report Metrics Calculator

## When to use

Use this instruction when normalized Jira-like issue data is available and delivery metrics must be calculated for a reporting period. Use `tools/report_metrics.py` for reproducible counts and story-point totals from a local JSON file. Do not use it as a Jira retrieval client; it only processes the supplied file.

## Input format

The input file must be a JSON object with an `issues` list. Each issue may contain:

- `key`
- `status`
- `created_date` in `YYYY-MM-DD` format
- `completed_date` in `YYYY-MM-DD` format
- `due_date` in `YYYY-MM-DD` format
- `story_points` as a number

Missing dates are not invented. Missing story points on completed issues produce a warning and are excluded from the story-point total.

## Invocation

From the repository root, run:

```text
python tools/report_metrics.py --input <path-to-json> --start <YYYY-MM-DD> --end <YYYY-MM-DD>
```

For example:

```text
python tools/report_metrics.py --input data/issues.json --start 2026-08-31 --end 2026-09-06
```

The command also calculates the prior period as the seven days immediately before the requested period.

## Metric definitions

- `completed`: issues whose `completed_date` is within the requested period.
- `opened`: issues whose `created_date` is within the requested period.
- `in_progress`: issues whose status is `In Progress`, `In-Progress`, or `In_Progress`.
- `overdue`: issues with a due date before the period end that were not completed by their due date.
- `throughput`: the completed issue count.
- `completed_story_points`: story points on completed issues; missing values are excluded and warned about.
- `backlog`: issues without a completion date or completed after the period end.

## Presenting results

Report the `period`, `metrics`, `prior_period_metrics`, and `warnings` fields. Keep counts and story points as separate units. Preserve `Not available` or warning states when source data is missing; never substitute zero or fabricate Jira values. Mention the input file and reporting dates when summarizing results.
