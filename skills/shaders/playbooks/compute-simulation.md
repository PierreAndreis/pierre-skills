# Compute and Simulation

## When to use

Use for compute shaders, particles, cellular automata, image processing, reductions, GPU tensors, storage buffers, and stateful simulations.

## Inputs

- input/output schemas, element count, dimensions, units, and invariants;
- dispatch shape, workgroup size, storage access, and synchronization needs;
- deterministic seed/time-step policy and CPU reference;
- readback, visualization, precision, memory, and device constraints.

## Procedure

1. Write a scalar CPU reference for a tiny deterministic input.
2. Define buffer layouts and ownership from reflected WGSL types; avoid parallel handwritten layout definitions.
3. Choose workgroup dimensions from access pattern and target limits, then calculate dispatch counts with explicit bounds checks.
4. Run the smallest compute case and read back exact values.
5. Compare GPU output element-by-element with the CPU reference and a justified tolerance.
6. Add ping-pong state or multiple passes only after one step is correct.
7. Visualize the storage result without round-tripping through CPU when the application consumes it on GPU.
8. Measure at representative element count and warm state.

## Indexing contract

- Convert global invocation IDs to logical indices in one tested function.
- Guard out-of-range invocations because dispatch dimensions round up.
- Document row-major/column-major and multidimensional flattening.
- Use integer math for indices and capacities; check multiplication overflow on the CPU allocation side.
- Test first, last, boundary, padded, empty, and single-element cases.

## Workgroup and memory rules

- Workgroup size is a measured choice, not a universal constant.
- Coalesce adjacent memory access where the algorithm permits.
- Use workgroup memory only when reuse exceeds synchronization and complexity cost.
- Every barrier is reached by all invocations in the workgroup through uniform control flow.
- Separate passes when global synchronization is required; a workgroup barrier is not a device-wide barrier.
- Avoid atomics when a reduction, prefix strategy, or partitioned ownership is clearer and faster; when atomics are necessary, test contention.

## Stateful simulation

- Keep previous and next state in distinct ping-pong resources unless in-place updates are mathematically safe.
- Use fixed time steps for deterministic state evolution; cap catch-up work after long pauses.
- Apply forces and constraints in declared units.
- Define boundary conditions explicitly: wrap, clamp, reflect, absorb, or emit.
- Provide reset and seed controls so bugs can be reproduced.
- Assert invariants such as finite values, nonnegative mass, bounded energy, conserved count, or legal cell states.

## Precision and tolerance

- Choose scalar/vector precision and texture/buffer format from numerical range and error budget.
- Compare exact integers exactly. Compare floating values with absolute/relative tolerances justified by operation depth.
- Do not mask NaNs through tolerant comparison.
- Test zeros, denormals where relevant, large magnitudes, cancellation, and boundary values.
- Encode diagnostic flags or counters for invalid states rather than waiting for visual corruption.

## Readback policy

- Read back in tests, debugging, export, or deliberate low-frequency telemetry.
- Batch readbacks and await completion outside the animation-critical path.
- Keep production GPU results resident when subsequent render/compute passes consume them.
- For large diagnostics, sample or reduce on GPU before readback.

## Completion

Tiny GPU results match the CPU oracle, index boundaries and dispatch padding are tested, invariants remain true over multiple deterministic steps, state ownership is explicit, visualization consumes GPU data directly where intended, and representative throughput/memory meet budget.

## Escalate

Escalate algorithms requiring global synchronization inside one pass, precision guarantees unsupported by target adapters, ML buffer ownership conflicts, nondeterminism that breaks product requirements, or memory demand beyond a bounded device policy.
