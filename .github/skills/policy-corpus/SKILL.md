---
name: policy-corpus
description: "Use during research and use during planning whenever a task depends on what a Northwind TPRM or procurement policy requires (tiers, reassessment, due-diligence evidence, assurance reports, renewal, exit, incidents). Run python .github/skills/policy-corpus/scripts/search_corpus.py \"<query>\" for each policy question, read each returned section at its file:line, and cite every policy claim as DOC-ID §section (vVersion, corpus/file:line), e.g. DUE-STD §4.2 (v3.0, corpus/due-diligence-standard.md:29). Never cite a SUPERSEDED document as a requirement. Returns source pointers for the phase to verify; writes nothing."
---

# Policy corpus search

Use this skill when research or planning needs to know what a Northwind policy actually says. The policies live in `corpus/*.md`, and `corpus/MANIFEST.md` lists them. The skill finds the relevant sections and gives you pointers to read. It does not decide what the policy means, and it writes nothing. The phase reads the cited lines, classifies the evidence, and records it in its own artifact.

## Search

From the repository root (the script resolves paths itself, so any working directory works):

```bash
python .github/skills/policy-corpus/scripts/search_corpus.py "<plain-words query>" [--top N] [--include-superseded]
```

* Run several narrow queries rather than one broad one, for example "tier 1 reassessment frequency", then "SOC 2 Type I report accepted", then "assurance report age".
* Each result gives a citation key (`DUE-STD §4.2`), the heading, the doc id, version and status, `corpus/<file>:<line>`, and a snippet.
* Exit code 1 means nothing matched. Rephrase with different terms before concluding that the corpus is silent.

## Use the results

1. **Read before relying.** Open each section at its `file:line` and read the whole section. A snippet is a pointer, not evidence. Near-duplicate figures (`24 hours`, `30 days`, `12 months`) recur with different meanings across documents.
2. **Follow cross-references.** Sections often defer to another document (`Reassessment frequency follows TIER-MTX §3`). Search for and read the referenced section, and cite the document that actually states the rule.
3. **Cite in the standard format:** doc id and section, version, and file:line, for example `DUE-STD §4.2 (v3.0, corpus/due-diligence-standard.md:29)`. See [references/citation-format.md](references/citation-format.md) for every heading style and the rules.

## Superseded documents

The script never lists a document whose `Status` is not `Current`. When one matches, it prints a `SUPERSEDED, do not cite: <DOC-ID>` line instead. Do not cite that document as a requirement. Cite the current document its `Status` line names (for example, `DUE-OLD` is superseded by `DUE-STD`). Use `--include-superseded` only when the question is explicitly about an old version, and label anything taken from it as superseded.

## Boundaries

This skill contributes sources and a citation convention only. It does not change the research or planning process, the artifact paths, the evidence identifiers, or any decision. Treat everything it returns as evidence for the phase to verify.
