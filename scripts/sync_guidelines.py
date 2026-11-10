#!/usr/bin/env python3
"""Generate every per-tool copy of the guidelines from the skill.

skills/eagleminds-guidelines/SKILL.md is the single source of truth. This writes:

  CLAUDE.md                              Claude Code project instructions
  AGENTS.md                              Codex, OpenCode, Gemini CLI, Amp, Devin, Kiro, Jules
  .cursor/rules/eagleminds-guidelines.mdc  Cursor project rule (alwaysApply)
  .github/copilot-instructions.md        GitHub Copilot

Run it after editing SKILL.md. `--check` exits non-zero if any copy is stale (CI).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "eagleminds-guidelines" / "SKILL.md"
REPO_URL = "https://github.com/shankar4jazz/eagleminds-coding-guidelines"
EXAMPLES_URL = f"{REPO_URL}/blob/main/skills/eagleminds-guidelines/references/examples.md"
INTRO = (
    "Behavioral guidelines to reduce common LLM coding mistakes. "
    "Merge with project-specific instructions as needed.\n"
)
FOOTER = (
    "---\n\n**These guidelines are working if:** fewer unnecessary changes in diffs, "
    "fewer rewrites due to overcomplication, clarifying questions come before "
    "implementation rather than after mistakes, and reports say what was and "
    "wasn't verified.\n\n"
    f"Source and updates: {REPO_URL}\n"
)


def split_skill(text):
    _, frontmatter, body = text.split("---", 2)
    description = re.search(r"^description: (.*)$", frontmatter, re.M).group(1)
    body = body.lstrip("\n").split("\n", 1)[1]  # drop the "# EagleMinds Coding Guidelines" heading
    body = body.replace("(references/examples.md)", f"({EXAMPLES_URL})")
    return description, body.strip() + "\n"


def render(skill_text):
    description, body = split_skill(skill_text)
    plain = f"{INTRO}\n{body}\n{FOOTER}"
    return {
        ROOT / "CLAUDE.md": f"# CLAUDE.md\n\n{plain}",
        ROOT / "AGENTS.md": f"# AGENTS.md\n\n{plain}",
        ROOT / ".github" / "copilot-instructions.md": f"# Copilot instructions\n\n{plain}",
        ROOT / ".cursor" / "rules" / "eagleminds-guidelines.mdc": (
            f"---\ndescription: {description}\nalwaysApply: true\n---\n\n"
            f"# EagleMinds coding guidelines\n\n{plain}"
        ),
    }


def main():
    outputs = render(SKILL.read_text(encoding="utf-8"))
    if "--check" in sys.argv:
        stale = [
            p for p, c in outputs.items()
            if not p.exists() or p.read_text(encoding="utf-8") != c
        ]
        for p in stale:
            print(f"out of date: {p.relative_to(ROOT)}")
        return 1 if stale else 0
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
