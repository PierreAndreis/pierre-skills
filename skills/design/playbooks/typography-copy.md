# Typography and Copy

## When to use

Use for type selection, hierarchy, labels, headings, tables, long-form text, numeric displays, localization, truncation, or interface copy.

## Inputs

- existing font families, files, licensed weights, and fallback stacks;
- content hierarchy, reading length, density, languages, and numeric needs;
- available type tokens and rendered screenshots across platforms;
- actual labels, errors, empty states, and data—not lorem ipsum.

## Type-system procedure

1. **Preserve or justify.** Use the existing family unless a change is explicitly requested or the current face cannot serve the content. A new typeface changes loading, metrics, language support, and brand.
2. **Assign roles.** Define display, page title, section heading, subsection, body, compact body, label, metadata, and code/identifier roles only when each has a real job.
3. **Keep the scale small.** Prefer a few clearly separated roles over many near-identical sizes. Test the scale in context, not as isolated specimens.
4. **Pair size, weight, leading, and tracking.** A token owns the full role. Do not resize one peer because its content is longer.
5. **Set measure.** Keep reading prose near 55–70 characters per line. Dense UI labels and tables follow their task rather than article measure.
6. **Load deliberately.** Include only used subsets, weights, and styles. Define metric-compatible fallbacks and reserve space to avoid font-swap layout shift.
7. **Inspect rendering.** Compare macOS, Windows, and mobile when typography is a material part of the direction.

## Heading rules

- Write sentence-case headings that state the claim, question, or task directly.
- Use one heading element per level and preserve semantic order.
- Omit eyebrow text, kickers, overlines, decorative chapter numbers, and tiny all-caps labels above headings.
- Do not repeat the same idea in an eyebrow, title, lede, and first sentence.
- Use a display role only for one page-defining statement whose importance earns the scale.
- Fix awkward line breaks by improving copy, measure, or planned line breaks before shrinking the type.
- Use `text-wrap: balance` for short headings only when it improves the shape; inspect the result at every relevant width.
- Avoid single orphan words and stranded punctuation. Do not force symmetry that changes meaning.

## Body and UI text

- Body text uses comfortable leading, usually around 1.45–1.65 depending on face, size, and measure.
- Compact UI text can use tighter leading but must remain legible under density and zoom.
- Use space between paragraphs; first-line indentation is for deliberate editorial systems, not default product copy.
- Use `text-wrap: pretty` for short descriptions when supported and beneficial. Leave long text to normal wrapping when it performs better.
- Keep links recognizable without relying only on color. Underline body links by default; control-like links may follow established component treatment.
- Italics express voice, titles, or linguistic stress. Use weight and placement for interface hierarchy.
- Underlines signal links. Do not reuse them as generic emphasis.

## Weight and emphasis

- Body copy normally uses regular weight; headings use one consistent heading weight; medium or semibold is reserved for local emphasis and controls.
- Avoid very light weights at small sizes or low contrast.
- Do not change font weight on hover, selection, or async updates if metrics would shift. Change color, underline, background, or add an invariant reserved width.
- Use bold sparingly enough that emphasis remains meaningful.
- Equal peers use identical role, weight, line-height, and numeric treatment.

## Numbers and code

- Use tabular figures in tables, timers, financial comparisons, counters, and values that update or align vertically.
- Right-align numeric table columns, including their headers, placeholders, and totals.
- Keep units, periods, bases, and precision consistent among peers. Do not add decimal precision the source does not support.
- Use a monospaced face for code, commands, paths, raw tokens, timestamps, and short operational identifiers—not for whole explanatory sentences.
- Preserve selectable text for values users may copy. Avoid rendering important text into images or canvas.

## Labels, actions, and messages

- Button labels name the action and object: “Save changes,” “Download CSV,” “Delete workspace.” Avoid generic “Submit,” “Continue,” or “Confirm” when the specific action fits.
- Front-load notification meaning: “Export ready” before location details.
- Persistent labels identify inputs; placeholders demonstrate format or optional examples.
- Error messages name what failed, why when known, and the next action. Keep them beside the responsible field or control.
- Empty states distinguish “nothing exists,” “filters found nothing,” “loading failed,” and “permission denied.” Give a relevant next step.
- Destructive copy names the object and consequence. Do not hide irreversible meaning behind reassuring language.
- Use the user's vocabulary rather than internal architecture names.

## Truncation and localization

- Prefer reflow, wrapping, or wider allocation before truncation.
- Truncate only when the full value is available through an accessible detail mechanism and the task can proceed without seeing it.
- Never truncate errors, primary actions, required instructions, or values that differ at the end.
- Test labels at 30–50% expansion and with representative long names, email addresses, paths, and numbers.
- Avoid embedding direction or word order into icons and layout. Support bidirectional content when the product requires it.

## Typographic polish

- Use typographically correct apostrophes, quotes, ellipses, and dashes where the content system supports them; do not silently alter code, IDs, filenames, or user input.
- Optical alignment can correct punctuation, play icons, or uneven glyph shapes when geometric alignment looks wrong.
- Font smoothing is a platform-specific rendering choice, not a substitute for selecting a readable weight.
- Headings and body should remain readable at 200% zoom without clipped lines or overlapping regions.

## Completion

Every type role has a distinct job, headings contain no eyebrow layer, content order and heading semantics agree, line lengths and wraps hold across target widths, numbers align where needed, and real copy—including errors and long values—was rendered.

## Escalate

Escalate missing font licenses, brand-mandated type that fails language or readability needs, copy whose legal/commercial meaning is unclear, or localization constraints that require product decisions.
