# Truthful TDD Reference

## Judge every test on three axes

- **Fidelity:** it fails when the promised behavior is broken.
- **Resilience:** it stays green when implementation changes preserve behavior.
- **Precision:** its failure identifies the broken behavior and useful cause.

An empty test is resilient but has no fidelity. A full-system test can have high fidelity but low precision. A mock-heavy unit test can be fast while having neither useful fidelity nor resilience.

## Select a seam before a test type

| Behavior | Preferred seam | Typical test |
| --- | --- | --- |
| Pure domain rule | Exported domain operation | In-process behavior test |
| Persistence workflow | Service/API plus ephemeral real database | Integration test |
| HTTP contract | Real route, serialization, middleware, and database | Route integration test |
| UI behavior | Rendered DOM and user events | Component/route integration test |
| External service adapter | Owned adapter | Contract test against sandbox, hermetic service, or owner fake |
| Cross-system critical journey | User-visible deployed entry point | Focused E2E test |

Do not split a vertical behavior into mocked layer tests merely to call them units. Keep pure computation in a functional core when that makes important rules cheap to exercise, then cover the imperative shell at its real integration seam.

## Balance the suite with SMURF

Evaluate candidate coverage by **Speed, Maintainability, Utilization, Reliability, and Fidelity**. The test pyramid is a rough cost heuristic, not a quota. Prefer the smallest test that exposes the risk while retaining the required fidelity.

- Small tests dominate fast feedback and precise diagnosis.
- Integration tests prove contracts between real parts and should carry most boundary permutations.
- E2E tests prove a few critical journeys in near-production conditions.
- Coverage percentage is evidence of execution, not evidence of useful assertions or risk reduction.

## Mocking decision record

Before adding a mock, answer:

1. What external boundary prevents the real implementation from running?
2. Why is a hermetic instance, ephemeral database, sandbox, or owner fake insufficient?
3. What behavior will remain unverified because the mock defines its own contract?
4. Which separate test proves the owned adapter against the real contract?

### Usually acceptable

- A clock or random source injected to make edge cases deterministic.
- A payment/email/vendor adapter where a real call is destructive or costly, paired with adapter contract coverage.
- A narrow fault injector for timeout, quota, or transport failure paths.
- A filesystem boundary when the platform behavior is irrelevant and a temporary filesystem is impractical.

### Usually unacceptable

- Mocking internal services, repositories, or domain collaborators to verify call choreography.
- Mocking a database when the behavior depends on SQL, constraints, transactions, migrations, or serialization.
- Mocking third-party SDK types directly; wrap them behind an owned narrow adapter.
- A mock whose conditional logic recreates the implementation or protocol.
- A graph of mocks returning mocks.

Fakes need conformance tests run against both fake and real implementations. Put the fake at the lowest boundary possible so the test executes the maximum amount of real application code.

## Oracle independence

Good sources of expected truth include:

- a literal worked by hand from the requirement;
- a standards example or approved golden fixture;
- a value produced by an independently implemented reference system;
- a domain invariant that is logically independent of the production algorithm;
- a round trip through a public interface when the reverse operation has an independently tested contract.

Weak sources include copying production constants, calling another method that shares the same bug, generating expectations through the same transformation, recording current output without review, or asserting only what a mock was instructed to return.

Use non-default values and distinct values for multiple inputs. Include boundaries, empty/missing cases, meaningful equivalence classes, and failure paths. Fuzzing or property testing can expand an already credible oracle; it does not repair a tautological property.

## Readable tests

- Name the behavior and condition, not the production method.
- Keep one scenario per test; a multi-step user journey can still be one scenario.
- Keep cause, action, and effect together. Shared setup contains only universally irrelevant mechanics.
- Prefer DAMP tests: repeat meaningful details when abstraction would hide the example.
- Put complex test utilities under their own tests.
- Assert only the fields and arguments relevant to the behavior. One broad equality or screenshot can cover the canonical shape; use narrow assertions elsewhere.
- Make failures actionable with scenario names, focused assertions, and preserved diagnostics.

## UI strategy

1. Render the smallest component or route that owns the user behavior.
2. Provide real state, router, validation, and local services when they can run hermetically.
3. Query by role, accessible name, label, or visible text rather than implementation selectors.
4. Act with user-level events and realistic event sequences.
5. Assert what the user can perceive or what the public workflow returns.

Snapshots are broad change detectors unless the visual/content contract truly requires the whole snapshot and a human reviews the change. Prefer narrow DOM assertions for behavior and a deliberately small visual suite for layout.

## E2E admission test

Add an E2E test only when all are true:

- The behavior is important enough to pay ongoing maintenance cost.
- A smaller test cannot reliably expose the cross-boundary risk.
- The scenario has isolated, ephemeral data and a stable public interface.
- Failure captures enough evidence to diagnose the responsible boundary.

Use one journey per important success class and important error class, not every input permutation. Move logic and edge cases to cheaper integration/component tests.

## Source basis

This skill synthesizes the official Google Testing/Tech on the Toilet corpus and Matt Pocock's TDD skill. Particularly influential sources:

- [Change-Detector Tests Considered Harmful](https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html)
- [Don't Put Logic in Tests](https://testing.googleblog.com/2014/07/testing-on-toilet-dont-put-logic-in.html)
- [Prefer Testing Public APIs](https://testing.googleblog.com/2015/01/testing-on-toilet-prefer-testing-public.html)
- [Testing UI Logic? Follow the User!](https://testing.googleblog.com/2020/10/testing-on-toilet-testing-ui-logic.html)
- [Increase Test Fidelity By Avoiding Mocks](https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html)
- [Exercise Service Call Contracts in Tests](https://testing.googleblog.com/2018/11/testing-on-toilet-exercise-service-call.html)
- [What Makes a Good End-to-End Test?](https://testing.googleblog.com/2016/09/testing-on-toilet-what-makes-good-end.html)
- [SMURF: Beyond the Test Pyramid](https://testing.googleblog.com/2024/10/smurf-beyond-test-pyramid.html)
- [The Way of TDD](https://testing.googleblog.com/2026/03/the-way-of-tdd.html)
- [Matt Pocock's TDD skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)

The official `TotT` label feed was reviewed as a corpus; the links above identify the entries most directly reflected in the workflow.
