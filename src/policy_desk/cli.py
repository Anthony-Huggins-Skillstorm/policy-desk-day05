"""Ask policy-desk a question from the terminal.

    python -m policy_desk.cli "How often is a Tier 1 vendor reassessed?"
"""

from __future__ import annotations

import argparse
import asyncio
import sys

from policy_desk.agent import ask
from policy_desk.runtime import live_agent


async def _main(questions: list[str]) -> None:
    async with live_agent() as (agent, turn):
        for question in questions:
            answer = await ask(agent, turn, question)
            print(f"Q: {question}\n")
            print(answer.text or "(no answer)")
            print(f"\nretrieved:   {sorted({h.doc_id for h in answer.hits})}")
            print(f"cited:       {answer.citations.cited}")
            print(f"verified:    {answer.citations.verified}")
            print(f"unsupported: {answer.citations.unsupported}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("question", nargs="+", help="One or more questions, each in quotes.")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(_main(args.question))


if __name__ == "__main__":
    main()
