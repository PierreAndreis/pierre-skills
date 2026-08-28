# Shader Correctness Contract

## Coordinate contract

Write down every coordinate space crossing:

- fragment UV: range, origin, axis direction, and pixel-center convention;
- clip/NDC, view, world, model, tangent, and texture spaces;
- resolution and aspect correction;
- handedness, depth convention, camera projection, and normal transform.

Do not patch flipped axes or stretched circles with unexplained signs. Centralize conversions and test landmark coordinates such as corners, center, near/far plane, and canonical basis vectors.

## Color contract

- Perform lighting and blending in a declared linear space.
- Apply tone mapping once, at the final HDR-to-display boundary.
- Encode for display once; do not double-apply gamma or mix encoded and linear colors.
- Declare straight versus premultiplied alpha and match the pipeline blend state.
- Choose texture formats from required operations: rendering, filtering, storage access, readback, precision, and dynamic range.
- Dither or add subtle grain only when it solves visible banding; keep it stable enough not to shimmer.

## Numerical contract

- Protect denominators and normalization from zero with a scale-appropriate epsilon.
- Define domains before `sqrt`, `log`, inverse trigonometry, fractional powers, and reciprocal operations.
- Keep loops statically bounded where possible and document termination for raymarches and iterative solvers.
- Reject NaN and infinity at the earliest meaningful boundary during debugging.
- Use `select` or uniform control flow when derivatives or texture sampling make divergent branches unsafe.
- Avoid equality tests on interpolated floating-point values.
- Keep units explicit: seconds, pixels, radians, world units, luminance, and normalized ranges must not drift together.

## Sampling contract

- Match sampler filtering to texture format and declaration.
- Choose clamp, repeat, or mirror addressing from the visual model.
- Use explicit LOD or gradients when control flow or nonuniform coordinates make implicit derivatives unreliable.
- For reconstruction, blur, or pyramids, test edges, single-pixel features, and extreme LODs.
- Account for texel centers and half-pixel offsets when mapping pixels to UV.
- Separate data textures from color textures; do not color-decode normals, depth, IDs, or masks.

## Motion contract

- Drive motion from explicit elapsed time or an external ticker, not frame count.
- Keep deterministic time and seed inputs for snapshots and tests.
- Clamp large deltas after background-tab pauses when the simulation cannot safely catch up.
- Use fixed simulation steps with bounded catch-up for stateful physics; rendering can interpolate.
- Make direct manipulation follow input immediately and independently of display refresh rate.
- Provide a still or reduced-motion mode that preserves content and interaction.

## Edge quality

- Correct aspect ratio before distance-field or procedural shape evaluation.
- Use analytic antialiasing such as `fwidth`-scaled transitions where derivatives are valid.
- Test at 1× and bounded high DPR, narrow and wide aspect ratios, and non-integer canvas sizes.
- Avoid resolution-specific magic constants. Express thickness in pixels or normalized units deliberately.
- Inspect silhouettes, intersections, horizon lines, texture seams, and transparent edges against contrasting backgrounds.

## Resource contract

- One owner creates and disposes each GPU context, loop, target, buffer, texture, observer, and event listener.
- Resource sizes have a formula and a maximum. DPR, target pyramids, history buffers, and MSAA multiply memory.
- Reuse targets and buffers across frames. Recreate only when format, capacity, or topology changes.
- Readback is an explicit synchronization cost and belongs in tests, diagnostics, exports, or low-frequency tooling—not the render loop.
- Browser and Node paths use the same public vgpu abstractions where practical; runtime-specific setup remains isolated.

## Evidence ladder

1. **Reflection:** imports, bindings, entry points, and WGSL validation are correct.
2. **Environment:** the selected adapter can render the required format/features.
3. **Pixel assertions:** known coordinates and extracted intermediate values match expectations.
4. **Image metrics:** output is nonblank, bounded, sufficiently opaque, and structurally varied when expected.
5. **Visual inspection:** composition, motion, edge quality, color, and resizing look correct.
6. **Browser path:** the shipping runtime handles lifecycle, input, resize, visibility, fallback, and reduced motion.
7. **Performance:** warm frame time, allocations, memory, compilation, and bundle cost meet a stated budget.

Never use a lower rung to claim a higher one.

## Research basis

- [vgpu agent guide](https://vgpu.sh/agents.md) defines its versioned docs, verified examples, CLI, and read-only MCP surfaces.
- [vgpu shader workflow](https://vgpu.sh/docs/guides/shader-workflow.md) establishes validation, machine diagnosis, headless pixel rendering, browser observation, and extraction-first debugging.
- [vgpu source](https://github.com/vercel-labs/vgpu) documents the cross-runtime API, typed WGSL modules, mock adapter, and MIT license.
- [WebGPU specification](https://www.w3.org/TR/webgpu/) is the authority for pipeline, resource, validation, and execution semantics.
- [WGSL specification](https://www.w3.org/TR/WGSL/) is the authority for shader language semantics and validation.
