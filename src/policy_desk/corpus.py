"""Load policy documents and split them into retrievable chunks.

Every document starts with a metadata block:

    # <Title>

    Doc ID: TPR-POL
    Version: 4.0
    Owner: TPRM Office
    Effective: 2026-03-01
    Status: Current

Fields other than Doc ID are optional; documents in the wild are inconsistent.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_META_RE = re.compile(r"^(Doc ID|Version|Owner|Effective|Status):\s*(.+?)\s*$", re.MULTILINE)
_HEADING_RE = re.compile(r"^#{2,3}\s+.+$|^\*\*[^*\n]{3,80}\.\*\*", re.MULTILINE)


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    status: str
    version: str | None
    owner: str | None
    effective: str | None
    path: Path
    body: str

    @property
    def superseded(self) -> bool:
        return self.status.lower().startswith("superseded")


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    status: str
    section: str
    text: str


def parse_document(path: Path) -> Document:
    raw = path.read_text(encoding="utf-8")
    title_line = next((line for line in raw.splitlines() if line.startswith("# ")), path.stem)
    meta = {key: value for key, value in _META_RE.findall(raw[:600])}
    if "Doc ID" not in meta:
        raise ValueError(f"{path.name}: missing 'Doc ID:' line in the metadata block")
    # Body starts after the last metadata line.
    last_meta = max(m.end() for m in _META_RE.finditer(raw[:600]))
    return Document(
        doc_id=meta["Doc ID"],
        title=title_line.removeprefix("# ").strip(),
        status=meta.get("Status", "Current"),
        version=meta.get("Version"),
        owner=meta.get("Owner"),
        effective=meta.get("Effective"),
        path=path,
        body=raw[last_meta:].strip(),
    )


def load_corpus(corpus_dir: Path) -> list[Document]:
    docs = [parse_document(p) for p in sorted(corpus_dir.glob("*.md")) if p.name != "MANIFEST.md"]
    seen: dict[str, Path] = {}
    for doc in docs:
        if doc.doc_id in seen:
            raise ValueError(f"Duplicate Doc ID {doc.doc_id} in {doc.path.name} and {seen[doc.doc_id].name}")
        seen[doc.doc_id] = doc.path
    return docs


def _sections(body: str) -> list[tuple[str, str]]:
    """Split a body on headings. Text before the first heading is the 'Preamble' section."""
    marks = list(_HEADING_RE.finditer(body))
    if not marks:
        return [("Preamble", body)]
    sections = []
    if marks[0].start() > 0 and body[: marks[0].start()].strip():
        sections.append(("Preamble", body[: marks[0].start()]))
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        heading = mark.group(0).strip("#* ").rstrip(".")
        sections.append((heading, body[mark.start() : end]))
    return sections


def chunk_document(doc: Document, max_chars: int = 1500) -> list[Chunk]:
    """One chunk per section; long sections are split on paragraph boundaries."""
    chunks: list[Chunk] = []
    for section, text in _sections(doc.body):
        buffer = ""
        for para in re.split(r"\n\s*\n", text.strip()):
            if buffer and len(buffer) + len(para) > max_chars:
                chunks.append(_make_chunk(doc, section, buffer, len(chunks)))
                buffer = ""
            buffer = f"{buffer}\n\n{para}" if buffer else para
        if buffer.strip():
            chunks.append(_make_chunk(doc, section, buffer, len(chunks)))
    return chunks


def _make_chunk(doc: Document, section: str, text: str, ordinal: int) -> Chunk:
    # The title travels with every chunk so a chunk retrieved alone still says what it is.
    header = f"{doc.title} ({doc.doc_id}, {doc.status})\nSection: {section}\n\n"
    return Chunk(
        chunk_id=f"{doc.doc_id}#{ordinal:02d}",
        doc_id=doc.doc_id,
        title=doc.title,
        status=doc.status,
        section=section,
        text=header + text.strip(),
    )
