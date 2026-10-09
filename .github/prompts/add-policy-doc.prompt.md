---
description: "Add a policy document to the corpus: validate it, register it in the manifest, rebuild the index, and report retrieval recall before and after"
argument-hint: "docPath=<full path to the new policy .md file>"
agent: agent
---

# Add a policy document

Add the policy document at `${input:docPath:Full path to the new policy markdown file}` to the policy-desk corpus. Follow the steps in order. Stop at the first failure, report what failed, and change nothing else.

The current manifest is attached: #file:../../corpus/MANIFEST.md

## 1. Validate (refuse on any failure)

Read the file. Refuse, without copying or editing anything, if any of these is true:

* It does not start with the metadata block every corpus document uses, in this order: a `# Title` line, then `Doc ID:`, `Version:`, `Owner:`, `Effective:`, and `Status:` lines.
* The `Doc ID` value is not uppercase letter segments joined by hyphens, each segment three or four letters (for example `TPR-POL`, `EXIT-PLN`).
* The `Doc ID` already appears in the `Doc ID` column of `corpus/MANIFEST.md`.
* A file with the target name (step 3) already exists in `corpus/`.

When refusing, state which check failed and quote the offending line or manifest row.

## 2. Baseline evaluation

Before changing anything, run the offline retrieval evaluation and keep its JSON output as the baseline:

```bash
python eval/eval.py --retrieval-only --json
```

## 3. Copy into the corpus

Copy the file into `corpus/` with a kebab-case file name derived from its `# Title` (lowercase, words joined by hyphens, punctuation dropped, `.md` extension). Do not change the file's content.

## 4. Register in the manifest

In `corpus/MANIFEST.md`:

* Add one row to the table, after the last document row, in the existing format: `| <Doc ID> | <file name> | <Title> | <Status> | <Words> |`.
* Compute `Words` exactly as the manifest defines it: whitespace-delimited tokens over the full file, including the metadata block (for example `python -c "import sys; print(len(open(sys.argv[1], encoding='utf-8').read().split()))" corpus/<file>`). Do not estimate.
* Update the `Total:` line below the table: increase the document count by one and the word total by the new document's word count. Keep the rest of the line unchanged.
* Do not edit any other part of the manifest.

## 5. Rebuild and verify

Run, in order, and stop on the first failure:

```bash
python -m policy_desk.build_index
pytest
python eval/eval.py --retrieval-only --json
```

`build_index` calls the Azure embedding deployment. If it fails with an authentication error (for example `AADSTS70043`), stop and tell the user to run `az login`, then rerun this prompt.

## 6. Report and stop

Report:

* The doc id, the new file name, and its word count.
* The manifest `Total:` line before and after.
* Retrieval recall before and after, from the two evaluation runs, and any other metric that changed. Call out any decrease as a regression.
* The `pytest` result.

Do not commit, stage, or push anything. Leave the changes for the user to review.
