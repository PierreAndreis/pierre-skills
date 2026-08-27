# Responsive and Accessibility

## When to use

Use for responsive layouts, touch behavior, keyboard access, focus management, screen-reader semantics, zoom, color contrast, reduced motion, or cross-device review.

## Inputs

- supported viewport and browser range;
- real content expansion and localization cases;
- input methods: keyboard, mouse, coarse pointer, touch, voice, and assistive technology;
- current accessibility target and component primitives;
- sticky regions, overlays, safe areas, media, and time limits.

## Responsive procedure

1. **Begin with content order.** The DOM must make sense without layout CSS.
2. **Find pressure points.** Resize continuously and add a breakpoint where content, target size, reading order, or task efficiency fails.
3. **Recompose.** Collapse sidebars into disclosure, move secondary detail after the primary task, change multi-column comparisons to aligned rows, and preserve context.
4. **Protect targets and type.** Do not solve narrow layouts by shrinking controls and prose below usable sizes.
5. **Test extremes.** Use the narrowest supported width, short landscape height, wide desktop, 200% zoom, long text, browser chrome, and on-screen keyboard.

## Touch and pointer

- Prefer 44×44 CSS-pixel hit areas for touch controls; WCAG 2.2's AA minimum is 24×24 with spacing exceptions, not the comfort target.
- Dense desktop controls may be visually smaller when their hit areas remain distinct and do not overlap.
- Gate hover enhancements with `(hover: hover) and (pointer: fine)`. Core information and actions must work without hover.
- Use `touch-action: manipulation` for ordinary controls; reserve `touch-action: none` for components that intentionally own gestures.
- Do not trigger irreversible action on pointer-down. Activation should allow cancellation before release.
- Place mobile primary controls within comfortable reach without covering content or the system safe area.
- Test drag, swipe, long-press, and scroll gestures against native page movement.

## Keyboard

- Every operable element is reachable in a logical order, and nonoperable or hidden elements are absent from the tab sequence.
- Focus indication is visible against every adjacent color and not clipped by overflow.
- Use `:focus-visible` to avoid suppressing keyboard feedback while allowing appropriate pointer styling.
- Opening overlays moves focus according to the pattern; closing returns it to the initiating control.
- Keyboard movement must keep the focused item in view without disruptive whole-page jumps.
- Support standard keys before adding shortcuts. Display platform-appropriate shortcuts and avoid collisions with browser or assistive commands.
- Provide a skip link when repeated navigation makes reaching main content burdensome.

## Semantics and names

- Prefer native landmarks, headings, lists, tables, links, buttons, fields, and details/disclosure elements.
- Accessible names describe purpose: “Search,” not “magnifying glass icon.”
- Heading levels express structure and do not skip merely for visual size.
- Associate labels, descriptions, errors, table headers, captions, and status messages programmatically.
- Use live regions sparingly for asynchronous changes users must know; avoid announcing every keystroke or visual update.
- Decorative media is ignored by assistive technology; meaningful media has a concise text alternative conveying the same conclusion.

## Contrast and non-color meaning

- Ordinary text needs at least 4.5:1 contrast; large text needs at least 3:1 under WCAG AA.
- Focus indicators, control boundaries needed to identify the control, and meaningful graphics need 3:1 against adjacent colors.
- Test actual composite colors, including transparency, gradients, images, hover, disabled, and autofill states.
- Pair color with text, icon, shape, pattern, position, or another cue for error, selection, status, and charts.
- Thin fonts can look weaker than their calculated contrast; inspect rendered legibility and exceed the minimum where necessary.

## Zoom and reflow

- At 200% zoom, content remains readable and operable without overlap or loss.
- At narrow reflow widths, avoid two-dimensional scrolling except where the content itself requires it, such as a map or wide data table.
- Do not disable pinch zoom or set restrictive viewport scaling.
- Let text grow without clipping fixed-height buttons, tabs, chips, inputs, and table rows.
- Keep sticky regions small enough that zoomed users retain usable content area.

## Reduced motion and media

- Provide a reduced-motion behavior, not merely a media-query token. Remove travel, scale, parallax, smooth scrolling, looping decoration, and layout movement.
- Preserve immediate state feedback through visibility, color, or short opacity changes where appropriate.
- Do not autoplay motion-heavy media for users requesting reduced motion; offer controls or a static alternative.
- Videos that autoplay where allowed are muted and inline, with captions or transcripts when speech or meaningful audio exists.
- Pause time limits, carousels, and transient content when the document is hidden or the user is interacting with them.

## Content resilience

- Test long personal names, email addresses, URLs, numbers, untranslated strings, empty values, and user-generated content.
- Do not encode meaning in left/right directions that fail under RTL.
- Make truncation discoverable and avoid it for primary actions, errors, and distinguishing values.
- Preserve user preferences for font size, contrast, reduced motion, and input method.

## Completion

The primary flow works by keyboard and coarse pointer, targets and focus are usable, semantics expose the same structure as the visual design, contrast and non-color cues pass, zoom and narrow reflow preserve content and actions, and reduced-motion behavior was actually exercised.

## Escalate

Escalate inaccessible brand requirements, custom interactions without an established keyboard model, time limits imposed by policy, or platform constraints that prevent equivalent access without changing product scope.
