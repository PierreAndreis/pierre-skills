# Change Safety Playbook

## When to use

Use before and after any repository merge, deployment, configuration/IaC change, alarm change, index build, scaling action, rollback, or canary.

## Inputs

- recorded authority and target environment;
- change envelope, baseline, gates, and laboratory report;
- branch protection, CI, deploy pipeline, and environment protections;
- blast radius, rollout mechanism, rollback, and observation window.

## Procedure

### Plan

1. Resolve the exact resource, repository SHA, environment, account, region, and current state immediately before action.
2. State the hypothesis and predicted metric movement. Define invariant gates and stop conditions.
3. Choose the smallest reversible scope: fixture/staging, then canary, then gradual rollout.
4. Write exact apply and rollback operations. Confirm rollback remains compatible with schema, data, cache, message, and client versions.
5. Generate a dry-run or provider plan and compare it to the intended target. Unexpected replacements, deletes, permission changes, or new spend stop the change.

### Validate

6. Run repository tests, IaC/config validation, policy checks, and the laboratory baseline/candidate comparison.
7. Confirm required checks correspond to the current SHA. A prior green run does not cover a rebased or amended commit.
8. Verify credentials, quotas, disk/headroom, backup/recovery, and audit writer before deployment.

### Execute

9. Apply through the recorded workflow. Use idempotency and concurrency guards. Record provider operation and deployment IDs immediately.
10. Watch canary health and stop conditions before expansion. Advance one stage at a time.
11. Verify the user path, SLOs, correctness, cost, and resource effects—not only deployment status.
12. Set the change to `watching`; close only after the observation window.

### Revert

Revert when any invariant gate fails, impact is ambiguous beyond the allowed window, or the candidate loses its measured benefit. Record the reason and verify the rollback like a new change.

## Workflow behavior

- **Observe-only:** create evidence and a proposed plan; no branch or production mutation.
- **Reviewed PR:** push a branch and open/update a PR; wait for human approval.
- **Auto-merge PR:** enable merge only after required checks, laboratory gates, and rollback readiness; verify the final merged SHA.
- **Direct main:** push only when branch protection permits and the same gates pass; directness does not remove review or observation obligations.

## Gotchas

- IaC plans can become stale between plan and apply.
- A successful provider API call can start an asynchronous operation that later fails.
- Rollback can be destructive when forward migrations or messages are incompatible.
- Canary success with unrepresentative tenants or cache warmth does not prove rollout safety.
- Alarm changes need their own shadow and watch window.

## Completion

The exact final SHA/resource is verified, gates pass on that version, rollout and rollback evidence are linked, the user path is healthy, and the full observation window closes without regression.

## Escalate

Escalate unexpected destructive plans, no tested rollback, stale required checks, schema/data incompatibility, high-consequence authority, or a canary population that cannot represent the production risk.
