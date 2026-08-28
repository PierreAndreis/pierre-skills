# Fullscreen Effects

## When to use

Use for procedural backgrounds, gradients, noise, SDF shapes, raymarching, generative art, fragment-only post effects, and canvas-covering visual fields.

## Inputs

- effect contract: purpose, palette, motion, interaction, output alpha, and fallback;
- target sizes, aspect ratios, DPR policy, and frame budget;
- explicit uniforms such as resolution, time, seed, pointer, intensity, and reduced-motion state;
- color-space and target-format contract.

## Procedure

1. Read the installed effect concept and getting-started pages.
2. Search the verified gallery by technique and visual intent before writing boilerplate.
3. Build a static shader at fixed resolution, time, seed, and input.
4. Center and aspect-correct coordinates once:

```wgsl
var p = uv * 2.0 - 1.0;
p.x *= resolution.x / resolution.y;
```

Confirm the vgpu effect UV origin in the installed docs instead of assuming another shader playground's convention.
5. Separate reusable pure math—hash, noise, SDF, palette, ray functions—from entry-point bindings.
6. Add time only after the static frame passes pixel and visual gates.
7. Update uniforms in place inside the frame loop. Keep the effect, surface, clocks, and resources stable.
8. Resize through the surface API and clamp DPR to an intentional range. Verify non-square and fractional CSS sizes.
9. Add reduced-motion and WebGPU fallback behavior before integration is complete.

## SDF rules

- Keep distance units consistent after aspect correction and transforms.
- Compose distance fields with operations that preserve or intentionally alter distance quality.
- Use derivative-scaled antialiasing near boundaries when available.
- Separate geometry distance from material/color selection so debugging can display each independently.
- Test shape centers, edges, corners, unions, subtraction cavities, and near-zero thickness.

## Noise and procedural fields

- Choose noise from the visual frequency, tiling, dimensionality, and cost—not popularity.
- Keep seeds explicit and deterministic.
- Limit octave count and attenuate amplitude/frequency intentionally.
- Avoid evaluating expensive noise repeatedly when a shared result or lower-frequency field suffices.
- Check temporal coherence. Frame-varying random seeds produce shimmer rather than motion.
- Use domain warping sparingly; inspect gradients and aliasing at high frequency.

## Raymarching

- State camera origin, ray convention, maximum distance, maximum steps, and hit epsilon.
- Scale the hit threshold with scene scale and distance when needed.
- Break on hit and far escape; expose normalized step count as a debug view.
- Calculate normals with a documented finite-difference strategy and epsilon.
- Guard shadow, reflection, and secondary rays with separate budgets.
- Start with unlit normals/depth/step-count views before materials.
- Test inside-geometry starts, grazing rays, thin features, discontinuities, and missed surfaces.

## Color and alpha

- Compute procedural color in the declared working space.
- Match output alpha to the canvas composition model; opaque backgrounds should not accidentally produce transparent edges.
- Avoid clipping HDR intermediate values before the final map to the target.
- Check contrast and legibility of overlaid product content at every animated phase, not one screenshot.

## Performance gates

- Warm frame time is measured at representative physical resolution.
- No resource or shader recreation occurs per frame.
- Ray steps, noise octaves, samples, and branches have explicit ceilings.
- Reduced mode and hidden/offscreen state stop unnecessary frame work.
- Visual frequency remains below what the target resolution can represent without severe aliasing.

## Completion

The static frame is deterministic, coordinates stay correct across aspect ratios, color/alpha are intentional, motion is time-based and reducible, WGSL validates, headless pixels pass, browser output was observed, and warm frame cost meets budget.

## Escalate

Escalate visual requirements that demand unsupported precision/features, effects that make product text unreadable, mobile budgets incompatible with the requested sample count, or a fallback whose product meaning is unclear.
