"""Calculate a Monday-to-Sunday reporting period and its prior equivalent."""

import argparse
import json
from datetime import date, timedelta


def reporting_periods(reference_date: date) -> dict[str, str]:
    """Return current and prior Monday-to-Sunday periods containing reference_date."""
    current_start = reference_date - timedelta(days=reference_date.weekday())
    current_end = current_start + timedelta(days=6)
    prior_start = current_start - timedelta(days=7)
    prior_end = current_end - timedelta(days=7)
    return {
        "current_start": current_start.isoformat(),
        "current_end": current_end.isoformat(),
        "prior_start": prior_start.isoformat(),
        "prior_end": prior_end.isoformat(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate current and prior Monday-to-Sunday reporting periods."
    )
    parser.add_argument(
        "reference_date",
        help="Reference date in YYYY-MM-DD format",
    )
    args = parser.parse_args()

    try:
        reference_date = date.fromisoformat(args.reference_date)
    except ValueError as error:
        parser.error(f"reference_date must be YYYY-MM-DD: {error}")

    print(json.dumps(reporting_periods(reference_date), indent=2))


if __name__ == "__main__":
    main()
