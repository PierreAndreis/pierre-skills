# Performance Playbook

## When to use

Use for latency, throughput, cold starts, CPU/memory pressure, cache behavior, payload size, queue delay, or a performance regression.

## Inputs

- critical user journey and SLO;
- traces or stage timing across the full path;
- representative workload, traffic mix, payload distribution, and concurrency;
- resource saturation, deploy markers, cache state, and dependency latency;
- correctness and cost gates.

## Procedure

1. **Name the user outcome.** Choose a full-path metric such as successful checkout p95, not only an inner function benchmark.
2. **Segment.** Break down by route, operation, tenant class, region, payload size, cache state, cold/warm, dependency, and status. Find whether a tail or a population shift drives the aggregate.
3. **Trace the budget.** Attribute end-to-end time to queueing, application work, database, network, external services, serialization, and client rendering where available.
4. **Check saturation and contention.** Correlate latency with CPU, memory, GC, threads, connection pools, locks, queues, throttles, and autoscaling transitions.
5. **Check recent changes.** Compare deploy, configuration, dependency, traffic, and data-shape changes without assuming correlation is causation.
6. **Build the laboratory.** Pin representative inputs; record cold and warm baselines; use multiple samples and tail percentiles; alternate baseline/candidate if ambient load drifts.
7. **Rank hypotheses.** Prefer changes that remove work, reduce round trips, bound fan-out, improve locality, or eliminate contention before adding capacity.
8. **Change one variable.** Preserve output equivalence, correctness, resource ceilings, and cost per unit.
9. **Verify under load.** Test representative concurrency and failure behavior, then canary and observe production tails.
10. **Accept or revert.** A faster microbenchmark loses when the user-visible path, reliability, or cost worsens.

## Opportunity patterns

- repeated remote or database round trips;
- unbounded concurrency or fan-out;
- cache miss storms, low-value caching, or stale-key fragmentation;
- oversized payloads, serialization copies, or compression tradeoffs;
- synchronous work that can be safely moved off the critical path;
- cold-start package/config work;
- lock or pool contention;
- queueing caused by mismatched capacity or retry amplification.

## Gotchas

- Average latency hides tails and affected cohorts.
- Load generators can measure themselves or bypass authentication, proxies, caches, and databases.
- Warm benchmarks can conceal the production cold path; cold-only tests can overstate normal cost.
- More concurrency often raises throughput until it collapses latency and downstream health.
- Sampling and tracing overhead can alter the path; record instrumentation settings.

## Completion

The change has a reproducible baseline, representative repeated samples, end-to-end improvement, passed correctness/SLO/cost gates, production observation across a comparable traffic window, and a recorded rollback.

## Escalate

Escalate when the path cannot be reproduced, traffic cannot be safely generated, the bottleneck belongs to an external owner, or improvement requires a product/SLO tradeoff.
