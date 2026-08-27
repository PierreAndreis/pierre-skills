#!/usr/bin/env python3
"""Validate the design skill router, playbooks, examples, and behavior evals."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_PLAYBOOK_HEADINGS = {"## When to use", "## Inputs", "## Completion", "## Escalate"}


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON in {path.relative_to(path.parents[1])}: {exc}")
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    root = Path(args.skill).resolve()
    errors: list[str] = []

    try:
        entry = root / "SKILL.md"
        text = entry.read_text(encoding="utf-8")
        line_count = len(text.splitlines())
        if line_count >= 100:
            errors.append(f"SKILL.md has {line_count} lines; expected fewer than 100")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            errors.append("SKILL.md frontmatter markers are missing")

        links = re.findall(r"\[[^]]+\]\(([^)]+)\)", text)
        local_links = [link for link in links if "://" not in link and not link.startswith("#")]
        for link in local_links:
            if not (root / link).is_file():
                errors.append(f"missing linked file: {link}")

        indexed = {link for link in local_links if link.startswith("playbooks/")}
        actual = {str(path.relative_to(root)) for path in (root / "playbooks").glob("*.md")}
        for path in sorted(actual - indexed):
            errors.append(f"unindexed playbook: {path}")
        for path in sorted(indexed - actual):
            errors.append(f"indexed playbook does not exist: {path}")

        for path in sorted(actual):
            body = (root / path).read_text(encoding="utf-8")
            headings = {line.strip() for line in body.splitlines() if line.startswith("## ")}
            for heading in sorted(REQUIRED_PLAYBOOK_HEADINGS - headings):
                errors.append(f"{path} missing {heading}")

        triggers = load_json(root / "evals" / "trigger_queries.json", errors)
        if isinstance(triggers, list):
            classes: set[bool] = set()
            if len(triggers) < 20:
                errors.append("trigger_queries.json must contain at least 20 queries")
            for index, item in enumerate(triggers):
                if not isinstance(item, dict) or not isinstance(item.get("query"), str) or not item["query"].strip():
                    errors.append(f"trigger query {index} must have a non-empty query")
                if not isinstance(item, dict) or not isinstance(item.get("should_trigger"), bool):
                    errors.append(f"trigger query {index} must have a boolean should_trigger")
                else:
                    classes.add(item["should_trigger"])
            if classes != {True, False}:
                errors.append("trigger queries must include positive and near-miss negative cases")

        output_evals = load_json(root / "evals" / "evals.json", errors)
        if isinstance(output_evals, dict):
            if output_evals.get("skill_name") != "design":
                errors.append("evals.json skill_name must be design")
            cases = output_evals.get("evals")
            if not isinstance(cases, list) or len(cases) < 6:
                errors.append("evals.json must contain at least six output evals")
            else:
                ids: set[str] = set()
                for index, case in enumerate(cases):
                    if not isinstance(case, dict):
                        errors.append(f"output eval {index} must be an object")
                        continue
                    case_id = case.get("id")
                    if not isinstance(case_id, str) or not case_id or case_id in ids:
                        errors.append(f"output eval {index} has a missing or duplicate id")
                    else:
                        ids.add(case_id)
                    for key in ("prompt", "expected_output"):
                        if not isinstance(case.get(key), str) or not case[key].strip():
                            errors.append(f"output eval {index} must have {key}")
                    if not isinstance(case.get("assertions"), list) or not case["assertions"]:
                        errors.append(f"output eval {index} must have assertions")

        payload = {
            "valid": not errors,
            "skill": str(root),
            "entry_lines": line_count,
            "playbooks": len(actual),
            "trigger_queries": len(triggers) if isinstance(triggers, list) else 0,
            "output_evals": len(output_evals.get("evals", [])) if isinstance(output_evals, dict) else 0,
            "errors": errors,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if not errors else 1
    except OSError as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
