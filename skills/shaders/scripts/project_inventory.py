#!/usr/bin/env python3
"""Inventory vgpu dependencies, WGSL modules, loaders, and runtime imports in a project."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path


SKIP_DIRS = {".git", ".next", ".turbo", "build", "coverage", "dist", "node_modules", "vendor"}
SOURCE_SUFFIXES = {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts"}
CONFIG_NAMES = {
    "next.config.js", "next.config.mjs", "next.config.ts",
    "vite.config.js", "vite.config.mjs", "vite.config.ts",
    "webpack.config.js", "webpack.config.mjs", "webpack.config.ts",
    "tsconfig.json", "package.json",
}
LOCKS = {
    "pnpm-lock.yaml": "pnpm",
    "yarn.lock": "yarn",
    "bun.lock": "bun",
    "bun.lockb": "bun",
    "package-lock.json": "npm",
    "npm-shrinkwrap.json": "npm",
}


def walk(root: Path, max_files: int) -> list[Path]:
    files: list[Path] = []
    for directory, names, filenames in os.walk(root):
        names[:] = sorted(name for name in names if name not in SKIP_DIRS and not name.startswith(".cache"))
        for name in sorted(filenames):
            files.append(Path(directory) / name)
            if len(files) > max_files:
                raise ValueError(f"project contains more than --max-files={max_files}; narrow the root")
    return files


def read_text(path: Path, maximum: int = 1_000_000) -> str:
    if path.stat().st_size > maximum:
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--max-files", type=int, default=20_000)
    parser.add_argument("--output", help="write JSON to this file instead of stdout")
    args = parser.parse_args()

    try:
        root = Path(args.root).resolve()
        if not root.is_dir():
            raise ValueError(f"project root is not a directory: {root}")
        if args.max_files < 1:
            raise ValueError("--max-files must be positive")
        files = walk(root, args.max_files)
        relative = {path: str(path.relative_to(root)) for path in files}

        package_path = root / "package.json"
        package: dict[str, object] = {}
        if package_path.is_file():
            parsed = json.loads(package_path.read_text(encoding="utf-8"))
            if not isinstance(parsed, dict):
                raise ValueError("package.json must contain an object")
            package = parsed

        dependency_versions: dict[str, str] = {}
        for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
            values = package.get(section, {})
            if isinstance(values, dict):
                for name, version in values.items():
                    if (name == "vgpu" or name.startswith("@vgpu/")) and isinstance(version, str):
                        dependency_versions[name] = version

        managers = sorted({manager for lock, manager in LOCKS.items() if (root / lock).exists()})
        package_manager_field = package.get("packageManager")
        if isinstance(package_manager_field, str) and package_manager_field:
            managers.insert(0, package_manager_field)

        wgsl_files = sorted(relative[path] for path in files if path.suffix.lower() == ".wgsl")
        configs = []
        for path in files:
            if path.name in CONFIG_NAMES:
                content = read_text(path)
                if "vgpu" in content.lower() or path.name in {"package.json", "tsconfig.json"}:
                    configs.append(relative[path])

        imports: Counter[str] = Counter()
        import_files: dict[str, list[str]] = {}
        import_pattern = re.compile(r"(?:from\s+|import\s*\(\s*)['\"]([^'\"]+)['\"]")
        for path in files:
            if path.suffix.lower() not in SOURCE_SUFFIXES:
                continue
            content = read_text(path)
            matched = sorted({
                specifier
                for specifier in import_pattern.findall(content)
                if specifier == "vgpu" or specifier.startswith("vgpu/") or specifier.startswith("@vgpu/")
            })
            for token in matched:
                imports[token] += 1
            if matched:
                import_files[relative[path]] = matched

        payload = {
            "root": str(root),
            "package_manager_evidence": managers,
            "vgpu_dependencies": dict(sorted(dependency_versions.items())),
            "wgsl_files": wgsl_files,
            "wgsl_count": len(wgsl_files),
            "vgpu_import_counts": dict(sorted(imports.items())),
            "vgpu_import_files": dict(sorted(import_files.items())),
            "relevant_configs": sorted(configs),
            "recommended_next": (
                ["install vgpu with the repository package manager", "read https://vgpu.sh/docs/get-started/web.md"]
                if "vgpu" not in dependency_versions
                else ["npx vgpu --version", "npx vgpu docs cat getting-started.md", "npx vgpu doctor --pretty"]
            ),
        }
        rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
