"""Validate the Copilot customization artifacts under .github/ so broken ones fail loudly.

    python scripts/validate_artifacts.py

Checks every *.agent.md, *.prompt.md, *.instructions.md, and SKILL.md under .github/:

* the frontmatter parses with yaml.safe_load;
* required fields are present: description for agents, prompts, and instructions; name and
  description for skills, with name matching the folder and ^[a-z][a-z0-9-]*$;
* every name in an agent's agents: list resolves to the name of an existing agent;
* every applyTo glob matches at least one file in the repository;
* an agent whose description says "read-only" lists no edit/ or execute/ tools.

Prints one line per failure and exits 1 if any check fails.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
GITHUB_DIR = REPO_ROOT / ".github"
SKILL_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
IGNORED_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".copilot-tracking"}


def kind_of(path: Path) -> str | None:
    name = path.name
    if name.endswith(".agent.md"):
        return "agent"
    if name.endswith(".prompt.md"):
        return "prompt"
    if name.endswith(".instructions.md"):
        return "instructions"
    if name == "SKILL.md":
        return "skill"
    return None


def read_frontmatter(path: Path) -> dict:
    """Return the parsed frontmatter, or raise ValueError with a readable reason."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("no frontmatter: the file must start with a '---' line")
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        raise ValueError("frontmatter is not closed with a '---' line") from None
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        where = f" (frontmatter line {mark.line + 1}, column {mark.column + 1})" if mark else ""
        problem = getattr(exc, "problem", None) or str(exc).splitlines()[0]
        raise ValueError(f"YAML error{where}: {problem}") from None
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping of key: value fields")
    return data


def as_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    return [str(item) for item in value]


def glob_matches(pattern: str) -> bool:
    pattern = pattern.strip().lstrip("/")
    for match in REPO_ROOT.glob(pattern):
        if match.is_file() and not IGNORED_DIRS.intersection(match.relative_to(REPO_ROOT).parts):
            return True
    return False


def validate() -> tuple[int, list[str]]:
    artifacts = sorted(p for p in GITHUB_DIR.rglob("*.md") if kind_of(p))
    failures: list[str] = []
    parsed: dict[Path, dict] = {}

    for path in artifacts:
        rel = path.relative_to(REPO_ROOT).as_posix()
        try:
            parsed[path] = read_frontmatter(path)
        except ValueError as exc:
            failures.append(f"{rel}: {exc}")

    agent_names = {str(fm.get("name")) for p, fm in parsed.items() if kind_of(p) == "agent" and fm.get("name")}

    for path, fm in parsed.items():
        rel = path.relative_to(REPO_ROOT).as_posix()
        kind = kind_of(path)
        description = fm.get("description")
        if not isinstance(description, str) or not description.strip():
            failures.append(f"{rel}: missing required field 'description'")
            description = ""

        if kind == "skill":
            name = fm.get("name")
            folder = path.parent.name
            if not isinstance(name, str) or not name:
                failures.append(f"{rel}: missing required field 'name'")
            else:
                if not SKILL_NAME_RE.match(name):
                    failures.append(f"{rel}: skill name '{name}' must match ^[a-z][a-z0-9-]*$")
                if name != folder:
                    failures.append(f"{rel}: skill name '{name}' does not match its folder '{folder}'")

        if kind == "agent":
            for target in as_list(fm.get("agents")):
                if target not in agent_names:
                    failures.append(f"{rel}: agents: entry '{target}' does not match the name of any agent "
                                    f"(known: {', '.join(sorted(agent_names))})")
            if "read-only" in description.lower():
                bad = [t for t in as_list(fm.get("tools")) if t.startswith(("edit/", "execute/"))]
                if bad:
                    failures.append(f"{rel}: description says read-only but tools include {', '.join(bad)}")

        if "applyTo" in fm:
            for pattern in as_list(fm.get("applyTo")):
                if not glob_matches(pattern):
                    failures.append(f"{rel}: applyTo glob '{pattern}' matches no file in the repository")

    return len(artifacts), failures


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    count, failures = validate()
    for failure in failures:
        print(f"FAIL {failure}")
    print(f"checked {count} artifacts: {len(failures)} failure{'' if len(failures) == 1 else 's'}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
