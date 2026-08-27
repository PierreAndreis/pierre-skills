# Capacity Playbook

## When to use

Use for saturation, autoscaling, quotas, connection limits, queue growth, storage retention, hot partitions, forecasted exhaustion, or overload behavior.

## Inputs

- demand and growth time series by workload class;
- resource utilization, saturation, throttling, and queue metrics;
- hard/soft quotas, scaling bounds and delays, startup time, and provider limits;
- redundancy/failover requirements and regional topology;
- cost, performance, and reliability gates.

## Procedure

1. **Define the constrained resource.** CPU percentage alone is not capacity; identify the resource whose exhaustion harms the user path.
2. **Measure demand and service rate.** Track arrival rate, completed work, concurrency, queue depth/age, utilization, throttling, and rejected work.
3. **Segment.** Find tenant, shard, partition, region, operation, or payload skew. Aggregate headroom can coexist with a hot partition.
4. **Measure scaling dynamics.** Record detection, provisioning, warm-up, rebalancing, and cooldown delays. Confirm the load can survive this lag.
5. **Model failure headroom.** Recalculate capacity with one required failure domain unavailable and while backlogs drain.
6. **Forecast exhaustion.** Use multiple windows and known events. State uncertainty; do not extrapolate a short spike as permanent growth.
7. **Test overload behavior.** In a safe environment, verify admission control, backpressure, timeouts, retry budgets, load shedding, and graceful degradation.
8. **Choose the smallest lever.** Remove waste/contension, rebalance, adjust bounds, request quota, or add capacity. Preserve cost-per-unit and recovery gates.
9. **Canary and observe.** Watch oscillation, thrashing, queue age, downstream pressure, and cost.

## Capacity register

For each constrained resource, record owner, current usage, usable limit, safe operating ceiling, failure-mode ceiling, growth rate, time to exhaust, scaling lag, quota lead time, and last tested overload behavior.

## Gotchas

- Requested capacity is not usable capacity after redundancy and failure margins.
- Autoscaling on lagging signals can oscillate or arrive after the queue is already unrecoverable.
- Retries multiply load during failure and can consume nominal headroom.
- Raising a connection limit can transfer saturation to the database or dependency.
- Storage growth includes indexes, WAL/logs, replicas, snapshots, and temporary build space.

## Completion

The constrained resource, demand model, failure headroom, scale lag, quota lead time, overload behavior, cost effect, and observation window are measured and recorded; the path remains within its SLO under the tested demand and failure case.

## Escalate

Escalate forecasted exhaustion inside procurement/quota lead time, unknown failure margin, unsafe load testing, cross-team resource contention, or any capacity purchase outside recorded authority.
