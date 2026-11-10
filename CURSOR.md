# Using the guidelines in Cursor

## In this repository

The rule at [`.cursor/rules/eagleminds-guidelines.mdc`](.cursor/rules/eagleminds-guidelines.mdc) is committed with `alwaysApply: true`. Open the folder in Cursor and it is active; it shows up under **Settings → Rules** as `eagleminds-guidelines`.

## In your own project

Copy `.cursor/rules/eagleminds-guidelines.mdc` into your project's `.cursor/rules/` directory (create it if needed). Merge with any rules you already have.

For tools that only read a root instruction file, copy [`AGENTS.md`](AGENTS.md) (Codex, OpenCode, Gemini CLI, Amp, Devin, Jules) or [`CLAUDE.md`](CLAUDE.md) (Claude Code) instead. All of these files carry the same text.

## For contributors

[`skills/eagleminds-guidelines/SKILL.md`](skills/eagleminds-guidelines/SKILL.md) is the single source of truth. After editing it, run `python scripts/sync_guidelines.py` to regenerate **[`CLAUDE.md`](CLAUDE.md)**, **[`AGENTS.md`](AGENTS.md)**, **[`.cursor/rules/eagleminds-guidelines.mdc`](.cursor/rules/eagleminds-guidelines.mdc)** and **[`.github/copilot-instructions.md`](.github/copilot-instructions.md)**; `--check` reports drift without writing.
