"""Runtime settings, read once from the environment (or a .env file)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
CORPUS_DIR = PACKAGE_ROOT / "corpus"
INDEX_DIR = PACKAGE_ROOT / "index"


@dataclass(frozen=True)
class Settings:
    project_endpoint: str
    model_deployment: str
    aoai_endpoint: str
    embedding_deployment: str

    @classmethod
    def from_env(cls) -> Settings:
        load_dotenv()
        missing = [
            name
            for name in ("PROJECT_ENDPOINT", "MODEL_DEPLOYMENT", "AOAI_ENDPOINT", "EMBEDDING_DEPLOYMENT")
            if not os.environ.get(name)
        ]
        if missing:
            raise RuntimeError(f"Missing environment variables: {', '.join(missing)}. Copy .env.example to .env.")
        return cls(
            project_endpoint=os.environ["PROJECT_ENDPOINT"],
            model_deployment=os.environ["MODEL_DEPLOYMENT"],
            aoai_endpoint=os.environ["AOAI_ENDPOINT"],
            embedding_deployment=os.environ["EMBEDDING_DEPLOYMENT"],
        )
