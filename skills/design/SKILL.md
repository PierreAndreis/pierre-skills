---
name: design
description: Designs, builds, reviews, and refines distinctive production web interfaces with deliberate composition, rigorous color systems, typography, responsive behavior, accessibility, data presentation, and rendered verification. Use for pages, components, forms, dashboards, reports, landing pages, design systems, visual reviews, or any interface that feels generic, inconsistent, unclear, unfinished, or difficult to use.
---

# Design

Make the interface communicate before it decorates. Preserve the product's established language unless the user requests a new direction.

## Non-negotiable defaults

- Begin with the user's job, strongest supported answer, and information order.
- Use sentence-case headings that state the point directly. Omit eyebrows, kickers, overlines, decorative section numbers, and all-caps labels above headings.
- Establish hierarchy with composition, typography, spacing, and density before adding surfaces or color.
- Give color semantic work. Default to one restrained accent plus reserved status colors; never scatter accents as decoration.
- Keep one continuous canvas unless a boundary communicates interaction, selection, warning, contrast, or real grouping.
- Avoid generic centered hero copy followed by a card grid, repeated metric boxes, nested cards, decorative pills, arbitrary icon tiles, gratuitous gradients, glows, glass, blobs, and ornamental shadows.
- Use realistic content and preserve facts, qualifiers, units, formulas, states, privacy, and product behavior.
- Build accessible semantics and touch behavior into the first implementation, not a cleanup pass.
- Verify the rendered interface. Source inspection alone cannot establish visual quality.

## Choose the mode

- **Build:** establish direction, implement the complete surface, then verify it.
- **Refine:** preserve the product model and correct the highest-leverage defects.
- **Review:** inspect and report evidence before editing unless fixes were requested.
- **Explore:** build three structurally different variants on named axes; cosmetic reskins do not count.

## Route to the craft playbook

Read only the playbooks the task activates, plus [REFERENCE.md](REFERENCE.md) for shared completion rules.

| Situation | Read |
| --- | --- |
| Direction is missing, generic, or structurally undecided | [Visual direction and composition](playbooks/visual-direction.md) |
| Selecting, repairing, or reviewing a palette or themes | [Color systems](playbooks/color.md) |
| Type hierarchy, labels, headings, wrapping, or UI copy | [Typography and copy](playbooks/typography-copy.md) |
| Grid, spacing, density, surfaces, radii, or imagery | [Layout and surfaces](playbooks/layout-surfaces.md) |
| Buttons, forms, dialogs, menus, states, or component APIs | [Components and controls](playbooks/components-controls.md) |
| Narrow screens, touch, keyboard, focus, or assistive technology | [Responsive and accessibility](playbooks/responsive-accessibility.md) |
| Tables, charts, comparisons, metrics, or calculators | [Data and evidence](playbooks/data-evidence.md) |
| Landing pages, reports, docs, pricing, or narrative pages | [Marketing and editorial](playbooks/marketing-editorial.md) |
| Layout shift, asset loading, rendering cost, or motion | [Performance and motion](playbooks/performance-motion.md) |
| Visual QA, review, screenshots, or handoff | [Verification and review](playbooks/verification-review.md) |

## Working sequence

1. **Recon:** inspect the rendered product, neighboring screens, tokens, primitives, assets, content, states, stack, and responsive behavior.
2. **Frame:** state one sentence naming the intended character and the concrete choices that carry it.
3. **Compose:** decide reading order and geometry before selecting components.
4. **Systematize:** define semantic type, color, spacing, radius, elevation, and state roles; reuse the project's system where it is coherent.
5. **Implement:** build the complete primary flow and its loading, empty, error, success, disabled, and destructive states.
6. **Observe:** render representative narrow and wide viewports; use keyboard and touch-equivalent input; inspect light and dark themes when present.
7. **Refine:** fix the highest-impact systemic defect, render again, and repeat until no known material visual or usability defect remains.

## Deliver

State the direction, what changed, what was actually rendered and exercised, and any remaining subjective, browser, device, or content risk. In review mode, cite `file:line`, explain the user consequence, and propose the smallest coherent correction.
