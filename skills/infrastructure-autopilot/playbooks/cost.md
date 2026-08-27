# Cost Playbook

## When to use

Use for spend anomalies, idle or oversized resources, storage/egress/log growth, commitment decisions, or cost-efficiency improvement.

## Inputs

- itemized cost and usage with billing freshness and currency;
- allocation dimensions such as service, environment, tenant, region, SKU, and owner;
- useful business or resource units;
- traffic, reliability, latency, capacity, and retention requirements;
- pricing terms, commitments, credits, and amortization policy.

## Procedure

1. **Validate the bill.** Record source window, currency, discounts, credits, amortization, and unallocated spend. Billing lag is a limitation, not current truth.
2. **Choose a useful denominator.** Prefer successful request, completed job, active tenant, GB retained, or another value-bearing unit. Use `scripts/cost_efficiency.py` to make the calculation reproducible. When cost is split into service rows, repeat one period-wide denominator; never add duplicated denominators together.
3. **Separate drivers.** Decompose change into traffic/units, price, mix, retention, idle baseline, and implementation efficiency.
4. **Attribute ownership.** Map spend to services and owners; preserve a visible unallocated bucket rather than spreading uncertainty invisibly.
5. **Find waste and design opportunities.** Check idle resources, oversizing, schedules, storage classes/retention, egress paths, log cardinality/volume, duplicate data, build minutes, and architecture-level work multiplication.
6. **Model constraints.** Preserve peak and failover headroom, latency, durability, security, recovery time, and provider quotas.
7. **Build the laboratory.** Baseline cost per unit and gates. Test one change; include transition and rollback costs.
8. **Canary where possible.** Use a tenant, workload class, region, or bounded resource group.
9. **Observe a comparable cycle.** Normalize for traffic and seasonality. Separate realized savings from forecast or negotiated rates.
10. **Record disposition.** Accept, revert, or mark inconclusive with the next evidence window.

## Change classes

- **Remove waste:** idle resource, unused snapshot, obsolete log, orphaned IP. Verify ownership and recovery need before deletion.
- **Right-size:** match capacity to measured demand and headroom. Include scaling lag and failure mode.
- **Rate optimization:** commitment, reserved capacity, or pricing plan. This is a paid commitment and needs explicit authority.
- **Architecture:** reduce duplicated work, storage, transfer, or vendor calls. Measure engineering and reliability tradeoffs.
- **Demand shaping:** cache, batch, schedule, compress, or retain differently. Preserve product semantics.

## Gotchas

- Total spend can rise while cost per useful unit improves; both facts matter.
- Credits and one-time adjustments can fabricate apparent savings.
- Removing redundancy may save money by spending the recovery margin.
- Log reduction can destroy incident evidence; preserve required signals and retention.
- Deleting resources is irreversible enough to require identity, ownership, backup, and explicit authority checks.

## Completion

Cost improvement is complete only when realized cost per useful unit improves over a comparable window, allocation and billing caveats are recorded, reliability/performance/correctness gates pass, and the savings survive the watch period.

## Escalate

Escalate commitments, destructive cleanup, retention-policy changes, cross-team allocation disputes, missing business-unit data, or any saving that trades against an undefined reliability requirement.
