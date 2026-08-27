#!/usr/bin/env python3
"""Summarize alert actionability, duplication, acknowledgement, and resolution evidence."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def timestamp(raw: str) -> datetime | None:
    if not raw:
        return None
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))


def boolean(raw: str) -> bool:
    value = raw.strip().lower()
    if value in {"true", "1", "yes"}:
        return True
    if value in {"false", "0", "no"}:
        return False
    raise ValueError(f"actionable must be true or false, got {raw!r}")


def minutes(start: datetime | None, end: datetime | None) -> float | None:
    if not start or not end:
        return None
    value = (end - start).total_seconds() / 60
    if value < 0:
        raise ValueError("event timestamps are out of order")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="CSV with alert_id,fired_at,actionable and optional timing/incident columns")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        with Path(args.input).open(newline="", encoding="utf-8") as source:
            reader = csv.DictReader(source)
            required = {"alert_id", "fired_at", "actionable"}
            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                raise ValueError("CSV must contain alert_id,fired_at,actionable columns")
            groups: dict[str, list[dict[str, str]]] = defaultdict(list)
            for row in reader:
                if not row["alert_id"]:
                    raise ValueError("alert_id cannot be empty")
                groups[row["alert_id"]].append(row)
        results = []
        for alert_id, rows in sorted(groups.items()):
            actionable = [boolean(row["actionable"]) for row in rows]
            ack: list[float] = []
            resolve: list[float] = []
            incident_counts: dict[str, int] = defaultdict(int)
            missing_runbook = 0
            for row in rows:
                fired = timestamp(row["fired_at"])
                ack_value = minutes(fired, timestamp(row.get("acknowledged_at", "")))
                resolve_value = minutes(fired, timestamp(row.get("resolved_at", "")))
                if ack_value is not None:
                    ack.append(ack_value)
                if resolve_value is not None:
                    resolve.append(resolve_value)
                if row.get("incident_id"):
                    incident_counts[row["incident_id"]] += 1
                if row.get("runbook_present", "true").strip().lower() in {"false", "0", "no"}:
                    missing_runbook += 1
            duplicates = sum(max(0, count - 1) for count in incident_counts.values())
            rate = sum(actionable) / len(actionable)
            signals = []
            if rate < 0.5:
                signals.append("low-actionability")
            if duplicates:
                signals.append("duplicate-pages")
            if missing_runbook:
                signals.append("missing-runbook")
            results.append({
                "alert_id": alert_id,
                "fires": len(rows),
                "actionable_rate": rate,
                "duplicate_pages": duplicates,
                "median_ack_minutes": statistics.median(ack) if ack else None,
                "median_resolve_minutes": statistics.median(resolve) if resolve else None,
                "missing_runbook_events": missing_runbook,
                "review_signals": signals,
            })
        payload = {"alerts": results, "total_fires": sum(item["fires"] for item in results)}
        rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
