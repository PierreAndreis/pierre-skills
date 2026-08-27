# GitHub Audit Playbook

## When to use

Use when creating/updating the control issue, posting a loop entry, recording a change or incident, or requesting human input.

## Inputs

- repository, control issue number, labels, and authenticated GitHub identity;
- ledger loop ID, focus domain, authority, evidence, actions, and outcome;
- configured human assignee;
- stable fingerprint for any unresolved decision.

## Procedure

### Control issue

Create one open control issue with a stable marker such as `<!-- infrastructure-autopilot-control:v1 -->`. Its body is the current index, not the event log:

- authority and owner;
- schedule and last successful loop;
- environments, SLOs, dashboards, and evidence sources;
- active incidents, changes, experiments, and human decisions;
- state location and tested restoration command;
- links to prior dated control issues.

Update mutable summary fields while preserving the append-only event history in comments and the ledger.

### Loop comment

1. Run `scripts/render_audit.py <state-dir> --loop-id <id> --output <file>`.
2. Inspect for secrets, raw bind values, customer data, misleading health claims, and missing links.
3. Search the issue for the loop marker `<!-- autopilot-loop:<id> -->`.
4. If present, do not create a duplicate; update only when correcting a failed/incomplete post and record the correction.
5. Post through `gh issue comment` or the versioned GitHub REST endpoint with bounded retries.
6. Capture the resulting comment URL in the ledger.
7. Update the control issue's last-success and active-item index.

Issue comments trigger notifications and can hit secondary rate limits. A 15-minute loop therefore posts one compact comment, avoids retries that duplicate content, and rolls to a new dated control issue when the current issue becomes unwieldy.

### Human-input issue

1. Compute a stable fingerprint from repository, environment, resource, and decision class.
2. Search open issues for `<!-- autopilot-human:<fingerprint> -->`.
3. Update the existing issue when found; otherwise create one with the configured label and assignee.
4. Include decision needed, deadline/reason, safe default while waiting, options, recommendation, evidence, blast radius, and exact unblock response.
5. Link the issue from the control issue and ledger.
6. Continue unrelated loops; block only the scoped action.
7. When answered, record the authority/decision event and close only after the outcome is incorporated.

## Failure handling

An audit write failure is an operational failure. Persist the rendered comment and error locally/durably, record `unknown` audit status, retry with backoff, and create/route a human issue when permission or sustained rate limiting blocks recovery. Never discard the loop result because GitHub is unavailable.

## Completion

The loop marker exists exactly once, the comment URL is in the ledger, the control index reflects current active state, sensitive data is absent, and every unresolved human decision is assigned and linked.

## Escalate

Escalate invalid assignee, missing issue permission, persistent rate limiting, repository transfer/rename, accidentally posted sensitive data, or audit history that cannot be reconstructed.

## Primary references

- [GitHub issue comments REST API](https://docs.github.com/en/rest/issues/comments)
- [GitHub CLI issue creation](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue)
