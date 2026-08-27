# Infrastructure Autopilot Examples

## Initial authority question

> Before I activate the loop, which workflow authorizes repository changes: direct merge to `main`, auto-merge PRs after required gates, PRs requiring your review, or observe-only? Separately, which reversible production runbooks may I execute without approval, and which GitHub login should receive human-decision issues? Until you answer, I will remain observe-only.

## Control issue body

```markdown
# Infrastructure autopilot control plane

- Schedule: every 15 minutes
- Git workflow: auto-merge PR after required checks
- Production authority: rollback known-bad deploy; scale within documented bounds
- Human owner: @owner
- Environments: production and staging
- SLOs: <links and thresholds>
- Evidence sources: <dashboards, CI, billing, database statistics>
- State restoration: <location and verified command>
- Active experiment: none
- Open human decisions: none
```

## Loop audit comment

```markdown
### Loop `2026-08-27T23:15Z-0042`

- Focus: database; broad scan: no active SLO violation
- Freshness: metrics 2m, traces 4m, slow-query stats 9m, billing 6h
- Detected: query fingerprint `orders-by-account` consumed 31% of DB time
- Experiment: index candidate reduced representative p95 from 410ms to 96ms over 20 alternating runs; correctness, write-latency, and size gates passed
- Action: opened PR #412; no production mutation
- Evidence: <lab report>, <query plan>, <trace>, <PR>
- Rollback: drop concurrent index using runbook `DB-07`
- Next check: after CI, then 30m and 24h after deploy
- Outcome: changed
```

## Human-input issue

```markdown
Title: [infra-autopilot][human] Choose failover policy for payments database

Assignee: @owner
Linked control loop: #400
Decision needed by: <UTC time and why>
Safe default while waiting: keep primary serving; stop autonomous database changes
Observed impact: <user-facing evidence and blast radius>
Options: <bounded choices with tradeoffs>
Recommendation: <one option and evidence>
Unblock action: comment with the chosen option or approve runbook `<id>`
```

Use a stable fingerprint in the issue body and search open issues before creating another. Update the existing issue when the same decision remains unresolved.

## Probe configuration

Commands are argument arrays, never shell strings. Put credentials in the runner's secret store rather than this file.

```json
{
  "probes": [
    {
      "id": "public-readiness",
      "command": ["curl", "--fail", "--silent", "--show-error", "https://example.com/ready"],
      "timeout_seconds": 8,
      "expected_exit_codes": [0],
      "max_output_bytes": 2048
    },
    {
      "id": "deployment-state",
      "command": ["./ops/autopilot/probes/deployment-state"],
      "timeout_seconds": 20,
      "require_json": true,
      "redact_patterns": ["(?i)(account_id=)[^&\\s]+"]
    }
  ]
}
```

```bash
python scripts/probe_runner.py probes.json --dry-run
python scripts/probe_runner.py probes.json --output .autopilot/current/probes.json
```

Exit code `0` means every probe is healthy, `1` means at least one probe is unhealthy, and `2` means configuration failed or at least one probe is unknown.

## Slow-query ranking

Export a bounded `pg_stat_statements` window as CSV, then rank without emitting SQL text:

```bash
python scripts/slow_query_rank.py pg-stat-statements.csv \
  --limit 20 \
  --output .autopilot/current/slow-queries.json
```

Use `--include-query` only when the output destination is approved for potentially sensitive SQL text.

## Cost efficiency

Input columns are `period,cost,units` and optional `service`:

```csv
period,cost,units,service
2026-07,1200,400000,api
2026-07,300,400000,database
2026-08,1100,440000,api
2026-08,280,440000,database
```

```bash
python scripts/cost_efficiency.py cost.csv --output .autopilot/current/cost.json
```

`units` is the one period-wide denominator and must repeat unchanged on each service-cost row. The tool sums service costs but counts that denominator once, rejecting conflicting values instead of inventing an allocation. The result distinguishes total cost from cost per useful unit; it does not claim savings when the denominator is zero.

## Alarm-quality evidence

Input columns require `alert_id,fired_at,actionable`; optional fields are `acknowledged_at,resolved_at,incident_id,runbook_present`.

```bash
python scripts/alarm_quality.py alert-events.csv --output .autopilot/current/alarms.json
```

The output supplies review signals, not automatic permission to loosen or delete an alarm.

## Audit rendering

```bash
python scripts/render_audit.py .autopilot \
  --loop-id 20260827T230100Z-000001-0c0ffa \
  --output .autopilot/current/comment.md
```

Inspect the rendered Markdown for secrets and misleading health claims before posting it to the control issue.
