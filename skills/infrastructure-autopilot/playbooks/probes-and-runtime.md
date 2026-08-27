# Probes and Runtime Playbook

## When to use

Use when creating or changing a collector, provider adapter, background script, scheduler, credential path, state store, or runner configuration; also use when a probe or scheduled loop fails.

## Inputs

- provider API/CLI contract and least-privilege credential path;
- required signal schema, freshness, timeout, and rate limits;
- scheduler capabilities, runner lifetime, filesystem persistence, and concurrency controls;
- expected normal, unhealthy, unknown, and partial-source cases.

## Procedure

1. **Define the contract first.** Write input flags, environment requirements, JSON output schema, statuses, exit codes, timeout, maximum output, and redaction policy.
2. **Prefer existing stable tools.** Wrap a pinned provider CLI or API rather than scraping a dashboard. Keep provider-specific facts in the repository adapter.
3. **Make it non-interactive.** All input comes from flags, environment, config, or stdin. Authentication prompts are failures with a human-action message.
4. **Use safe execution.** Pass argument arrays without a shell; bound time and output; cap retries with backoff/jitter; identify read versus mutate operations.
5. **Redact at collection.** Remove secrets and sensitive values before stdout, files, logs, ledger, or issue comments. Keep raw restricted evidence only in an approved store.
6. **Separate channels.** Structured data goes to stdout; diagnostics go to stderr. Use meaningful exit codes.
7. **Support dry-run and idempotency.** Stateful operations show the plan, target, authority, and idempotency key before execution.
8. **Test failure modes.** Normal, unhealthy, timeout, auth failure, rate limit, malformed output, truncation, stale data, partial source, concurrent run, and retry.
9. **Schedule with a lease.** Prefer native heartbeats; otherwise scheduled CI/service timer. Add manual dispatch, concurrency group/lock, maximum runtime, and cleanup.
10. **Prove persistence and audit.** Run in a fresh scheduler context, restore state, write evidence, and post the GitHub entry.

## Bundled runner

`scripts/probe_runner.py` accepts a JSON configuration with command arrays, timeouts, expected exit codes, maximum output, and redaction patterns. It never uses a shell. Start with `--dry-run`, then exercise a synthetic unhealthy and timeout case before scheduling.

## Generated adapter checklist

- [ ] Versioned provider endpoint/CLI and required permissions documented
- [ ] Read-only default; mutation isolated behind an explicit flag
- [ ] UTC timestamps and source window included
- [ ] `healthy`, `unhealthy`, and `unknown` distinct
- [ ] Secrets and bind values redacted
- [ ] Bounded timeout, retries, output, and pagination
- [ ] Rate-limit headers/backoff handled
- [ ] Idempotency key for mutations
- [ ] `--help`, examples, and exit codes tested
- [ ] Fixture tests avoid live production mutation

## Gotchas

- GitHub scheduled workflows can be delayed and may be disabled after inactivity; measure actual cadence and expose missed runs.
- A runner-local file disappears unless explicitly persisted and restored.
- `curl | jq` pipelines often lose the first command's exit status unless wrapped carefully.
- Provider CLIs can change output; request JSON and validate the schema.
- Truncated output can omit the error; summarize and persist full restricted artifacts.

## Completion

The script and scheduler pass every failure-mode test, run non-interactively with least privilege, emit bounded structured redacted output, prevent overlap, restore durable state, and produce an audit entry from a fresh run.

## Escalate

Escalate missing least-privilege credentials, interactive authentication, unbounded provider pagination, undocumented mutation semantics, unavailable persistence, or a scheduler incapable of enforcing concurrency.

## Skill-authoring basis

The [Agent Skills scripting guide](https://agentskills.io/skill-creation/using-scripts) recommends non-interactive inputs, concise `--help`, helpful errors, structured stdout, diagnostic stderr, idempotency, dry runs, safe defaults, and bounded output.
