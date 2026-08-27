# Design Shared Contract

These rules apply across every design playbook.

## Evidence before taste

Separate four kinds of evidence:

- **Product evidence:** task success, support requests, search behavior, analytics, errors, and user feedback.
- **System evidence:** existing tokens, components, brand rules, framework constraints, and neighboring screens.
- **Rendered evidence:** screenshots, viewport checks, keyboard paths, touch behavior, state transitions, and browser output.
- **Judgment:** hierarchy, tone, rhythm, optical balance, and distinctiveness.

Never present judgment as measured fact. Never claim a screen is polished, accessible, responsive, or matched to a reference without observing the relevant output.

## Priority order

When requirements compete, protect them in this order:

1. Facts, formulas, units, qualifiers, privacy, and requested behavior.
2. Task completion, semantics, accessibility, and destructive-action safety.
3. The host project's routes, framework, primitives, tokens, and interaction conventions.
4. Information hierarchy and the strongest supported answer.
5. Responsive composition, content resilience, and performance.
6. Brand character, visual distinction, and polish.

## State completeness

For every interactive surface, account for applicable states:

- default, hover, focus-visible, active, selected, and disabled;
- loading, skeleton, empty, partial, success, warning, and error;
- optimistic, queued, retrying, offline, permission-denied, and destructive confirmation;
- short, typical, long, localized, missing, and user-generated content;
- light, dark, high-contrast, reduced-motion, narrow, wide, touch, and keyboard contexts.

Do not invent states the product cannot enter. Do not omit a real state because it is inconvenient to design.

## System rules

- Use semantic names such as `text-primary`, `surface-raised`, and `border-subtle`; component-specific raw colors are an escape hatch.
- Repeated values express a token or a deliberate local relationship. Remove accidental near-duplicates.
- Keep a component's external layout with its parent; keep its internal rhythm inside the component.
- Prefer composition and variants over large prop matrices and boolean combinations.
- Use established accessible primitives for dialogs, menus, selects, comboboxes, tooltips, and focus traps.
- Preserve DOM order as reading and keyboard order; CSS rearrangement must not create a different story.

## Completion

Design work is complete when:

- the first read, primary action, and information order are unambiguous;
- the implemented direction is specific enough that it would not fit an unrelated product unchanged;
- all applicable states have coherent semantics and visuals;
- narrow and wide layouts recompose without overflow, clipping, broken reading order, or unusable density;
- keyboard focus, labels, errors, touch targets, contrast, and reduced-motion behavior have been checked;
- the real interface was rendered after the final material change;
- remaining risks are named without turning them into false claims.

## Escalate

Ask one grouped question only when proceeding could change product meaning, brand ownership, customer claims, formulas, privacy, destructive behavior, accessibility policy, or the intended audience. Otherwise inspect the repository, choose the safest coherent default, state the assumption, and continue.

## Research basis

- [Vercel design guidance](https://vercel.com/design.md) informed the reader-first framing, evidence hierarchy, continuous-canvas composition, restraint, data-integrity, and rendered-revision rules.
- [WCAG 2.2 text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), and [target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) provide the accessibility baselines.
- [CSS Color Level 4](https://www.w3.org/TR/css-color-4/#ok-lab) defines OKLab and OKLCH, used here as tools for perceptually organized palettes rather than as substitutes for contrast testing.
