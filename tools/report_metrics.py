"""Calculate weekly delivery metrics from normalized issue JSON data."""

import argparse
import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any


IN_PROGRESS_STATUSES = {"in progress", "in-progress", "in_progress"}
DONE_STATUSES = {"done", "closed", "resolved", "complete", "completed"}


def parse_date(value: str, field_name: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{field_name} must be YYYY-MM-DD: {error}") from error


def issue_date(issue: dict[str, Any], field_name: str) -> date | None:
    value = issue.get(field_name)
    if not value:
        return None
    return parse_date(value, f"issue {issue.get('key', '<unknown>')} {field_name}")


def in_period(value: date | None, start: date, end: date) -> bool:
    return value is not None and start <= value <= end


def calculate_metrics(
    issues: list[dict[str, Any]], start: date, end: date
) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    completed = 0
    opened = 0
    in_progress = 0
    overdue = 0
    completed_story_points = 0.0
    missing_story_points = 0

    for issue in issues:
        created = issue_date(issue, "created_date")
        completed_date = issue_date(issue, "completed_date")
        due_date = issue_date(issue, "due_date")
        status = str(issue.get("status", "")).strip().lower()

        if in_period(created, start, end):
            opened += 1
        if in_period(completed_date, start, end):
            completed += 1
            story_points = issue.get("story_points")
            if story_points is None:
                missing_story_points += 1
            else:
                completed_story_points += float(story_points)
        if status in IN_PROGRESS_STATUSES:
            in_progress += 1
        if due_date is not None and due_date < end and (
            completed_date is None or completed_date > due_date
        ):
            overdue += 1

    if missing_story_points:
        warnings.append(
            f"Story points missing for {missing_story_points} completed issue(s); "
            "completed story points exclude them."
        )

    metrics = {
        "completed": completed,
        "opened": opened,
        "in_progress": in_progress,
        "overdue": overdue,
        "throughput": completed,
        "completed_story_points": completed_story_points,
        "backlog": sum(
            1
            for issue in issues
            if (completed_date := issue_date(issue, "completed_date")) is None
            or completed_date > end
        ),
    }
    return metrics, warnings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate weekly metrics from a JSON object containing an issues list."
    )
    parser.add_argument("--input", required=True, type=Path, help="Path to normalized issue JSON")
    parser.add_argument("--start", required=True, help="Reporting period start in YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="Reporting period end in YYYY-MM-DD")
    args = parser.parse_args()

    try:
        start = parse_date(args.start, "start")
        end = parse_date(args.end, "end")
    except ValueError as error:
        parser.error(str(error))
    if end < start:
        parser.error("end must be on or after start")

    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        parser.error(f"could not read JSON input: {error}")
    if not isinstance(payload, dict) or not isinstance(payload.get("issues"), list):
        parser.error("input JSON must be an object with an issues list")

    try:
        metrics, warnings = calculate_metrics(payload["issues"], start, end)
        prior_metrics, prior_warnings = calculate_metrics(
            payload["issues"], start - timedelta(days=7), end - timedelta(days=7)
        )
    except (TypeError, ValueError) as error:
        parser.error(str(error))

    result = {
        "period": {"start": start.isoformat(), "end": end.isoformat()},
        "metrics": metrics,
        "prior_period_metrics": prior_metrics,
        "warnings": warnings + prior_warnings,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
