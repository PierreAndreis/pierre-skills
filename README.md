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

## Install

Copy the skill directory into the skills folder used by your agent:

```bash
git clone https://github.com/PierreAndreis/pierre-skills.git
cp -R pierre-skills/skills/agent-laboratory ~/.agents/skills/
cp -R pierre-skills/skills/truthful-tdd ~/.agents/skills/
```

For Codex installations that use `$CODEX_HOME/skills`, copy it there instead:

```bash
cp -R pierre-skills/skills/agent-laboratory "$CODEX_HOME/skills/"
cp -R pierre-skills/skills/truthful-tdd "$CODEX_HOME/skills/"
```

Restart the agent or begin a new session after installation so it refreshes its
skill catalog.

## License

[MIT](LICENSE)
