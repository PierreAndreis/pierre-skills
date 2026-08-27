# Performance and Motion

## When to use

Use for layout shift, slow rendering, font or image loading, large lists, expensive effects, transitions, theme changes, or deciding whether motion belongs in a design.

## Inputs

- actual browser trace, Core Web Vitals, frame behavior, and device class when available;
- asset sizes, fonts, images, video, DOM volume, and rendering path;
- interaction frequency, motion purpose, reduced-motion requirements, and existing motion language;
- framework and dependencies already installed.

## Stability first

- Give images and video explicit dimensions or aspect ratios.
- Reserve realistic space for async content and skeletons.
- Use tabular figures for values whose width changes.
- Keep font weight and control geometry stable across states.
- Load metric-compatible fallback fonts and only the weights/subsets used.
- Hydrate initial theme and persisted UI state before first paint where possible; avoid a visible default-state flash.
- Keep error, validation, and loading messages from unexpectedly pushing critical actions off-screen.

## Rendering procedure

1. Measure the real path before optimizing.
2. Identify whether the bottleneck is network, script, style, layout, paint, compositing, or server response.
3. Fix the largest user-visible cause with the smallest coherent change.
4. Re-run the same interaction and device profile.
5. Preserve visual and accessibility behavior; faster but incomplete is a regression.

## Assets

- Preload only fonts and above-the-fold images proven critical. Excess preloads compete with more important requests.
- Serve responsive image sizes and modern formats while retaining a correct fallback.
- Lazy-load below-the-fold media with reserved dimensions.
- Pause video, canvas, observers, and loops when off-screen or hidden.
- Keep decorative media out of the critical path.
- Prefer static generation or caching for content whose freshness requirements allow it.

## DOM and lists

- Remove decorative wrappers that do not contribute semantics, layout, or styling.
- Paginate or virtualize large interactive lists only when DOM volume is measured as a problem; virtualization adds focus, measurement, and accessibility complexity.
- Use `content-visibility` cautiously and test search, focus, print, and anchor navigation.
- Avoid inherited CSS variables that change every animation frame across deep subtrees.
- Keep high-frequency pointer or animation state outside framework rerenders when the rendering model makes per-frame state expensive.

## Motion decision

Motion earns its cost when it:

- explains where an object came from or went;
- preserves continuity across a state or layout change;
- confirms input immediately;
- communicates progress or causality;
- makes direct manipulation track the user's gesture.

Frequent product actions favor immediate stillness or very short feedback. Marketing surfaces can carry more motion only when the narrative benefits. Default to stillness when purpose is unclear.

For detailed motion design and implementation, use the `animation` skill.

## Motion implementation rules

- Use CSS transitions for interruptible user-controlled state changes.
- Use keyframes for autonomous loops or finite staged sequences.
- Animate composite-friendly `transform` and `opacity` by default.
- Name exact transitioned properties. Never use `transition: all`.
- Use `will-change` only after observing first-frame stutter and remove it from long-lived large element sets.
- Keep blur and filter animation restrained, especially on large surfaces and Safari.
- Entering elements normally decelerate into place; on-screen movement uses a balanced acceleration/deceleration; exiting may be quicker and less prominent.
- Anchor popovers, menus, and dialogs to their trigger or spatial source when that continuity helps.
- Ensure mid-flight reversal starts from the current visual state rather than restarting.
- Disable broad transitions during theme changes so components do not repaint at different rates.

## Reduced motion

- Remove travel, parallax, scale, smooth scrolling, layout movement, and decorative loops.
- Keep immediate feedback through color, visibility, or a concise opacity change when useful.
- Do not gate content or task completion behind an animation.
- Replace autoplaying motion-heavy media with a still image or explicit controls.
- Test the reduced variant directly; a media query in source is not evidence that the result works.

## Loading feedback

- Use a skeleton when the final geometry is known and reserving shape improves comprehension.
- Use a spinner for compact indeterminate work where the future structure is not meaningful.
- Show determinate progress when measurable.
- After roughly a human-perceptible delay, explain what is happening; for long operations, let the user leave and return.
- Do not animate a skeleton so aggressively that loading becomes the most visually prominent state.

## Completion

The measured bottleneck improved on the same path, layout remains stable, critical assets are prioritized without over-preloading, motion has a named purpose and reduced variant, and no visual optimization regressed semantics, interaction, or accessibility.

## Escalate

Escalate performance work without reproducible measurements, requests for motion that conflicts with accessibility policy, virtualization that would break required navigation, or asset-quality reductions that change product meaning.
