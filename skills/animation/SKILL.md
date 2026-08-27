---
name: animation
description: Decides, specifies, builds, debugs, reviews, and improves purposeful web animation with appropriate timing, easing, interruption, spatial continuity, reduced-motion behavior, and frame-budget discipline. Use when adding or fixing UI motion, transitions, gestures, entrances, exits, popovers, drawers, toasts, layout or shared-element animation, CSS keyframes, Motion for React, SVG motion, or animation that feels slow, janky, excessive, or inaccessible.
---

# Animation

Motion earns its place by explaining change, confirming input, preserving spatial continuity, indicating state, or preventing a jarring transition. Delight is valid only when the interaction is rare enough to stay delightful.

## Choose the mode

- **Decide:** inspect the surface and produce a motion brief before code.
- **Build or fix:** make the smallest implementation that satisfies the brief.
- **Review:** inspect every changed motion surface and return evidence-backed findings and a verdict.
- **Improve:** map existing motion, prioritize a short list by leverage, and implement only when requested.
- **Name:** give the established term for an effect, plus close alternatives if ambiguous.

## Recon

Inspect the trigger, start and end states, frequency, existing libraries and motion tokens, component primitives, reduced-motion handling, and the work occurring during the animation. Use the existing stack when it fits; adding a second motion system is a design cost.

For an underspecified animation, settle these decisions: purpose, frequency, properties, origin and direction, re-trigger behavior, personality, easing with duration, reduced-motion variant, and load risk. Ask users about feel or references—not cubic-bezier coordinates they cannot meaningfully choose. Record assumptions.

## Decide whether to animate

- Keyboard-driven or extremely frequent actions should be instant.
- Frequent product interactions get little or no motion.
- Occasional state changes may use concise functional motion.
- Rare, first-run, and marketing moments may carry more expression.

If the static change communicates just as well and motion adds delay, cut it. One purposeful animation beats several ornamental ones.

## Choose the mechanism

- **CSS transition:** interruptible user-driven state changes such as hover, press, and open/close.
- **CSS keyframes:** autonomous loops or simple one-shot sequences that will not be retargeted.
- **CSS or WAAPI:** motion that must remain smooth while the main thread is busy.
- **Motion for React or an existing spring system:** real springs, gestures, momentum, layout/shared-element transitions, or React exit presence.
- **Accessible primitive:** dialogs, menus, popovers, selects, toasts, and drawers whose focus and keyboard behavior should not be rebuilt casually.

Do not add a dependency when the existing stack or a small CSS transition solves the problem.

## Craft the movement

1. Enter and exit with responsive deceleration; use acceleration-deceleration for objects moving on screen; use linear only for constant motion.
2. Tune easing and duration together. Product UI usually finishes in a few hundred milliseconds; exits are typically shorter than entries.
3. Preserve object permanence: triggered surfaces emerge from their trigger; entry and exit directions agree; forward and back feel spatially related.
4. Begin scale entrances near full size with opacity, not from zero. Keep hover and press scale subtle.
5. Anything rapidly reversed or re-triggered must continue from its current state. Prefer transitions or springs over restarting keyframes.
6. Give a container one entrance. If staggering helps hierarchy, keep it short and vary it by importance.

## Accessibility and performance are acceptance criteria

Ship a reduced-motion variant for every animation touched: remove travel, scale, and layout movement while preserving useful opacity or color feedback; stop decorative loops and autoplay. Gate hover motion to devices that support hover and precise pointing.

Prefer `transform` and `opacity`. Avoid animating layout properties, inherited variables across large subtrees, React state on every frame, excessive blur, and speculative `will-change`. Measure with browser performance tooling when the surface is important or feels janky, and test on a representative device.

## Verify by watching

Run the real interface. Replay, reverse, and interrupt the motion; record and scrub it when feel is uncertain. Check rapid input, keyboard and touch paths, reduced motion, slow or growing content, busy-page conditions, console errors, and dropped frames. A code review alone cannot prove that motion feels right.

Read [REFERENCE.md](REFERENCE.md) for the brief, timing ranges, failure patterns, tooling choices, and review rubric. Read [EXAMPLES.md](EXAMPLES.md) for sample briefs and findings.

## Deliver

State what motion was kept, cut, or changed; why; what was observed; and what remains subjective or device-dependent. Reviews cite `file:line`, prioritize user impact, and end with **Block** or **Approve**.
