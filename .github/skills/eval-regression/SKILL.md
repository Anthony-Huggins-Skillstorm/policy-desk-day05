---
name: eval-regression
description: "Prints the current golden-question numbers (recall@5 and grounded-answer count) for a quick before-and-after spot check during an edit session. Use when someone asks for the current eval numbers or to compare against a previous run in the same conversation. For a regression verdict against the saved baseline, use golden-eval instead."
---

# Eval Regression

Runs policy-desk's golden question set and summarizes regressions.

## When to use

Use after any change to retrieval, chunking, the agent instructions, or citation handling.

## Steps

1. Run `python eval/eval.py --retrieval-only` and record `recall@5`.
2. Run `python eval/eval.py --recorded` and record the grounded-answer count.
3. Compare both numbers with the previous run's numbers in the conversation or in `LAB-LOG.md`. Report any drop, with the question ids that changed.
