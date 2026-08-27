# Design Examples

## Direction brief

> A dense operational dashboard with crisp typography, compact controls, quiet neutral surfaces, and one warm status color; hierarchy comes from alignment and type weight rather than a field of cards.

This is actionable because it constrains density, typography, surfaces, color, and composition.

## Three honest variants

For an incident-management page:

- **Command center:** persistent left navigation, dense event table, fixed action rail.
- **Timeline:** chronological incident narrative with contextual actions beside each event.
- **Focused queue:** one incident at a time with a compact queue and keyboard-first triage.

The variants change structure and workflow while preserving the same data and actions.

## Review finding

| Severity | Location | Finding | Consequence | Correction |
| --- | --- | --- | --- | --- |
| High | `Dialog.tsx:48` | Custom overlay opens without focus transfer or return | Keyboard users can interact with obscured content and lose their place | Use the repository's accessible dialog primitive and verify initial focus, Escape, trap, and return |
| Medium | `Metric.tsx:21` | Proportional figures display a changing counter | Digits shift laterally on every update | Apply the existing tabular-number utility |

## Verification note

> Rendered at 390px and 1440px; completed the primary flow by keyboard; checked loading, empty, and error states; observed no layout shift. Touch-device hover behavior and Safari rendering remain unverified.
