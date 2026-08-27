# Infrastructure Autopilot Reference

## Control-plane layout

Keep generated infrastructure automation easy to inspect. Adapt names to the repository, but prefer a shape like:

```text
ops/autopilot/
  README.md            # authority, setup, reproduction, rollback
  probes/              # read-only collectors with structured output
  runbooks/            # bounded, reversible remediations
  queries/             # read-only diagnostic SQL and explain helpers
  schemas/             # output contracts
.autopilot/
  state.json           # rotation and current checkpoints
  events.jsonl         # append-only machine audit
  laboratories/        # baselines, trials, and reports
```

If scheduled runners are ephemeral, persist `.autopilot` in an approved durable store or reconstruct it from the GitHub control issue and provider evidence. Test restoration. A cache without restore verification is not durable state.

Every probe must define timeout, retry ceiling, data source, freshness, redaction, schema, and failure semantics. A failed collector is `unknown`, never `healthy`.

## Authority matrix

| Workflow | Repository changes | Production actions |
| --- | --- | --- |
| Observe-only | Audit and human-input issues only | Read-only evidence collection |
| Review PR | Push branch and open PR | Only explicitly authorized runbooks |
| Auto-merge PR | Merge after required checks, experiment gates, and rollback readiness | Only explicitly authorized runbooks |
| Direct main | Push only after the same gates and branch protection allow it | Still limited by the separate production policy |

Treat these as new authority requests even under direct-main mode: destructive schema or data changes, irreversible resource deletion, access-control changes, secrets, new paid commitments, weakening security controls, and actions outside the named environments.

## Loop state machine

`observe → detect → validate → rank → experiment → change → verify → watch → close/revert`

- **Observe:** collect timestamped evidence and freshness.
- **Detect:** compare to SLOs, budgets, baselines, and anomaly rules.
- **Validate:** corroborate alerts and rule out collector failure or deploy transitions.
- **Rank:** prioritize impact divided by risk and experiment cost.
- **Experiment:** use `agent-laboratory`; record losing trials too.
- **Change:** create the smallest reversible change through the authorized workflow.
- **Verify:** test correctness plus the user-visible path and target metric.
- **Watch:** define an observation window appropriate to traffic and seasonality.
- **Close/revert:** retain only measured winners; revert on violated gates.

Use a lease or concurrency group so two scheduled loops cannot apply overlapping changes. Attach idempotency keys to remediations. Cap retries and exponential backoff; persistent failure becomes a human-input issue.

## Broad-scope rotation

The rotating focus prevents recency bias while the broad scan catches urgent problems:

1. **Reliability:** SLO/error-budget burn, availability, correctness, queue age, failed jobs, dependency health.
2. **Performance:** end-to-end latency percentiles, throughput, saturation, cold starts, payload and cache behavior.
3. **Cost:** cost per successful request/job/customer, idle capacity, storage growth, egress, log volume, reserved versus burst usage.
4. **Database:** slow-query fingerprints, total database time, p95/p99, calls, rows examined, locks, deadlocks, replication lag, pool saturation.
5. **Capacity:** headroom, autoscaling behavior, quotas, hot partitions, retention, forecasted exhaustion.
6. **Alert quality:** missed symptoms, false positives, duplicate pages, stale thresholds, missing runbooks, and time-to-detect/recover.

Track `last_scanned`, evidence freshness, open hypotheses, and next due validation for every domain. A recent change is a watch item, not permission to skip unrelated domains.

## Incident policy

Classify severity using the repository's policy. When none exists, infer severity from user impact, data risk, duration, and blast radius, and label the inference.

During an incident:

1. Freeze optimization work that could interfere.
2. Preserve timestamps, deploy identifiers, traces, logs, and relevant configuration.
3. Confirm the symptom through a second signal or the real user path.
4. Prefer known rollback or failover over an untested code change.
5. Apply one bounded action, then remeasure.
6. Escalate when the action fails, the blast radius grows, authority is insufficient, or evidence suggests data/security risk.
7. After recovery, add a regression monitor or test and record follow-up work without rewriting the incident timeline.

## Performance laboratory

Measure the complete user-visible path with representative traffic. Preserve cold and warm results when both matter. Record sample count and spread, not only averages. Optimize only among candidates that keep correctness, reliability, and resource ceilings green. Watch after deployment for workload drift and tail-latency regressions.

## Cost laboratory

Use normalized metrics such as cost per successful request, job, tenant, or stored useful unit. Separate fixed and variable cost. Attribute savings to traffic, pricing, retention, or implementation changes. Model peak capacity and failure recovery before removing headroom. A smaller bill that violates an SLO is a failed experiment.

## Slow-query laboratory

1. Collect slow-query evidence from the database's native statistics or logs and fingerprint normalized statements.
2. Rank by total time and user impact, not only single-call duration.
3. Map the fingerprint to its application path and confirm representative parameter distributions.
4. Save the current plan and runtime. Prefer read-only `EXPLAIN`; use `EXPLAIN ANALYZE` on production only when the statement is proven read-only, bounded, and authorized.
5. Test one hypothesis: query shape, index, statistics, batching, caching, pagination, or access pattern.
6. Measure runtime, rows, buffers/I/O, locks, plan stability, write amplification, index size, and migration risk.
7. Deploy through the authorized workflow, watch under real load, and retain rollback steps.

Never interpolate secrets or user data into logs. Redact bind values by default. Never run mutating diagnostic SQL against production.

## Alarm lifecycle

For each alarm, record owner, symptom, threshold, evaluation window, data freshness, severity, runbook, and downstream action. Measure page volume, false-positive rate, missed incidents, and time to acknowledge/mitigate.

Create or adjust an alarm only from a stated failure mode and baseline. Shadow-evaluate new thresholds when possible. Changes that merely silence a noisy alarm fail unless the underlying symptom is known harmless and coverage remains. Remove an alarm only when another signal covers the same user risk.

## Audit contract

The GitHub control issue is the human index. Post one compact comment per loop containing:

- loop ID and UTC interval;
- authority mode and focused domain;
- source freshness and signals checked;
- incidents or opportunities detected;
- commands/runbooks/changes executed;
- experiment baseline, candidate, gates, and result;
- commit, PR, deployment, alarm, dashboard, and raw-evidence links;
- rollback state and next validation time;
- outcome: changed, reverted, escalated, or no change.

Keep detailed structured events in `events.jsonl`; the issue comment must still be sufficient to understand what happened without the runner's filesystem. When the issue becomes unwieldy, open a new dated control issue and link both directions from an immutable index issue.

## Generated-script review

Before scheduling any script, test normal, timeout, authentication-failure, malformed-output, rate-limit, and partial-source cases. Verify nonzero exit codes, bounded retries, secret redaction, lock behavior, and idempotency. Pin dependencies and preserve `--help` output. Run in read-only or dry-run mode before enabling mutations.
