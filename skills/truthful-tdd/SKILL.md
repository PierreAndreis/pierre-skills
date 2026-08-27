---
name: truthful-tdd
description: Runs test-driven development in vertical behavior slices with change-sensitive, non-tautological tests through public seams and real dependencies. Use when building or fixing code test-first, choosing unit/integration/UI/E2E coverage, auditing weak tests, or deciding whether a dependency is acceptable to mock.
---

# Truthful TDD

A test tells the truth only when it can disagree with the implementation. Run one vertical red → green → refactor cycle at a time; leave behind executable behavior specifications, not change detectors.

## Start at a vertical seam

1. Read the local test commands, nearby tests, domain vocabulary, and architecture decisions.
2. State one externally observable behavior and the risk its test must catch.
3. Choose the narrowest **public seam** that still crosses the real layers responsible for that behavior.
4. Choose the cheapest test level that can observe it credibly. Prefer a real in-process path; escalate only for risks a smaller test cannot expose.

A seam is an interface a real caller uses: exported API, HTTP route, command, rendered component, message boundary, or persisted workflow. A vertical slice exercises one behavior through that seam and the necessary layers beneath it. It does not test each internal class horizontally.

## Run the loop

### Red

- Write one focused scenario in domain language with explicit cause and effect.
- Use an independently known expected result: a worked example, specification literal, approved fixture, or separately derived invariant.
- Run the narrow test and observe the expected failure. Confirm it fails because the behavior is absent or wrong, not because setup, imports, or infrastructure are broken.
- Prove sensitivity when doubt remains: temporarily remove or invert the intended behavior and confirm the test goes red.

### Green

- Write the smallest production change that satisfies the behavior through the selected seam.
- Run the narrow test, then the adjacent suite. Keep unrelated behavior unchanged.

### Refactor

- Improve production and test clarity while keeping every test green.
- Preserve the seam and observable behavior; remove duplication only when the result remains easier to inspect.
- Start the next vertical slice only after the current slice is green and coherent.

## Reject tautological tests

A test is tautological or a change detector when its oracle comes from the same information as the implementation. Reject or rewrite tests that:

- recompute the expected value with the production algorithm;
- assert constants, fixtures, generated snapshots, or mocks against themselves;
- mirror internal call order or method structure instead of observing an outcome;
- pass only because inputs equal language or database defaults;
- exercise a helper, handler, or implementation class while bypassing the public path;
- remain green when the promised behavior is deliberately broken.

Prefer concrete non-default inputs, distinct values for distinct fields, narrow assertions on relevant outcomes, and an independent oracle. Treat mechanically accepted snapshots as unverified output, not truth.

## Use real dependencies by default

Choose in this order: real local implementation → hermetic service or ephemeral test database → owner-maintained fake with shared contract tests → narrow stub/mock at an owned boundary.

A mock is acceptable only when the real boundary is destructive, non-deterministic, unavailable, prohibitively slow or costly, or when a rare failure such as a timeout cannot be induced safely. Mock the smallest adapter you own, return static data, and keep logic out of the mock. Cover the adapter separately against the real contract. Mocking internal collaborators, domain objects, database repositories that can use a test database, or third-party types directly is not acceptable.

Prefer state and returned outcomes over interaction assertions. Verify an interaction only when the interaction itself is the externally promised behavior, such as publishing an event or sending a message; then verify only the state-changing call and relevant arguments.

## Test UI through the front door

Render the component, locate controls as a user does, perform user actions, and assert visible or accessible outcomes. The DOM/accessibility surface is the public seam. Calling handlers, hooks, controllers, or component methods directly bypasses UI behavior and can miss disabled, hidden, wiring, focus, and validation failures.

Use component or route integration tests for most UI logic. Use a small number of screenshot tests for visual layout and narrow DOM assertions for behavior.

## Spend E2E carefully

E2E tests are valuable for critical journeys and failures that only appear across deployed boundaries, but they are slow, flaky, imprecise, and costly to maintain. Keep the set small. Cover permutations below the E2E layer, keep data ephemeral, and preserve logs, screenshots, traces, and relevant state for diagnosis.

See [REFERENCE.md](REFERENCE.md) for seam selection, test-level tradeoffs, mock exceptions, and suite design. See [EXAMPLES.md](EXAMPLES.md) when reviewing tautologies, UI tests, or boundary doubles.

## Done means

- Every new behavior was observed red before green.
- Each test can fail under a plausible defect and uses an independent oracle.
- Tests exercise public vertical seams with the highest practical fidelity.
- Mock exceptions are documented and contract-covered.
- Narrow, adjacent, and proportionate broader suites pass; unverified risks are stated explicitly.
