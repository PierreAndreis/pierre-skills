#!/usr/bin/env python3
"""Normalize one or more JUnit XML reports into auditable JSON evidence."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def report_paths(raw_paths: list[str]) -> list[Path]:
    paths: set[Path] = set()
    for raw in raw_paths:
        path = Path(raw)
        if path.is_dir():
            paths.update(item.resolve() for item in path.rglob("*.xml") if item.is_file())
        elif path.is_file():
            paths.add(path.resolve())
        else:
            raise ValueError(f"JUnit input does not exist: {path}")
    if not paths:
        raise ValueError("no JUnit XML reports found")
    return sorted(paths)


def safe_xml(path: Path) -> ET.Element:
    prefix = path.read_bytes()[:4096].upper()
    if b"<!DOCTYPE" in prefix or b"<!ENTITY" in prefix:
        raise ValueError(f"DTD/entity declarations are not accepted: {path}")
    try:
        return ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise ValueError(f"invalid JUnit XML {path}: {exc}") from exc


def seconds(raw: str | None) -> float:
    try:
        value = float(raw or 0)
    except ValueError:
        return 0.0
    return value if math.isfinite(value) and value >= 0 else 0.0


def child_text(case: ET.Element, names: set[str], limit: int) -> str:
    values: list[str] = []
    for child in case:
        if local_name(child.tag) in names:
            message = child.attrib.get("message", "")
            body = "".join(child.itertext()).strip()
            values.append("\n".join(part for part in (message, body) if part))
    return "\n".join(values)[:limit]


def parse_case(source: Path, suite_name: str, case: ET.Element, message_limit: int) -> dict[str, object]:
    child_names = {local_name(child.tag) for child in case}
    if "failure" in child_names:
        outcome = "failed"
    elif "error" in child_names:
        outcome = "error"
    elif "skipped" in child_names:
        outcome = "skipped"
    else:
        outcome = "passed"
    file_name = case.attrib.get("file", "")
    class_name = case.attrib.get("classname", "")
    name = case.attrib.get("name", "<unnamed>")
    identity = "::".join(part for part in (suite_name, file_name, class_name, name) if part)
    retry_tags = {"flakyFailure", "flakyError", "rerunFailure", "rerunError"}
    return {
        "source": str(source),
        "suite": suite_name,
        "identity": identity,
        "name": name,
        "classname": class_name,
        "file": file_name,
        "outcome": outcome,
        "seconds": seconds(case.attrib.get("time")),
        "retry_evidence": bool(child_names & retry_tags),
        "message": child_text(case, {"failure", "error"} | retry_tags, message_limit),
    }


def parse_report(path: Path, message_limit: int) -> list[dict[str, object]]:
    root = safe_xml(path)
    executions: list[dict[str, object]] = []
    for suite in root.iter():
        if local_name(suite.tag) != "testsuite":
            continue
        suite_name = suite.attrib.get("name", "<unnamed suite>")
        for case in suite:
            if local_name(case.tag) == "testcase":
                executions.append(parse_case(path, suite_name, case, message_limit))
    return executions


def aggregate(executions: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for execution in executions:
        grouped[str(execution["identity"])].append(execution)
    cases: list[dict[str, object]] = []
    for identity, runs in sorted(grouped.items()):
        outcomes = [str(run["outcome"]) for run in runs]
        durations = [float(run["seconds"]) for run in runs]
        decisive = {outcome for outcome in outcomes if outcome != "skipped"}
        cases.append({
            "identity": identity,
            "runs": len(runs),
            "passed": outcomes.count("passed"),
            "failed": outcomes.count("failed"),
            "errors": outcomes.count("error"),
            "skipped": outcomes.count("skipped"),
            "mixed_outcomes": len(decisive) > 1,
            "retry_evidence": any(bool(run["retry_evidence"]) for run in runs),
            "total_seconds": round(sum(durations), 6),
            "mean_seconds": round(statistics.mean(durations), 6),
            "median_seconds": round(statistics.median(durations), 6),
            "max_seconds": round(max(durations), 6),
        })
    return cases


def command(args: argparse.Namespace) -> None:
    paths = report_paths(args.inputs)
    executions = [case for path in paths for case in parse_report(path, args.max_message_chars)]
    if not executions:
        raise ValueError("reports contain no JUnit testcase elements")
    cases = aggregate(executions)
    outcomes = [str(item["outcome"]) for item in executions]
    payload = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": [str(path) for path in paths],
        "summary": {
            "reports": len(paths),
            "executions": len(executions),
            "unique_cases": len(cases),
            "passed": outcomes.count("passed"),
            "failed": outcomes.count("failed"),
            "errors": outcomes.count("error"),
            "skipped": outcomes.count("skipped"),
            "testcase_seconds": round(sum(float(item["seconds"]) for item in executions), 6),
            "mixed_outcome_cases": sum(bool(case["mixed_outcomes"]) for case in cases),
            "retry_evidence_cases": sum(bool(case["retry_evidence"]) for case in cases),
        },
        "cases": cases,
        "executions": executions,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {output}")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("inputs", nargs="+", help="JUnit XML files or directories")
    result.add_argument("--output", required=True)
    result.add_argument("--max-message-chars", type=int, default=2000)
    return result


def main() -> int:
    try:
        args = parser().parse_args()
        if args.max_message_chars < 0:
            raise ValueError("--max-message-chars must be non-negative")
        command(args)
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
