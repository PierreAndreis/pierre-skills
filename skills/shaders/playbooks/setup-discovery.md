# Setup and Discovery

## When to use

Use when adding vgpu, entering an unfamiliar shader project, choosing browser/Node/test runtimes, configuring WGSL imports, or resolving environment/tooling failures.

## Inputs

- package manager, framework, bundler, TypeScript configuration, and supported runtimes;
- installed `vgpu` version and package lock;
- target browsers, Node/CI platform, GPU requirements, and fallback policy;
- existing canvases, shader files, tests, and build scripts.

## Procedure

1. Run `scripts/project_inventory.py .` and inspect its JSON before changing dependencies.
2. If `vgpu` is installed, use the local CLI so docs match the locked API. If absent, inspect the current official quickstart, then install through the repository's package manager.
3. Run `npx vgpu --version` and `npx vgpu docs cat getting-started.md`.
4. Use `docs find` for concepts/symbols and `docs grep` for errors or prose. Load one page at a time.
5. Search verified examples with the CLI. `search`, `show`, and `cat` are read-only. Treat `pull` as a filesystem write into an explicit empty directory.
6. Configure the existing bundler rather than replacing it:
   - Vite uses the vgpu WGSL plugin;
   - Next/Turbopack or webpack uses the vgpu webpack loader;
   - no-bundler paths pass WGSL as strings;
   - TypeScript loads the package's WGSL import type reference.
7. Run the existing build before shader work so loader failures are separated from shader failures.
8. Run `npx vgpu doctor --pretty` before diagnosing Node rendering. Apply only its structured recommended fix, then rerun.

## Runtime choice

| Need | Runtime |
| --- | --- |
| Shipping browser canvas | `vgpu` |
| Real headless WebGPU and pixel readback | `vgpu/node` |
| Deterministic orchestration tests without GPU behavior | `vgpu/mock` |
| Geometry, camera, lighting helpers | `vgpu/scene` |
| Low-level WebGPU ownership | `vgpu/core` |
| Mesh inspection/edit/perf helpers | focused `@vgpu/render/*` subpath |

Stay at the highest layer that expresses the task. Do not drop to core merely to feel in control.

## Environment policy

- Local workstations normally use automatic adapter discovery.
- Deterministic CI snapshots pin the software adapter and cache its runtime.
- GPU-required CI explicitly requires hardware so a CPU fallback cannot make the gate misleadingly green.
- Air-gapped environments prepopulate verified runtimes and documentation while network access exists.
- Record adapter name/type and vgpu version with artifacts; pixel differences without environment identity are difficult to interpret.

## Gotchas

- A parse/reflection success may coexist with skipped device validation; inspect the validation object or require validation.
- Browser WebGPU support does not establish Node/Dawn support, and the reverse is also true.
- The site reflects current docs; the installed CLI reflects the project's version and wins for implementation.
- `npx` can fetch a package when no local binary exists. Be explicit about whether network installation is acceptable.
- Pulled examples are starting evidence, not project architecture. Preserve the host framework and conventions.
- A mock adapter verifies API choreography, not WGSL execution or rendered pixels.

## Completion

The package/version and runtime policy are recorded, version-matched docs were read, WGSL imports compile through the host build, doctor reports a usable intended adapter, and a minimal static frame renders in the selected runtime.

## Escalate

Escalate unsupported target browsers, CI that cannot install an approved runtime, required GPU features absent on supported adapters, package-manager policy conflicts, or changes that would replace the application's build system.
