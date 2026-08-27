#!/usr/bin/env python3
"""Record repeatable experiment trials and render a compact Markdown report."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_pairs(values: list[str], kind: str) -> dict[str, object]:
    pairs: dict[str, object] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"{kind} must use NAME=VALUE: {value!r}")
        name, raw = value.split("=", 1)
        if not name:
            raise ValueError(f"{kind} name cannot be empty")
        if kind == "metric":
            try:
                parsed = float(raw)
            except ValueError as exc:
                raise ValueError(f"metric value must be numeric: {value!r}") from exc
            if not math.isfinite(parsed):
                raise ValueError(f"metric value must be finite: {value!r}")
            pairs[name] = parsed
        else:
            pairs[name] = raw
    return pairs


def require_lab(directory: Path) -> tuple[Path, Path]:
    metadata = directory / "lab.json"
    trials = directory / "trials.jsonl"
    if not metadata.is_file():
        raise ValueError(f"not a laboratory (missing {metadata})")
    return metadata, trials


def command_init(args: argparse.Namespace) -> None:
    directory = Path(args.directory)
    directory.mkdir(parents=True, exist_ok=True)
    metadata = directory / "lab.json"
    if metadata.exists() and not args.force:
        raise ValueError(f"laboratory already exists: {directory}")
    payload = {
        "objective": args.objective,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    metadata.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (directory / "trials.jsonl").touch(exist_ok=True)
    print(f"initialized {directory}")


def command_record(args: argparse.Namespace) -> None:
    directory = Path(args.directory)
    _, trials = require_lab(directory)
    metrics = parse_pairs(args.metric, "metric")
    if not metrics:
        raise ValueError("at least one --metric is required")
    payload = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "variant": args.variant,
        "metrics": metrics,
        "parameters": parse_pairs(args.parameter, "parameter"),
        "note": args.note,
    }
    with trials.open("a", encoding="utf-8") as output:
        output.write(json.dumps(payload, sort_keys=True) + "\n")
    print(f"recorded {args.variant}")


def load_trials(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not path.exists():
        return rows
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON on {path}:{number}: {exc}") from exc
    return rows


def fmt(value: float) -> str:
    return f"{value:.6g}"


def command_report(args: argparse.Namespace) -> None:
    directory = Path(args.directory)
    metadata_path, trials_path = require_lab(directory)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    rows = load_trials(trials_path)
    grouped: dict[str, list[float]] = {}
    for row in rows:
        metrics = row.get("metrics", {})
        if args.primary in metrics:
            grouped.setdefault(str(row["variant"]), []).append(float(metrics[args.primary]))
    if args.baseline not in grouped:
        raise ValueError(f"baseline variant has no {args.primary!r} samples: {args.baseline!r}")
    baseline = statistics.median(grouped[args.baseline])
    lines = [
        f"# Experiment: {metadata['objective']}",
        "",
        f"Primary metric: `{args.primary}` ({args.direction} is better). Baseline: `{args.baseline}`.",
        "",
        "| Variant | Samples | Median | Min | Max | Change vs baseline |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for variant, samples in sorted(grouped.items()):
        median = statistics.median(samples)
        if variant == args.baseline:
            change = "baseline"
        else:
            relative = math.nan if baseline == 0 else (median - baseline) / abs(baseline) * 100
            improvement = -relative if args.direction == "lower" else relative
            change = "n/a" if math.isnan(improvement) else f"{improvement:+.2f}% better"
        lines.append(
            f"| {variant} | {len(samples)} | {fmt(median)} | {fmt(min(samples))} | {fmt(max(samples))} | {change} |"
        )
    lines.extend(["", f"Raw trials: `{trials_path}`", ""])
    report = "\n".join(lines)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
        print(f"wrote {output}")
    else:
        print(report, end="")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="create a laboratory directory")
    init.add_argument("directory")
    init.add_argument("--objective", required=True)
    init.add_argument("--force", action="store_true")
    init.set_defaults(run=command_init)

    record = commands.add_parser("record", help="append one measured trial")
    record.add_argument("directory")
    record.add_argument("--variant", required=True)
    record.add_argument("--metric", action="append", default=[])
    record.add_argument("--parameter", action="append", default=[])
    record.add_argument("--note", default="")
    record.set_defaults(run=command_record)

    report = commands.add_parser("report", help="summarize a primary metric by variant")
    report.add_argument("directory")
    report.add_argument("--baseline", required=True)
    report.add_argument("--primary", required=True)
    report.add_argument("--direction", choices=("lower", "higher"), required=True)
    report.add_argument("--output")
    report.set_defaults(run=command_report)
    return root


def main() -> int:
    try:
        args = parser().parse_args()
        args.run(args)
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
