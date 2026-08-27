---
name: test-suite-auditor
description: Exhaustively inventories and evaluates every test suite and case for defect sensitivity, oracle independence, flake risk, surface coverage, redundancy, and maintenance value; it can consolidate or delete weak tests after replacement coverage is proven. Use when auditing a repository's tests, finding flaky or tautological tests, reducing test spam, or pruning and merging suites.
---

# Test Suite Auditor

Audit every test, not a sample. A test earns its place by preventing a plausible defect through an independent oracle at a useful product seam.

## Choose the mode

- **Audit mode is read-only:** inventory, run, assess, and report. A request to review or audit does not authorize test edits.
- **Prune mode changes tests:** use only when the user asks to delete, merge, consolidate, repair, or implement the recommendations.

## 1. Prove the inventory is complete

1. Read repository instructions, workspace/package structure, test scripts, runner configs, CI workflows, and custom harnesses.
2. Generate a filesystem manifest with `scripts/audit_inventory.py scan <repo> --output <manifest>`.
3. Ask each configured runner to list or collect its tests without executing them. Add nonstandard suites the filesystem scan missed.
4. Include generated, platform-specific, contract, migration, browser, native, smoke, and E2E suites when they belong to the repository. Exclude vendored dependencies and build output.
5. Record the exact commands and any suite that cannot be collected. The inventory is complete only when runner listings, configs, and the manifest reconcile.

## 2. Establish runtime evidence

- Run the normal test commands once and record failures, skips, retries, duration, environment, and seed.
- Use existing CI history when available to identify intermittent failures and slow suites.
- Re-run suspicious suites under changed order, seed, concurrency, timezone, locale, and clock where supported. Repeat targeted suites enough to distinguish a pattern; never call “passed repeatedly” proof that flaking is impossible.
- Separate **observed flakes** from **predicted flake risk**.

## 3. Judge every suite and every case

Read each suite completely. For every test case, answer:

1. What public behavior or pure function does it exercise?
2. What exact plausible defect would make it fail?
3. Is the expected result independent of the implementation?
4. Does it cross a valuable integration/E2E surface, or unit-test only a pure function?
5. What unique protection remains after accounting for broader tests?
6. Which concrete flake mechanisms exist?

When safe, run a **sensitivity probe**: reversibly remove or invert the behavior and confirm the test fails for the intended reason. Keep probes out of the final diff. Preserve pre-existing changes and skip probes that would overlap them.

Record one suite verdict plus case-level exceptions in the manifest. Use `record`, then run `verify`; zero pending entries is mandatory.

## 4. Classify with evidence

- **Essential:** uniquely protects a major capability, contract, or costly regression.
- **Useful:** catches a plausible defect with an independent oracle at a credible seam.
- **Redundant:** its unique protection is already supplied by a stronger broad test.
- **Misleading:** tautological, self-testing, implementation-coupled, or incapable of detecting its stated defect.
- **Unknown:** evidence is insufficient; state the missing experiment rather than guessing.

Rate flake risk `low`, `medium`, or `high`, with named mechanisms and confidence. Static signals are clues, never verdicts. See [REFERENCE.md](REFERENCE.md) for the rubric.

## 5. Report before pruning

Produce a table with suite, cases reviewed, product surface, verdict, defect prevented, oracle, overlap, observed flakes, predicted mechanisms, confidence, and proposed action. Summarize:

- protection that would be lost by deletion;
- broad surfaces with no credible coverage;
- redundant clusters suitable for consolidation;
- misleading tests that create false confidence;
- the highest-value repairs and flake removals.

## 6. Prune and consolidate safely

In prune mode:

1. Write or identify the stronger integration/E2E replacement first.
2. Prove the replacement goes red under the defect and green after restoration.
3. Merge overlapping scenarios into a small number of coherent broad journeys; keep input matrices below E2E.
4. Delete a test only when it is misleading or its unique protection is demonstrably preserved elsewhere.
5. Prefer real dependencies. Unit tests remain only for pure functions.
6. Run affected suites, adjacent integration tests, and the full repository suite. Repeat changed high-risk suites under perturbation.
7. Re-scan the repository, verify no suite disappeared unintentionally, and report exact deletions, consolidations, coverage changes, and residual uncertainty.

Do not commit, push, resolve review threads, or merge Git branches unless the user separately asks. “Merge tests” means consolidate test coverage in the working tree.

See [EXAMPLES.md](EXAMPLES.md) for verdict examples and consolidation patterns.
