# Design Examples

## Direction brief

> A dense operational workspace that prioritizes rapid scanning: narrow neutral palette, compact sans-serif type, aligned numeric columns, one blue action color, flat continuous canvas, and a persistent command area. Its memorable move is a live incident timeline aligned directly with service health, not a grid of status cards.

This predicts typography, density, color, surfaces, composition, and the subject-specific organizing move.

## Heading correction

Before:

```text
PLATFORM
Built for the future
Everything your team needs to move faster
```

After:

```text
Ship an authenticated preview in under five minutes
Connect the repository, choose an environment, and deploy with the existing access policy.
```

The revision removes the eyebrow layer, replaces generic praise with a supported outcome, and makes the next step concrete.

## Color contract

```markdown
### Palette intent

- Neutral family: cool, nearly achromatic, optimized for dense operational content
- Accent: blue, reserved for links, primary actions, selected navigation, and focus
- Success: green, used only for confirmed completed state
- Warning: amber, used for degraded or intervention-needed state
- Danger: red, used for destructive actions and verified failure
- Themes: independent semantic mappings with equivalent hierarchy

### Required pairs

| Foreground | Background | Role | Minimum |
| --- | --- | --- | --- |
| `text-primary` | `canvas` | body text | 4.5:1 |
| `text-secondary` | `surface` | supporting text | 4.5:1 |
| `on-accent` | `accent` | button label | 4.5:1 |
| `focus` | adjacent surface | focus indicator | 3:1 |
| `danger-border` | `danger-surface` | control/state boundary | 3:1 |
```

The table is a verification contract. Palette coordinates alone are not proof.

## Three honest variants

For an incident-management page:

- **Timeline command:** a chronological incident stream owns the center; controls align to the active event.
- **Service matrix:** services form rows and diagnostic layers form columns; exceptions become immediately scannable.
- **Focused queue:** one incident owns the workspace, with a narrow keyboard-operated queue and evidence drawer.

The variants change topology and workflow while preserving the same incidents, actions, and evidence.

## State inventory

```markdown
### Invite member

- Default: email field and role selector
- Invalid: malformed address remains in field; specific inline error is announced
- Existing member: explains current role and links to member settings
- Submitting: controls remain stable; duplicate submission is prevented
- Success: member row appears optimistically, then reconciles with server response
- Permission denied: action is removed or disabled with an explanation based on product policy
- Network failure: input remains; retry does not duplicate an accepted invitation
```

## Data choice

Question: Which service consumes the latency budget?

- Use a common-scale horizontal bar list for service contribution.
- Put service name, bar, exact milliseconds, and percentage in shared lanes.
- Direct-label each row; omit a legend.
- Show the observation window and request population beside the caption.
- Do not use independent full-width progress bars, because equal tracks would imply a shared whole while hiding the comparison.

## Review finding

```markdown
### High — Error state disappears for keyboard users

- Location: `src/components/EmailField.tsx:48`
- Evidence: the border changes from gray to red, but no message, icon, `aria-invalid`, or description relationship is present
- User consequence: color-blind and screen-reader users cannot identify or correct the failure
- Correction: preserve the input, add a specific inline message, connect it with `aria-describedby`, set `aria-invalid`, and pair the red boundary with an error icon
- Verification: submit the invalid value by keyboard and confirm visual and screen-reader feedback
```

## Verification note

> Rendered the final route at 360×800, 768×1024, 1440×900, and 1728×1117. Exercised default, loading, empty, invalid, permission-denied, and success states in light and dark themes; completed the primary flow by keyboard; inspected 200% zoom and reduced motion. Safari touch behavior and Windows font rendering remain unverified.
