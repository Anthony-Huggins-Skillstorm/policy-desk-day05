"""Embedding client. Keyless: the token comes from your az login, never an API key."""

from __future__ import annotations

from typing import Protocol

import numpy as np
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
from openai import AsyncAzureOpenAI

from policy_desk.settings import Settings

_SCOPE = "https://cognitiveservices.azure.com/.default"
_BATCH = 64


class Embedder(Protocol):
    async def embed(self, texts: list[str]) -> np.ndarray: ...


class AzureEmbedder:
    """Embeds text with the Foundry resource's embedding deployment."""

    def __init__(self, settings: Settings) -> None:
        self._credential = DefaultAzureCredential()
        self._client = AsyncAzureOpenAI(
            azure_endpoint=settings.aoai_endpoint,
            azure_ad_token_provider=get_bearer_token_provider(self._credential, _SCOPE),
            api_version="2024-10-21",
            timeout=30.0,
            max_retries=3,
        )
        self._deployment = settings.embedding_deployment

    async def embed(self, texts: list[str]) -> np.ndarray:
        vectors: list[list[float]] = []
        for start in range(0, len(texts), _BATCH):
            response = await self._client.embeddings.create(
                model=self._deployment, input=texts[start : start + _BATCH]
            )
            vectors.extend(item.embedding for item in response.data)
        return np.asarray(vectors, dtype=np.float32)

    async def close(self) -> None:
        await self._client.close()
        await self._credential.close()
