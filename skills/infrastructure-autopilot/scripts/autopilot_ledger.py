#!/usr/bin/env python3
"""Maintain durable loop rotation and an append-only infrastructure audit ledger."""

from __future__ import annotations

import argparse
import fcntl
import json
import math
import os
import sys
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


DOMAINS = ["reliability", "performance", "cost", "database", "capacity", "alert-quality"]
KINDS = {"observation", "incident", "opportunity", "experiment", "change", "revert", "alarm", "human-input"}
OUTCOMES = {"changed", "reverted", "escalated", "no-change", "failed"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            json.dump(payload, output, indent=2, sort_keys=True)
            output.write("\n")
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def load(directory: Path) -> dict[str, object]:
    path = directory / "state.json"
    if not path.is_file():
        raise ValueError(f"not initialized: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def append(directory: Path, payload: dict[str, object]) -> None:
    with (directory / "events.jsonl").open("a", encoding="utf-8") as output:
        output.write(json.dumps(payload, sort_keys=True) + "\n")


@contextmanager
def ledger_lock(directory: Path):
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".lock").open("a+", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def pairs(values: list[str]) -> dict[str, float]:
    result: dict[str, float] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"metric must use NAME=VALUE: {value!r}")
        key, raw = value.split("=", 1)
        if not key:
            raise ValueError("metric name cannot be empty")
        parsed = float(raw)
        if not math.isfinite(parsed):
            raise ValueError(f"metric value must be finite: {value!r}")
        result[key] = parsed
    return result


def cmd_init(args: argparse.Namespace) -> None:
    directory = Path(args.directory)
    state_path = directory / "state.json"
    if state_path.exists() and not args.force:
        raise ValueError(f"already initialized: {state_path}")
    directory.mkdir(parents=True, exist_ok=True)
    state = {
        "schema_version": 1,
        "repo": args.repo,
        "audit_issue": args.audit_issue,
        "git_workflow": args.git_workflow,
        "production_policy": args.production_policy,
        "human_assignee": args.human_assignee,
        "created_at": now(),
        "next_sequence": 1,
        "next_domain_index": 0,
        "active_loop": None,
        "domain_last_scanned": {domain: None for domain in DOMAINS},
    }
    write_json(state_path, state)
    (directory / "events.jsonl").touch(exist_ok=True)
    print(json.dumps({"initialized": str(directory), "state": state}, sort_keys=True))


def cmd_start(args: argparse.Namespace) -> None:
    directory = Path(args.directory)
    with ledger_lock(directory):
        state = load(directory)
        if state.get("active_loop"):
            raise ValueError(f"loop already active: {state['active_loop']}")
        sequence = int(state["next_sequence"])
        domain_index = int(state["next_domain_index"])
        loop_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{sequence:06d}-{uuid.uuid4().hex[:6]}"
        focus = DOMAINS[domain_index]
        started = now()
        state["next_sequence"] = sequence + 1
        state["next_domain_index"] = (domain_index + 1) % len(DOMAINS)
        state["active_loop"] = {"id": loop_id, "focus": focus, "started_at": started}
        write_json(directory / "state.json", state)
        append(directory, {"at": started, "event": "loop-started", "loop_id": loop_id, "focus": focus})
        print(json.dumps(state["active_loop"], sort_keys=True))


def cmd_record(args: argparse.Namespace) -> None:
    directory = Path(args.directory)
    with ledger_lock(directory):
        state = load(directory)
        active = state.get("active_loop")
        if not isinstance(active, dict) or active.get("id") != args.loop_id:
            raise ValueError("--loop-id is not the active loop")
        payload = {
            "at": now(),
            "event": args.kind,
            "loop_id": args.loop_id,
            "summary": args.summary,
            "status": args.status,
            "url": args.url,
            "metrics": pairs(args.metric),
            "detail": args.detail,
        }
        append(directory, payload)
        print(json.dumps(payload, sort_keys=True))


def cmd_finish(args: argparse.Namespace) -> None:
    directory = Path(args.directory)
    with ledger_lock(directory):
        state = load(directory)
        active = state.get("active_loop")
        if not isinstance(active, dict) or active.get("id") != args.loop_id:
            raise ValueError("--loop-id is not the active loop")
        finished = now()
        focus = str(active["focus"])
        state["domain_last_scanned"][focus] = finished
        state["active_loop"] = None
        write_json(directory / "state.json", state)
        payload = {
            "at": finished,
            "event": "loop-finished",
            "loop_id": args.loop_id,
            "focus": focus,
            "outcome": args.outcome,
            "summary": args.summary,
            "next_validation": args.next_validation,
        }
        append(directory, payload)
        print(json.dumps(payload, sort_keys=True))


def cmd_abort(args: argparse.Namespace) -> None:
    directory = Path(args.directory)
    with ledger_lock(directory):
        state = load(directory)
        active = state.get("active_loop")
        if not isinstance(active, dict) or active.get("id") != args.loop_id:
            raise ValueError("--loop-id is not the active loop")
        state["active_loop"] = None
        write_json(directory / "state.json", state)
        payload = {
            "at": now(),
            "event": "loop-aborted",
            "loop_id": args.loop_id,
            "focus": active["focus"],
            "reason": args.reason,
        }
        append(directory, payload)
        print(json.dumps(payload, sort_keys=True))


def cmd_report(args: argparse.Namespace) -> None:
    directory = Path(args.directory)
    if args.limit < 1:
        raise ValueError("--limit must be positive")
    state = load(directory)
    events_path = directory / "events.jsonl"
    lines = [line for line in events_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    events = [json.loads(line) for line in lines[-args.limit :]]
    output = [
        "# Infrastructure autopilot state",
        "",
        f"- Repository: `{state['repo']}`",
        f"- Audit issue: {state['audit_issue'] or 'not set'}",
        f"- Git workflow: `{state['git_workflow']}`",
        f"- Active loop: `{state['active_loop'] or 'none'}`",
        "",
        "## Domain coverage",
        "",
        "| Domain | Last scanned (UTC) |",
        "| --- | --- |",
    ]
    for domain in DOMAINS:
        output.append(f"| {domain} | {state['domain_last_scanned'][domain] or 'never'} |")
    output.extend(["", "## Recent events", ""])
    for event in events:
        summary = event.get("summary") or event.get("outcome") or event["event"]
        output.append(f"- `{event['at']}` `{event['event']}` — {summary}")
    rendered = "\n".join(output) + "\n"
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered, end="")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init")
    init.add_argument("directory")
    init.add_argument("--repo", required=True)
    init.add_argument("--audit-issue", default="")
    init.add_argument("--git-workflow", choices=("observe-only", "review-pr", "auto-merge-pr", "direct-main"), default="observe-only")
    init.add_argument("--production-policy", default="read-only")
    init.add_argument("--human-assignee", default="")
    init.add_argument("--force", action="store_true")
    init.set_defaults(run=cmd_init)

    start = commands.add_parser("start")
    start.add_argument("directory")
    start.set_defaults(run=cmd_start)

    record = commands.add_parser("record")
    record.add_argument("directory")
    record.add_argument("--loop-id", required=True)
    record.add_argument("--kind", choices=sorted(KINDS), required=True)
    record.add_argument("--summary", required=True)
    record.add_argument("--status", default="observed")
    record.add_argument("--url", default="")
    record.add_argument("--metric", action="append", default=[])
    record.add_argument("--detail", default="")
    record.set_defaults(run=cmd_record)

    finish = commands.add_parser("finish")
    finish.add_argument("directory")
    finish.add_argument("--loop-id", required=True)
    finish.add_argument("--outcome", choices=sorted(OUTCOMES), required=True)
    finish.add_argument("--summary", required=True)
    finish.add_argument("--next-validation", default="")
    finish.set_defaults(run=cmd_finish)

    abort = commands.add_parser("abort", help="clear a crashed loop while preserving an audit event")
    abort.add_argument("directory")
    abort.add_argument("--loop-id", required=True)
    abort.add_argument("--reason", required=True)
    abort.set_defaults(run=cmd_abort)

    report = commands.add_parser("report")
    report.add_argument("directory")
    report.add_argument("--limit", type=int, default=20)
    report.add_argument("--output")
    report.set_defaults(run=cmd_report)
    return root


def main() -> int:
    try:
        args = parser().parse_args()
        args.run(args)
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
