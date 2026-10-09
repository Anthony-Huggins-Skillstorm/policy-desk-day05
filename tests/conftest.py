"""Shared fixtures. Nothing here touches the network."""

from __future__ import annotations

import numpy as np
import pytest

from policy_desk.corpus import Chunk

SAMPLE_DOC = """# Vendor Onboarding Procedure

Doc ID: ONB-PRC
Version: 2.3
Owner: Procurement
Effective: 2026-02-01
Status: Current

## 1. Purpose

This procedure sets out how a vendor is onboarded.

## 2. Steps

1. Submit the intake form.
2. Complete due diligence per DUE-STD.
"""


class FakeEmbedder:
    """Deterministic embedder: maps known strings to fixed vectors, everything else to zeros."""

    def __init__(self, table: dict[str, list[float]], dim: int = 3) -> None:
        self.table = table
        self.dim = dim

    async def embed(self, texts: list[str]) -> np.ndarray:
        return np.asarray([self.table.get(t, [0.0] * self.dim) for t in texts], dtype=np.float32)


def make_chunk(doc_id: str, ordinal: int = 0, status: str = "Current") -> Chunk:
    return Chunk(
        chunk_id=f"{doc_id}#{ordinal:02d}",
        doc_id=doc_id,
        title=f"Title of {doc_id}",
        status=status,
        section="Purpose",
        text=f"Text of {doc_id}",
    )


@pytest.fixture
def sample_doc_path(tmp_path):
    path = tmp_path / "vendor-onboarding-procedure.md"
    path.write_text(SAMPLE_DOC, encoding="utf-8")
    return path
