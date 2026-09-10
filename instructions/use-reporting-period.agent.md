# Use Reporting Period Calculator

## When to use

Use this instruction when a weekly report needs a deterministic Monday-to-Sunday reporting window and the immediately preceding equivalent period. Use `tools/reporting_period.py` when the reference date is known and the periods should be calculated rather than inferred manually.

## Invocation

From the repository root, run:

```text
python tools/reporting_period.py <reference_date>
```

Pass `reference_date` in `YYYY-MM-DD` format. For example:

```text
python tools/reporting_period.py 2026-09-10
```

The reference date may be any date in the target week. The tool returns the Monday and Sunday for that week and the corresponding Monday and Sunday from the prior week.

## Presenting results

Preserve the JSON field names and ISO date values:

```json
{
  "current_start": "2026-09-07",
  "current_end": "2026-09-13",
  "prior_start": "2026-08-31",
  "prior_end": "2026-09-06"
}
```

State that the current period is Monday through Sunday and that the prior period is the immediately preceding seven-day period. Do not change the dates based on assumptions about holidays, time zones, or the current date. Invalid dates must be reported as errors rather than repaired or guessed.
