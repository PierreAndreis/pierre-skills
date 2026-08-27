#!/usr/bin/env python3
"""Aggregate cost and useful units into comparable cost-per-unit periods."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


def finite(raw: str, field: str) -> float:
    value = float(raw)
    if not math.isfinite(value):
        raise ValueError(f"{field} must be finite")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="CSV with period,cost,units and optional service columns")
    parser.add_argument("--baseline", help="baseline period; defaults to previous sorted period")
    parser.add_argument("--current", help="current period; defaults to latest sorted period")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        with Path(args.input).open(newline="", encoding="utf-8") as source:
            reader = csv.DictReader(source)
            required = {"period", "cost", "units"}
            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                raise ValueError("CSV must contain period,cost,units columns")
            totals: dict[str, dict[str, float | None]] = defaultdict(lambda: {"cost": 0.0, "units": None})
            services: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
            for row in reader:
                period = row["period"].strip()
                if not period:
                    raise ValueError("period cannot be empty")
                cost = finite(row["cost"], "cost")
                units = finite(row["units"], "units")
                if cost < 0 or units < 0:
                    raise ValueError("cost and units cannot be negative")
                totals[period]["cost"] = float(totals[period]["cost"] or 0.0) + cost
                recorded_units = totals[period]["units"]
                if recorded_units is not None and not math.isclose(float(recorded_units), units):
                    raise ValueError(
                        f"period {period!r} has conflicting units ({recorded_units} and {units}); "
                        "repeat one period-wide denominator on every service row"
                    )
                totals[period]["units"] = units
                if row.get("service"):
                    services[period][row["service"]] += cost
        periods = sorted(totals)
        if not periods:
            raise ValueError("CSV has no data rows")
        current = args.current or periods[-1]
        baseline = args.baseline or (periods[-2] if len(periods) > 1 else periods[-1])
        if current not in totals or baseline not in totals:
            raise ValueError(f"period not found; available: {', '.join(periods)}")
        series = []
        for period in periods:
            data = totals[period]
            unit_cost = float(data["cost"] or 0.0) / float(data["units"]) if data["units"] else None
            series.append({"period": period, **data, "cost_per_unit": unit_cost, "service_cost": dict(sorted(services[period].items()))})
        base_cpu = float(totals[baseline]["cost"] or 0.0) / float(totals[baseline]["units"]) if totals[baseline]["units"] else None
        current_cpu = float(totals[current]["cost"] or 0.0) / float(totals[current]["units"]) if totals[current]["units"] else None
        change = None if base_cpu in (None, 0) or current_cpu is None else (current_cpu - base_cpu) / abs(base_cpu)
        payload = {
            "baseline_period": baseline,
            "current_period": current,
            "baseline_cost_per_unit": base_cpu,
            "current_cost_per_unit": current_cpu,
            "relative_change": change,
            "classification": "unknown" if change is None else ("improved" if change < 0 else ("regressed" if change > 0 else "unchanged")),
            "series": series,
        }
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
