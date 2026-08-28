# Debugging and Testing

## When to use

Use for WGSL errors, black or transparent output, incorrect pixels, NaNs, flicker, visual regressions, adapter differences, multipass bugs, and shader CI.

## Inputs

- exact shader/import graph, vgpu version, adapter identity, target format/size, uniforms, seed, time, and artifact;
- validation/reflection JSON and browser/Node errors;
- smallest reproducible frame and expected values;
- prior baseline and CPU reference when available.

## Diagnosis sequence

1. **Freeze:** fixed size, seed, time, camera, inputs, and adapter policy.
2. **Validate:** run `npx vgpu check` on every file; inspect reflection names and device-validation status.
3. **Diagnose runtime:** run `npx vgpu doctor --pretty`; distinguish environment failure from shader failure.
4. **Prove a write:** replace output with opaque constant color. If absent, inspect target/pass/lifecycle rather than shader math.
5. **Add coordinates:** render UV, depth, normal, or IDs to establish orientation and bindings.
6. **Minimize:** remove passes/material terms until the first failing boundary remains.
7. **Extract:** encode internal scalar/vector values into a tiny target or storage buffer.
8. **Compare:** compute the same landmark cases on CPU and compare exact/tolerant values.
9. **Restore:** reintroduce one term/pass at a time and keep the diagnostic as a regression test.

## Black-output checklist

- target has nonzero physical size and correct format;
- frame/pass is actually submitted and awaited where needed;
- fragment alpha and blend mode do not erase the result;
- coordinates land inside geometry or fullscreen primitive;
- culling/winding and depth comparison allow fragments;
- uniforms/bindings match reflected names, types, and groups;
- textures/samplers are initialized and compatible;
- values are finite and display encoding produces a visible range;
- browser canvas is observed with WebGPU enabled rather than inferred from a blank screenshot artifact.

## Extraction patterns

- Map a bounded scalar into one channel and reserve alpha as a finite sentinel.
- Map signed vectors from `[-1,1]` to `[0,1]` only for diagnostic byte targets.
- Use float readback for HDR or precision-sensitive values.
- Assign one pixel per landmark ray, invocation, sample, or iteration case.
- Encode boolean hit/miss, branch choice, object ID, and normalized iteration count in separate channels.
- Keep extraction code calling the same pure WGSL functions that ship; copied math can reproduce the same bug incorrectly or drift from it.

## Test layers

- **Static structure:** import resolution, reflection, and device-backed WGSL validation.
- **Mock orchestration:** resource/pass/update lifecycle without claiming GPU execution.
- **Headless pixel:** real Dawn/software rendering, landmark assertions, raw RGBA metrics, and tolerant snapshot diff.
- **Browser integration:** public `vgpu` API, surface resize, input, visibility, reduced motion, and fallback.
- **Hardware matrix:** only for bugs/features sensitive to vendor, limits, or precision.

## Snapshot policy

- Pin size, adapter type, vgpu version, seed, time, and inputs.
- Prefer semantic landmark assertions over a single whole-image checksum.
- Use pixel diff thresholds justified by format and adapter variability.
- Baseline updates require a reviewed visual artifact and explanation of the expected change.
- A blank image must never become a baseline; gate alpha, black fraction, variance, and representative pixels first.
- Keep artifacts small enough for fast local and CI iteration.

## Common root causes

- mismatched UV origin or missing aspect correction;
- uniform name/type mismatch despite a plausible value;
- linear/display color confusion or alpha/blend mismatch;
- normalization of a zero vector or invalid math domain;
- implicit derivative inside divergent control flow;
- out-of-range dispatch invocation or texture coordinate;
- uninitialized history target or wrong ping-pong swap order;
- stale target after resize;
- wrong depth space or projection reconstruction;
- resource recreated while a pass still references the old identity.

## Completion

The failure is reproduced deterministically, localized to the first wrong boundary, explained by extracted numeric evidence or a specific API invariant, fixed in shipped code, and protected by a test that goes red on the previous behavior and green on the correction.

## Escalate

Escalate irreproducible vendor-only behavior without device access, validation/runtime disagreement that persists on the pinned version, suspected vgpu defects with a minimal reproduction, or visual expectations lacking an authoritative reference.
