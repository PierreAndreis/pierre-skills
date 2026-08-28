# Multipass and Textures

## When to use

Use for offscreen rendering, feedback, ping-pong state, blur/bloom, depth composition, G-buffers, post-processing, texture sampling, mipmaps, and target-format decisions.

## Inputs

- pass graph, dependencies, formats, dimensions, sample counts, and clear/load behavior;
- texture sources, color/data semantics, filtering, wrapping, and mip requirements;
- lifetime and resize policy for every target;
- memory and frame-time budget.

## Procedure

1. Draw the pass graph before code: resources are nodes; reads/writes are directed edges.
2. Read installed docs for passes, frames, texture formats, ping-pong, and two-pass depth.
3. Implement each pass with a diagnostic output before composing the next.
4. State format operations for every resource: render attachment, sampled texture, storage texture, readback, filterability, and precision.
5. Allocate targets once and recreate only when size/format/sample count changes.
6. Batch related passes into one explicit frame submission.
7. Verify clears, load operations, and first-frame initialization.
8. Extract intermediate values numerically when final pixels disagree.

## Pass graph rules

- A pass never reads and writes the same texture view unless the API and algorithm explicitly permit it.
- Ping-pong resources swap roles after a complete step; initial contents are defined.
- Feedback loops have a reset path and deterministic seed/frame state.
- Each target has one lifetime owner and a resize strategy.
- Keep pass order explicit. Hidden scene-graph state must not decide correctness.
- Label passes and resources so validation and GPU traces identify them.

## Texture-format choice

Select format from required operations, not merely channel count:

- display color normally uses an 8-bit normalized display-compatible format;
- HDR intermediates use a float format that supports required rendering/filtering;
- scalar masks can use a single-channel normalized format;
- IDs and counters need integer semantics rather than color normalization;
- depth uses a depth format and sampling path compatible with the effect;
- readback requires a supported layout or a conversion/blit pass.

Check adapter feature requirements. A format that stores the value may not be filterable, renderable, blendable, or writable as storage under the chosen profile.

## Sampling and mipmaps

- Generate or supply mips before sampling levels beyond zero.
- Match linear/nonfiltering sampler types to texture declarations and format capabilities.
- Use `textureLoad` for exact data access and sample functions for filtered color/fields.
- Explicitly handle UV outside `[0,1]` through sampler address modes or math.
- Verify texture orientation at upload boundaries.
- For blur pyramids, test smallest levels, odd sizes, and LOD clamps.
- Avoid sampling uninitialized padding or stale resized targets.

## Blur, bloom, and post-processing

- Use separable filters when mathematically suitable.
- Keep kernel weights normalized unless exposure change is intended.
- Downsample with an appropriate prefilter to prevent aliasing.
- Define threshold and knee in linear HDR space for bloom.
- Composite once with explicit exposure/tone map; avoid repeated gamma conversions between passes.
- Compare each intermediate target with a CPU or diagnostic reference at landmark pixels.

## Depth and G-buffers

- State what each channel stores, in which coordinate space and range.
- Clear depth and attachments to values consistent with “no geometry.”
- Reconstruct positions using the exact projection convention used to write depth.
- Do not store one ray/object's data and consume it as another's; encode object/pass IDs during debugging.
- Test background pixels, near/far extremes, discontinuities, silhouettes, and overlapping geometry.

## Memory budget

Estimate before allocation:

```text
bytes = width × height × bytes-per-pixel × samples × history-count × mip-factor
```

Include color, depth, ping-pong pairs, bloom levels, readback buffers, and DPR. Record peak resize behavior because old and new targets may coexist briefly.

## Completion

The pass graph and resource ownership are explicit, every intermediate pass has independent evidence, formats support all required operations, first-frame/resize/reset paths are correct, memory is bounded, and final composition passes headless and browser validation.

## Escalate

Escalate format/feature gaps on supported adapters, memory exceeding device policy, algorithms that require forbidden read/write aliasing, or pass graphs whose product behavior on reset/context loss is undefined.
