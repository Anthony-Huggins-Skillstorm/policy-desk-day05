"""The grounded policy agent: one retrieval tool, citations verified after every turn."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Annotated

from agent_framework import Agent, tool
from pydantic import Field

from policy_desk.citations import CitationReport, verify_citations
from policy_desk.retriever import Hit, Retriever

INSTRUCTIONS = """\
You answer questions from Northwind Capital Group staff about third-party risk management
and procurement policy.

Rules:
- ALWAYS call search_policies before answering. Never answer from general knowledge.
- Cite every factual claim with the doc_id field of the passage it came from, written as
  [doc_id: <the id>]. The text "doc_id:" is literal. Example: a claim from the Contract
  Renewal Procedure ends with [doc_id: RNW-PRC]. Cite each document separately.
- Prefer documents whose status is Current. Never rely on a SUPERSEDED document unless the
  user asks about the old version, and say so when you do.
- If the retrieved passages do not answer the question, say that the policies do not cover
  it. Do not guess.
- Be brief: answer first, then the supporting detail.
"""

TOP_K = 5


@dataclass
class TurnRecord:
    """What retrieval returned during one turn. Reset before every question."""

    hits: list[Hit] = field(default_factory=list)

    @property
    def retrieved_doc_ids(self) -> set[str]:
        return {h.doc_id for h in self.hits}


@dataclass(frozen=True)
class Answer:
    question: str
    text: str
    citations: CitationReport
    hits: list[Hit]


def build_agent(client, retriever: Retriever, turn: TurnRecord, instructions: str = INSTRUCTIONS) -> Agent:
    """Wire the retrieval tool to this agent's turn record and return the agent."""

    @tool(name="search_policies", approval_mode="never_require")
    async def search_policies(
        query: Annotated[str, Field(description="A search query describing what the user wants to know.")],
    ) -> str:
        """Search Northwind's TPRM and procurement policy documents."""
        hits = await retriever.retrieve(query, k=TOP_K)
        turn.hits.extend(hits)
        return json.dumps(
            [{"doc_id": h.doc_id, "title": h.title, "status": h.status, "section": h.section, "text": h.text}
             for h in hits]
        )

    return Agent(client, instructions=instructions, name="policy-desk", tools=[search_policies])


async def ask(agent: Agent, turn: TurnRecord, question: str) -> Answer:
    turn.hits.clear()
    response = await agent.run(question)
    text = (response.text or "").strip()
    return Answer(
        question=question,
        text=text,
        citations=verify_citations(text, turn.retrieved_doc_ids),
        hits=list(turn.hits),
    )
