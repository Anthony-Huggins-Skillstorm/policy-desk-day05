---
description: "Test conventions for policy-desk: offline fakes only, sentence-named tests, edge cases first"
applyTo: 'tests/**/*.py'
---

# Test conventions

- Tests never touch the network. Use or extend the fakes in `tests/conftest.py`.
- Test functions are plain synchronous `def` functions. Drive async code with `asyncio.run(...)`.
- Name each test as a full sentence describing the behavior.
- Order cases edge-first, happy path last. Use `pytest.mark.parametrize` when the same assertion runs over many inputs.
