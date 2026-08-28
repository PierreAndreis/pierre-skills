# Shader Examples

## Effect contract

```markdown
### Aurora field

- Runtime: browser canvas through `vgpu`; deterministic Node render through `vgpu/node`
- Output: fullscreen premultiplied RGBA in display-encoded `rgba8unorm`
- Inputs: resolution in physical pixels, elapsed seconds, seed, pointer in normalized canvas coordinates
- Coordinates: UV origin top-left from effect input; centered coordinates corrected by `width / height`
- Color: procedural values computed in linear space, one final display encoding
- Motion: time-based; static at `time = 0`; reduced mode freezes time and preserves pointer response
- DPR: clamped to `[1, 2]`
- Budget: warm GPU frame p95 below 2 ms on the target device; no per-frame allocation
- Fallback: authored CSS radial field using the same palette
```

## Discovery commands

```bash
python scripts/project_inventory.py .
npx vgpu docs cat getting-started.md
npx vgpu docs find "full screen effect"
npx vgpu examples search "procedural noise" --pretty
npx vgpu examples show <id> --pretty
```

Inspect the manifest before using `pull`. Pull only into an explicit empty project subdirectory.

## Validation ladder

```bash
npx vgpu check src/shaders/aurora.wgsl
npx vgpu check src/shaders/noise.wgsl
npx vgpu doctor --pretty
VGPU_VALIDATE=require npx vgpu check src/shaders/aurora.wgsl
```

The ordinary check may report reflection while device validation is unavailable. CI uses required validation so missing GPU validation is not mistaken for success.

## Headless render assertions

For a deterministic 64×64 static frame, assert:

- alpha is 255 at the center and representative corners when the effect is opaque;
- the center pixel is inside the expected channel interval;
- black and transparent fractions remain below chosen thresholds;
- unique-color count exceeds a minimum for a gradient or noise field;
- the same seed/time produces the same reference pixels on the pinned software renderer.

```bash
python scripts/rgba_metrics.py artifacts/aurora.rgba --width 64 --height 64
```

Use exact pixel assertions for math. Use tolerant pixel diffs for whole images only after accounting for adapter and precision variability.

## Bundled smoke render

Copy `templates/static-field.wgsl` and `templates/headless-smoke.mts` into a small project directory with `vgpu` and a TypeScript runner installed. The `.mts` extension makes the ESM-only Node entrypoint explicit. After the software adapter is available:

```bash
npx vgpu check static-field.wgsl --require-validation
npx tsx headless-smoke.mts
python rgba_metrics.py static-field.rgba \
  --width 64 --height 64 \
  --max-black-fraction 0 \
  --max-transparent-fraction 0 \
  --min-luma-stddev 0.05 \
  --min-unique-colors 16
```

This proves validation, a real vgpu Node render, readback, and nonblank pixel structure. It does not prove the shipping browser integration or final visual quality.

## Internal-value extraction

When a raymarch produces a wrong highlight, render a tiny diagnostic target where channels encode:

```text
R = normalized step count
G = hit flag
B = encoded surface normal z
A = finite-value sentinel
```

Read those pixels in Node and compare them to a CPU implementation at the same rays. This turns an ambiguous image into four inspectable numbers per ray.

## Visual handoff

> Validated both WGSL modules, rendered a deterministic 320×180 Node frame through the pinned software adapter, checked landmark pixels and RGBA metrics, then observed the browser canvas at 360×800 and 1440×900 with DPR 1 and 2. Reduced motion freezes autonomous time while pointer response remains. Hardware timing on the lowest supported mobile GPU remains unverified.
