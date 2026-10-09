from __future__ import annotations

import pytest

from policy_desk.citations import extract_citations, verify_citations


class TestExtractCitations:
    def test_returns_empty_list_when_answer_has_no_citations(self):
        assert extract_citations("The policies do not cover parental leave.") == []

    def test_ignores_malformed_citation_markers(self):
        assert extract_citations("See doc_id: ONB-PRC and [ONB-PRC].") == []

    def test_deduplicates_while_keeping_first_appearance_order(self):
        answer = "A [doc_id: RNW-PRC]. B [doc_id: DUE-STD]. C [doc_id: RNW-PRC]."
        assert extract_citations(answer) == ["RNW-PRC", "DUE-STD"]

    @pytest.mark.parametrize(
        "answer, expected",
        [
            ("Tier 1 vendors are reassessed annually [doc_id: DUE-STD].", ["DUE-STD"]),
            ("Exit plans are required [doc_id:DPA-REQ].", ["DPA-REQ"]),
            ("Bids over the threshold need three quotes [doc_id:  PRC-POL].", ["PRC-POL"]),
        ],
    )
    def test_extracts_well_formed_citations(self, answer, expected):
        assert extract_citations(answer) == expected


class TestVerifyCitations:
    def test_answer_without_citations_is_not_grounded(self):
        report = verify_citations("Some uncited claim.", {"DUE-STD"})
        assert report.cited == []
        assert not report.grounded

    def test_citation_that_was_never_retrieved_is_unsupported(self):
        report = verify_citations("Claim [doc_id: ACC-STD].", {"DUE-STD"})
        assert report.unsupported == ["ACC-STD"]
        assert not report.grounded

    def test_one_unsupported_citation_makes_the_answer_ungrounded(self):
        report = verify_citations("A [doc_id: DUE-STD]. B [doc_id: ACC-STD].", {"DUE-STD"})
        assert report.verified == ["DUE-STD"]
        assert report.unsupported == ["ACC-STD"]
        assert not report.grounded

    def test_answer_citing_only_retrieved_documents_is_grounded(self):
        report = verify_citations("A [doc_id: DUE-STD]. B [doc_id: RNW-PRC].", {"DUE-STD", "RNW-PRC"})
        assert report.verified == ["DUE-STD", "RNW-PRC"]
        assert report.grounded
