# Verification and Review

## When to use

Use after building or refining UI, when reviewing a design implementation, when matching a reference, or whenever visual quality, responsiveness, or accessibility must be claimed.

## Inputs

- runnable application and route;
- design direction, requirements, references, and acceptance criteria;
- representative accounts, permissions, states, content, themes, and devices;
- source diff and relevant performance/accessibility tools.

## Render matrix

Choose the smallest matrix that covers material risk:

- narrow phone, wider phone or tablet when composition changes, normal desktop, and wide desktop;
- short landscape viewport for sticky and modal behavior;
- light and dark themes when supported;
- default, loading, empty, error, success, disabled, selected, destructive, and permission states as applicable;
- short, typical, long, localized, and missing content;
- mouse, keyboard, coarse pointer or touch-equivalent input, reduced motion, and 200% zoom;
- Chromium plus any explicitly supported browser with different rendering risk.

## Inspection order

Review in this order because later polish cannot rescue earlier failures:

1. **Task:** Can the user identify and complete the primary job?
2. **Truth:** Are content, values, units, claims, permissions, and destructive consequences accurate?
3. **First read:** Is the dominant information/action and reading path obvious?
4. **Semantics:** Do heading, landmark, control, label, table, and status structures match the visual interface?
5. **Keyboard and touch:** Are focus order, focus return, targets, hover independence, and gesture behavior correct?
6. **Responsive composition:** Does the interface recompose without loss, overlap, accidental emptiness, or broken order?
7. **Typography and color:** Are roles consistent, wraps deliberate, contrast sufficient, and non-color cues present?
8. **Controls and states:** Are all applicable states distinct, stable, and recoverable?
9. **Evidence:** Are charts, tables, metrics, and calculators honest and aligned?
10. **Performance:** Is there layout shift, delayed input, jank, asset flash, or unnecessary work?
11. **Restraint:** Can a border, box, pill, icon, color, paragraph, animation, or section be removed without losing meaning or rhythm? Remove it.

## Visual tests

- **Squint test:** dominant object and grouping remain visible when detail disappears.
- **Baseline test:** peer labels, values, actions, and table columns align.
- **Edge test:** inspect every container edge, crop, radius, outline, shadow, and overflow boundary.
- **Theme parity:** light and dark preserve the same hierarchy; neither hides focus, borders, media, or chart series.
- **Content stress:** long labels, names, values, translated strings, empty rows, and failures do not break geometry.
- **Reference comparison:** use side-by-side screenshots at the same viewport. Distinguish required fidelity from intentional adaptation.
- **Motion observation:** watch full and reduced variants, including rapid interruption and repeated use.

## Review findings

Report only actionable findings. Each finding contains:

```markdown
### [Severity] Short consequence-led title

- Location: `file:line`
- Evidence: what is present in code or rendered output
- User consequence: what becomes unclear, inaccessible, incorrect, slow, or inconsistent
- Correction: the smallest coherent system-level fix
- Verification: how to prove the correction
```

Severity:

- **Critical:** blocks the primary task, exposes unsafe behavior, or makes material content inaccessible.
- **High:** breaks a common path, viewport, state, or truthful interpretation.
- **Medium:** creates recurring confusion, inconsistency, or significant polish debt.
- **Low:** localized refinement with a clear but limited benefit.

Do not file subjective preference as a defect unless it violates the stated direction or system. Distinguish source evidence from rendered judgment.

## Refinement loop

1. Select the highest-impact systemic defect.
2. Correct its source of truth—token, layout rule, primitive, content model, or shared component.
3. Render every surface likely to inherit the change.
4. Re-run the affected task and state.
5. Continue until no known material defect remains or a clearly named blocker requires human judgment.

Avoid broad restyles during review. A coherent correction to one shared cause is safer and more useful than many unrelated tweaks.

## Handoff

State:

- the direction and primary organizing move;
- surfaces and system rules changed;
- exact routes, viewports, themes, states, and input methods exercised;
- automated checks run and what they cover;
- remaining browser, device, content, data, or subjective risk;
- screenshots or artifacts when useful.

Do not say “pixel perfect,” “fully accessible,” “responsive,” or “production ready” when the evidence covers only a subset.

## Completion

The final rendered version was inspected after the last material edit, primary flow and risky states were exercised, every reported issue has evidence and a correction, inherited surfaces were checked after system changes, and the handoff distinguishes verified behavior from remaining risk.

## Escalate

Escalate when the application cannot be rendered, test data cannot reach a material state, a reference is ambiguous, supported-browser behavior conflicts, or correctness depends on product/brand judgment not present in the repository.
