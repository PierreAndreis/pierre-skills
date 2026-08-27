# Knowledge Index Playbook

## When to use

Use when the agent missed context, keeps loading irrelevant material, repeats a mistake, tunnels into recent work, adds a new infrastructure domain/provider, or finds stale/conflicting documentation.

## Goal

Build a map that changes behavior at the moment a branch is chosen. The index should route; the destination should execute. A long index that explains every domain defeats progressive disclosure.

## Inputs

- current `SKILL.md`, playbooks, scripts, and direct links;
- real execution traces, user corrections, incidents, and missed branches;
- trigger and output eval results against the previous skill version;
- repository sources of truth, owners, verification dates, and stale documents.

## Procedure

1. **Inventory branches, not topics.** A branch is a situation that requires a different procedure: outage, slow query, noisy alert, cost anomaly, failed runner. Synonyms are one branch.
2. **Choose a leading trigger.** Start each pointer with the observable condition the agent will see: “SLO violation,” “slow query,” “audit write failure.”
3. **Point directly.** Link every operational playbook from `SKILL.md`; avoid reference chains where one index sends the agent to another index.
4. **Put invariants above routing.** Authority, evidence freshness, audit, and destructive-action boundaries apply to every branch and stay in the entrypoint/shared contract.
5. **Put branch-only detail below routing.** SQL plan rules do not occupy incident-response context unless a database signal fires.
6. **Give each playbook a contract.** Required headings are `When to use`, `Inputs`, `Procedure`, `Completion`, and `Escalate`. Add `Gotchas` where assumptions repeatedly fail.
7. **Make completion checkable.** “Investigate” is not a bound; “every configured source is fresh, unhealthy, or unknown” is.
8. **Set defaults.** Name the preferred method and one escape hatch; menus of equal options dilute behavior.
9. **Pair risky execution with validation.** Plan → validate against source of truth → execute → observe → accept/revert.
10. **Mechanically validate.** Run `scripts/validate_skill.py` after any index/playbook/script change.

## Behavioral evals

Maintain realistic should-route and should-not-route prompts for every playbook. Include indirect phrasing, typos, paths, provider context, and near misses. Run each more than once because model routing is nondeterministic. Compare the current skill against the previous version in clean contexts and inspect traces, not only final answers.

For output quality, test at least:

- outage prioritizes mitigation and freezes optimization;
- a missing metric becomes unknown rather than healthy;
- index advice measures write/lock/storage cost, not only query speed;
- cost advice normalizes by useful units and preserves SLOs;
- direct-main authority does not authorize destructive production actions;
- unresolved decisions become deduplicated assigned issues;
- a no-change loop still audits and advances rotation;
- recent work does not prevent the next domain scan.

Record assertions, evidence, token/time cost, and with-skill versus prior-skill results. Add corrections when a real execution exposes a miss; prune instructions that never affect behavior.

## Repository knowledge maintenance

- Keep architecture, SLO, runbook, ownership, and generated-schema indexes versioned beside code.
- Mark owner, last verified date/SHA, source of truth, and superseded documents.
- Link decisions and incidents to implementation and rollback paths.
- Run a recurring doc-gardening pass for broken links, stale owners, missing playbooks, and contradictions.
- Prefer generated facts from schemas/config over copied prose; copied facts rot.

## Gotchas

- More markdown can reduce compliance when the agent loads it all at once.
- Generic pointers such as “see references” do not encode the trigger and are often skipped.
- Duplicating a rule across playbooks creates conflicting sources of truth.
- A keyword-only router overfits phrasing; intent and observable conditions generalize better.
- An index without link/freshness validation becomes an attractive nuisance.

## Completion

Every distinct operational branch has one direct pointer, every pointer names its trigger, every playbook passes the required-heading validator, routing/output evals improve or hold against the previous version, and stale/duplicate rules are removed.

## Escalate

Escalate irreconcilable source-of-truth conflicts, overlapping branches that require different authority, or a broad skill whose routing evals remain poor after structural revision; that is evidence to split a standalone skill.

## Research basis

- [OpenAI harness engineering](https://openai.com/index/harness-engineering/) reports that a short map with deeper versioned sources outperformed one large instruction manual.
- [Agent Skills specification](https://agentskills.io/specification) defines progressive disclosure and recommends focused, directly referenced resources.
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices) recommends conditional pointers, coherent units, procedures, defaults, gotchas, validators, and execution-driven refinement.
- [Agent Skills description optimization](https://agentskills.io/skill-creation/optimizing-descriptions) recommends realistic positive and near-miss negative routing evals, repeated runs, and train/validation separation.
- [Agent Skills evaluation guide](https://agentskills.io/skill-creation/evaluating-skills) recommends clean-context comparisons, concrete assertions, evidence-backed grading, and with-skill baselines.
