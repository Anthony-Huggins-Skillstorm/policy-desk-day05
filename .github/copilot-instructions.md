---
description: "Repository-wide guidance for policy-desk"
---

# policy-desk

policy-desk answers Northwind Capital Group staff questions about third-party risk management and procurement policy. It is a single Microsoft Agent Framework agent with one retrieval tool over a local vector index, and every answer cites the policy documents it relied on.

## Non-negotiables

- **Keyless authentication only.** Credentials come from `azure-identity` (`AzureCliCredential`, `DefaultAzureCredential`, or a bearer-token provider). Never add an API key, a `api_key=` argument, or a key-based environment variable.
- **Citations are a contract.** Answers cite sources as `[doc_id: <ID>]`. Doc ids are uppercase segments joined by a hyphen, and segments may be three or four letters (`TPR-POL`, `EXIT-PLN`). Any change to the citation format changes `src/policy_desk/citations.py` and its tests together.
- **Tests never call the network.** Use or extend the fakes in `tests/conftest.py`.
- **Do not edit `corpus/` or `index/` as a side effect.** Corpus changes are deliberate and are followed by `python -m policy_desk.build_index`.

## Commands

- Tests: `pytest`
- Offline retrieval eval: `python eval/eval.py --retrieval-only`
- Live question: `python -m policy_desk.cli "<question>"`
