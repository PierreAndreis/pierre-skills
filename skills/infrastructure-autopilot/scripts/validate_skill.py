#!/usr/bin/env python3
"""Validate the infrastructure-autopilot router, playbook contracts, and scripts."""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_HEADINGS = {"## When to use", "## Inputs", "## Procedure", "## Completion", "## Escalate"}


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
        skill = root / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        if len(text.splitlines()) >= 100:
            errors.append(f"SKILL.md has {len(text.splitlines())} lines; expected fewer than 100")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            errors.append("SKILL.md frontmatter markers are missing")
        links = re.findall(r"\[[^]]+\]\(([^)]+)\)", text)
        local_links = [link for link in links if "://" not in link and not link.startswith("#")]
        for link in local_links:
            if not (root / link).is_file():
                errors.append(f"missing linked file: {link}")
        playbook_links = [link for link in local_links if link.startswith("playbooks/")]
        linked_names = set(playbook_links)
        actual_names = {str(path.relative_to(root)) for path in (root / "playbooks").glob("*.md")}
        for extra in sorted(actual_names - linked_names):
            errors.append(f"unindexed playbook: {extra}")
        for link in sorted(linked_names):
            body = (root / link).read_text(encoding="utf-8")
            headings = {line.strip() for line in body.splitlines() if line.startswith("## ")}
            for heading in sorted(REQUIRED_HEADINGS - headings):
                errors.append(f"{link} missing {heading}")
        scripts = sorted((root / "scripts").glob("*.py"))
        for script in scripts:
            try:
                ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
            except SyntaxError as exc:
                errors.append(f"{script.name} syntax error: {exc}")
                continue
            if script.name != "validate_skill.py" and script.stat().st_mode & 0o111 == 0:
                errors.append(f"script is not executable: scripts/{script.name}")
            help_run = subprocess.run([sys.executable, str(script), "--help"], capture_output=True, text=True, timeout=10)
            if help_run.returncode != 0 or "usage:" not in help_run.stdout.lower():
                errors.append(f"script --help failed: scripts/{script.name}")
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
                errors.append("trigger_queries.json must include positive and near-miss negative queries")
        output_evals = load_json(root / "evals" / "evals.json", errors)
        if isinstance(output_evals, dict):
            if output_evals.get("skill_name") != "infrastructure-autopilot":
                errors.append("evals.json skill_name must be infrastructure-autopilot")
            cases = output_evals.get("evals")
            if not isinstance(cases, list) or not cases:
                errors.append("evals.json must contain a non-empty evals array")
            else:
                for index, case in enumerate(cases):
                    if not isinstance(case, dict) or not all(isinstance(case.get(key), str) and case[key].strip() for key in ("id", "prompt", "expected_output")):
                        errors.append(f"output eval {index} must have id, prompt, and expected_output")
                    if not isinstance(case, dict) or not isinstance(case.get("assertions"), list) or not case["assertions"]:
                        errors.append(f"output eval {index} must have assertions")
        payload = {"valid": not errors, "skill": str(root), "playbooks": len(actual_names), "scripts": len(scripts), "errors": errors}
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if not errors else 1
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
