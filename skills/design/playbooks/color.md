# Color Systems

## When to use

Use when creating or changing a palette, adding light or dark themes, repairing weak contrast, defining state colors, styling charts, or reviewing inconsistent raw values.

## Inputs

- current tokens, brand colors, logos, imagery, and themes;
- required states and data series;
- actual adjacent foreground/background pairs;
- display contexts, browser support, and accessibility target;
- screenshots of the palette in real components, not swatches alone.

## Start with roles

Define semantic roles before selecting values:

```text
canvas
surface-subtle / surface / surface-raised / surface-overlay
text-primary / text-secondary / text-muted / text-inverse
border-subtle / border / border-strong
accent / accent-hover / accent-active / on-accent
focus
info / success / warning / danger and their surface/text/border variants
data-1 … data-n
```

Components consume roles. Palette ramps and raw values remain implementation details.

## Palette procedure

1. **Inventory jobs.** List every semantic role and real adjacent pair. Do not start by generating a ten-step rainbow.
2. **Choose the neutral family.** A slight hue bias may connect neutrals to the brand, but chroma must remain low enough that large surfaces feel stable.
3. **Choose one primary accent.** Reserve it for primary actions, links, selected states, focus, or a single authored emphasis. Do not use it for unrelated decoration.
4. **Reserve state colors.** Success, warning, danger, and information communicate state. Brand and success should not be visually indistinguishable.
5. **Build perceptually.** OKLCH can organize ramps with intentional lightness and chroma. Keep hue shifts deliberate. Convert and test in the actual target color space.
6. **Map semantic tokens.** A dark theme is a new mapping of roles, not a mechanical inversion of light values.
7. **Test components.** Render text, icons, borders, controls, selected rows, code, charts, overlays, disabled content, and focus rings in every theme.
8. **Test contrast.** Measure every material pair. WCAG AA requires at least 4.5:1 for ordinary text and 3:1 for large text; meaningful control boundaries and graphical objects need 3:1 against adjacent colors.
9. **Test without hue.** Use grayscale and color-vision simulations. Meaning must survive through text, icon, shape, position, pattern, or another non-color cue.
10. **Prune.** Merge values that do not produce a perceptible or semantic difference.

## Color budget

- One accent family is the default for a product surface.
- Status families are functional and appear only when their state exists.
- Neutral surfaces carry most of the page.
- A second decorative family requires a named brand or data role.
- Use saturation locally. Large areas need lower chroma than small indicators.
- Do not color a number green merely because it is favorable; explain the basis and pair state with text or iconography.

## Light-theme rules

- Separate canvas, surface, and raised surface with small but visible lightness differences.
- Primary text should feel decisive; secondary text remains readable, not washed out.
- Subtle borders may use low-alpha black only when their composite result is verified on every allowed background.
- Use shadows only to express elevation; a crisp boundary is often enough.
- White is not automatically a raised surface if the canvas is also white. Use spacing, border, or a controlled tonal step.

## Dark-theme rules

- Design dark mode independently. Preserve hierarchy rather than reversing a numeric scale.
- Avoid pure black as the only canvas unless the product direction calls for it; slight tonal separation helps layers remain legible.
- Reduce accent chroma or increase lightness when saturated colors vibrate against dark surfaces.
- Prefer solid dark border tokens over glowing translucent white when a quiet boundary is intended.
- Shadows cannot carry hierarchy alone. Use surface lightness and borders.
- Recheck images, logos, code, syntax colors, charts, focus, and browser autofill.

## Status construction

Each status needs a coordinated set:

```text
status-surface: low-chroma background
status-border: visible boundary
status-text: readable label/detail
status-icon: recognizable cue
status-solid: optional high-emphasis control or indicator
```

Warnings are not decorations. Danger must not look like the primary action. Disabled content uses explicit muted tokens rather than blanket opacity when opacity would produce unpredictable composites.

## Data color

- First ask whether position, length, direct labels, or line style can encode the distinction without color.
- Use a categorical palette only for true categories; use an ordered lightness/chroma scale for ordered values.
- A continuous gradient is acceptable only for a labeled continuous scale.
- Keep the decisive series strongest in both themes; supporting series recede without becoming illegible.
- Direct-label series when space allows. Legends force memory and eye travel.
- Check every series against its plot background and every pair that must be distinguished.

## Token example

```css
:root {
  --color-canvas: oklch(98% 0.006 255);
  --color-surface: oklch(100% 0 0);
  --color-surface-raised: oklch(100% 0 0);
  --color-text: oklch(20% 0.018 255);
  --color-text-secondary: oklch(43% 0.02 255);
  --color-border: oklch(87% 0.012 255);
  --color-accent: oklch(56% 0.19 255);
  --color-on-accent: white;
  --color-focus: oklch(68% 0.17 255);
}

[data-theme="dark"] {
  --color-canvas: oklch(15% 0.014 255);
  --color-surface: oklch(19% 0.016 255);
  --color-surface-raised: oklch(23% 0.018 255);
  --color-text: oklch(95% 0.008 255);
  --color-text-secondary: oklch(73% 0.016 255);
  --color-border: oklch(31% 0.018 255);
  --color-accent: oklch(72% 0.14 255);
  --color-on-accent: oklch(15% 0.014 255);
  --color-focus: oklch(78% 0.13 255);
}
```

Treat these as structural examples, not a universal palette. Measure actual rendered pairs; OKLCH coordinates do not guarantee WCAG contrast.

## Rejection rules

- No decorative gradient text, glows, blobs, glass, colored haze, or rainbow accents by default.
- No raw hex values scattered through components.
- No color-only error, success, selection, required-field, or chart meaning.
- No theme implemented as hundreds of local `dark:` overrides when semantic tokens can switch once.
- No low-contrast muted text used to make a crowded layout appear calmer.

## Completion

Every color maps to a semantic or data role, every material adjacency passes its required contrast, themes preserve equivalent hierarchy, states survive without hue, and the palette was inspected in real components at both low and high emphasis.

## Escalate

Escalate when brand colors cannot meet required contrast in their requested role, when legal brand rules prohibit accessible alternatives, or when data needs more distinct series than the display can communicate reliably.
