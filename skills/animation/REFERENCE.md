# Animation Reference

## Motion brief

```markdown
## Motion brief — <surface>

**Verdict:** animate | cut
**Trigger and frequency:** <event and uses per user>
**Purpose:** <what motion communicates>
**Enter / exit:** <properties and start/end values>
**Origin / direction:** <anchor and spatial rule>
**Easing + duration:** <paired choice>
**Interruption:** <what a mid-flight reversal does>
**Reduced motion:** <what remains without movement>
**Mechanism:** <CSS transition, keyframes, WAAPI, spring, layout>
**Open risk:** <uncertainty and observation method>
```

## Starting ranges, not cargo cult values

Tune against the actual size, distance, frequency, and product personality.

| Surface | Typical starting range |
| --- | --- |
| Press or small hover response | 100–160ms |
| Tooltip or small popover | 125–200ms |
| Dropdown or select | 150–250ms |
| Modal or drawer | 200–500ms |
| Large travel or marketing sequence | Longer only when observation supports it |

Use a strong decelerating curve for enter/exit, an acceleration-deceleration curve for movement already on screen, a gentle asymmetric curve for color/opacity, and linear for constant-rate loops. Treat spring bounce as personality, not a default; start without overshoot for serious product UI.

## Common failures

- `transition: all`: silently animates unrelated or expensive properties.
- `ease-in` on an interaction: delays the response the user is watching.
- `scale(0)` entrance: destroys physical continuity.
- Center-origin popover: disconnects the surface from its trigger.
- Keyframes on rapid state changes: restart instead of retargeting.
- Parent entrance plus child entrance: makes one event feel layered and slow.
- Uniform long stagger: blocks content and erases hierarchy.
- Movement under reduced motion: honors the media query in name only.
- Ungated hover motion: touch taps produce accidental hover states.
- Width, height, margin, top, or left animation: triggers repeated layout work.
- Per-frame React state or inherited CSS variables: scales main-thread work with content.
- Large animated blur or blanket `will-change`: spends GPU memory and paint budget without proof.

## Mechanism decisions

Choose CSS transitions for user-controlled state because they reverse from the current value. Choose keyframes for autonomous loops and finite sequences. Choose WAAPI when programmatic control and compositor execution matter. Choose a spring library when continuous interruption, momentum, drag, exit presence, or shared layout justifies its cost. Prefer a primitive library already in the repo for focus-heavy UI.

For Motion for React, verify stable keys for exit presence, current direction data for exiting elements, neighboring layout participation, and reduced-motion configuration. Use motion values rather than React renders for high-frequency input.

## Reduced-motion transformation

Remove spatial travel, scale, parallax, layout movement, smooth scrolling, and decorative loops. Retain concise opacity, color, or visibility changes that explain state. Pause autoplaying media with controls or provide a static alternative. Test the actual reduced variant in browser emulation.

## Review rubric

Review every motion surface against:

1. Purpose and frequency
2. Easing and duration
3. Origin, direction, and physical continuity
4. Interruptibility and input tracking
5. Rendering and main-thread cost
6. Reduced motion, hover gating, and touch targets
7. Cohesion with the product's motion language

Block motion that harms a frequent or keyboard action, has no defensible purpose, breaks accessibility, visibly drops frames, or has an easy correction for a severe continuity problem. Approve only after watching the relevant full and reduced variants.
