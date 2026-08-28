# Visual and Product Integration

## When to use

Use when a shader becomes part of a page/component, provides a background or visualization, responds to input, animates, carries brand color, or needs responsive/accessibility/fallback behavior.

## Inputs

- user task and whether the shader is content, evidence, feedback, atmosphere, or decoration;
- design tokens, color roles, motion language, layout, stacking, and content contrast;
- canvas CSS size, physical resolution, DPR policy, and interaction model;
- reduced-motion, fallback, loading, failure, and device-support requirements.

## Product role

Name one role:

- **Content:** the shader is the thing users inspect or create.
- **Evidence:** geometry/data communicates a measurable relationship.
- **Feedback:** pixels confirm an action or state.
- **Continuity:** motion explains spatial/state change.
- **Atmosphere:** visual texture supports brand without carrying meaning.
- **Decoration:** removable without information or task loss.

The weaker the role, the stricter the cost and motion budget.

## Composition

- Give content/evidence shaders enough size and labels to be understood.
- Keep atmospheric shaders subordinate to text, controls, and primary evidence at every frame.
- Do not place essential text over a moving high-contrast field unless a stable contrast treatment preserves readability throughout the animation.
- Align shader geometry with page composition deliberately; avoid arbitrary centered blobs or full-bleed noise as default design.
- Use one focal visual behavior. Multiple independent animated fields compete for attention.

## Color

- Consume product palette roles as uniforms or generated constants rather than duplicating raw values across WGSL and CSS.
- Convert colors at a declared boundary; CSS encoded values may need linearization for shader math.
- Preserve status semantics. A decorative field must not accidentally resemble error, success, selection, or loading.
- Check light/dark themes independently and update shader inputs atomically during theme changes.
- Add grain/dither only to correct banding and ensure it does not reduce text legibility or create visible temporal noise.

## Responsive canvas

- Separate CSS display size from physical target size.
- Resize from the actual element box and clamp DPR, usually to the smallest range that passes visual gates.
- Recalculate aspect-dependent uniforms when physical size changes.
- Debounce/reuse targets according to vgpu's resize model without leaving stale targets.
- Test narrow portrait, short landscape, normal desktop, wide desktop, DPR 1/2, zoom, and fractional sizes.
- Preserve layout space during initialization so canvas readiness does not shift content.

## Interaction

- Convert pointer/touch coordinates through the canvas bounding rect and physical resolution exactly once.
- Pointer motion affects only the shader when the canvas owns that interaction; decorative canvases use `pointer-events: none`.
- Provide keyboard/touch alternatives when interaction reveals content or changes state.
- Bound input, define behavior outside the canvas, and clean up listeners.
- Direct manipulation follows input immediately; autonomous motion remains time-based.

## Reduced motion and visibility

- Freeze time at a deliberately composed state or replace the shader with a static artifact.
- Preserve pointer-driven or state feedback only when it does not create disallowed movement.
- Stop the frame loop when the output is frozen, page hidden, canvas offscreen, or component unmounted.
- On resume, clamp elapsed delta so motion or simulation does not jump.
- Never gate reading or action behind a shader intro.

## Fallback and failure

- Detect WebGPU support and adapter/init failure; do not leave a black rectangle or infinite loader.
- Choose an authored fallback: static image, CSS gradient, simplified SVG/canvas, or nonvisual equivalent.
- The fallback preserves information and controls when the shader carries content or evidence.
- Loading state reserves geometry and avoids flashing an unrelated default palette.
- Log actionable diagnostics without exposing device details unnecessarily to end users.

## Visual verification

- Inspect the static canonical frame before animation.
- Observe at least one full loop or representative interaction, including interruption and resize.
- Check all content overlays against the brightest/darkest shader phases.
- Compare reduced-motion and fallback states with the full effect.
- Verify no canvas stretching, blur, clipping, transparent seam, black first frame, or theme flash.
- Use the `design` skill for composition/color review and `animation` for detailed timing/interruption craft when those concerns are material.

## Completion

The shader has a named product role, remains subordinate or focal as intended, uses product color semantics, resizes sharply within DPR/memory bounds, supports input and reduced motion, stops work when hidden, fails into an authored fallback, and was observed in the real interface.

## Escalate

Escalate when the shader carries essential information without an accessible equivalent, brand colors fail required contrast, fallback semantics are undefined, or the visual/performance budget conflicts with supported devices.
