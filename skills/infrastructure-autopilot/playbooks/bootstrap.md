# Bootstrap Playbook

## When to use

Use on the first run, after an authority or ownership change, when the scheduler/state/control issue is missing, or when monitoring claims cannot be reproduced.

## Inputs

- repository instructions, architecture, IaC, CI/CD, runbooks, ownership, and environments;
- GitHub repository and authenticated identity;
- authority answers and human assignee;
- provider accounts and telemetry sources available to the agent;
- existing SLOs, budgets, incident history, deploy history, and alarms.

## Procedure

1. **Map the service.** Identify user journeys, entrypoints, compute, network, queues, storage, databases, external dependencies, deployment units, and environment boundaries. Record unknowns instead of inventing topology.
2. **Map authority.** Capture Git workflow separately from production actions. Resolve branch protection, required checks, environment protections, and which account performs scheduled runs.
3. **Map evidence.** For every user journey, locate an SLI or create a read-only probe. Then locate diagnostic metrics, logs, traces, deploy markers, costs, slow-query data, quotas, and alarms. Record source freshness and access gaps.
4. **Map recovery.** Inventory runbooks and test whether their referenced commands, dashboards, owners, and rollback targets still exist. Mark an untested runbook as unverified.
5. **Create repository control files.** Add `ops/autopilot/README.md`, provider-specific probes, schemas, and runbook wrappers only where missing. Keep secrets outside the repository.
6. **Create the GitHub control issue.** Use the template in `EXAMPLES.md`; record authority, schedule, evidence, SLOs, open gaps, and restoration command.
7. **Initialize state.** Run `scripts/autopilot_ledger.py init`. Persist the directory in a durable approved location and prove restoration in a fresh runner.
8. **Install the scheduler.** Prefer a native thread heartbeat when it preserves the working context. Otherwise use a repository schedule or service timer with concurrency control and a manual trigger.
9. **Dry-run end to end.** Execute collectors without mutations, classify at least one synthetic unhealthy/unknown case, render an audit comment, and post it.
10. **Activate.** Enable mutations only to the recorded authority level after the dry run passes.

## Bootstrap artifacts

- service and environment map;
- authority matrix and assignee;
- evidence inventory with freshness and permissions;
- tested scheduler plus manual invocation;
- durable state and restoration proof;
- GitHub control issue;
- explicit coverage gaps and human-input issues.

## Gotchas

- A health endpoint that proves only the web process is alive is not an end-to-end readiness signal.
- Scheduled GitHub workflows use the workflow on the default branch and can be delayed; record actual start time rather than assuming exact cadence.
- A cache is not durable state until a new runner restores it successfully.
- Access to a dashboard UI does not prove the background runner has API credentials.
- A control issue without a verified writer token is documentation, not an audit trail.

## Completion

Bootstrap is complete only after a scheduled or scheduler-equivalent run executes in a fresh context, restores state, gathers evidence, handles an injected unknown/unhealthy condition, writes the ledger, and posts the control-issue audit entry.

## Escalate

Create a human-input issue for missing credentials, absent SLO ownership, contradictory production authority, unassignable owner, untestable recovery, or a runner that cannot persist state.
