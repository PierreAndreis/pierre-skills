# Alerting Playbook

## When to use

Use to create, tune, consolidate, route, test, mute, or remove an alarm, or when incidents were missed or pages were noisy.

## Inputs

- SLOs and user-facing SLIs;
- alert definitions, notification routes, owners, and runbooks;
- firing/resolution/acknowledgement history and linked incidents;
- data freshness, traffic volume, maintenance/deploy windows, and known gaps.

## Procedure

1. **Name the protected failure.** State which user outcome or hard exhaustion risk the alert detects and the action a recipient can take.
2. **Prefer symptoms.** Page on user-impacting SLO/error-budget threats. Use internal cause alerts mainly for imminent hard limits or actionable precursor failures.
3. **Inventory current behavior.** Run `scripts/alarm_quality.py` on event history. Measure fires, actionable rate, duplicates, time to acknowledge/resolve, and unowned pages.
4. **Choose notification urgency.** Page only when action is needed now; create a ticket when the response can wait; dashboards are not notifications.
5. **Set windows from risk.** For SLOs, prefer multi-window, multi-burn-rate logic over one brittle threshold when traffic supports it. Handle low-traffic services separately.
6. **Specify delivery.** Owner, severity, labels, dedup key, inhibit/suppression rules, runbook, dashboard, and fallback route are part of the alert.
7. **Replay before enabling.** Evaluate against historical or synthetic time series to estimate detection, false positives, missed events, reset time, and page volume.
8. **Shadow.** Run the candidate without paging through representative traffic and deploy periods when possible.
9. **Activate and watch.** Record the prior rule, exact change, rollback, and observation window.
10. **Retire carefully.** Remove or consolidate only when another signal demonstrably covers the same failure.

## Alarm contract

```yaml
id: stable-alert-id
protects: user outcome or hard-limit failure
signal: metric/query and labels
threshold: expression
windows: [short, long]
severity: page | ticket
owner: team-or-human
runbook: URL
dashboard: URL
dedup_key: stable-key
freshness: maximum source age
```

## Gotchas

- Alerting on implementation internals often pages without mapping to user impact.
- Relaxing a threshold after a page can conceal the failure rather than fix noise.
- Silence and inhibition need expiry, owner, reason, and coverage check.
- A no-data condition may mean healthy zero traffic or broken telemetry; define which.
- Low traffic makes ratio alerts unstable; use longer windows, synthetic probes, or event-count guards.
- Issue comments and alert sends can hit rate limits; deduplicate and back off.

## Completion

The alert has a named failure, owner, immediate action, fresh signal, tested rule, historical/shadow evidence, deduplication, runbook, delivery verification, rollback, and measured observation window.

## Escalate

Escalate absent SLO ownership, unavoidable high page volume, undefined no-data semantics, missing notification permissions, or a proposed mute/removal with no replacement coverage.

## Primary references

- [Google SRE: Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [Google SRE: Incident management guide](https://sre.google/resources/practices-and-processes/incident-management-guide/)
