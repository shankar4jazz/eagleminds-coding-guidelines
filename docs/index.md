---
layout: default
title: EagleMinds Coding Guidelines for AI Coding Agents
description: Drop-in CLAUDE.md, AGENTS.md, Cursor rule, Claude Code skill and Copilot instructions built from how LLM coding agents fail in practice. Five rules, worked examples, tested with and without.
---

# EagleMinds Coding Guidelines for AI Coding Agents

Working rules that make LLM coding agents assume less, build less, touch less, and verify more. Built from how LLM coding agents fail in practice, and tested with and without.

**Five rules:** understand before you build, build the minimum, change only what the task needs, define done then loop, report what you verified. Plus a calibration table so trivial tasks skip the ceremony.

**Works with:** Claude Code, Cursor, OpenAI Codex, GitHub Copilot, Gemini CLI, OpenCode, Amp, and any agent that reads `AGENTS.md`.

## Install in 10 seconds

Claude Code plugin:

```
/plugin marketplace add shankar4jazz/eagleminds-coding-guidelines
/plugin install eagleminds-guidelines@eagleminds-coding-guidelines
```

Any other tool: copy the matching file from the repository into your project.

| Tool | File |
|---|---|
| Claude Code | [CLAUDE.md](https://raw.githubusercontent.com/shankar4jazz/eagleminds-coding-guidelines/main/CLAUDE.md) |
| Codex, OpenCode, Gemini CLI, Amp, Devin, Jules | [AGENTS.md](https://raw.githubusercontent.com/shankar4jazz/eagleminds-coding-guidelines/main/AGENTS.md) |
| Cursor | [.cursor/rules/eagleminds-guidelines.mdc](https://raw.githubusercontent.com/shankar4jazz/eagleminds-coding-guidelines/main/.cursor/rules/eagleminds-guidelines.mdc) |
| GitHub Copilot | [.github/copilot-instructions.md](https://raw.githubusercontent.com/shankar4jazz/eagleminds-coding-guidelines/main/.github/copilot-instructions.md) |

## Read more

- [Full README: the five rules, with-vs-without results, FAQ](https://github.com/shankar4jazz/eagleminds-coding-guidelines#readme)
- [The guidelines themselves (SKILL.md)](https://github.com/shankar4jazz/eagleminds-coding-guidelines/blob/main/skills/eagleminds-guidelines/SKILL.md)
- [Before/after examples](https://github.com/shankar4jazz/eagleminds-coding-guidelines/blob/main/skills/eagleminds-guidelines/references/examples.md)

MIT licensed, by EagleMinds.
