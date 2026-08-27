# Test Suite Audit Rubric

## Usefulness

Judge the test's counterfactual value: what bad production state becomes harder to ship because this test exists?

| Dimension | Strong evidence | Weak evidence |
| --- | --- | --- |
| Defect sensitivity | A plausible mutation makes it red for the intended reason | It stays green when behavior is broken |
| Oracle independence | Requirement literal, approved fixture, independent system, domain invariant | Recomputes production logic or asserts mock setup |
| Surface value | Public integration/E2E seam or pure-function contract | Private method, handler, internal choreography |
| Fidelity | Real stack, hermetic service, test database, owner fake | Graph of mocks or mocked service contract |
| Uniqueness | Protects a distinct risk or platform | Strictly subsumed by a stronger test |
| Resilience | Survives behavior-preserving refactors | Breaks on call order, shape, or incidental markup |
| Precision | Failure names the broken capability and preserves diagnostics | Broad failure with no causal evidence |

Do not add the dimensions into a fake mathematical score. Explain the tradeoff and assign `essential`, `useful`, `redundant`, `misleading`, or `unknown`.

## Tautological and self-testing patterns

- Expected output is computed with the same algorithm, constants, mapping, schema, or helper as production.
- The test configures a mock response and asserts only that response or the call choreography needed to obtain it.
- A generated snapshot or golden file is accepted from current output without independent review.
- Setup and assertion share the same mistaken default, identifier, field order, or serialization assumption.
- A test compares a value, fixture, constant, or transformed copy to itself.
- The test exercises a test helper more than production behavior.
- The assertion checks that code exists or methods were called, while no public outcome is observed.
- The test remains green after the stated behavior is inverted or removed.

Call these **change detectors** when they mirror implementation and fail on harmless refactors. They can have negative value even if they technically fail sometimes.

## Flake prediction

### High-risk mechanisms

- Fixed sleeps, polling without a condition, or timeouts close to normal runtime.
- Wall-clock, timezone, locale, daylight-saving, or calendar dependence without control.
- Unseeded randomness, nondeterministic generators, or assertions that depend on iteration order.
- Shared mutable databases, files, ports, caches, accounts, environment variables, or global state.
- Test-order dependence, parallel workers mutating the same resource, or cleanup that runs only on success.
- Unmanaged network, vendor, browser, device, or cloud dependencies.
- Concurrency asserted without synchronization on the actual completion condition.
- UI selectors tied to generated classes, layout, animation timing, or incidental text.
- Retries or quarantine that conceal a first-attempt failure.

### Medium-risk mechanisms

- Broad E2E setup with many independently changing dependencies.
- Temporary resources with collision-prone names or non-atomic cleanup.
- Large snapshots, unordered serialization, floating-point exact equality, or platform path assumptions.
- Async assertions with generous but unexplained timeouts.
- Test data coupled to the current date, production-like shared fixtures, or implicit runner defaults.

### Low-risk evidence

- Hermetic dependencies, isolated data, deterministic seeds, condition-based waits, explicit cleanup, stable public selectors, and repeatable runs under perturbation.

`Low` is a prediction, not a guarantee. Report observed run count, environments, and confidence separately.

## Redundancy and consolidation

A test is redundant only when another test fails under the same meaningful defect and preserves at least the same public-surface fidelity. Similar names or overlapping lines are not enough.

Prefer consolidation when:

- several UI tests each verify one step of a single major journey;
- mocked layer tests duplicate a real route or workflow integration test;
- multiple E2E tests repeat identical setup for incidental variants;
- a parameter matrix can live in one integration suite;
- a broad acceptance test makes implementation-detail assertions unnecessary.

Keep tests separate when they protect materially different permissions, failure classes, platforms, data-integrity guarantees, or recovery paths.

## Deletion gate

Before deleting, record:

1. The test's current verdict and evidence.
2. The exact defect it claims to prevent.
3. The replacement test and public surface, if any.
4. A sensitivity probe showing the replacement catches that defect.
5. The affected and full-suite commands that pass after deletion.

If any claimed protection cannot be mapped, classify it `unknown` and investigate instead of deleting.

## Audit report template

```md
| Suite | Cases | Surface | Verdict | Prevents | Oracle | Flake risk | Evidence | Action |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
```

Follow with uncovered surfaces, redundant clusters, proposed replacements, deletion gates, runtime evidence, inventory reconciliation, and limitations.
