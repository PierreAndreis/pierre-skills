# Pierre Skills

Reusable agent skills by Pierre Ortega.

## Skills

### Agent Laboratory

Builds a self-verifying feedback loop before optimizing performance, quality,
cost, correctness, or visual fidelity. It combines a laboratory for controlled
experiments with a stopwatch for objective before-and-after measurement.

The skill includes:

- A baseline-to-report experimental workflow.
- Domain-specific measurement patterns and evidence rules.
- A dependency-free Python ledger for recording and comparing trials.

See [`skills/agent-laboratory/SKILL.md`](skills/agent-laboratory/SKILL.md).

### Truthful TDD

Runs integration- and E2E-first red–green–refactor through broad vertical
surfaces, with unit tests reserved for pure functions. Every bug gets regression
coverage and every feature gets acceptance coverage, while the suite stays
small by testing capabilities rather than incidental details.

See [`skills/truthful-tdd/SKILL.md`](skills/truthful-tdd/SKILL.md).

### Test Suite Auditor

Inventories every test suite in a repository, judges each suite and case for
real defect prevention, independent oracles, redundancy, and predicted flake
risk, then can consolidate or delete weak tests after replacement coverage is
proven. A bundled manifest tool prevents sample-based audits from claiming
completion while suites remain unreviewed. Existing CI jobs and Git history can
add reachability, runtime, retry, churn, and minute-usage evidence; a JUnit
normalizer combines machine-readable local or CI reports across repeated runs.

See [`skills/test-suite-auditor/SKILL.md`](skills/test-suite-auditor/SKILL.md).

### Design

Designs, builds, reviews, and refines production web interfaces through ten
directly routed craft playbooks. It covers visual direction, semantic color and
theme systems, typography and copy, layout and surfaces, controls, responsive
accessibility, data evidence, editorial pages, performance, and rendered QA.
Direct sentence-case headings replace eyebrow/kicker layers, while behavioral
evals and a bundled validator preserve the design rules over time.

See [`skills/design/SKILL.md`](skills/design/SKILL.md).

### Animation

Decides, specifies, builds, debugs, and reviews purposeful web motion. It
combines frequency-aware motion decisions with easing and timing craft,
interruptibility, spatial continuity, reduced-motion variants, frame-budget
discipline, and real-interface observation.

See [`skills/animation/SKILL.md`](skills/animation/SKILL.md).

### Shaders

Builds, integrates, debugs, tests, and optimizes WebGPU shaders with vgpu,
typed WGSL modules, browser canvases, and headless Node rendering. Eight routed
playbooks cover effects, geometry, compute, multipass textures, debugging,
performance, setup, and product integration. Bundled tools inventory an
existing vgpu project and enforce deterministic raw-pixel sanity gates.

See [`skills/shaders/SKILL.md`](skills/shaders/SKILL.md).

### Infrastructure Autopilot

Runs a persistent 15-minute infrastructure control loop with explicit merge
and production authority. It discovers and builds monitors, responds to
outages through bounded runbooks, improves performance, cost, SQL, capacity,
and alert quality through measured experiments, and keeps a GitHub issue plus
machine ledger as its audit trail. Twelve directly routed playbooks keep the
large domain progressively disclosed, while bundled tools handle probe
execution, loop state, slow-query ranking, cost-per-unit trends, alarm quality,
audit rendering, and structural validation.

See [`skills/infrastructure-autopilot/SKILL.md`](skills/infrastructure-autopilot/SKILL.md).

## Install

Copy the skill directory into the skills folder used by your agent:

```bash
git clone https://github.com/PierreAndreis/pierre-skills.git
cp -R pierre-skills/skills/agent-laboratory ~/.agents/skills/
cp -R pierre-skills/skills/truthful-tdd ~/.agents/skills/
cp -R pierre-skills/skills/test-suite-auditor ~/.agents/skills/
cp -R pierre-skills/skills/design ~/.agents/skills/
cp -R pierre-skills/skills/animation ~/.agents/skills/
cp -R pierre-skills/skills/shaders ~/.agents/skills/
cp -R pierre-skills/skills/infrastructure-autopilot ~/.agents/skills/
```

For Codex installations that use `$CODEX_HOME/skills`, copy it there instead:

```bash
cp -R pierre-skills/skills/agent-laboratory "$CODEX_HOME/skills/"
cp -R pierre-skills/skills/truthful-tdd "$CODEX_HOME/skills/"
cp -R pierre-skills/skills/test-suite-auditor "$CODEX_HOME/skills/"
cp -R pierre-skills/skills/design "$CODEX_HOME/skills/"
cp -R pierre-skills/skills/animation "$CODEX_HOME/skills/"
cp -R pierre-skills/skills/shaders "$CODEX_HOME/skills/"
cp -R pierre-skills/skills/infrastructure-autopilot "$CODEX_HOME/skills/"
```

Restart the agent or begin a new session after installation so it refreshes its
skill catalog.

## License

[MIT](LICENSE)
