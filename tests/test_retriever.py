from __future__ import annotations

import asyncio

import numpy as np
import pytest

from conftest import FakeEmbedder, make_chunk
from policy_desk.retriever import Retriever, VectorIndex


@pytest.fixture
def index():
    chunks = [make_chunk("DUE-STD"), make_chunk("RNW-PRC"), make_chunk("ACC-STD")]
    vectors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)
    return VectorIndex(chunks, vectors)


class TestVectorIndex:
    def test_rejects_mismatched_chunk_and_vector_counts(self):
        with pytest.raises(ValueError):
            VectorIndex([make_chunk("DUE-STD")], np.zeros((2, 3), dtype=np.float32))

    def test_zero_query_vector_does_not_crash(self, index):
        hits = index.search(np.zeros(3, dtype=np.float32), k=2)
        assert len(hits) == 2

    def test_k_larger_than_index_returns_every_chunk(self, index):
        assert len(index.search(np.array([1, 1, 1], dtype=np.float32), k=10)) == 3

    def test_save_and_load_round_trip(self, index, tmp_path):
        index.save(tmp_path)
        loaded = VectorIndex.load(tmp_path)
        assert [h.doc_id for h in loaded.search(np.array([0, 0, 1], dtype=np.float32), k=1)] == ["ACC-STD"]

    def test_ranks_by_cosine_similarity(self, index):
        hits = index.search(np.array([0.1, 0.9, 0.0], dtype=np.float32), k=2)
        assert [h.doc_id for h in hits] == ["RNW-PRC", "DUE-STD"]
        assert hits[0].score > hits[1].score


class TestRetriever:
    def test_embeds_the_question_and_searches_the_index(self, index):
        retriever = Retriever(index, FakeEmbedder({"renewal notice": [0, 1, 0]}))
        hits = asyncio.run(retriever.retrieve("renewal notice", k=1))
        assert hits[0].doc_id == "RNW-PRC"
