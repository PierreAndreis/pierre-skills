#!/usr/bin/env python3
"""Rank PostgreSQL statement-statistics CSV by workload impact without exposing SQL by default."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path


def number(row: dict[str, str], *names: str, default: float = 0.0) -> float:
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            parsed = float(value)
            if not math.isfinite(parsed):
                raise ValueError(f"{name} must be finite")
            return parsed
    return default


def identity(row: dict[str, str]) -> str:
    query_id = row.get("queryid") or row.get("query_id")
    if query_id:
        return str(query_id)
    query = row.get("query", "")
    return "sha256:" + hashlib.sha256(query.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="CSV export from pg_stat_statements or equivalent")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--include-query", action="store_true", help="include a truncated query sample; may expose sensitive text")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        if args.limit < 1:
            raise ValueError("--limit must be positive")
        with Path(args.input).open(newline="", encoding="utf-8") as source:
            rows = list(csv.DictReader(source))
        ranked: list[dict[str, object]] = []
        total_work = 0.0
        for row in rows:
            calls = number(row, "calls")
            total_ms = number(row, "total_exec_time", "total_time")
            mean_ms = number(row, "mean_exec_time", "mean_time", default=(total_ms / calls if calls else 0.0))
            read_blocks = number(row, "shared_blks_read")
            hit_blocks = number(row, "shared_blks_hit")
            item: dict[str, object] = {
                "fingerprint": identity(row),
                "calls": calls,
                "total_exec_ms": total_ms,
                "mean_exec_ms": mean_ms,
                "rows_per_call": number(row, "rows") / calls if calls else None,
                "shared_read_ratio": read_blocks / (read_blocks + hit_blocks) if read_blocks + hit_blocks else None,
                "temp_blocks_written": number(row, "temp_blks_written"),
                "wal_bytes": number(row, "wal_bytes"),
            }
            if args.include_query:
                item["query_sample"] = row.get("query", "")[:500]
            total_work += total_ms
            ranked.append(item)
        ranked.sort(key=lambda item: (float(item["total_exec_ms"]), float(item["mean_exec_ms"])), reverse=True)
        for item in ranked:
            item["share_of_observed_exec_time"] = float(item["total_exec_ms"]) / total_work if total_work else None
        payload = {"source_rows": len(rows), "observed_total_exec_ms": total_work, "ranked": ranked[: args.limit]}
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
