# Data and Evidence

## When to use

Use for dashboards, metrics, tables, charts, comparisons, benchmarks, audit ledgers, calculators, pricing, ROI, and any visual claim based on data.

## Inputs

- source data, definitions, units, periods, populations, denominators, and freshness;
- formulas, rounding, uncertainty, exclusions, and comparison basis;
- reader question and decision;
- privacy requirements and audit needs;
- realistic value ranges, missing data, and error states.

## Truth contract

Preserve the distinction between observation, derivation, projection, recommendation, and causation. A visual must not imply more certainty, normality, representativeness, or causal meaning than its source supports.

Before designing, record:

```text
Question:
Claim or decision:
Source and freshness:
Population and period:
Unit and denominator:
Formula and precision:
Uncertainty and exclusions:
What this does not establish:
```

## Choose the representation

- Use prose for one conclusion that does not require visual comparison.
- Use aligned values for a small exact comparison.
- Use a table for precise lookup across several dimensions.
- Use position or length on a common scale for magnitude and rank.
- Use horizontal order plus aligned position for change over time.
- Use proportion only when the whole and parts are valid and legible.
- Use distance from a marked boundary for threshold or range.
- Use connection and sequence for process or dependency.
- Use a calculator when changing assumptions is the reader's primary job.
- Omit a chart when it does not make the relationship faster to understand.

## Honest encoding

- Length encodings normally start at zero. If a bounded range or delta view answers the question better, mark the baseline and explain it.
- All peer bars share one documented scale and identical plot start/end tracks.
- Do not compare numerators when denominators differ without showing the bases or choosing an appropriate rate.
- Keep units and precision consistent among peers. Do not fabricate decimal confidence.
- Show the exact delta when nearly equal totals make differences hard to see.
- Encode missing, zero, not applicable, suppressed, and unavailable as different values.
- A bar track is not a decorative divider. If length carries no value, use alignment or a rule instead.
- Preserve negative values, reversals, and uncertainty rather than forcing every result into a positive visual grammar.

## Charts

- Give a primary chart enough space to carry the argument. Tiny charts surrounded by panels are decoration.
- Align repeated rows with one parent grid: label lane, plot lane, value lane, and annotation lane.
- Direct-label series where possible. Legends are a fallback when labels would collide.
- Keep labels outside marks and reserve space so lines, bars, and annotations never cross glyphs.
- Use gridlines sparingly and make the reference baseline or threshold stronger than incidental guides.
- Add a caption that states the important relationship and the material limit, not a description of the chart type.
- Provide a semantic table or concise text alternative for material chart data.
- Test every series and annotation in light, dark, grayscale, and color-vision simulations.

## Tables

- Use semantic `<table>`, `<caption>`, `<thead>`, `<tbody>`, scoped headers, and row groups where appropriate.
- Give evidence tables enough width. Move explanation above rather than compressing a wide table beside prose.
- Left-align text columns and headers. Right-align numeric columns and headers.
- Baseline-align body cells so wrapped content does not vertically center unrelated values.
- Give the row-label column enough width for ordinary labels. Reorder or remove columns before shrinking text.
- Do not repeat one category down a whole column when row groups or separate tables communicate it better.
- Highlight a recommendation only when the source supports the recommendation.
- Compact density is for genuine lookup volume, not for making an overfull table fit.
- On narrow screens, choose an explicit strategy: priority columns, stacked labeled rows, horizontal scrolling with a clear affordance, or a separate summary. Never clip silently.

## Metrics and comparisons

- A set of peer metrics shares label, value, detail, unit, period, and precision structure.
- Do not enlarge one value because it is favorable while keeping equivalent peers smaller.
- Show context near the value: compared with what, over which period, for which population.
- Avoid repeated bordered KPI cards when a single aligned strip, sentence, or composed comparison is clearer.
- Status color does not replace a threshold label or trend explanation.

## Calculators

1. Define canonical variables, fixed inputs, formulas, units, ranges, steps, defaults, dependencies, and display precision.
2. Let one control own each variable. Fixed parameters look like evidence, not disabled fake controls.
3. Pre-render the default result and update all dependent outputs atomically from full-precision state.
4. Preserve invalid input and the last valid result while explaining the correction; do not silently clamp.
5. Keep controls, focal result, assumptions, and supporting outputs in one coherent tool.
6. When the calculator is the primary task, put the working tool in the first viewport rather than below ceremonial copy.
7. Make controls keyboard and screen-reader usable and announce one concise result update.
8. Show formulas and assumptions where they help trust or reproducibility.

## Audit paths

Support two reading speeds when evidence is extensive:

- **Decision path:** headings, decisive values, captions, recommendation, and caveat communicate the answer quickly.
- **Audit path:** exact table, method, assumptions, source, exclusions, and all rows preserve verification.

If a large audit table defaults to a subset, use a neutral rule such as failures, exceptions, or rows named in the decision. State the active rule and show selected and total counts. Provide a direct path to all rows.

## Completion

Every visible claim traces to a source and definition, geometry matches the relationship, scales and denominators are honest, units and precision are present, missing values are explicit, the decision and audit paths agree, and the visualization remains interpretable without color alone.

## Escalate

Escalate contradictory sources, missing denominators, privacy-sensitive detail, unsupported causal claims, formulas with commercial consequences, or recommendations whose decision rule has not been approved.
