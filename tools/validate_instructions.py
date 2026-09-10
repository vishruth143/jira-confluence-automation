"""Validate instruction files independently and write Markdown results."""

import argparse
import re
from pathlib import Path


CHECKS = (
    ("title", re.compile(r"^#\s+\S+", re.MULTILINE), "level-one Markdown title"),
    (
        "purpose",
        re.compile(
            r"(^##\s+(When to use|Task|Purpose|Usage)\s*$)|(^-\s+(Input|Processing|Output|Constraints))",
            re.MULTILINE | re.IGNORECASE,
        ),
        "use case, task, or operational purpose guidance",
    ),
    (
        "workflow",
        re.compile(
            r"(^\s*\d+\.\s+\S)|(^\s*[-+]\s+\S)|(^```)|\b(run|use|pass|report|preserve|state|do|calculate|validate|create|define|filter|aggregate)\b",
            re.MULTILINE | re.IGNORECASE,
        ),
        "actionable steps, bullets, commands, or imperative prose",
    ),
    (
        "io",
        re.compile(r"(input|output|result|format|invocation|presenting)", re.IGNORECASE),
        "input, output, or result guidance",
    ),
    (
        "constraints",
        re.compile(r"(constraint|must|should|reject|error|warning|missing|exclude|do not)", re.IGNORECASE),
        "constraints or failure handling",
    ),
    (
        "focused",
        re.compile(r"\S", re.MULTILINE),
        "non-empty practical Markdown content",
    ),
)


def check_file(path: Path) -> list[tuple[str, str, str]]:
    content = path.read_text(encoding="utf-8")
    body_after_title = re.sub(r"^#\s+[^\n]+\n?", "", content, count=1)
    results = []
    for name, pattern, evidence in CHECKS:
        if name == "purpose":
            status = "PASS" if pattern.search(content) or body_after_title.strip() else "FAIL"
        else:
            status = "PASS" if pattern.search(content) else "FAIL"
        results.append((name, status, evidence))
    return results


def render_result(path: Path, results: list[tuple[str, str, str]]) -> str:
    lines = [f"# Validation: {path.name}", "", f"Source: `{path}`", "", "| Check | Status | Evidence |", "|---|---|---|"]
    lines.extend(f"| {name} | {status} | {evidence} |" for name, status, evidence in results)
    failures = [name for name, status, _ in results if status == "FAIL"]
    lines.extend(["", f"Overall: {'FAIL' if failures else 'PASS'}"])
    if failures:
        lines.append(f"Failed checks: {', '.join(failures)}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate instruction files independently.")
    parser.add_argument("--source", type=Path, default=Path("instructions"))
    parser.add_argument("--output", type=Path, default=Path("work/instruction-validation-results"))
    args = parser.parse_args()

    files = sorted(path for path in args.source.glob("*.agent.md") if path.name != "main.agent.md")
    args.output.mkdir(parents=True, exist_ok=True)
    for stale_result in args.output.glob("*-validation.md"):
        stale_result.unlink()
    summary = ["# Instruction Validation Summary", "", f"Files processed: {len(files)}", ""]
    for path in files:
        results = check_file(path)
        result_path = args.output / f"{path.stem}-validation.md"
        result_path.write_text(render_result(path, results), encoding="utf-8")
        status = "PASS" if all(item[1] == "PASS" for item in results) else "FAIL"
        summary.append(f"- `{path}`: {status} -> `{result_path}`")

    (args.output / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"Files processed: {len(files)}")
    print(f"Results directory: {args.output}")


if __name__ == "__main__":
    main()
