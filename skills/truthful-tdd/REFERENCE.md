# Truthful TDD Reference

## Judge every test on three axes

- **Fidelity:** it fails when the promised behavior is broken.
- **Resilience:** it stays green when implementation changes preserve behavior.
- **Precision:** its failure identifies the broken behavior and useful cause.

An empty test is resilient but has no fidelity. A full-system test can have high fidelity but low precision. A mock-heavy unit test can be fast while having neither useful fidelity nor resilience.

## Select a seam before a test type

| Behavior | Preferred seam | Typical test |
| --- | --- | --- |
| Pure domain rule | Pure exported function | Unit test |
| Persistence workflow | Service/API plus ephemeral real database | Integration test |
| HTTP contract | Real route, serialization, middleware, and database | Route integration test |
| UI behavior | Rendered DOM and user events | Component/route integration test |
| External service adapter | Owned adapter | Contract test against sandbox, hermetic service, or owner fake |
| Cross-system critical journey | User-visible deployed entry point | Focused E2E test |

Do not split a vertical behavior into mocked layer tests merely to call them units. Unit-test only the functional core: deterministic functions whose result depends solely on explicit inputs. Cover services, orchestrators, repositories, framework code, and the imperative shell through integration or E2E seams with real dependencies.

## Meet obligations without test spam

- For a **feature**, add one acceptance journey for its primary capability. Add another only when a distinct permission, failure, platform, or cross-system path carries material risk.
- For a **bug**, add the broadest stable regression that would have caught it before release. It must fail on the unfixed code.
- Prefer adding a clear case or assertion to an existing journey over creating a new near-duplicate test.
- Keep one coherent journey per test, but let that journey cross UI, API, policy, persistence, and retrieval when those layers form one product surface.
- Put input matrices and edge permutations in integration tests. Keep E2E focused on representative success and important failure classes.
- Delete or consolidate tests made redundant by stronger broad coverage when no unique risk would be lost.

## Balance the suite with SMURF

Evaluate candidate coverage by **Speed, Maintainability, Utilization, Reliability, and Fidelity**. The test pyramid is a rough cost heuristic, not a quota. This suite deliberately favors fidelity: choose the broadest stable integration or E2E seam that covers the capability without making failures opaque.

- Pure-function unit tests provide fast feedback for dense deterministic logic.
- Integration tests prove contracts between real parts and carry most boundary permutations.
- E2E tests prove a small number of large product surfaces in near-production conditions.
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

1. Prefer the page or route that represents the user capability; use a smaller component only when it is itself a reusable public surface.
2. Provide real state, router, validation, and local services when they can run hermetically.
3. Query by role, accessible name, label, or visible text rather than implementation selectors.
4. Act with user-level events and realistic event sequences.
5. Assert what the user can perceive or what the public workflow returns.

Snapshots are broad change detectors unless the visual/content contract truly requires the whole snapshot and a human reviews the change. Prefer narrow DOM assertions for behavior and a deliberately small visual suite for layout.

## E2E portfolio

Keep an E2E test when all are true:

- It proves a major user capability or an important cross-system regression.
- It crosses a broad, stable public surface rather than checking an incidental detail.
- The scenario has isolated, ephemeral data.
- Failure captures enough evidence to diagnose the responsible boundary.

Use one journey per major success class and materially different error class, not every input permutation. Let integration tests cover variants and localize failures. Consolidate overlapping E2E journeys instead of allowing the suite to grow by accumulation.

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
