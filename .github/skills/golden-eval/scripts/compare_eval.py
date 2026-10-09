"""Compare policy-desk's offline evaluation against a saved baseline.

    python .github/skills/golden-eval/scripts/compare_eval.py                  # compare
    python .github/skills/golden-eval/scripts/compare_eval.py --save-baseline  # record current numbers

Runs both offline modes of eval/eval.py (no network calls), prints old -> new -> delta for each
metric, and exits 0 when nothing regressed, 1 on a regression, 2 when there is no baseline.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[2]
BASELINE = SKILL_DIR / "references" / "baseline.json"

# Metric name -> direction of improvement: +1 means higher is better, -1 means lower is better.
METRICS: dict[str, int] = {
    "recall_found": +1,
    "recall_total": 0,
    "superseded_above_current": -1,
    "in_scope_min_top_score": +1,
    "out_of_scope_max_top_score": -1,
    "score_gap": +1,
    "grounded": +1,
    "answers": 0,
}
# A change in any of these fails the run (exit 1).
GATED = {"recall_found": +1, "superseded_above_current": -1, "grounded": +1}


def run_eval(mode: str) -> dict:
    result = subprocess.run(
        [sys.executable, "eval/eval.py", mode, "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if result.returncode != 0:
        sys.exit(f"eval/eval.py {mode} failed (exit {result.returncode}):\n{result.stderr.strip()}")
    return json.loads(result.stdout)


def current_results() -> dict:
    retrieval = run_eval("--retrieval-only")
    recorded = run_eval("--recorded")
    return {
        "recall_found": retrieval["recall_found"],
        "recall_total": retrieval["recall_total"],
        "superseded_above_current": retrieval["superseded_above_current"],
        "in_scope_min_top_score": retrieval["in_scope_min_top_score"],
        "out_of_scope_max_top_score": retrieval["out_of_scope_max_top_score"],
        "score_gap": round(retrieval["in_scope_min_top_score"] - retrieval["out_of_scope_max_top_score"], 4),
        "grounded": recorded["grounded"],
        "answers": recorded["answers"],
        "not_grounded_ids": sorted(recorded["not_grounded_ids"]),
    }


def format_delta(old: float, new: float) -> str:
    delta = new - old
    return f"{delta:+.4f}" if isinstance(delta, float) and not float(delta).is_integer() else f"{int(delta):+d}"


def compare(baseline: dict, current: dict) -> int:
    regressions: list[str] = []
    for name, direction in METRICS.items():
        old, new = baseline.get(name), current[name]
        if old is None:
            print(f"{name:<28} {'(new)':>8} -> {new}")
            continue
        print(f"{name:<28} {old!s:>8} -> {new!s:<8} ({format_delta(old, new)})")
        if name in GATED and (new - old) * GATED[name] < 0:
            regressions.append(f"{name} {old} -> {new}")

    newly_ungrounded = sorted(set(current["not_grounded_ids"]) - set(baseline.get("not_grounded_ids", [])))
    newly_grounded = sorted(set(baseline.get("not_grounded_ids", [])) - set(current["not_grounded_ids"]))
    if newly_ungrounded:
        print(f"newly NOT grounded: {', '.join(newly_ungrounded)}")
    if newly_grounded:
        print(f"newly grounded:     {', '.join(newly_grounded)}")

    if regressions:
        print("REGRESSION: " + "; ".join(regressions))
        return 1
    print("OK: no regression")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--save-baseline", action="store_true", help="Record the current results as the baseline.")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    current = current_results()
    if args.save_baseline:
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps(current, indent=1) + "\n", encoding="utf-8")
        print(f"Saved baseline to {BASELINE.relative_to(REPO_ROOT).as_posix()}")
        for name in METRICS:
            print(f"{name:<28} {current[name]}")
        sys.exit(0)

    if not BASELINE.exists():
        print(f"No baseline at {BASELINE.relative_to(REPO_ROOT).as_posix()}. "
              "Run with --save-baseline once the current results are known to be good.")
        sys.exit(2)

    sys.exit(compare(json.loads(BASELINE.read_text(encoding="utf-8")), current))


if __name__ == "__main__":
    main()
