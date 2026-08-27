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
