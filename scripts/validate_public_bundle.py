"""Validate the complete public Skill bundle without network or dependencies."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FORBIDDEN_PARTS = {
    ".venv", "__pycache__", "node_modules", "data", "uploads", "reports", "artifacts",
    "frontend", "src", "config", "policies", "static", "tests",
}
FORBIDDEN_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".key", ".pem", ".p12", ".pyc", ".pyo"}
REQUIRED_FILES = {
    "SKILL.md",
    "README.md",
    "LICENSE",
    "VERSION.json",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "PROVENANCE.md",
    ".gitignore",
    ".github/workflows/validate.yml",
    "examples/synthetic-ledger.csv",
    "examples/synthetic-policy.md",
    "examples/expected-review-report.md",
    "evals/prompts.csv",
    "evals/rubric.md",
    "scripts/run_governance_case.py",
    "scripts/run_examples.py",
    "scripts/build_skill_zip.py",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def check_links(root: Path) -> None:
    markdown = list(root.rglob("*.md"))
    for source in markdown:
        text = source.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if link.startswith(("http://", "https://", "#")):
                continue
            target = (source.parent / link.split("#", 1)[0]).resolve()
            if not target.is_file():
                fail(f"broken local reference: {source.relative_to(root)} -> {link}")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    missing = sorted(path for path in REQUIRED_FILES if not (root / path).is_file())
    if missing:
        fail(f"missing required files: {', '.join(missing)}")

    skills = [path for path in root.rglob("*") if path.is_file() and path.name.lower() == "skill.md"]
    if len(skills) != 1 or skills[0] != root / "SKILL.md":
        fail("bundle must contain exactly one root SKILL.md")

    text = (root / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    match = re.match(r"^---\nname:\s*([^\n]+)\ndescription:\s*(.+)\n---\n", text, re.S)
    if not match:
        fail("frontmatter must contain name and description")
    name, description = match.group(1).strip(), match.group(2).strip()
    if not NAME_RE.fullmatch(name) or len(name) > 64:
        fail(f"invalid skill name: {name}")
    if not description or len(description) > 1024:
        fail("description must be non-empty and at most 1024 characters")
    if len(text.splitlines()) > 500:
        fail("SKILL.md exceeds 500 lines")

    version = json.loads((root / "VERSION.json").read_text(encoding="utf-8"))
    if version.get("skill_name") != name or not re.fullmatch(r"\d+\.\d+\.\d+", version.get("version", "")):
        fail("VERSION.json must contain the root skill name and semantic version")
    workflow = (root / ".github/workflows/validate.yml").read_text(encoding="utf-8")
    for command in ("validate_public_bundle.py", "run_examples.py", "run_governance_case.py", "build_skill_zip.py"):
        if command not in workflow:
            fail(f"CI workflow is missing command: {command}")

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if ".git" in rel.parts:
            continue
        if any(part in FORBIDDEN_PARTS for part in rel.parts) or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(f"forbidden file in bundle: {rel}")
        if path.name.lower() in {".env", "credentials.json", "secrets.json"}:
            fail(f"secret-like file in bundle: {rel}")
        if path.name == "validate_public_bundle.py":
            continue
        if path.suffix.lower() in {".md", ".csv", ".py", ".yaml", ".yml", ".json"}:
            content = path.read_text(encoding="utf-8", errors="strict")
            if "BEGIN PRIVATE KEY" in content or re.search(r"\bsk-[A-Za-z0-9]{20,}\b", content):
                fail(f"secret pattern in bundle: {rel}")

    with (root / "evals/prompts.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 10 or not {"id", "should_trigger", "prompt"} <= set(rows[0] if rows else {}):
        fail("evals/prompts.csv must contain at least 10 cases with id, should_trigger, and prompt")
    if not any(row["should_trigger"].lower() == "false" for row in rows):
        fail("evals/prompts.csv needs a negative control")

    check_links(root)
    print(f"OK: {name}; files={sum(1 for path in root.rglob('*') if path.is_file() and '.git' not in path.relative_to(root).parts)}; evals={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



