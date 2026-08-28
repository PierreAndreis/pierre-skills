#!/usr/bin/env python3
"""Validate the shaders skill router, playbooks, scripts, and behavior evals."""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_HEADINGS = {"## When to use", "## Inputs", "## Completion", "## Escalate"}


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON in {path.name}: {exc}")
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
        entry_lines = len(text.splitlines())
        if entry_lines >= 100:
            errors.append(f"SKILL.md has {entry_lines} lines; expected fewer than 100")
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
            errors.append(f"missing indexed playbook: {path}")
        for path in sorted(actual):
            body = (root / path).read_text(encoding="utf-8")
            headings = {line.strip() for line in body.splitlines() if line.startswith("## ")}
            for heading in sorted(REQUIRED_HEADINGS - headings):
                errors.append(f"{path} missing {heading}")

        scripts = sorted((root / "scripts").glob("*.py"))
        for script in scripts:
            try:
                ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
            except SyntaxError as exc:
                errors.append(f"{script.name} syntax error: {exc}")
                continue
            if script.stat().st_mode & 0o111 == 0:
                errors.append(f"script is not executable: scripts/{script.name}")
            help_run = subprocess.run([sys.executable, str(script), "--help"], capture_output=True, text=True, timeout=10)
            if help_run.returncode != 0 or "usage:" not in help_run.stdout.lower():
                errors.append(f"script --help failed: scripts/{script.name}")

        for required in ("templates/static-field.wgsl", "templates/headless-smoke.mts"):
            if not (root / required).is_file():
                errors.append(f"missing bundled smoke template: {required}")

        triggers = load_json(root / "evals" / "trigger_queries.json", errors)
        if isinstance(triggers, list):
            classes = {item.get("should_trigger") for item in triggers if isinstance(item, dict)}
            if len(triggers) < 20 or classes != {True, False}:
                errors.append("trigger queries need at least 20 positive and near-miss negative cases")
            for index, item in enumerate(triggers):
                if not isinstance(item, dict) or not isinstance(item.get("query"), str) or not item["query"].strip() or not isinstance(item.get("should_trigger"), bool):
                    errors.append(f"invalid trigger query {index}")

        output = load_json(root / "evals" / "evals.json", errors)
        output_cases = output.get("evals", []) if isinstance(output, dict) else []
        if not isinstance(output, dict) or output.get("skill_name") != "shaders" or not isinstance(output_cases, list) or len(output_cases) < 7:
            errors.append("evals.json needs skill_name shaders and at least seven evals")
        else:
            for index, case in enumerate(output_cases):
                if not isinstance(case, dict) or not all(isinstance(case.get(key), str) and case[key].strip() for key in ("id", "prompt", "expected_output")):
                    errors.append(f"invalid output eval {index}")
                if not isinstance(case, dict) or not isinstance(case.get("assertions"), list) or not case["assertions"]:
                    errors.append(f"output eval {index} needs assertions")

        payload = {
            "valid": not errors,
            "skill": str(root),
            "entry_lines": entry_lines,
            "playbooks": len(actual),
            "scripts": len(scripts),
            "trigger_queries": len(triggers) if isinstance(triggers, list) else 0,
            "output_evals": len(output_cases) if isinstance(output_cases, list) else 0,
            "errors": errors,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if not errors else 1
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
