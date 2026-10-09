"""In-process vector index: cosine similarity over a matrix of chunk embeddings."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from policy_desk.corpus import Chunk
from policy_desk.embeddings import Embedder


@dataclass(frozen=True)
class Hit:
    chunk_id: str
    doc_id: str
    title: str
    status: str
    section: str
    text: str
    score: float


class VectorIndex:
    def __init__(self, chunks: list[Chunk], vectors: np.ndarray) -> None:
        if len(chunks) != vectors.shape[0]:
            raise ValueError(f"{len(chunks)} chunks but {vectors.shape[0]} vectors")
        self.chunks = chunks
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        self._unit = vectors / np.where(norms == 0, 1.0, norms)

    def search(self, query: np.ndarray, k: int = 5) -> list[Hit]:
        q = query / (np.linalg.norm(query) or 1.0)
        scores = self._unit @ q
        top = np.argsort(-scores)[:k]
        return [Hit(**asdict(self.chunks[i]), score=round(float(scores[i]), 4)) for i in top]

    def save(self, index_dir: Path) -> None:
        index_dir.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(index_dir / "index.npz", vectors=self._unit.astype(np.float32))
        (index_dir / "chunks.json").write_text(
            json.dumps([asdict(c) for c in self.chunks], indent=1), encoding="utf-8"
        )

    @classmethod
    def load(cls, index_dir: Path) -> VectorIndex:
        vectors = np.load(index_dir / "index.npz")["vectors"]
        chunks = [Chunk(**c) for c in json.loads((index_dir / "chunks.json").read_text(encoding="utf-8"))]
        return cls(chunks, vectors)


class Retriever:
    def __init__(self, index: VectorIndex, embedder: Embedder) -> None:
        self.index = index
        self.embedder = embedder

    async def retrieve(self, question: str, k: int = 5) -> list[Hit]:
        [vector] = await self.embedder.embed([question])
        return self.index.search(vector, k=k)
