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


class ScriptTests(unittest.TestCase):
    def test_ledger_lifecycle_overlap_and_audit_rendering(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            ledger = Path(temporary) / "ledger"
            initialized = run(
                "autopilot_ledger.py",
                "init",
                ledger,
                "--repo",
                "owner/repo",
                "--git-workflow",
                "review-pr",
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr)
            started = run("autopilot_ledger.py", "start", ledger)
            self.assertEqual(started.returncode, 0, started.stderr)
            loop_id = json.loads(started.stdout)["id"]
            overlap = run("autopilot_ledger.py", "start", ledger)
            self.assertEqual(overlap.returncode, 2)
            self.assertIn("loop already active", overlap.stderr)
            recorded = run(
                "autopilot_ledger.py",
                "record",
                ledger,
                "--loop-id",
                loop_id,
                "--kind",
                "observation",
                "--summary",
                "Readiness was healthy",
                "--metric",
                "availability=1",
            )
            self.assertEqual(recorded.returncode, 0, recorded.stderr)
            finished = run(
                "autopilot_ledger.py",
                "finish",
                ledger,
                "--loop-id",
                loop_id,
                "--outcome",
                "no-change",
                "--summary",
                "No intervention required",
                "--next-validation",
                "2026-08-28T00:00:00Z",
            )
            self.assertEqual(finished.returncode, 0, finished.stderr)
            rendered = run("render_audit.py", ledger, "--loop-id", loop_id)
            self.assertEqual(rendered.returncode, 0, rendered.stderr)
            self.assertIn(f"<!-- autopilot-loop:{loop_id} -->", rendered.stdout)
            self.assertIn("Readiness was healthy", rendered.stdout)
            self.assertIn("review-pr", rendered.stdout)

    def test_probe_runner_health_unknown_redaction_and_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            config = Path(temporary) / "probes.json"
            config.write_text(
                json.dumps(
                    {
                        "probes": [
                            {
                                "id": "healthy",
                                "command": [sys.executable, "-c", "print('token=top-secret')"],
                                "timeout_seconds": 2,
                            },
                            {
                                "id": "invalid-json",
                                "command": [sys.executable, "-c", "print('not json')"],
                                "require_json": True,
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            dry_run = run("probe_runner.py", config, "--dry-run")
            self.assertEqual(dry_run.returncode, 0, dry_run.stderr)
            self.assertTrue(all(item["validated"] for item in json.loads(dry_run.stdout)["probes"]))
            completed = run("probe_runner.py", config)
            self.assertEqual(completed.returncode, 2, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["summary"], {"healthy": 1, "unhealthy": 0, "unknown": 1})
            self.assertNotIn("top-secret", completed.stdout)
            self.assertIn("token=[REDACTED]", completed.stdout)

    def test_slow_query_ranking_is_workload_first_and_private_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            csv_path = Path(temporary) / "queries.csv"
            csv_path.write_text(
                "queryid,query,calls,total_exec_time,mean_exec_time,rows,shared_blks_read,shared_blks_hit\n"
                "11,SELECT secret FROM slow,2,900,450,2,10,90\n"
                "22,SELECT public FROM frequent,1000,1200,1.2,1000,5,995\n",
                encoding="utf-8",
            )
            completed = run("slow_query_rank.py", csv_path)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["ranked"][0]["fingerprint"], "22")
            self.assertAlmostEqual(payload["ranked"][0]["share_of_observed_exec_time"], 1200 / 2100)
            self.assertNotIn("query_sample", payload["ranked"][0])
            self.assertNotIn("secret", completed.stdout)

    def test_cost_efficiency_counts_one_period_denominator(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            csv_path = Path(temporary) / "cost.csv"
            csv_path.write_text(
                "period,cost,units,service\n"
                "2026-07,1200,400000,api\n"
                "2026-07,300,400000,database\n"
                "2026-08,1100,440000,api\n"
                "2026-08,280,440000,database\n",
                encoding="utf-8",
            )
            completed = run("cost_efficiency.py", csv_path)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["series"][0]["units"], 400000)
            self.assertAlmostEqual(payload["baseline_cost_per_unit"], 1500 / 400000)
            self.assertAlmostEqual(payload["current_cost_per_unit"], 1380 / 440000)
            self.assertEqual(payload["classification"], "improved")

            conflict = Path(temporary) / "conflict.csv"
            conflict.write_text(
                "period,cost,units,service\n2026-08,1100,440000,api\n2026-08,280,400000,database\n",
                encoding="utf-8",
            )
            rejected = run("cost_efficiency.py", conflict)
            self.assertEqual(rejected.returncode, 2)
            self.assertIn("conflicting units", rejected.stderr)

    def test_alarm_quality_surfaces_actionability_duplicates_and_runbooks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            csv_path = Path(temporary) / "alerts.csv"
            csv_path.write_text(
                "alert_id,fired_at,actionable,acknowledged_at,resolved_at,incident_id,runbook_present\n"
                "checkout,2026-08-27T10:00:00Z,true,2026-08-27T10:05:00Z,2026-08-27T10:30:00Z,inc-1,true\n"
                "checkout,2026-08-27T10:01:00Z,false,2026-08-27T10:08:00Z,2026-08-27T10:41:00Z,inc-1,false\n"
                "checkout,2026-08-27T11:00:00Z,false,,,inc-2,true\n",
                encoding="utf-8",
            )
            completed = run("alarm_quality.py", csv_path)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            alert = json.loads(completed.stdout)["alerts"][0]
            self.assertAlmostEqual(alert["actionable_rate"], 1 / 3)
            self.assertEqual(alert["duplicate_pages"], 1)
            self.assertEqual(alert["median_ack_minutes"], 6)
            self.assertEqual(alert["missing_runbook_events"], 1)
            self.assertEqual(alert["review_signals"], ["low-actionability", "duplicate-pages", "missing-runbook"])

    def test_skill_contract_validator(self) -> None:
        completed = run("validate_skill.py", ROOT)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["playbooks"], 12)
        self.assertGreaterEqual(payload["scripts"], 7)


if __name__ == "__main__":
    unittest.main()
