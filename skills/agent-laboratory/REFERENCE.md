# Laboratory Patterns and Measurement Traps

## Choose the feedback instrument

| Goal | Laboratory inputs | Stopwatch or evaluator | Quality gates |
| --- | --- | --- | --- |
| Performance | Representative workloads and critical paths | Wall/CPU time, allocations, traces, throughput | Tests, output equivalence, resource ceilings |
| Bug reduction | Minimal reproduction plus regression corpus | Pass/fail rate, failing seed count, error classes | Existing suite, adjacent routes, adversarial cases |
| Visual fidelity | Reference design and fixed viewports | Screenshots, overlays, pixel or property diffs | Accessibility, responsive behavior, interaction |
| Extraction or ranking | Labelled real-world corpus | Precision, recall, exact match, rubric evaluator | Latency, cost, deterministic failure handling |
| Cost reduction | Representative usage distribution | Cost per successful unit and total projected cost | Accuracy, latency, reliability |
| Media transformation | Reference transcript or decoded source | WER, duration, bitrate, perceptual checks | No clipping, decode validation, required format |

## Benchmark hygiene

- Measure the user-visible path, not only a convenient inner function.
- Pin inputs and configuration. Record dependencies and remote model versions when possible.
- Separate setup from the timed region unless setup is part of the experience.
- Warm caches and runtimes deliberately; report cold and warm results when both matter.
- Use medians for skewed latency data and retain the individual samples.
- Alternate baseline and candidate runs when machine or service load can drift.
- Report absolute values, relative change, sample count, and spread. Avoid percentages without denominators.
- Treat evaluator models as instruments that need calibration against human-labelled examples.

## Search patterns

### Pipeline search

Enumerate plausible stages and orderings, then evaluate combinations on a fixed corpus. Cache intermediate outputs to reduce cost. Start with ablations to learn which stages matter before testing every combination.

### Parameter sweep

Choose a safe range, coarse-search it, then refine around the best region. Optimize for the primary metric only among candidates that pass every quality gate. Inspect the boundary where quality first degrades rather than selecting the most extreme passing sample.

### Visual refinement loop

Capture the implementation and reference at identical viewports. List concrete deltas in spacing, color, typography, radius, shadows, borders, alignment, overflow, responsive behavior, and interaction states. Fix a small group, recapture, and repeat until remaining differences are explained or accepted.

### Hypothesis ladder

For each hypothesis, record mechanism, predicted metric movement, cheapest discriminating experiment, and outcome. Prefer experiments that can disprove a hypothesis quickly.

## Evidence rules

- A green test says the tested behavior passed; it does not prove production readiness.
- A faster microbenchmark does not prove the end-to-end path improved.
- A screenshot match at one viewport does not prove responsive fidelity.
- A cheaper pipeline does not win if it crosses the accuracy or reliability floor.
- “Could not measure” is a result. State the missing instrument and do not convert it into a success claim.

## Suggested report shape

```md
# Experiment: <objective>

## Decision
<winner, magnitude, and gates passed>

## Method
<inputs, environment, harness, commands, sample count>

## Results
| Variant | Primary metric | Quality gates | Notes |

## Discarded hypotheses
<what failed and what was learned>

## Limitations
<noise, proxies, missing coverage, production unknowns>

## Reproduce
<exact command and raw-data path>
```

## Source essays

- [Give your agent a laboratory](https://brianlovin.com/writing/give-your-agent-a-laboratory-jH5ryjC)
- [Give your agent a stopwatch](https://brianlovin.com/writing/give-your-agent-a-stopwatch-zNa2M3o)
- [Give your agent a laboratory, pt. II](https://brianlovin.com/writing/give-your-agent-a-laboratory-pt-ii-KjFnCW9)
