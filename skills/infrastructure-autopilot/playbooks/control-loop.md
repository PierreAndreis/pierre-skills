# Fifteen-Minute Control Loop

## When to use

Use on every scheduled wake-up, including loops where nothing changes.

## Inputs

- active ledger loop and selected focus domain;
- control issue, open human decisions, active incidents, and active changes;
- due observation windows and previous loop outcomes;
- fresh broad-scan signals and focused-domain evidence.

## Procedure

### 1. Orient

Read authority, current default branch, recent deploys, provider status, audit issue, open incidents, active experiments, and due validations. Confirm the current environment and timestamps. Completion: every active or due item has a next action in this loop.

### 2. Broad scan

Run cheap, user-centered signals across all domains:

- availability and correctness SLIs;
- fast and slow error-budget burn;
- p95/p99 latency and saturation;
- failed deploys/jobs and queue age;
- database connectivity, locks, replication, and pool pressure;
- cost anomaly and forecast change;
- quota/headroom risk;
- alarm delivery and collector freshness.

Completion: every configured source is fresh, unhealthy, or explicitly unknown.

### 3. Incident gate

Any credible user impact, fast burn, data/security signal, or failed recovery switches to the incident-response playbook. Pause unrelated mutations. Completion: incident declared or evidence shows the signal is not an incident, with reasoning recorded.

### 4. Recheck changes

For every change whose watch window is due, compare the same workload and gates used at approval. Accept, extend the window, or revert. Completion: no due change remains silently pending.

### 5. Focus scan

Load the ledger-selected domain playbook and apply every required check. Rotation continues even when recent work was in another domain. Completion: domain `last_scanned` can be advanced with evidence.

### 6. Rank

Combine new opportunities with the backlog. Remove stale, duplicated, disproven, already-fixed, or unauthorized items. Score user impact, confidence, urgency, risk, and experiment cost. Completion: one selected hypothesis or a documented no-change result.

### 7. Experiment and change

Invoke `agent-laboratory`. Preserve the baseline, invariant gates, raw samples, and rollback. One material optimization may be active unless separate incidents force more. Completion: winner deployed through authority workflow, loser reverted, or hypothesis remains inconclusive.

### 8. Audit and schedule

Record events, render the GitHub comment, post it, update human issues, set next validations, and finish the lease. If posting fails, record and escalate the audit failure before finishing.

## Anti-tunnel-vision rules

- Broad scan all domains every loop; deep-scan one rotating domain.
- A prior improvement creates a watch obligation, not a permanent priority.
- After three consecutive loops on one causal cluster, force a fresh topology and evidence review.
- Re-rank from current evidence; do not inherit the previous winner automatically.
- Track `never` and stale domain scans as debt visible in every report.

## Completion

Every collector has a classified result, incidents and due watches were handled first, the focused domain was scanned, one material action or no-change decision was recorded, the GitHub entry exists, and the ledger lease is closed.

## Escalate

Escalate stale critical evidence, repeated scheduler failure, overlapping mutations, audit-write failure, violated authority, or an opportunity whose safe experiment cannot be built.
