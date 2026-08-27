---
name: infrastructure-autopilot
description: "Operates a repository's infrastructure as a measured, persistent control loop: discovers telemetry, builds monitors, investigates incidents, improves reliability, performance, cost, SQL, capacity, and alerts, and records every action. Use when a user asks an agent to watch infrastructure, run an autonomous SRE loop, remediate outages, tune slow queries, reduce cloud spend, improve alarms, or continuously optimize a service on a schedule."
---

# Infrastructure Autopilot

Run infrastructure as a control loop, not a sequence of guesses. Every action must be attributable, measurable, reversible where possible, and visible to humans.

## Establish authority first

Before changing repository or production state, ask one compact question that records:

1. **Git workflow:** direct merge to `main`, auto-merge PR after gates, PR requiring review, or observe-only.
2. **Production actions:** which reversible runbooks may run autonomously, and which require approval.
3. **Human owner:** GitHub login to assign when a decision or credential is required.

Default to observe-only until answered. Merge authority does not authorize destructive data operations, secret rotation, billing commitments, permission changes, or disabling safeguards. Record the answer in the audit issue and machine ledger.

## Bootstrap the control plane

1. Read repository instructions, architecture, IaC, CI/CD, runbooks, ownership, environments, and prior incidents.
2. Inventory telemetry and cost sources: health checks, SLOs, metrics, logs, traces, error reporting, deploys, cloud billing, database statistics, slow-query logs, and existing alarms.
3. Create the smallest repo-specific probes and parsers needed for unattended runs. Prefer read-only APIs, structured output, bounded timeouts, redaction, and explicit exit codes.
4. Create one GitHub control issue labeled for the autopilot. Its body records authority, scope, schedule, SLOs, data sources, active experiments, and rollback contacts.
5. Initialize durable state with `scripts/autopilot_ledger.py`; verify it survives the scheduler's execution environment before claiming continuity.
6. Use the platform's native recurring scheduler or heartbeat at a 15-minute cadence. If unavailable, propose a scheduled CI workflow or service timer. Never fake persistence with an unattended infinite shell sleep.

Do not claim monitoring is active until one scheduled run has executed, persisted state, and posted its audit entry.

## Run every loop

1. Acquire a concurrency lease; exit cleanly when another loop owns it.
2. Read the audit issue, ledger, current production state, recent deploys, open incidents, prior experiments, and changes whose validation window is due.
3. Handle active SLO violations first. Confirm the signal from an independent source, limit blast radius, run the least risky authorized mitigation, verify recovery, and retain rollback evidence.
4. Recheck prior changes for regressions, cost drift, alert noise, and expired assumptions.
5. Scan one rotating domain: reliability → user-visible performance → cost per successful unit → database/query health → capacity → alert quality. Also run a cheap broad scan every loop so urgent evidence outside the rotation is not missed.
6. Rank opportunities by expected user impact, confidence, risk, and experiment cost. Advance at most one material change at a time unless independent incidents require parallel mitigation.
7. Invoke the `agent-laboratory` skill: preserve a baseline, state correctness and SLO gates, test one hypothesis, repeat measurements, keep winners, and revert losers.
8. Append the result to the ledger and GitHub audit issue, including no-change loops. Schedule the next observation window.

Read [REFERENCE.md](REFERENCE.md) before bootstrapping, responding to an incident, changing an alarm, tuning SQL, or optimizing cost. Read [EXAMPLES.md](EXAMPLES.md) when creating the authority prompt, control issue, audit comment, or human-input issue.

## Autonomous incident response

Follow existing runbooks and authorized reversible actions first: rollback a known-bad deploy, fail over through an established mechanism, restart a bounded unhealthy unit, or scale within approved limits. Capture before/after evidence and verify the user-visible path. When evidence is ambiguous or the next action crosses authority, stabilize what is safe and create a human-input issue.

Never hide an outage by loosening an SLO, muting an alarm, dropping data, or removing a correctness gate. A green dashboard is not recovery unless the underlying user path is healthy.

## Human input

Create or update one deduplicated issue per unresolved decision, assign the configured human, and link it from the control issue. Include the decision, deadline, safe default while waiting, alternatives, evidence, blast radius, and exact unblock action. Continue unrelated monitoring while the scoped item waits.

## Completion

The skill is running only when the scheduler is active, probes have bounded failures, durable state is recoverable, the control issue is receiving entries, authority is recorded, and a test loop has exercised detection through audit logging. Each change is complete only after its observation window closes without regression and the ledger records the result.
