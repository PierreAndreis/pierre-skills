# Database and SQL Playbook

## When to use

Use for slow queries, index proposals, plan regressions, locks, deadlocks, connection pools, replication lag, vacuum/statistics, or database saturation.

## Inputs

- engine/version, schema, migrations, table/index sizes, and data distribution;
- slow-query statistics or logs with collection window and reset time;
- application path, representative parameter distributions, and concurrency;
- plans in machine-readable form when supported;
- write rate, lock/replication/pool evidence, SLOs, and maintenance constraints.

## Procedure

1. **Protect data and privacy.** Use read-only credentials and redact bind values. Diagnostic output defaults to fingerprints/query IDs, not raw SQL.
2. **Validate the statistics window.** Record database restart/statistics reset, calls, total time, mean/tail where available, rows, I/O, and temporary work.
3. **Rank workload impact.** Use `scripts/slow_query_rank.py`; prioritize total database time and user impact before worst single execution.
4. **Map to product behavior.** Find the call site, transaction boundary, request frequency, pagination, retry behavior, and whether the statement is on a critical path.
5. **Capture the baseline plan.** Use estimated `EXPLAIN` first and a machine-readable format. Confirm planner statistics freshness and representative parameters.
6. **Use execution carefully.** `EXPLAIN ANALYZE` executes the statement. Prefer staging/replica. On production, require proven read-only bounded SQL and recorded authority; never run it on a mutating statement.
7. **Form one hypothesis.** Query shape, compound/partial/covering index, statistics, batching, caching, pagination, transaction scope, pool sizing, or access-pattern redesign.
8. **Evaluate an index as a write-path change.** Measure read gain, build time/locks, index size, write amplification, vacuum/maintenance, cache pressure, uniqueness semantics, and rollback.
9. **Test representative distribution and concurrency.** A rare literal or empty test table is not a useful oracle. Watch plan selection across parameter classes.
10. **Deploy safely.** Use engine-appropriate online/concurrent creation, timeouts, progress monitoring, and cancellation. Respect transaction restrictions.
11. **Observe production.** Compare query and user-path metrics, writes, locks, replication, storage, and plan stability. Retain or remove only after the watch window.

## PostgreSQL evidence

`pg_stat_statements` groups structurally equivalent queries and provides planning/execution totals, calls, rows, I/O, WAL, and related statistics when configured. Record its reset/collection window. PostgreSQL recommends machine-readable `EXPLAIN` output for programmatic analysis, and warns that `EXPLAIN ANALYZE` actually executes the statement and adds profiling overhead.

## Index checklist

- Predicate and leading columns match real filters and joins.
- Column order reflects equality, range, ordering, and selectivity needs.
- Partial predicate is implied by the production query.
- Included columns have a measured index-only benefit.
- Existing indexes are checked for overlap and write cost.
- Build method, lock level, disk headroom, replica impact, and failure cleanup are known.
- Migration is idempotent or safely resumable.
- Drop rollback is documented but not executed until the watch window closes.

## Gotchas

- Planner cost is not elapsed milliseconds.
- A sequential scan can be correct for a large result fraction or small table.
- More indexes can slow writes, vacuum, backups, cache residency, and migrations.
- Generic and custom prepared-statement plans can behave differently.
- Connection-pool growth can move overload into the database instead of fixing it.

## Completion

The query's product path, statistics window, representative parameters, before/after plans, repeated runtime/I/O evidence, write and lock impact, migration safety, production watch, and rollback are all recorded.

## Escalate

Escalate any mutating production diagnostic, long/uncertain index build, insufficient disk or replica headroom, semantic query rewrite, cross-tenant data risk, or change requiring a maintenance window.

## Primary references

- [PostgreSQL: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL: pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html)
