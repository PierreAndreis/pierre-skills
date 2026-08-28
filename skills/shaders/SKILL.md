---
name: shaders
description: Builds, integrates, debugs, tests, and optimizes WebGPU shaders with vgpu, typed WGSL modules, browser canvases, headless Node rendering, and deterministic evidence. Use for WGSL, fragment effects, procedural graphics, raymarching, GPU compute, particles, simulations, post-processing, textures, 3D scenes, shader visual bugs, GPU performance, or adding vgpu.sh to a TypeScript web project.
---

# Shaders with vgpu

Treat pixels as program output. Validate the shader, render a small deterministic frame, inspect or extract its values, then integrate it into the user-facing runtime.

## Non-negotiable defaults

- Inspect the project and installed `vgpu` version before writing API calls.
- Use version-matched local docs through `npx vgpu docs`; load one relevant page at a time.
- Search verified examples before inventing integration code.
- Keep WGSL in importable modules and validate every entry and helper file with `npx vgpu check`.
- Use one `Gpu` context and stable resource identities; update values in place instead of rebuilding GPU objects per frame.
- Make time, resolution, pointer, seed, and other animation inputs explicit.
- Render and read actual pixels. A successful compile is not visual proof.
- Debug nontrivial math by encoding internal values into pixels and comparing them with a CPU reference.
- Preserve reduced-motion behavior, responsive resolution, device-pixel-ratio bounds, and a usable fallback when WebGPU is unavailable.
- Dispose Node resources and stop frame loops, observers, and listeners during cleanup.

## Route to the playbook

Read [REFERENCE.md](REFERENCE.md) for shared shader correctness rules, then only the relevant branch.

| Situation | Read |
| --- | --- |
| Installing, discovering APIs, loaders, examples, or runtime support | [Setup and discovery](playbooks/setup-discovery.md) |
| Fullscreen fragment shader, procedural background, noise, SDF, or raymarch | [Fullscreen effects](playbooks/fullscreen-effects.md) |
| Vertex/fragment geometry, camera, lighting, mesh, or scene graph | [Geometry and scenes](playbooks/geometry-scenes.md) |
| Compute shader, storage buffer, particles, tensor, or simulation | [Compute and simulation](playbooks/compute-simulation.md) |
| Feedback, ping-pong, offscreen targets, post-processing, depth, or textures | [Multipass and textures](playbooks/multipass-textures.md) |
| Wrong pixels, black output, validation error, NaN, or cross-runtime bug | [Debugging and testing](playbooks/debugging-testing.md) |
| Frame time, allocations, compilation stalls, bundle size, or memory | [Performance](playbooks/performance.md) |
| Color, composition, motion, interaction, responsive canvas, or fallback | [Visual and product integration](playbooks/visual-integration.md) |

## Bundled laboratory

- `scripts/project_inventory.py` maps vgpu versions, runtimes, loaders, and WGSL files without changing the project.
- `scripts/rgba_metrics.py` measures raw `target.read()` RGBA8 output and enforces nonblank-image gates.
- `templates/static-field.wgsl` plus ESM-explicit `templates/headless-smoke.mts` form a small real-vgpu smoke render whose raw output can feed the metrics tool.

## Default workflow

1. Run `scripts/project_inventory.py .` and inspect package manager, version, loaders, WGSL graph, and runtime surfaces.
2. Read the installed getting-started page, then the one concept page for the selected branch.
3. Search `npx vgpu examples search "<intent>" --pretty`; inspect before pulling.
4. State a shader contract: inputs, output, coordinate space, color space, deterministic seed/time, target format, and performance budget.
5. Implement the smallest static frame. Keep reusable math in pure WGSL modules.
6. Run `npx vgpu check <file.wgsl>` on every changed WGSL file; require device validation in CI.
7. Run `npx vgpu doctor --pretty`, render headlessly through `vgpu/node`, read pixels, and save a small artifact.
8. Use `scripts/rgba_metrics.py` or targeted pixel assertions to reject blank, clipped, transparent, or numerically implausible output.
9. Integrate the same effect into the browser and observe the real canvas at narrow/wide sizes, reduced motion, and bounded DPR.
10. Measure after correctness. Accept only when pixel, visual, lifecycle, and budget gates pass.

## Deliver

State the effect contract, vgpu/runtime paths used, WGSL files changed, exact validation and render evidence, performance measurements, fallbacks, and remaining device/browser risk. Never describe a shader as correct from source or compilation alone.
