---
description: "Microsoft Agent Framework 1.15 and Python conventions for policy-desk"
applyTo: '**/*.py'
---

# Agent Framework 1.15 and Python conventions

## Agent Framework

- Import from `agent_framework`: `Agent`, `tool`, `AgentResponse`, `AgentSession`, `function_middleware`, `FunctionInvocationContext`, `MiddlewareTermination`, `Content`. The chat client is `agent_framework.foundry.FoundryChatClient`.
- Do not use names from earlier releases: `ChatAgent`, `ai_function`, `AgentThread`, `AgentRunResponse` no longer exist and fail at import.
- Define tools with `@tool(name=..., approval_mode="never_require")` and `Annotated[..., Field(description=...)]` parameters. A tool returns a string (JSON for structured results).
- Use the async credential from `azure.identity.aio` with `FoundryChatClient`, and close it (`async with`).

## Python

- Python 3.11+, type hints on every public function, `from __future__ import annotations` at the top of each module.
- I/O is async. Do not call `asyncio.run` inside library code; only entry points (`cli.py`, `eval.py`) and tests do.
- Log with the standard `logging` module using structured events (`logger.info("retrieval.completed", extra={...})`). Never log a user's question verbatim; log a SHA-256 hash.
- Tests are synchronous `def` functions named as full sentences, edge cases first, happy path last.
