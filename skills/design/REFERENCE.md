# Design Reference

## Direction test

A useful direction answers five questions:

1. What job is the user doing?
2. What must they notice first, second, and last?
3. What character fits the product: quiet, editorial, utilitarian, technical, playful, luxurious, or another specific posture?
4. Which concrete choices carry that character?
5. What single detail makes this surface recognizable without obstructing the task?

If the direction can be applied unchanged to an unrelated product, it is not specific enough.

## Exploration without noise

Use three variants by default and no more than five. Name the axis each explores. Strong axes include navigation, information density, content sequencing, typography, composition, and interaction model. Weak axes include changing only accent color, radius, or shadow.

All variants must use the same realistic content, work at the same viewport, and support the same core action. Keep the comparison harness visually neutral. Variant switching is a high-frequency comparison action, so it must be instant.

## Interface craft checklist

### Hierarchy and composition

- The primary action and primary information are unmistakable.
- Reading order follows visual order and DOM order.
- Repetition creates rhythm; intentional exceptions create emphasis.
- Responsive layouts recompose rather than merely shrink.
- Empty space has a grouping purpose.

### Typography

- Type choices support the product's character and render reliably.
- The scale is small enough to feel systematic.
- Body measure and line height remain comfortable at every viewport.
- Headings avoid awkward single-word wraps where practical.
- Numbers align with tabular figures in tables, timers, and changing metrics.

### Color and surfaces

- Color has semantic jobs; accents are not scattered decoration.
- Text, controls, and focus indicators have sufficient contrast.
- Nested radii visually share a center: outer radius approximately equals inner radius plus inset.
- Elevation uses a consistent light direction and restrained layered shadows.
- Images on similar-colored backgrounds receive a subtle boundary.

### Controls and forms

- Use native semantics and accessible primitives before custom behavior.
- Labels persist; placeholders are examples, not labels.
- Errors are specific, adjacent, announced, and do not erase user input.
- Disabled, busy, success, and destructive states are distinct.
- Keyboard order, Escape behavior, focus return, and focus trapping are correct.
- Touch targets are at least 44 by 44 CSS pixels; mobile text inputs use at least 16px text.
- Hover-only information is also available through focus or touch.

### Polish and performance

- Avoid layout shift from images, fonts, state changes, and loading content.
- Animate only named properties; never use `transition: all`.
- Use `will-change` only after measuring a real problem.
- Press feedback is subtle and does not move the hit target.
- Decorative effects do not compromise scrolling, loading, or input latency.

## Review order

Review in this order because later polish cannot rescue earlier failures:

1. Task completion and information hierarchy
2. Accessibility and interaction correctness
3. Responsive composition and content resilience
4. Typography, spacing, color, and surfaces
5. Motion and micro-polish
6. Performance and implementation consistency

Report only actionable findings. Each should include severity, `file:line`, observed consequence, and the smallest coherent correction. Distinguish code evidence from visual judgment; request or perform a rendered check when code alone cannot establish the result.

## Source lineage

This original synthesis was informed by locally installed `frontend-design`, `emil-design-engineering`, `make-interfaces-feel-better`, and `prototype` skills. It condenses their shared design-engineering ideas rather than reproducing their templates or prose. `frontend-design` is distributed under Apache-2.0. Emil Kowalski's public design and motion work is available at [emilkowal.ski](https://emilkowal.ski/) and [animations.dev](https://animations.dev/).
