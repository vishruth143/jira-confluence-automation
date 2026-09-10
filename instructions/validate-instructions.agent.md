# Validate Instruction Files

## Task

Validate every leaf `instructions/*.agent.md` file individually. Exclude `main.agent.md`, which is the catalog rather than a leaf workflow.

## Checks

For each file, verify:

1. It starts with a level-one Markdown title.
2. It states when or why the instruction should be used, either in a purpose heading or descriptive opening text.
3. It defines an actionable workflow using steps, operational bullet points, commands, or imperative prose.
4. It identifies expected inputs, outputs, or result format.
5. It documents constraints, exclusions, validation, or failure handling.
6. It follows the repository convention of focused, practical English Markdown.
## Processing

Use `tools/validate_instructions.py` from the repository root. The script processes files one at a time and writes one Markdown result per source file plus a summary report.

Do not infer missing content. Mark a check as `PASS` only when evidence appears in the file; otherwise report the check as `FAIL` with the missing requirement.
