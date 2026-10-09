"""Citation extraction and verification.

The agent is told to cite as [doc_id: TPR-POL]. An answer is only as trustworthy as
its citations, so every cited id is checked against what retrieval actually returned
this turn. A cited id that was never retrieved is reported as unsupported.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

CITATION_RE = re.compile(r"\[doc_id:\s*([A-Z]{3,4}-[A-Z]{3,4})\]")


@dataclass(frozen=True)
class CitationReport:
    cited: list[str] = field(default_factory=list)
    verified: list[str] = field(default_factory=list)
    unsupported: list[str] = field(default_factory=list)

    @property
    def grounded(self) -> bool:
        return bool(self.verified) and not self.unsupported


def extract_citations(answer: str) -> list[str]:
    """Cited doc ids in first-appearance order, without duplicates."""
    return list(dict.fromkeys(CITATION_RE.findall(answer)))


def verify_citations(answer: str, retrieved_doc_ids: set[str]) -> CitationReport:
    cited = extract_citations(answer)
    return CitationReport(
        cited=cited,
        verified=[d for d in cited if d in retrieved_doc_ids],
        unsupported=[d for d in cited if d not in retrieved_doc_ids],
    )
