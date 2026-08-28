# Shader Performance

## When to use

Use for slow frames, compilation stalls, per-frame allocations, bind-group churn, oversized targets, excessive readbacks, bundle growth, or scaling an effect/scene/simulation.

## Inputs

- stated device/runtime/resolution and frame or throughput budget;
- cold and warm CPU/GPU timing, compilation events, and adapter identity;
- pass count, draw/dispatch count, target formats/sizes, buffer/texture inventory, and bundle size;
- representative content complexity and visibility/lifecycle behavior.

## Measure the right cost

Separate:

- cold initialization and adapter acquisition;
- lazy pipeline compilation and first-use target variants;
- CPU command encoding and JavaScript/framework work;
- GPU pass/frame time;
- uploads, bind-group recreation, and readback synchronization;
- target/buffer memory and resize peaks;
- downloaded JavaScript/WGSL/asset bytes.

Do not optimize a warm GPU shader from a cold wall-clock measurement.

## Procedure

1. Build a repeatable benchmark with fixed resolution, inputs, adapter, warm-up, sample count, and percentile.
2. Record the baseline and capture a representative frame/artifact for correctness gates.
3. Identify whether the dominant cost is initialization, compilation, CPU encoding, GPU execution, memory, upload, or readback.
4. Change one causal factor.
5. Re-run the same benchmark and pixel/visual gates.
6. Accept only a repeatable improvement that preserves output and lifecycle behavior.

## vgpu identity model

- Create effects, draws, computes, targets, buffers, samplers, and shared uniforms outside the frame loop.
- Use in-place `set()` updates so stable layout/resource identities can be reused.
- Prewarm every target format/sample/depth variant before a latency-sensitive first interaction when the installed docs support the path.
- Use render bundles for repeated static command structure when re-encoding is a measured CPU cost.
- Batch passes within explicit frames rather than submitting each step independently.
- Reuse ping-pong resources; swap identities instead of allocating history every step.

## Shader cost

- Reduce samples, ray steps, noise octaves, and secondary rays according to visual contribution.
- Move invariant work out of per-fragment/per-invocation paths.
- Share repeated expressions and texture reads when semantics permit.
- Prefer coherent control flow; measure branchless rewrites because extra arithmetic can be worse.
- Choose lower precision/format only when range and error gates pass.
- Reduce overdraw and fullscreen passes before micro-optimizing arithmetic.
- Use lower-resolution intermediate targets for blur/bloom when edge and temporal quality remain acceptable.
- Avoid large animated filters and unnecessary derivative-heavy high-frequency detail.

## Geometry and compute scaling

- Instance repeated geometry rather than issuing many equivalent draws.
- Cull or reduce detail using stable, measured criteria.
- Keep vertex formats compact and aligned with actual shader inputs.
- Match compute workgroups to memory access and adapter limits; benchmark candidates.
- Reduce atomic contention and redundant global memory traffic.
- Keep results on GPU across dependent passes.

## Memory

- Calculate every target/buffer allocation, including DPR, MSAA, depth, mips, history, and double-buffer resize peaks.
- Clamp canvas DPR to the quality actually needed.
- Release obsolete resources after a resize handoff.
- Avoid retaining CPU copies of large GPU assets unless recovery/export requires them.
- Bound caches and example/debug artifacts.

## Lifecycle savings

- Stop frame loops when output is static, offscreen, hidden, or reduced-motion mode freezes it.
- Resume with a bounded time delta.
- Remove event listeners, observers, and controls on unmount.
- Avoid rendering merely because the UI framework rerendered; submit GPU work when visual state changed.

## Performance evidence

Record:

```text
vgpu version and git/package lock
adapter name/type
browser/Node runtime
physical target size and formats
warm-up and sample count
CPU encode p50/p95
GPU frame p50/p95 when available
peak target/buffer estimate
bundle size delta
pixel/visual gate result
```

## Completion

The dominant cost is identified, before/after measurements use the same environment and inputs, improvement survives repeated samples, resource identity/lifecycle are stable, memory is bounded, and pixel plus visual gates confirm no unacceptable regression.

## Escalate

Escalate when required timing APIs/features are unavailable, device variance prevents a valid conclusion, visual quality and budget cannot both pass, or optimization requires changing product behavior or supported hardware.
