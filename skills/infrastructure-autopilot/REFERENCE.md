# Shared Operating Contracts

Load this file when defining or interpreting evidence shared by multiple infrastructure playbooks.

## Evidence envelope

Every collected signal carries:

```json
{
  "source": "provider or probe name",
  "observed_at": "UTC timestamp",
  "window_start": "UTC timestamp",
  "window_end": "UTC timestamp",
  "fresh_until": "UTC timestamp",
  "environment": "production",
  "status": "healthy | unhealthy | unknown",
  "metrics": {},
  "artifact_url": "durable evidence link",
  "limitations": []
}
```

A collector timeout, authentication failure, parse failure, missing series, or expired `fresh_until` produces `unknown`. Health requires current evidence from the intended environment.

## Change envelope

Every material change records:

- stable change ID and hypothesis;
- authority mode and actor;
- repository SHA, PR, deployment, environment, and provider operation IDs;
- baseline window, candidate window, raw samples, and traffic shape;
- primary metric plus correctness, SLO, security, and cost gates;
- exact apply and rollback commands or runbook IDs;
- blast radius, canary population, stop conditions, and observation deadline;
- final state: proposed, running, watching, accepted, reverted, or escalated.

The ledger is append-only. Corrections are new events that point to the incorrect event; historical evidence is not rewritten.

## Severity

Use the repository's incident policy when present. Otherwise infer and label:

| Severity | Default interpretation | Response |
| --- | --- | --- |
| SEV-1 | Broad outage, active data/security risk, or critical business path unavailable | Freeze optimization; immediate mitigation and human issue |
| SEV-2 | Material degradation or partial outage with meaningful user impact | Incident loop; bounded autonomous runbooks |
| SEV-3 | Limited impact, unhealthy redundancy, or slow-burn SLO threat | Prioritize above optimization; ticket may be sufficient |
| SEV-4 | Improvement opportunity without current user impact | Laboratory backlog |

Severity follows impact, not the apparent size of the code change.

## Prioritization

Score candidates from evidence, not intuition:

`priority = user_impact × confidence × urgency ÷ (change_risk × experiment_cost)`

Use ordinal 1–5 inputs and record the rationale. Active incidents and due regression checks bypass optimization ranking. Prefer the cheapest experiment that can disprove a high-impact hypothesis.

## Freshness

Each source owns a maximum age. Choose it from the failure's time constant: readiness seconds, fast SLO minutes, deploy metadata minutes, slow-query statistics minutes to hours, billing hours to days. The loop records both collection time and source window. Reusing a cached value does not refresh it.

## Observation windows

Match the window to traffic and risk. A low-traffic path may need a full business cycle; a high-volume regression can be visible in minutes. Always include at least one comparable traffic period and any relevant peak. Keep the change in `watching` until the window closes.

## Autonomous action classes

| Class | Examples | Default |
| --- | --- | --- |
| Read | Query metrics, logs, billing, plans, CI, deploys | Allowed after credentials are available |
| Prepare | Branch, patch, PR, proposed alarm, dry run | Governed by Git workflow |
| Reversible operate | Known rollback, bounded restart, approved scale range | Requires named production policy |
| High consequence | Data mutation, secrets, permissions, irreversible deletion, security weakening, new spend | Explicit scoped human authorization |

## Completion contract

A loop completes when every attempted collector has a recorded result, every material signal is classified, every action has an outcome, the audit comment is posted or its failure is escalated, and the ledger lease is finished or aborted. A change completes only after its watch window closes and all gates pass.

## Sources behind these contracts

- [OpenAI harness engineering](https://openai.com/index/harness-engineering/) supports a short map with deeper, mechanically checked sources of truth.
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices) recommends explicit conditional pointers, procedures, validators, defaults, and execution-driven refinement.
- [Google SRE monitoring](https://sre.google/workbook/monitoring/) separates user-impacting SLI signals from diagnostic cause metrics.
- [Google SRE alerting](https://sre.google/workbook/alerting-on-slos/) describes multi-window, multi-burn-rate alerting.
- [FinOps Unit Economics](https://www.finops.org/framework/capabilities/unit-economics/) connects technology cost to useful resource or business units.
