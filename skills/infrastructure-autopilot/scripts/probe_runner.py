#!/usr/bin/env python3
"""Run configured infrastructure probes with time, output, and redaction bounds."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path


BUILTIN_REDACTIONS = [
    r"(?i)(authorization:\s*bearer\s+)[^\s]+",
    r"(?i)((?:api[_-]?key|token|password|secret)\s*[=:]\s*)[^\s,;]+",
]


def redact(value: str, patterns: list[str]) -> str:
    result = value
    for pattern in BUILTIN_REDACTIONS + patterns:
        try:
            result = re.sub(pattern, lambda match: (match.group(1) if match.lastindex else "") + "[REDACTED]", result)
        except re.error as exc:
            raise ValueError(f"invalid redaction pattern {pattern!r}: {exc}") from exc
    return result


def validate(config: object) -> list[dict[str, object]]:
    if not isinstance(config, dict) or not isinstance(config.get("probes"), list):
        raise ValueError("config must be an object with a probes array")
    probes: list[dict[str, object]] = []
    seen: set[str] = set()
    for index, raw in enumerate(config["probes"]):
        if not isinstance(raw, dict):
            raise ValueError(f"probe {index} must be an object")
        probe_id = raw.get("id")
        command = raw.get("command")
        if not isinstance(probe_id, str) or not probe_id or probe_id in seen:
            raise ValueError(f"probe {index} has a missing or duplicate id")
        if not isinstance(command, list) or not command or not all(isinstance(x, str) and x for x in command):
            raise ValueError(f"probe {probe_id!r} command must be a non-empty string array")
        seen.add(probe_id)
        timeout = raw.get("timeout_seconds", 15)
        maximum = raw.get("max_output_bytes", 4096)
        expected = raw.get("expected_exit_codes", [0])
        patterns = raw.get("redact_patterns", [])
        if not isinstance(timeout, (int, float)) or timeout <= 0 or timeout > 300:
            raise ValueError(f"probe {probe_id!r} timeout_seconds must be in (0, 300]")
        if not isinstance(maximum, int) or maximum < 0 or maximum > 1_000_000:
            raise ValueError(f"probe {probe_id!r} max_output_bytes must be in [0, 1000000]")
        if not isinstance(expected, list) or not expected or not all(isinstance(x, int) for x in expected):
            raise ValueError(f"probe {probe_id!r} expected_exit_codes must be an integer array")
        if not isinstance(patterns, list) or not all(isinstance(x, str) for x in patterns):
            raise ValueError(f"probe {probe_id!r} redact_patterns must be a string array")
        probes.append(raw)
    return probes


def clip(value: str, maximum: int) -> tuple[str, bool]:
    encoded = value.encode("utf-8", errors="replace")
    if len(encoded) <= maximum:
        return value, False
    return encoded[:maximum].decode("utf-8", errors="replace"), True


def decoded(value: str | bytes | None) -> str:
    if value is None:
        return ""
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value


def run_probe(probe: dict[str, object]) -> dict[str, object]:
    started = time.monotonic()
    maximum = int(probe.get("max_output_bytes", 4096))
    patterns = list(probe.get("redact_patterns", []))
    result: dict[str, object] = {"id": probe["id"], "status": "unknown"}
    try:
        completed = subprocess.run(
            list(probe["command"]),
            capture_output=True,
            text=True,
            timeout=float(probe.get("timeout_seconds", 15)),
            shell=False,
            check=False,
        )
        stdout, stdout_truncated = clip(redact(completed.stdout, patterns), maximum)
        stderr, stderr_truncated = clip(redact(completed.stderr, patterns), maximum)
        expected = list(probe.get("expected_exit_codes", [0]))
        status = "healthy" if completed.returncode in expected else "unhealthy"
        if probe.get("require_json") and status == "healthy":
            try:
                json.loads(completed.stdout)
            except json.JSONDecodeError:
                status = "unknown"
                stderr = (stderr + "\nprobe stdout was not valid JSON").strip()
        result.update(
            status=status,
            exit_code=completed.returncode,
            stdout=stdout,
            stderr=stderr,
            stdout_truncated=stdout_truncated,
            stderr_truncated=stderr_truncated,
        )
    except subprocess.TimeoutExpired as exc:
        result.update(error="timeout", timeout_seconds=probe.get("timeout_seconds", 15))
        if exc.stdout:
            result["stdout"] = clip(redact(decoded(exc.stdout), patterns), maximum)[0]
    except OSError as exc:
        result.update(error="execution-failed", detail=str(exc))
    result["duration_ms"] = round((time.monotonic() - started) * 1000, 3)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", help="JSON file containing a probes array")
    parser.add_argument("--dry-run", action="store_true", help="validate and print probe metadata without executing")
    parser.add_argument("--output", help="write JSON to this file instead of stdout")
    args = parser.parse_args()
    try:
        config = json.loads(Path(args.config).read_text(encoding="utf-8"))
        probes = validate(config)
        if args.dry_run:
            results = [{"id": p["id"], "command_length": len(p["command"]), "validated": True} for p in probes]
        else:
            results = [run_probe(probe) for probe in probes]
        payload = {"probes": results, "summary": {status: sum(r.get("status") == status for r in results) for status in ("healthy", "unhealthy", "unknown")}}
        rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
        if args.dry_run:
            return 0
        return 2 if payload["summary"]["unknown"] else (1 if payload["summary"]["unhealthy"] else 0)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
