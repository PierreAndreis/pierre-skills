#!/usr/bin/env python3
"""Render one ledger loop as a deduplicatable GitHub issue audit comment."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", help="ledger state directory")
    parser.add_argument("--loop-id", required=True)
    parser.add_argument("--output", help="required for durable use; omit to print")
    args = parser.parse_args()
    try:
        directory = Path(args.directory)
        state = load_json(directory / "state.json")
        events = []
        for number, line in enumerate((directory / "events.jsonl").read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid events JSON on line {number}: {exc}") from exc
            if event.get("loop_id") == args.loop_id:
                events.append(event)
        if not events:
            raise ValueError(f"loop not found: {args.loop_id}")
        start = next((event for event in events if event.get("event") == "loop-started"), {})
        finish = next((event for event in reversed(events) if event.get("event") in {"loop-finished", "loop-aborted"}), {})
        lines = [
            f"<!-- autopilot-loop:{args.loop_id} -->",
            f"### Infrastructure loop `{args.loop_id}`",
            "",
            f"- Interval: `{start.get('at', 'unknown')}` → `{finish.get('at', 'active')}`",
            f"- Focus: `{start.get('focus', finish.get('focus', 'unknown'))}`",
            f"- Authority: git `{state.get('git_workflow', 'unknown')}`; production `{state.get('production_policy', 'unknown')}`",
            f"- Outcome: `{finish.get('outcome', finish.get('event', 'active'))}`",
            "",
            "#### Evidence and actions",
            "",
        ]
        substantive = [event for event in events if event.get("event") not in {"loop-started", "loop-finished", "loop-aborted"}]
        if not substantive:
            lines.append("- No material signals or actions were recorded.")
        for event in substantive:
            summary = str(event.get("summary") or event.get("detail") or event.get("event"))
            line = f"- `{event.get('event')}` `{event.get('status', 'recorded')}` — {summary}"
            if event.get("metrics"):
                metrics = ", ".join(f"{key}={value}" for key, value in sorted(event["metrics"].items()))
                line += f" ({metrics})"
            if event.get("url"):
                line += f" — [evidence]({event['url']})"
            lines.append(line)
        lines.extend([
            "",
            f"- Summary: {finish.get('summary', finish.get('reason', 'loop is still active'))}",
            f"- Next validation: `{finish.get('next_validation') or 'not scheduled'}`",
            "",
        ])
        rendered = "\n".join(lines)
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered, encoding="utf-8")
            print(json.dumps({"output": str(output), "loop_id": args.loop_id, "events": len(events)}, sort_keys=True))
        else:
            print(rendered, end="")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
