# Layout and Surfaces

## When to use

Use for page grids, spacing systems, alignment, responsive composition, density, cards, borders, radii, shadows, imagery, and visual rhythm.

## Inputs

- content hierarchy, repeated structures, and primary interaction path;
- existing grid, container, spacing, radius, border, and elevation tokens;
- realistic short, long, empty, and localized content;
- target viewport range, safe areas, sticky regions, and overlay behavior.

## Geometry before components

1. Map the content to a reading order and shared alignment grid.
2. Choose container width from content needs. Prose, dense tables, and visual evidence require different spans.
3. Identify the dominant object and give it proportionate space.
4. Group related content through proximity before adding a box.
5. Set parent-owned gaps for repeated layouts; components own only their internal rhythm.
6. Introduce breakpoints where the content or interaction fails, not at a named device by habit.
7. Recompose at narrow widths. Do not merely shrink every desktop relationship.

## Grid and alignment

- Use the smallest grid that expresses the composition. A complex column system is not a mark of quality.
- Align related headings, text, controls, charts, tables, and footers to shared edges or baselines.
- Make gutters wide enough that adjacent wrapped text cannot be mistaken for one line.
- Give tables, diagrams, and calculators the width their evidence requires; introductory prose can sit above them.
- Keep equivalent blocks aligned internally: label, value, detail, and action rows land on the same baselines.
- Optical balance may override mathematical centering for asymmetric icons, short labels, or uneven shapes. Record local nudges intentionally.
- Preserve DOM order as the visual reading order. Avoid responsive layouts that visually reorder a different story.

## Spacing system

- Start from a compact scale such as `2, 4, 8, 12, 16, 24, 32, 48, 64`, then adapt to the product rather than mixing arbitrary gaps.
- Within a semantic group, use the smallest gap that preserves distinction.
- Between groups, use a clearly larger gap so the hierarchy survives a squint test.
- Major section turns should be visibly stronger than paragraph or component gaps.
- Give every gap one owner. Parent `gap` is usually clearer than trailing child margins.
- Do not repair a broken composition with a one-off margin. Fix grouping, grid allocation, or the token relationship.
- Empty space amplifies a focal object. Unexplained empty rectangles from underfilled columns or orphaned items are defects.

## Density

- Match density to frequency and task: frequent operational tools favor compact, predictable scanning; narrative or high-stakes decisions need more orientation and breathing room.
- Density is not tiny type. Reduce redundant labels, borders, repeated metadata, and vertical ceremony before reducing legibility.
- Offer compact modes only when the extra density has a real user and preserves targets, focus, and readable values.
- A sparse screen still needs hierarchy. Large margins around equally weak objects produce emptiness, not calm.

## Surfaces and boundaries

- Start with one continuous canvas. Add a surface only for interaction, selection, warning, contrast, elevation, or a semantic group that spacing cannot explain.
- Avoid wrapping every section, metric, or paragraph in a card.
- Nested cards usually indicate a missing hierarchy. Flatten or regroup before styling the nesting.
- Borders separate; shadows elevate. Use each for its physical and semantic job.
- Keep one light direction and a small elevation scale. Overlays sit above raised content; not every card needs lift.
- Low-contrast hairlines must remain visible in both themes and on every allowed background.
- A strong contrast band should be rare, broad, and semantically meaningful—not repeated as a dark rounded box around every chart.

## Radius rules

- Keep a small radius vocabulary tied to component scale and tone.
- Nested nearby corners should be concentric: outer radius approximately equals inner radius plus the inset between them.
- When layers are far apart, treat them as separate surfaces rather than forcing the formula.
- Pills are for compact tags, tokens, statuses, or controls whose shape communicates containment. Ordinary metadata and headings remain text.
- Do not mix sharp and highly rounded geometry without a named reason.

## Images and illustration

- Use media when it proves, demonstrates, or materially explains something.
- Preserve intrinsic dimensions or aspect ratio to prevent layout shift.
- Give screenshots and images a subtle neutral boundary when their edges could disappear into the canvas.
- Match illustration stroke, palette, perspective, and lighting to the UI system.
- Choose a crop for each breakpoint; do not let focal content fall outside mobile crops.
- Decorative media has empty alt text and no pointer events. Informative media has a concise alternative that communicates its purpose.
- Avoid generic stock imagery, abstract blobs, fake screenshots, and illustration packs that look detached from the product.

## Sticky and fixed regions

- Verify sticky headers do not consume excessive short-viewport height.
- Add `scroll-margin` so anchor targets and focused content are not hidden.
- Account for `env(safe-area-inset-*)` on fixed mobile controls.
- Reserve bottom padding equal to fixed bars so the final input or action remains reachable.
- Test overlays and sticky regions with the on-screen keyboard, zoom, and browser chrome where relevant.

## Completion

The layout has a stable reading order, every major alignment and gap has a reason, surfaces communicate rather than decorate, nested radii and elevation are coherent, realistic content does not create overflow or accidental emptiness, and narrow layouts recompose successfully.

## Escalate

Escalate when required content cannot fit without changing product priority, when a fixed control obscures legally or operationally required content, or when brand geometry conflicts with accessibility and platform behavior.
