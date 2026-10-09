# policy-desk

Grounded Q&A over Northwind Capital Group's third-party risk management (TPRM) and procurement policies. Staff ask a question; the agent searches the policy corpus, answers, and cites every claim as `[doc_id: TPR-POL]`. After each turn the citations are checked against what retrieval actually returned.

## Layout

```
policy-desk/
├── corpus/                 23 policy documents + MANIFEST.md
├── index/                  prebuilt embeddings (index.npz) + chunk metadata (chunks.json)
├── eval/
│   ├── golden-questions.json   55 questions with expected documents
│   ├── golden-embeddings.npz   cached question embeddings for offline scoring
│   └── eval.py
├── infra/main.bicep        target Azure deployment (reference only)
├── src/policy_desk/
│   ├── settings.py         environment configuration
│   ├── corpus.py           document parsing and chunking
│   ├── embeddings.py       keyless Azure OpenAI embedding client
│   ├── retriever.py        in-process cosine-similarity index
│   ├── citations.py        citation extraction and verification
│   ├── agent.py            Agent Framework agent + search_policies tool
│   ├── runtime.py          live wiring: Foundry chat client, embedder, index
│   ├── cli.py              ask a question from the terminal
│   └── build_index.py      rebuild index/ from corpus/
└── tests/                  offline unit tests (no network)
```

## Request path

```
question ──▶ Agent (gpt-5-mini via FoundryChatClient)
                │  calls
                ▼
        search_policies tool ──▶ Retriever ──▶ embed query (text-embedding-3-small)
                │                                   │
                │                                   ▼
                │                          VectorIndex.search (cosine, top 5)
                │  hits recorded in TurnRecord ◀────┘
                ▼
        answer text with [doc_id: ...] citations
                │
                ▼
        verify_citations(answer, retrieved doc ids) ──▶ cited / verified / unsupported
```

## Setup

Python 3.11+. Keep the virtual environment on a short path on Windows; some Azure SDK wheels exceed the 260-character path limit.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env        # then fill in your Foundry endpoints
az login
```

**Windows PowerShell:** activate with `.venv\Scripts\Activate.ps1` and copy with `Copy-Item .env.example .env`.

Your account needs the **Cognitive Services OpenAI User** role on the Foundry resource (for embeddings) and **Azure AI User** on the project (for the agent).

## Commands

| Command | Needs Azure | What it does |
|---|---|---|
| `pytest` | No | Unit tests |
| `python eval/eval.py --retrieval-only` | No | Retrieval recall on the golden set, from cached question embeddings |
| `python eval/eval.py --recorded` | No | Re-verifies citations on recorded model answers |
| `python -m policy_desk.cli "question"` | Yes | Ask one question |
| `python eval/eval.py --limit 5` | Yes | Run the agent on the first 5 golden questions |
| `python -m policy_desk.build_index` | Yes | Rebuild the index after changing the corpus |

## Conventions

- **Keyless only.** Credentials come from `az login` through `azure-identity`. No API keys anywhere, including tests.
- **Agent Framework 1.15 names.** `Agent`, `@tool`, `AgentResponse`, `FoundryChatClient`.
- **Tests never call the network.** Use the fakes in `tests/conftest.py`.
- **Citations are a contract.** Answers cite `[doc_id: XXX-XXX]`; anything that changes the citation format changes `citations.py` and its tests in the same commit.
