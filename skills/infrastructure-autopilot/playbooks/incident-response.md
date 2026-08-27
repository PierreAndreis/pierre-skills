# Incident Response Playbook

## When to use

Use for confirmed or plausible user-impacting outages, severe degradation, data/security risk, failed deployment, fast SLO burn, or a recovery action that did not work.

## Inputs

- user-visible symptom and current SLI/error-budget evidence;
- incident policy, authority, owners, and relevant runbooks;
- recent deploy/config/provider changes;
- logs, traces, metrics, topology, and dependency status;
- known-good versions and rollback/failover paths.

## Procedure

1. **Declare and timestamp.** Assign severity, incident ID, environment, commander/owner when available, and first-known impact. Label inferred severity.
2. **Freeze interference.** Pause optimization and deployments that could complicate diagnosis. Preserve evidence before retention or restarts erase it.
3. **Confirm impact.** Corroborate the alert with a second signal or direct user-path probe. A failed collector remains unknown; it does not clear the incident.
4. **Bound blast radius.** Identify affected journeys, tenants, regions, data, and dependencies. Prefer segmentation over global action.
5. **Form a short hypothesis set.** Recent changes are leads, not proof. Rank by evidence and cheapest discriminating check.
6. **Mitigate first.** Prefer a documented rollback, failover, traffic shed, bounded scale action, or restart of a single unhealthy unit over novel code.
7. **One action, one measurement.** Record the exact action and wait only for the known propagation delay before judging it. Avoid action storms.
8. **Verify recovery.** Check the user journey, SLI, queue/backlog recovery, correctness, and secondary effects. Green internal metrics alone are insufficient.
9. **Watch.** Define a stabilization window and regression thresholds. Keep the incident open while the path oscillates or backlog is still draining.
10. **Follow through.** Add regression detection/tests, link the permanent fix, and create post-incident actions without rewriting the timeline.

## Autonomous actions

Autonomous response is limited to runbooks and bounds recorded in the production policy. Use idempotency keys and verify target identity immediately before execution. Stop after a failed or ambiguous action unless the runbook explicitly defines the next step.

## Evidence timeline

Append UTC entries for detection, validation, hypotheses, actions, observations, authority decisions, recovery, and closure. Separate fact, inference, and decision. Link raw artifacts before retention expires.

## Gotchas

- Muting an alert changes notification state, not service health.
- Scaling can hide leaks, hot keys, or queue poison while increasing cost.
- A rollback can leave schema, cache, or job-format incompatibilities.
- Provider status pages lag or omit tenant-specific failures.
- Metrics can recover before backlogs, retries, or customer-visible consistency do.

## Completion

The incident closes only when the affected user path is healthy, the SLO has stabilized for the declared window, backlogs and data correctness are accounted for, every action and authority decision is audited, and follow-up ownership exists.

## Escalate

Escalate immediately for data/security risk, unknown blast radius, absent known-good rollback, repeated failed mitigation, provider/account lockout, production action beyond authority, or worsening impact.
