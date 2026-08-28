from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(script: str, *arguments: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *(str(argument) for argument in arguments)],
        capture_output=True,
        text=True,
        check=False,
        timeout=15,
    )


class ShaderScriptTests(unittest.TestCase):
    def test_project_inventory_finds_exact_runtime_imports_and_wgsl(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "package.json").write_text(
                json.dumps({
                    "packageManager": "pnpm@10.0.0",
                    "dependencies": {"vgpu": "^0.3.1"},
                    "devDependencies": {"@vgpu/wgsl": "^0.3.1"},
                }),
                encoding="utf-8",
            )
            (project / "pnpm-lock.yaml").write_text("lockfileVersion: '9.0'\n", encoding="utf-8")
            source = project / "src"
            source.mkdir()
            (source / "effect.wgsl").write_text("@fragment fn fs_main() -> @location(0) vec4f { return vec4f(1); }\n", encoding="utf-8")
            (source / "browser.ts").write_text("import { init } from 'vgpu';\n", encoding="utf-8")
            (source / "node.ts").write_text("import { init } from 'vgpu/node';\n", encoding="utf-8")
            (source / "dynamic.ts").write_text("const runtime = import('vgpu/mock');\n", encoding="utf-8")

            completed = run("project_inventory.py", project)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["wgsl_files"], ["src/effect.wgsl"])
            self.assertEqual(payload["vgpu_dependencies"], {"@vgpu/wgsl": "^0.3.1", "vgpu": "^0.3.1"})
            self.assertEqual(payload["vgpu_import_counts"], {"vgpu": 1, "vgpu/mock": 1, "vgpu/node": 1})
            self.assertIn("npx vgpu doctor --pretty", payload["recommended_next"])

    def test_rgba_metrics_reports_channels_structure_and_passes_gates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            raw = Path(temporary) / "frame.rgba"
            raw.write_bytes(bytes([
                0, 0, 0, 255,
                255, 0, 0, 255,
                0, 255, 0, 255,
                0, 0, 255, 255,
            ]))
            completed = run(
                "rgba_metrics.py", raw,
                "--width", 2,
                "--height", 2,
                "--max-black-fraction", 0.25,
                "--max-transparent-fraction", 0,
                "--min-luma-stddev", 0.2,
                "--min-unique-colors", 4,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertTrue(payload["valid"])
            self.assertEqual(payload["unique_colors"], 4)
            self.assertFalse(payload["unique_colors_is_lower_bound"])
            self.assertEqual(payload["black_fraction"], 0.25)
            self.assertEqual(payload["opaque_fraction"], 1)
            self.assertGreater(payload["mean_neighbor_rgb_difference"], 0)

    def test_rgba_metrics_rejects_blank_and_wrong_length(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            blank = Path(temporary) / "blank.rgba"
            blank.write_bytes(bytes([0, 0, 0, 255] * 4))
            failed_gate = run("rgba_metrics.py", blank, "--width", 2, "--height", 2, "--max-black-fraction", 0.5)
            self.assertEqual(failed_gate.returncode, 1)
            self.assertFalse(json.loads(failed_gate.stdout)["valid"])

            malformed = Path(temporary) / "bad.rgba"
            malformed.write_bytes(b"short")
            rejected = run("rgba_metrics.py", malformed, "--width", 2, "--height", 2)
            self.assertEqual(rejected.returncode, 2)
            self.assertIn("expected exactly 16 bytes", rejected.stderr)

    def test_skill_validator(self) -> None:
        completed = run("validate_skill.py", ROOT)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["valid"])
        self.assertLess(payload["entry_lines"], 100)
        self.assertEqual(payload["playbooks"], 8)
        self.assertEqual(payload["scripts"], 3)
        self.assertEqual(payload["trigger_queries"], 20)
        self.assertEqual(payload["output_evals"], 7)
        self.assertTrue((ROOT / "templates" / "static-field.wgsl").is_file())
        self.assertTrue((ROOT / "templates" / "headless-smoke.mts").is_file())


if __name__ == "__main__":
    unittest.main()
