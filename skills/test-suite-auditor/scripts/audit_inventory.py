#!/usr/bin/env python3
"""Inventory test suites and track exhaustive audit verdicts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


EXCLUDED_DIRS = {
    ".git", ".hg", ".svn", ".next", ".nuxt", ".venv", "build", "coverage",
    "dist", "node_modules", "out", "target", "vendor",
}
TEST_DIRS = {"__tests__", "e2e", "integration", "spec", "specs", "test", "tests"}
EXTENSIONS = {
    ".bats", ".c", ".cc", ".cpp", ".cs", ".feature", ".go", ".java", ".js",
    ".jsx", ".kt", ".kts", ".mjs", ".mts", ".php", ".py", ".rb", ".rs",
    ".sh", ".swift", ".ts", ".tsx",
}
NAME_PATTERNS = [
    re.compile(r"(^test_.*|.*_test)\.[^.]+$", re.I),
    re.compile(r".*\.(test|spec)\.[^.]+$", re.I),
    re.compile(r".*\.(e2e|integration|contract|cy)\.[^.]+$", re.I),
    re.compile(r".*(Test|Tests)\.(java|kt|kts|cs|swift)$"),
    re.compile(r".*_spec\.rb$", re.I),
    re.compile(r".*\.feature$", re.I),
    re.compile(r".*\.bats$", re.I),
]
SIGNALS = {
    "fixed-sleep": re.compile(r"\b(sleep|waitForTimeout)\s*\(", re.I),
    "wall-clock": re.compile(r"Date\.now|new Date\s*\(|time\.time\s*\(|Instant\.now|datetime\.now", re.I),
    "randomness": re.compile(r"Math\.random|\brandom\.(random|randint|choice)|\brand\s*\(", re.I),
    "mocking": re.compile(r"jest\.mock|vi\.mock|unittest\.mock|\bmock\s*\(|@Mock\b|mockResolvedValue", re.I),
    "snapshot": re.compile(r"toMatchSnapshot|toMatchInlineSnapshot|assert_snapshot|snapshot\s*\(", re.I),
    "retry-or-flaky": re.compile(r"\b(retry|retries|rerun|flaky|quarantine)\b", re.I),
    "external-network": re.compile(r"https?://|\b(fetch|requests\.(get|post)|urllib|axios\.)", re.I),
    "shared-setup": re.compile(r"\b(beforeAll|afterAll|setup_module|teardown_module|setUpClass)\b", re.I),
    "broad-timeout": re.compile(r"\b(timeout|setTimeout)\s*\(", re.I),
}
VERDICTS = {"essential", "useful", "redundant", "misleading", "unknown"}
ACTIONS = {"keep", "repair", "consolidate", "delete", "investigate"}
RISKS = {"low", "medium", "high"}
CONFIDENCE = {"low", "medium", "high"}


def repo_files(root: Path) -> list[Path]:
    rg = shutil.which("rg")
    if rg:
        result = subprocess.run(
            [rg, "--files", "--hidden", "-g", "!.git/**"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        return [root / line for line in result.stdout.splitlines() if line]
    files: list[Path] = []
    for path in root.rglob("*"):
        if path.is_file() and not any(part in EXCLUDED_DIRS for part in path.relative_to(root).parts):
            files.append(path)
    return files


def is_test_file(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if path.suffix.lower() not in EXTENSIONS:
        return False
    return any(part.lower() in TEST_DIRS for part in relative.parts[:-1]) or any(
        pattern.fullmatch(path.name) for pattern in NAME_PATTERNS
    )


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(65536), b""):
            value.update(chunk)
    return value.hexdigest()


def static_signals(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ["unreadable"]
    return [name for name, pattern in SIGNALS.items() if pattern.search(text)]


def load(path: Path) -> dict[str, object]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read manifest {path}: {exc}") from exc


def save(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def command_scan(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    if not root.is_dir():
        raise ValueError(f"repository root is not a directory: {root}")
    candidates = {path.resolve() for path in repo_files(root) if is_test_file(path, root)}
    for raw in args.extra:
        path = (root / raw).resolve()
        if not path.is_file() or not path.is_relative_to(root):
            raise ValueError(f"extra suite is not a file inside the repository: {raw}")
        candidates.add(path)
    suites = []
    for path in sorted(candidates):
        suites.append({
            "path": path.relative_to(root).as_posix(),
            "sha256": digest(path),
            "bytes": path.stat().st_size,
            "signals": static_signals(path),
            "status": "pending",
            "assessment": {},
        })
    manifest = {
        "version": 1,
        "root": str(root),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "suite_count": len(suites),
        "suites": suites,
    }
    output = Path(args.output)
    save(output, manifest)
    print(f"wrote {output} with {len(suites)} suites")


def find_suite(data: dict[str, object], requested: str) -> dict[str, object]:
    matches = [suite for suite in data["suites"] if suite["path"] == requested]
    if not matches:
        raise ValueError(f"suite not found in manifest: {requested}")
    return matches[0]


def command_record(args: argparse.Namespace) -> None:
    manifest = Path(args.manifest)
    data = load(manifest)
    suite = find_suite(data, args.path)
    suite["status"] = "assessed"
    suite["assessment"] = {
        "cases_reviewed": args.cases_reviewed,
        "verdict": args.verdict,
        "flake_risk": args.flake_risk,
        "confidence": args.confidence,
        "action": args.action,
        "prevents": args.prevents,
        "oracle": args.oracle,
        "evidence": args.evidence,
        "case_exceptions": args.case_exception,
        "ci_evidence": args.ci_evidence,
        "history_evidence": args.history_evidence,
        "runtime_evidence": args.runtime_evidence,
    }
    save(manifest, data)
    print(f"recorded {args.path}")


def manifest_problems(data: dict[str, object], check_hashes: bool) -> list[str]:
    problems: list[str] = []
    root = Path(data["root"])
    for suite in data["suites"]:
        path = root / suite["path"]
        if suite.get("status") != "assessed":
            problems.append(f"pending: {suite['path']}")
            continue
        assessment = suite.get("assessment", {})
        for field in ("cases_reviewed", "verdict", "flake_risk", "confidence", "action", "prevents", "oracle", "evidence"):
            if assessment.get(field) in (None, ""):
                problems.append(f"missing {field}: {suite['path']}")
        if check_hashes:
            if not path.is_file():
                problems.append(f"missing file: {suite['path']}")
            elif digest(path) != suite.get("sha256"):
                problems.append(f"changed since scan: {suite['path']}")
    return problems


def command_verify(args: argparse.Namespace) -> None:
    data = load(Path(args.manifest))
    problems = manifest_problems(data, args.check_hashes)
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        raise ValueError(f"manifest verification failed with {len(problems)} problem(s)")
    print(f"verified {len(data['suites'])} assessed suites; zero pending")


def command_summary(args: argparse.Namespace) -> None:
    data = load(Path(args.manifest))
    counts: dict[str, int] = {"pending": 0}
    for suite in data["suites"]:
        verdict = suite.get("assessment", {}).get("verdict") if suite.get("status") == "assessed" else "pending"
        counts[verdict] = counts.get(verdict, 0) + 1
    print(json.dumps({"suite_count": len(data["suites"]), "verdicts": counts}, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    scan = commands.add_parser("scan", help="discover test suite files and create a manifest")
    scan.add_argument("root")
    scan.add_argument("--output", required=True)
    scan.add_argument("--extra", action="append", default=[], help="additional repository-relative suite path")
    scan.set_defaults(run=command_scan)

    record = commands.add_parser("record", help="record one suite assessment")
    record.add_argument("manifest")
    record.add_argument("--path", required=True)
    record.add_argument("--cases-reviewed", type=int, required=True)
    record.add_argument("--verdict", choices=sorted(VERDICTS), required=True)
    record.add_argument("--flake-risk", choices=sorted(RISKS), required=True)
    record.add_argument("--confidence", choices=sorted(CONFIDENCE), required=True)
    record.add_argument("--action", choices=sorted(ACTIONS), required=True)
    record.add_argument("--prevents", required=True)
    record.add_argument("--oracle", required=True)
    record.add_argument("--evidence", required=True)
    record.add_argument("--case-exception", action="append", default=[])
    record.add_argument("--ci-evidence", action="append", default=[])
    record.add_argument("--history-evidence", action="append", default=[])
    record.add_argument("--runtime-evidence", action="append", default=[])
    record.set_defaults(run=command_record)

    verify = commands.add_parser("verify", help="require every suite to have a complete assessment")
    verify.add_argument("manifest")
    verify.add_argument("--check-hashes", action="store_true")
    verify.set_defaults(run=command_verify)

    summary = commands.add_parser("summary", help="print manifest verdict counts")
    summary.add_argument("manifest")
    summary.set_defaults(run=command_summary)
    return parser


def main() -> int:
    try:
        args = build_parser().parse_args()
        args.run(args)
        return 0
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
