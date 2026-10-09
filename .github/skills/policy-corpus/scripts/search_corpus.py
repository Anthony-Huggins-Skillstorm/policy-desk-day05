"""Search the Northwind policy corpus at section level and print citable source pointers.

    python .github/skills/policy-corpus/scripts/search_corpus.py "SOC 2 Type I report accepted"
    python .github/skills/policy-corpus/scripts/search_corpus.py "tier 1 reassessment" --top 3
    python .github/skills/policy-corpus/scripts/search_corpus.py "assurance report age" --include-superseded

Standard library only and no network: ranks every section of corpus/*.md (except MANIFEST.md) by
BM25 term relevance. Only documents whose Status is Current are listed; a matching superseded
document is named on a "SUPERSEDED, do not cite" line instead. Exits 1 when nothing matches.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
CORPUS_DIR = REPO_ROOT / "corpus"

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does", "for", "from", "how", "in",
    "is", "it", "its", "must", "of", "on", "or", "should", "that", "the", "their", "this", "to",
    "what", "when", "which", "who", "with",
}
HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
BOLD_LEAD_RE = re.compile(r"^\*\*(.+?)\.?\*\*")
META_RE = re.compile(r"^(Doc ID|Version|Status):\s*(.+?)\s*$")
# Section-number styles: "3. Timing", "3 Timing", "4.2 Independent ...", "Section 3 — Timing", "Step 1: Intake".
NUMBERED_RE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.+)$")
SECTION_RE = re.compile(r"^Section\s+(\d+(?:\.\d+)*)\s*[—–:-]\s*(.+)$", re.IGNORECASE)
STEP_RE = re.compile(r"^Step\s+(\d+)\s*[:.—–-]\s*(.+)$", re.IGNORECASE)


@dataclass
class Section:
    doc_id: str
    version: str
    status: str
    file: str
    line: int
    heading: str
    key: str
    text: str = ""
    terms: Counter = field(default_factory=Counter)

    @property
    def current(self) -> bool:
        return self.status.lower() == "current"


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


def citation_key(doc_id: str, heading: str) -> str:
    if m := SECTION_RE.match(heading):
        return f"{doc_id} §{m.group(1)}"
    if m := STEP_RE.match(heading):
        return f"{doc_id} Step {m.group(1)}"
    if m := NUMBERED_RE.match(heading):
        return f"{doc_id} §{m.group(1)}"
    return f"{doc_id} — {heading}"


def parse_document(path: Path) -> list[Section]:
    lines = path.read_text(encoding="utf-8").splitlines()
    meta = {"Doc ID": path.stem, "Version": "unknown", "Status": "unknown"}
    for line in lines:
        if line.startswith("## "):
            break
        if m := META_RE.match(line):
            meta[m.group(1)] = m.group(2)

    sections: list[Section] = []
    has_headings = any(HEADING_RE.match(line) for line in lines)
    for number, line in enumerate(lines, start=1):
        heading = None
        if has_headings:
            if m := HEADING_RE.match(line):
                heading = m.group(2)
        elif m := BOLD_LEAD_RE.match(line):
            heading = m.group(1).rstrip(".")
        if heading is not None:
            sections.append(Section(meta["Doc ID"], meta["Version"], meta["Status"], path.name, number,
                                    heading, citation_key(meta["Doc ID"], heading)))
            if not has_headings:
                sections[-1].text = line + "\n"
            continue
        if sections:
            sections[-1].text += line + "\n"

    for section in sections:
        section.terms = Counter(tokenize(section.heading + " " + section.text))
    return sections


def load_sections() -> list[Section]:
    if not CORPUS_DIR.is_dir():
        sys.exit(f"Corpus not found at {CORPUS_DIR}")
    sections: list[Section] = []
    for path in sorted(CORPUS_DIR.glob("*.md")):
        if path.name != "MANIFEST.md":
            sections.extend(parse_document(path))
    return sections


def bm25(sections: list[Section], query: list[str], k1: float = 1.5, b: float = 0.75) -> list[tuple[float, Section]]:
    n = len(sections)
    avg_len = sum(sum(s.terms.values()) for s in sections) / max(n, 1)
    doc_freq = Counter(term for s in sections for term in set(s.terms))
    scored = []
    for section in sections:
        length = sum(section.terms.values())
        score = 0.0
        for term in set(query):
            tf = section.terms.get(term, 0)
            if not tf:
                continue
            idf = math.log(1 + (n - doc_freq[term] + 0.5) / (doc_freq[term] + 0.5))
            score += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * length / avg_len))
        if score > 0:
            scored.append((score, section))
    return sorted(scored, key=lambda pair: pair[0], reverse=True)


def snippet(section: Section, query: list[str], width: int = 160) -> str:
    text = " ".join(section.text.split())
    lowered = text.lower()
    starts = [lowered.find(term) for term in query if lowered.find(term) >= 0]
    start = max(min(starts) - 40, 0) if starts else 0
    piece = text[start:start + width]
    return ("…" if start else "") + piece + ("…" if start + width < len(text) else "")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("query", help="What to look for, in plain words.")
    parser.add_argument("--top", type=int, default=5, help="Number of results to list (default 5).")
    parser.add_argument("--include-superseded", action="store_true",
                        help="List superseded documents as results instead of naming them on a warning line.")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    query = tokenize(args.query)
    ranked = bm25(load_sections(), query) if query else []
    if not ranked:
        print(f"No corpus section matches {args.query!r}. Try different or fewer words.")
        sys.exit(1)

    listed = [(s, sec) for s, sec in ranked if args.include_superseded or sec.current][: args.top]
    superseded = [] if args.include_superseded else list(
        dict.fromkeys((sec.doc_id, sec.status, sec.file) for _, sec in ranked[: args.top * 3] if not sec.current)
    )

    for rank, (score, sec) in enumerate(listed, start=1):
        title = sec.key if sec.key.endswith(sec.heading) else f"{sec.key} — {sec.heading}"
        print(f"{rank}. {title}")
        print(f"   {sec.doc_id} v{sec.version} ({sec.status}) | corpus/{sec.file}:{sec.line} | score {score:.2f}")
        print(f"   {snippet(sec, query)}")
    for doc_id, status, file in superseded:
        print(f"SUPERSEDED, do not cite: {doc_id} (corpus/{file}) — Status: {status}. Cite the current document instead.")
    if not listed:
        print("Only superseded documents matched. Rerun with --include-superseded to inspect them; do not cite them.")
        sys.exit(1)


if __name__ == "__main__":
    main()
