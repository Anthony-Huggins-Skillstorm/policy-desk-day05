from __future__ import annotations

import pytest

from policy_desk.corpus import chunk_document, load_corpus, parse_document
from policy_desk.settings import CORPUS_DIR


class TestParseDocument:
    def test_rejects_a_document_without_a_doc_id_line(self, tmp_path):
        path = tmp_path / "bad.md"
        path.write_text("# Untitled\n\nVersion: 1.0\n\nBody.", encoding="utf-8")
        with pytest.raises(ValueError, match="Doc ID"):
            parse_document(path)

    def test_missing_optional_fields_default_sensibly(self, tmp_path):
        path = tmp_path / "minimal.md"
        path.write_text("# Minimal\n\nDoc ID: MIN-DOC\n\nBody text.", encoding="utf-8")
        doc = parse_document(path)
        assert doc.owner is None
        assert doc.status == "Current"
        assert not doc.superseded

    def test_reads_metadata_and_body(self, sample_doc_path):
        doc = parse_document(sample_doc_path)
        assert doc.doc_id == "ONB-PRC"
        assert doc.title == "Vendor Onboarding Procedure"
        assert doc.owner == "Procurement"
        assert doc.body.startswith("## 1. Purpose")


class TestChunkDocument:
    def test_long_section_is_split_on_paragraph_boundaries(self, tmp_path):
        paragraphs = "\n\n".join(f"Paragraph {i} " + "x" * 400 for i in range(6))
        path = tmp_path / "long.md"
        path.write_text(f"# Long\n\nDoc ID: LNG-DOC\n\n## 1. Scope\n\n{paragraphs}", encoding="utf-8")
        chunks = chunk_document(parse_document(path), max_chars=1000)
        assert len(chunks) > 1
        assert all(c.section == "1. Scope" for c in chunks)

    def test_every_chunk_carries_its_document_header(self, sample_doc_path):
        chunks = chunk_document(parse_document(sample_doc_path))
        assert all(c.text.startswith("Vendor Onboarding Procedure (ONB-PRC, Current)") for c in chunks)

    def test_one_chunk_per_heading(self, sample_doc_path):
        chunks = chunk_document(parse_document(sample_doc_path))
        assert [c.section for c in chunks] == ["1. Purpose", "2. Steps"]
        assert [c.chunk_id for c in chunks] == ["ONB-PRC#00", "ONB-PRC#01"]


class TestShippedCorpus:
    def test_shipped_corpus_loads_with_unique_ids(self):
        docs = load_corpus(CORPUS_DIR)
        assert len(docs) >= 20
        assert len({d.doc_id for d in docs}) == len(docs)
