"""Build the live agent stack (Foundry chat client + embedder + index) and tear it down."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import AzureCliCredential

from policy_desk.agent import TurnRecord, build_agent
from policy_desk.embeddings import AzureEmbedder
from policy_desk.retriever import Retriever, VectorIndex
from policy_desk.settings import INDEX_DIR, Settings


@asynccontextmanager
async def live_agent(settings: Settings | None = None) -> AsyncIterator[tuple[Agent, TurnRecord]]:
    settings = settings or Settings.from_env()
    embedder = AzureEmbedder(settings)
    retriever = Retriever(VectorIndex.load(INDEX_DIR), embedder)
    turn = TurnRecord()
    async with AzureCliCredential() as credential:
        client = FoundryChatClient(
            project_endpoint=settings.project_endpoint,
            model=settings.model_deployment,
            credential=credential,
        )
        try:
            yield build_agent(client, retriever, turn), turn
        finally:
            await embedder.close()
