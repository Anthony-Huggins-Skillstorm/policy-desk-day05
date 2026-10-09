# Policy citation format

A Northwind policy citation must let a reader open the exact text that supports a claim, and confirm it was in force.

## Format

```text
<DOC-ID> §<section> (v<version>, corpus/<file>:<line>)
```

Examples:

* `DUE-STD §4.2 (v3.0, corpus/due-diligence-standard.md:29)`: a dotted section number.
* `RNW-PRC §2 (v1.6, corpus/contract-renewal-procedure.md:13)`: from the heading `## Section 2 — Renewal Notice Windows`.
* `ONB-PRC Step 1 (v2.4, corpus/vendor-onboarding-procedure.md:13)`: from the heading `## Step 1: Intake`.
* `ONB-PRC — Overview (v2.4, corpus/vendor-onboarding-procedure.md:9)`: an unnumbered heading, cited by doc id and heading text.
* `GIFT-POL — Gifts (v3.3, corpus/vendor-gifts-conflicts-policy.md:13)`: GIFT-POL has no markdown headings. Each bold lead paragraph (`**Gifts.**`) is a section.

Where the policy-desk answer format is needed, the doc id alone, as `[doc_id: DUE-STD]`, is what the product's citation verifier checks. Research and planning artifacts use the fuller form above, so a reviewer can trace each claim to a line.

## Parts of a citation

| Part | Source | Why it matters |
|---|---|---|
| Doc ID | the `Doc ID:` line | Stable identifier. Doc ids are uppercase segments of 3 or 4 letters joined by a hyphen (`TPR-POL`, `EXIT-PLN`). |
| Section | the heading's number, `Section n`, `Step n`, or the heading text | Points to the clause, not just the document. Policies cross-reference each other this way (`TIER-MTX §3`). |
| Version | the `Version:` line | Records which revision the claim relied on, so a later revision can be checked against it. |
| File:line | the heading's line in `corpus/` | Lets a reviewer open the source directly and verify the claim. |

## Only `Current` documents are citable

Every corpus document has a `Status:` line. Cite a document only when its status is `Current`.

`DUE-OLD` (`due-diligence-standard-v2.md`, `Status: SUPERSEDED by DUE-STD`) is kept in the corpus on purpose. It is worded almost identically to `DUE-STD` but states requirements that are no longer in force, so any search, lexical or vector, ranks it highly. Citing it would present a retired rule as current policy. The only reliable guard is the `Status` line, which is why `search_corpus.py` never lists a superseded document as a result. If a superseded document matches, cite the current document it names in its `Status` line instead, and mention the superseded one only when the question is explicitly about the old version.
