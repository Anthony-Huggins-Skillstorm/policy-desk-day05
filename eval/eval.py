"""Score policy-desk against the golden question set.

Modes:
  python eval/eval.py --retrieval-only        offline; uses cached question embeddings
  python eval/eval.py --recorded              offline; re-verifies recorded model answers
  add --json to either offline mode for a machine-readable summary
  python eval/eval.py --limit 5               live; runs the agent (needs Azure)
  python eval/eval.py --limit 5 --record      live; also saves answers as the recorded fixture
  python eval/eval.py --refresh-embeddings    live; rebuilds the cached question embeddings
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from policy_desk.citations import verify_citations  # noqa: E402
from policy_desk.retriever import VectorIndex  # noqa: E402
from policy_desk.settings import INDEX_DIR  # noqa: E402

GOLDEN = ROOT / "eval" / "golden-questions.json"
QUESTION_VECTORS = ROOT / "eval" / "golden-embeddings.npz"
RECORDED = ROOT / "tests" / "fixtures" / "recorded-answers.json"
IN_SCOPE = {"answerable", "multi_hop", "typo", "ambiguous", "superseded_trap"}
REFUSAL_MARKERS = ("do not cover", "don't cover", "not covered", "no policy", "does not address")


def load_golden(category: str | None, limit: int | None) -> list[dict]:
    items = json.loads(GOLDEN.read_text(encoding="utf-8"))
    if category:
        items = [q for q in items if q["category"] == category]
    return items[:limit] if limit else items


def retrieval_only(items: list[dict], k: int, as_json: bool = False) -> None:
    index = VectorIndex.load(INDEX_DIR)
    cached = np.load(QUESTION_VECTORS)
    rows, hit_total, hit_found, trap_hits = [], 0, 0, 0
    oos_scores, in_scope_scores = [], []
    for q in items:
        hits = index.search(cached[q["id"]], k=k)
        got = [h.doc_id for h in hits]
        top = hits[0].score
        if q["category"] == "out_of_scope":
            oos_scores.append(top)
            rows.append((q["id"], q["category"], f"top={top:.3f}", ",".join(got[:3])))
            continue
        in_scope_scores.append(top)
        expected = set(q["expected_doc_ids"])
        found = expected & set(got)
        hit_total += len(expected)
        hit_found += len(found)
        if q["category"] == "superseded_trap" and "DUE-OLD" in got and got.index("DUE-OLD") < min(
            (got.index(d) for d in found), default=k
        ):
            trap_hits += 1
        rows.append((q["id"], q["category"], f"{len(found)}/{len(expected)}", ",".join(got[:3])))

    if as_json:
        print(json.dumps({
            "mode": "retrieval-only", "k": k, "questions": len(items),
            "recall_found": hit_found, "recall_total": hit_total,
            "superseded_above_current": trap_hits,
            "in_scope_min_top_score": min(in_scope_scores, default=None),
            "out_of_scope_max_top_score": max(oos_scores, default=None),
        }, indent=1))
        return
    for row in rows:
        print(f"{row[0]:8} {row[1]:16} {row[2]:>10}  {row[3]}")
    print(f"\nrecall@{k}: {hit_found}/{hit_total} expected documents retrieved")
    print(f"superseded doc ranked above the current one: {trap_hits} question(s)")
    if oos_scores and in_scope_scores:
        print(f"top score  in-scope min {min(in_scope_scores):.3f} | out-of-scope max {max(oos_scores):.3f}")


def recorded(as_json: bool = False) -> None:
    records = json.loads(RECORDED.read_text(encoding="utf-8"))
    grounded, not_grounded = 0, []
    for r in records:
        report = verify_citations(r["answer"], set(r["retrieved_doc_ids"]))
        grounded += report.grounded
        if not report.grounded:
            not_grounded.append(r["id"])
        if not as_json:
            flag = "grounded" if report.grounded else "NOT grounded"
            print(f"{r['id']:8} {flag:13} verified={report.verified} unsupported={report.unsupported}")
    if as_json:
        print(json.dumps({"mode": "recorded", "answers": len(records), "grounded": grounded,
                          "not_grounded_ids": not_grounded}, indent=1))
        return
    print(f"\ngrounded answers: {grounded}/{len(records)}")


async def live(items: list[dict], record: bool) -> None:
    from policy_desk.agent import ask
    from policy_desk.runtime import live_agent

    log_dir = ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / f"eval-{time.strftime('%Y%m%d-%H%M%S')}.jsonl"
    saved, passed = [], 0
    async with live_agent() as (agent, turn):
        for q in items:
            started = time.perf_counter()
            answer = await ask(agent, turn, q["question"])
            latency = time.perf_counter() - started
            text = answer.text.lower()
            if q["category"] == "out_of_scope":
                ok = any(m in text for m in REFUSAL_MARKERS) and not answer.citations.cited
            else:
                ok = all(s.lower() in text for s in q["expected_answer_contains"]) and answer.citations.grounded
            passed += ok
            print(f"{q['id']:8} {q['category']:16} {'PASS' if ok else 'FAIL'}  {latency:5.1f}s  "
                  f"verified={answer.citations.verified}")
            entry = {
                "id": q["id"],
                "question": q["question"],
                "answer": answer.text,
                "retrieved_doc_ids": sorted({h.doc_id for h in answer.hits}),
            }
            saved.append(entry)
            with log_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps({**entry, "pass": ok, "latency_s": round(latency, 2)}) + "\n")
    print(f"\npassed {passed}/{len(items)}  (log: {log_path.relative_to(ROOT)})")
    if record:
        RECORDED.parent.mkdir(parents=True, exist_ok=True)
        RECORDED.write_text(json.dumps(saved, indent=1), encoding="utf-8")
        print(f"recorded {len(saved)} answers to {RECORDED.relative_to(ROOT)}")


async def refresh_embeddings() -> None:
    from policy_desk.embeddings import AzureEmbedder
    from policy_desk.settings import Settings

    items = load_golden(None, None)
    embedder = AzureEmbedder(Settings.from_env())
    try:
        vectors = await embedder.embed([q["question"] for q in items])
    finally:
        await embedder.close()
    np.savez_compressed(QUESTION_VECTORS, **{q["id"]: v for q, v in zip(items, vectors)})
    print(f"cached {len(items)} question embeddings")


def main() -> None:
    parser = argparse.ArgumentParser(description="Score policy-desk against the golden set.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--retrieval-only", action="store_true", help="Offline retrieval scoring.")
    mode.add_argument("--recorded", action="store_true", help="Offline citation check on recorded answers.")
    mode.add_argument("--refresh-embeddings", action="store_true", help="Rebuild cached question embeddings.")
    parser.add_argument("--limit", type=int, help="Score only the first N questions.")
    parser.add_argument("--category", choices=sorted(IN_SCOPE | {"out_of_scope"}))
    parser.add_argument("--k", type=int, default=5, help="Top-k for retrieval-only mode.")
    parser.add_argument("--record", action="store_true", help="Live mode: save answers as the fixture.")
    parser.add_argument("--json", action="store_true", help="Offline modes: print a JSON summary only.")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if args.retrieval_only:
        retrieval_only(load_golden(args.category, args.limit), args.k, args.json)
    elif args.recorded:
        recorded(args.json)
    elif args.refresh_embeddings:
        asyncio.run(refresh_embeddings())
    else:
        asyncio.run(live(load_golden(args.category, args.limit), args.record))


if __name__ == "__main__":
    main()
