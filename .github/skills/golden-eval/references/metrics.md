# Golden-set evaluation metrics

These are the metrics `scripts/compare_eval.py` reports. All of them come from `eval/eval.py` in its two offline modes, scored against `eval/golden-questions.json` (55 questions):

- `--retrieval-only` uses cached question embeddings against `index/`.
- `--recorded` re-verifies the saved model answers in `tests/fixtures/recorded-answers.json`.

The exit code gates on recall, the superseded count, and the grounded count. The score metrics are reported for context.

## recall@5 (`recall_found` of `recall_total`)

**What it measures.** Across the in-scope questions, it counts how many of the documents each question *expects* (`expected_doc_ids`) appear in the top 5 retrieved chunks. `recall_total` is the number of expected documents. It only changes when the golden set changes.

**What a drop usually means:**
- The index was rebuilt with different chunking, or a new document now outranks the right one in the top 5. A new near-duplicate document (for example a second standard on the same topic) commonly displaces an older one.
- The embedding deployment or model changed.
- The corpus lost or renamed a document whose id the golden set expects.

A drop of one after adding a document is worth inspecting, not automatically a failure. Check which question lost its document.

## Superseded document ranked above the current one (`superseded_above_current`)

**What it measures.** For the `superseded_trap` questions, it counts how often the SUPERSEDED document (`DUE-OLD`) ranks above the current one (`DUE-STD`). **Lower is better.**

**What a rise usually means:**
- A chunking or index change made the old version more similar to typical questions.
- A new document pulled the current version down the ranking.

The agent then sees the outdated policy first and is more likely to cite it. That is a correctness risk even when recall is unchanged.

## In-scope and out-of-scope score gap (`in_scope_min_top_score`, `out_of_scope_max_top_score`, `score_gap`)

**What it measures:**
- `in_scope_min_top_score` is the *lowest* top-1 cosine score among answerable questions.
- `out_of_scope_max_top_score` is the *highest* top-1 score among out-of-scope questions.
- `score_gap` is their difference.

A **positive** gap would mean a single relevance threshold could separate answerable from unanswerable questions. A **negative** gap (currently about -0.01) means the two ranges overlap, so no threshold is perfect.

**What a change usually means:**
- A shrinking or more negative gap means a new document makes off-topic questions look more answerable, or makes some answerable question look weaker. Any relevance-gate threshold calibrated on the old numbers needs rechecking.
- A growing gap is an improvement.

## Grounded count (`grounded` of `answers`, with `not_grounded_ids`)

**What it measures.** For each recorded answer, it re-runs citation verification (`src/policy_desk/citations.py`). An answer is grounded when it has at least one verified citation (a cited doc id that retrieval returned) and no unsupported ones. `not_grounded_ids` lists the questions that fail.

**What a drop usually means:**
- **A change to citation parsing or verification**, which is the most common cause, for example a regex that stops matching some doc ids, or a stricter `grounded` rule.
- A change to the recorded fixture.

Because this mode does not call a model, a change in the grounded count isolates the verification code. The newly ungrounded ids show which answers to read. Today's baseline is 45 of 55, because of a known defect in citation parsing; a *rise* after fixing it is expected.
