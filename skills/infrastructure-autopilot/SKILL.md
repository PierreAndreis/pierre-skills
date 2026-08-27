---
name: infrastructure-autopilot
description: "Operates a repository's infrastructure as a measured, persistent control loop. Use this skill for continuous SRE work: watching production, responding to outages, improving latency and capacity, reducing cost per useful unit, tuning slow SQL and indexes, refining alarms, creating monitoring scripts, auditing autonomous changes, or scheduling a recurring infrastructure agent—even when the user asks indirectly to keep a service healthy or make it cheaper over time."
---

# Infrastructure Autopilot

Operate a service through evidence, bounded actions, and durable memory. Treat missing or stale evidence as `unknown`, never healthy.

Useful production operation requires Python 3.11+, repository access, GitHub issue access for the audit trail, and authorized provider telemetry credentials.

## Authority gate

Before the first mutation, ask one compact question for:

1. **Git workflow:** direct `main`, auto-merge PR after gates, reviewed PR, or observe-only.
2. **Production policy:** named reversible runbooks and environments allowed without approval.
3. **Human owner:** GitHub login for assigned decision issues.

Remain observe-only until recorded. Merge authority and production authority are separate. Destructive data work, secrets, permissions, security controls, irreversible deletion, and new paid commitments always need explicit scoped authority.

## Behavioral index

Load only the files whose trigger matches the current branch. References are direct from this entrypoint so routing never depends on a second index.

| Situation | Required playbook |
| --- | --- |
| First run, missing control plane, or changed authority | [Bootstrap](playbooks/bootstrap.md) |
| Every scheduled wake-up, including no-change loops | [Control loop](playbooks/control-loop.md) |
| SLO violation, outage, severe degradation, or failed deploy | [Incident response](playbooks/incident-response.md) |
| Latency, throughput, cold start, cache, payload, or CPU work | [Performance](playbooks/performance.md) |
| Cloud bill, idle resources, storage, egress, logs, or unit economics | [Cost](playbooks/cost.md) |
| Slow query, index, lock, deadlock, pool, replication, or plan work | [Database](playbooks/database.md) |
| Alert creation, tuning, noise, missing coverage, or escalation policy | [Alerting](playbooks/alerting.md) |
| Saturation, quota, autoscaling, retention, or exhaustion forecast | [Capacity](playbooks/capacity.md) |
| Probe, background script, scheduler, credentials, or runner failure | [Probes and runtime](playbooks/probes-and-runtime.md) |
| Commit, PR, deploy, canary, rollback, or observation window | [Change safety](playbooks/change-safety.md) |
| GitHub control issue, loop comment, human decision, or deduplication | [GitHub audit](playbooks/github-audit.md) |
| Stale docs, missing context, tunnel vision, or adding a new domain | [Knowledge index](playbooks/knowledge-index.md) |

Read [Shared contracts](REFERENCE.md) whenever defining schemas, severity, prioritization, freshness, or completion. Use [Examples](EXAMPLES.md) for issue and comment formats.

## Every wake-up

1. Run `scripts/autopilot_ledger.py start <state-dir>`; an active lease means this run exits without mutation.
2. Read the control-loop playbook, then the focused domain selected by the ledger. Add incident, change-safety, or audit playbooks when their triggers fire.
3. Check active incidents and due validation windows before new optimization work.
4. Run the cheap broad scan, then the focused scan. Corroborate material signals.
5. Rank opportunities and advance no more than one material optimization at once.
6. Invoke `agent-laboratory`: baseline, invariant gates, one hypothesis, repeated measurements, winner or revert.
7. Record structured evidence, post the GitHub audit entry, and finish or explicitly abort the ledger loop.

## Bundled tools

- `scripts/autopilot_ledger.py` — lease, rotation, append-only events, and recovery.
- `scripts/probe_runner.py` — bounded non-shell probe execution with redaction and JSON output.
- `scripts/slow_query_rank.py` — privacy-preserving ranking of PostgreSQL statement statistics.
- `scripts/cost_efficiency.py` — cost-per-unit trend and regression analysis.
- `scripts/alarm_quality.py` — actionability, duplication, acknowledgement, and resolution evidence.
- `scripts/render_audit.py` — render one loop's GitHub-ready audit comment.
- `scripts/validate_skill.py` — verify routing links, playbook contracts, and script interfaces.

Prefer adapting these scripts over regenerating their logic. Read each script's `--help` before use. Generated provider adapters follow the probes-and-runtime playbook.

## Hard stops

Stabilize within recorded authority; escalate the blocked decision. A dashboard color, suppressed page, lower bill, or faster microbenchmark is never proof of user recovery. Complete a change only after its observation window closes with correctness, SLO, cost, and rollback evidence recorded.
