from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DesignSkillTests(unittest.TestCase):
    def test_contract_validator(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_skill.py"), str(ROOT)],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["valid"])
        self.assertLess(payload["entry_lines"], 100)
        self.assertEqual(payload["playbooks"], 10)
        self.assertEqual(payload["trigger_queries"], 20)
        self.assertGreaterEqual(payload["output_evals"], 6)

    def test_direct_heading_rule_is_in_entrypoint_and_eval(self) -> None:
        entry = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        evals = (ROOT / "evals" / "evals.json").read_text(encoding="utf-8").lower()
        for term in ("eyebrows", "kickers", "overlines"):
            self.assertIn(term, entry)
        self.assertIn("no-eyebrow", evals)

    def test_color_contract_covers_roles_themes_contrast_and_non_color_cues(self) -> None:
        color = (ROOT / "playbooks" / "color.md").read_text(encoding="utf-8").lower()
        for term in ("semantic roles", "oklch", "light-theme", "dark-theme", "4.5:1", "3:1", "without hue"):
            self.assertIn(term, color)


if __name__ == "__main__":
    unittest.main()
