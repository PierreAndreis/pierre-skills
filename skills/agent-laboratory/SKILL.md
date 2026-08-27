---
name: agent-laboratory
description: Builds self-verifying experiment laboratories and measurement feedback loops for optimization, debugging, visual fidelity, quality, cost, and solution-search work. Use when a user asks to make something faster, cheaper, more accurate, less buggy, closer to a reference, or otherwise better across competing approaches where benchmarks, screenshots, traces, fixtures, or repeated trials can measure progress.
---

# Agent Laboratory

Turn an underspecified improvement request into a measured search. Give the agent both a laboratory for controlled experiments and a stopwatch for objective feedback.

## Quick start

1. State the objective as a measurable outcome.
2. Define correctness and quality gates that no candidate may violate.
3. Build the smallest harness that reproduces the important path.
4. Measure and save the untouched baseline before changing production code.
5. List a bounded set of hypotheses, then test one variable at a time.
6. Keep a change only when repeated measurements improve the objective and all gates pass.
7. Deliver the winning change, harness, raw results, and a before/after report.

Use `scripts/lab.py` when a lightweight, generic experiment ledger is useful:

```bash
python scripts/lab.py init work/lab --objective "Reduce export latency without changing output"
python scripts/lab.py record work/lab --variant baseline --metric latency_ms=820 --metric exact_match=1
python scripts/lab.py record work/lab --variant stream-parser --metric latency_ms=510 --metric exact_match=1 --parameter chunk_kb=64
python scripts/lab.py report work/lab --baseline baseline --primary latency_ms --direction lower --output work/lab/report.md
```

## Workflow

### 1. Frame the experiment

- Identify the representative inputs, critical path, primary metric, constraints, and stop condition.
- Separate optimization metrics from invariant gates. Speed never compensates for wrong output.
- Choose the closest observable proxy only when the real outcome cannot be measured; label the proxy.
- Record uncontrolled factors, tool versions, hardware, services, and likely sources of noise.

### 2. Build the laboratory

- Prefer real inputs and the real stack. Use fixtures only when they preserve the behavior under study.
- Add the missing feedback instrument: benchmark, test, trace, profiler, screenshot comparison, evaluator, debug log, cost counter, or todo ledger.
- Make runs reproducible and cheap enough to repeat. Preserve raw outputs and failure cases.
- For latency, include warmups and multiple measured runs. For stochastic systems, use a fixed evaluation set and enough repetitions to expose variance.

### 3. Establish the stopwatch

- Run the baseline before edits and save its commit, configuration, parameters, results, and sample count.
- Confirm the harness detects an intentional regression or known difference when practical.
- Do not claim improvement from one noisy sample, a changed workload, or a surrogate metric alone.

### 4. Search deliberately

- Rank three to five hypotheses by likely impact, confidence, and experiment cost.
- Change one independent variable per trial unless explicitly testing interactions.
- Record every trial, including failures. Revert losing changes; preserve useful evidence.
- When the search space is finite and affordable, automate a parameter or pipeline sweep.
- Use new evidence to refine the next hypothesis rather than blindly exhausting options.

### 5. Verify the winner

- Re-run the baseline and candidate under matching conditions, in alternating order when drift matters.
- Run correctness, regression, integration, and relevant adversarial tests.
- Check representative edge cases and inspect artifacts directly: screenshots, traces, decoded media, output diffs, or logs.
- Distinguish measured facts, evaluator judgments, and unverified inferences.

### 6. Report

Include the objective, harness, environment, baseline, candidates, discarded hypotheses, winning result, variance, quality gates, limitations, raw-data path, and exact reproduction command. Prefer a compact table or HTML chart when several candidates or metrics must be compared.

## Stop and ask

Ask the user only when the true success criterion requires their taste, authority, credentials, or an irreversible choice. Before asking them to manually verify routine work, first try to add the instrument that would let the agent verify it.

See [REFERENCE.md](REFERENCE.md) for domain-specific laboratory patterns and measurement traps.
