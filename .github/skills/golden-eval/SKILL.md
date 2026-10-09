---
name: golden-eval
description: "Detects answer-quality and retrieval regressions in policy-desk by running the offline golden-question evaluation (eval/eval.py --retrieval-only and --recorded) and comparing it with a saved baseline. Use when someone asks whether a change made answers, citations, grounding, or retrieval worse, or before merging changes to citations.py, retriever.py, corpus.py, agent.py, the corpus, or the index. Runs offline with no Azure calls."
---

# Golden evaluation regression check

Use this skill to answer "did this change make policy-desk worse?" with numbers rather than opinion. It applies to changes in:
- citation parsing or verification (`src/policy_desk/citations.py`);
- retrieval or chunking (`retriever.py`, `corpus.py`, `build_index.py`);
- the agent's instructions (`agent.py`);
- the policy corpus or the rebuilt `index/`.

Everything runs offline against cached embeddings and recorded answers, so it is safe in CI and needs no Azure login.

## Run the check

From the repository root, with the project's virtual environment:

```bash
python .github/skills/golden-eval/scripts/compare_eval.py
```

The script runs both offline evaluation modes and prints one line per metric with the baseline value, the current value, and the delta. It then lists any question ids that are newly not grounded.

| Exit code | Meaning |
|---|---|
| 0 | No regression. |
| 1 | Regression: recall fell, the superseded-document count rose, or the grounded count fell. |
| 2 | No baseline exists yet. |

For what each metric measures and what a change usually means, read [references/metrics.md](references/metrics.md). Do not guess the cause from the number alone.

## Baselines

The baseline lives in `references/baseline.json`. To record one, run:

```bash
python .github/skills/golden-eval/scripts/compare_eval.py --save-baseline
```

**Always ask the user before saving a baseline.** Never save one on your own initiative, and never save one to make a failing check pass. A baseline taken after a regression makes that regression the new normal, and it disappears from every later check. Save only when the user confirms that the current numbers are the intended state, for example after a deliberate fix that raises the grounded count. If exit code 2 says there is no baseline, report that and ask.

## Report

Report in this order:

1. **Verdict:** "No regression" or "Regression", with the exit code.
2. **Metric table:** each metric as baseline → current (delta).
3. **For a regression:** which gated metric moved, the newly ungrounded question ids (if any), and the likely cause from `references/metrics.md`, tied to the files the user changed.
4. **Improvements:** for example, newly grounded ids, noted as improvements. Suggest updating the baseline only if the user confirms the change is intended.

Do not modify source files, the corpus, the index, or the baseline as part of the check.
