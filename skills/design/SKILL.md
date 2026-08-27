---
name: design
description: Designs, builds, reviews, and refines distinctive production web interfaces with deliberate visual direction, coherent systems, responsive behavior, accessibility, and high-fidelity polish. Use when creating or improving pages, components, forms, dashboards, landing pages, design systems, responsive layouts, or when a UI feels generic, inconsistent, unfinished, or hard to use.
---

# Design

Make the interface feel intentional before making it decorative. Preserve the product's existing language unless the user asks for a new direction.

## Choose the mode

- **Build:** establish direction, implement the complete surface, then verify it.
- **Refine:** keep the product model and remove the few details making it feel unfinished.
- **Review:** inspect and report evidence before editing unless fixes were requested.
- **Explore:** when direction is genuinely undecided, make three meaningfully different working variants on named axes; do not create cosmetic reskins.

## Recon before taste

Inspect the actual product, neighboring screens, tokens, primitives, stack, assets, and responsive behavior. Identify:

- the user's task, audience, and information priority;
- established type, spacing, color, radius, elevation, and interaction conventions;
- constraints such as framework, browser support, performance, and accessibility;
- what should remain familiar and the one memorable choice this surface can own.

Do not ask for facts available in the repository. If the user gives no aesthetic direction, infer one from the product and state it briefly.

## State the direction

Write one sentence naming the intended character and the concrete choices that express it. A direction must affect typography, composition, color, surfaces, or imagery—not merely add decoration. Avoid generic defaults, interchangeable card grids, gratuitous gradients, and styling that could belong to any product.

When exploring, vary structural axes such as density, hierarchy, navigation model, content rhythm, or interaction model. Keep the same realistic content and functionality so the comparison is honest. Make switching variants instant and isolate the exploration from production routes.

## Build the system

1. Establish semantic hierarchy and reading order before styling details.
2. Use a restrained type scale, deliberate line lengths, and tabular numbers where alignment matters.
3. Define a small token vocabulary; repeated values should express a system, not coincidence.
4. Use spacing to group meaning. Align optically when mathematical centering looks wrong.
5. Make surfaces coherent: nested corners should feel concentric; shadows should imply one light source; borders should remain visible in every theme.
6. Build on semantic HTML and accessible primitives. Preserve keyboard order, visible focus, labels, errors, and at least 44px touch targets.
7. Design touch-first and enhance hover only for precise pointers. Inputs should not trigger mobile zoom.
8. Reserve motion for meaningful feedback or spatial continuity. If motion is material, use the `animation` skill.

Prefer the project's existing primitives and dependencies. Do not hand-roll complex focus management, dialogs, selects, or menus when a trusted accessible primitive already exists.

## Refine by leverage

Fix structure before decoration: hierarchy → layout → typography → controls → surfaces → imagery → micro-polish. Look for inconsistent radii, accidental spacing, weak contrast, layout shift, clipped focus, overly broad transitions, dead press states, and responsive breakage. A few coherent corrections beat a blanket restyle.

## Verify the real interface

Run the relevant app and inspect the rendered result, not only the source. Check representative narrow and wide viewports, keyboard navigation, focus visibility, touch behavior, long and empty content, loading and error states, both themes when present, console errors, and layout stability. Compare screenshots when matching a reference. Do not claim visual quality you did not observe.

For the detailed craft checklist, exploration method, and review format, read [REFERENCE.md](REFERENCE.md). For example direction briefs and findings, read [EXAMPLES.md](EXAMPLES.md).

## Deliver

State the direction, what changed, what you actually verified, and any remaining subjective or device-specific risk. In review mode, cite `file:line` and order findings by user impact.
