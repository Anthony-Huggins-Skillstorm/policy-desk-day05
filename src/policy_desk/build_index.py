"""Rebuild index/ from corpus/. Needs Azure (it calls the embedding deployment).

    python -m policy_desk.build_index
"""

from __future__ import annotations

import asyncio

from policy_desk.corpus import chunk_document, load_corpus
from policy_desk.embeddings import AzureEmbedder
from policy_desk.retriever import VectorIndex
from policy_desk.settings import CORPUS_DIR, INDEX_DIR, Settings


async def _main() -> None:
    docs = load_corpus(CORPUS_DIR)
    chunks = [chunk for doc in docs for chunk in chunk_document(doc)]
    embedder = AzureEmbedder(Settings.from_env())
    try:
        vectors = await embedder.embed([c.text for c in chunks])
    finally:
        await embedder.close()
    VectorIndex(chunks, vectors).save(INDEX_DIR)
    print(f"Indexed {len(docs)} documents as {len(chunks)} chunks into {INDEX_DIR}")


if __name__ == "__main__":
    asyncio.run(_main())
