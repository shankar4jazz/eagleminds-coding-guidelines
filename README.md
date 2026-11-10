# EagleMinds Coding Guidelines for AI Coding Agents

**A CLAUDE.md, Claude Code skill, Cursor rule, and AGENTS.md that stop LLM coding agents from guessing, overbuilding, touching code they shouldn't, and saying "done" without running anything.** Built from how LLM coding agents fail in practice, turned into rules an agent can follow mid-task, and tested with and without.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/shankar4jazz/eagleminds-coding-guidelines?style=flat)](https://github.com/shankar4jazz/eagleminds-coding-guidelines/stargazers)
[![Sync check](https://github.com/shankar4jazz/eagleminds-coding-guidelines/actions/workflows/sync-check.yml/badge.svg)](https://github.com/shankar4jazz/eagleminds-coding-guidelines/actions/workflows/sync-check.yml)

Works with **Claude Code**, **Cursor**, **OpenAI Codex**, **GitHub Copilot**, **Gemini CLI**, **OpenCode**, **Amp**, and any agent that reads `AGENTS.md`.

English | [简体中文](./README.zh.md)

- [Quick install](#quick-install)
- [What problem does this solve?](#what-problem-does-this-solve)
- [The five rules](#the-five-rules)
- [Does it actually work?](#does-it-actually-work)
- [Which tools are supported?](#which-tools-are-supported)
- [FAQ](#faq)
- [License](#license)

## Quick install

**Claude Code plugin** (adds the `eagleminds-guidelines` skill and the `/eagleminds-review` command to every project):

```
/plugin marketplace add shankar4jazz/eagleminds-coding-guidelines
/plugin install eagleminds-guidelines@eagleminds-coding-guidelines
```

**CLAUDE.md** (per project, for Claude Code):

```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/shankar4jazz/eagleminds-coding-guidelines/main/CLAUDE.md
```

**AGENTS.md** (per project, for Codex, OpenCode, Gemini CLI, Amp, Devin, Jules, and others):

```bash
curl -o AGENTS.md https://raw.githubusercontent.com/shankar4jazz/eagleminds-coding-guidelines/main/AGENTS.md
```

**Cursor** (project rule, always applied):

```bash
mkdir -p .cursor/rules && curl -o .cursor/rules/eagleminds-guidelines.mdc https://raw.githubusercontent.com/shankar4jazz/eagleminds-coding-guidelines/main/.cursor/rules/eagleminds-guidelines.mdc
```

**GitHub Copilot** (repository instructions):

```bash
mkdir -p .github && curl -o .github/copilot-instructions.md https://raw.githubusercontent.com/shankar4jazz/eagleminds-coding-guidelines/main/.github/copilot-instructions.md
```

Already have one of these files? Append instead of overwrite (`curl ... >> CLAUDE.md`). The rules are written to sit alongside project-specific instructions.

## What problem does this solve?

LLM coding agents fail in a few predictable ways:

- **They guess.** Faced with an ambiguous request, they pick a reading, never say which one, and build on it. They don't surface the inconsistency, don't present the tradeoff, and don't push back when the request looks like a mistake.
- **They overbuild.** A helper grows a config object, an interface, and three options nobody asked for. 1000 lines land where 100 would do, and the dead code stays.
- **They touch what they don't understand.** A comment gets rewritten, a `sleep()` gets removed, imports get reordered, all as side effects of an unrelated task.
- **They declare victory early.** "Fixed, should work now" on code that was never run, or tests that pass without meeting the requirement.

And one thing they do well: given a concrete success criterion, they loop against it until it passes. Don't tell them how; tell them what "done" looks like.

Naming a failure doesn't stop an agent from committing it. What stops it is a rule it can apply at the moment of temptation: a threshold for when to ask, a list of smells to spot in its own draft, a loop that starts with a failing check, and a reporting standard that makes "should work" unsayable. That's what this repository contains.

## The five rules

| Rule | What it prevents |
|---|---|
| **Calibrate first** | Full ceremony on a typo fix, or none on a schema change |
| **1. Understand before you build** | Silent wrong assumptions, and the opposite failure: interrogating the user instead of reading the code |
| **2. Build the minimum** | Speculative abstractions, options nobody asked for, 1000 lines where 100 would do |
| **3. Change only what the task needs** | Drive-by reformatting, renames, and deleting code the agent doesn't understand |
| **4. Define done, then loop** | "Fixed" without reproducing, tests that pass without meeting the requirement |
| **5. Report what you verified** | "Done, should work now" when nothing was run |

**Calibrate first.** An obvious one-liner gets no ceremony. A standard change gets a one-line assumption, a check, and a short report. Anything ambiguous, large, or hard to undo gets code reading, a plan with a check per step, and tradeoffs surfaced before coding.

**Understand before you build.** Look, decide, then say. Read the code before asking; most assumptions are answerable from the repo. Restate the task in one sentence. Ask only when the readings lead to materially different work or the action is hard to reverse, otherwise state the assumption and proceed. When you ask, ask one question and recommend an answer. Flag contradictions. Disagree out loud, then defer if the user reaffirms.

**Build the minimum.** Solve today's problem, with a list of overcomplication smells (options nobody passes, single-implementation interfaces, `try/except` around code that can't fail, reimplemented stdlib, narrating comments) so the agent recognizes them in its own draft. Simple does not mean thin: reuse existing helpers, keep boundary validation and security checks.

**Change only what the task needs.** Every changed hunk traces to the request. No reformatting, renaming, type hints, docstrings, or dependency bumps as side effects. Follow the file's style; if the style is harmful, say so rather than copy or silently fix it. Re-read the diff before reporting.

**Define done, then loop.** Turn the task into a check, run it and watch it fail, make the change, run it again. No harness? Use the cheapest signal available. The same failure three times means stop and report. Passing tests are not the same as meeting the requirement.

**Report what you verified.** "Tests pass" means you ran them. Separate verified from believed from skipped. Quote failures verbatim. If you stopped short, say so first. Keep it short.

The full text is [`skills/eagleminds-guidelines/SKILL.md`](skills/eagleminds-guidelines/SKILL.md), about 140 lines. Before/after examples for every rule are in [`references/examples.md`](skills/eagleminds-guidelines/references/examples.md). A diff reviewer that checks a change against the rules is [`skills/eagleminds-review/SKILL.md`](skills/eagleminds-review/SKILL.md).

## Does it actually work?

Short answer: the model already writes correct code either way. The guidelines change what else lands in the diff, and whether the agent moves or stalls when the request is vague.

Three tasks on a small pytest project, each run once with the guidelines and once without, in isolated copies of the repo:

| Task | Without guidelines | With guidelines |
|---|---|---|
| Fix a crash on a missing email | Correct fix. Also rewrote an existing comment, and the new test and the fix landed together, so the test was never seen failing. 14 lines added. | Same fix, comment untouched, test run and seen failing before the change. 8 lines added. |
| Add retry to a network call | Correct, but grew two keyword parameters nobody calls, a classification helper, and exponential backoff. 73 lines added. | Fixed 3 attempts with a 1s pause, two tests, failing run first. 50 lines added. |
| "We need to be able to export users", with the user unavailable | Stopped with a four-question questionnaire. No code. | Read the code, added an `export` CLI command next to the existing `list`, excluded the password hash, stated the assumptions, verified. |

Both runs used the same model and the same prompts. One run per task, so treat the numbers as directional. The one cost that showed up: reports with the guidelines were about a third longer. Rule 5 now says to keep them short.

## Which tools are supported?

| Tool | File it reads | How to install |
|---|---|---|
| Claude Code | plugin skill, or `CLAUDE.md` | `/plugin marketplace add shankar4jazz/eagleminds-coding-guidelines` |
| Cursor | `.cursor/rules/eagleminds-guidelines.mdc` | copy the rule file |
| OpenAI Codex | `AGENTS.md` | copy `AGENTS.md` |
| OpenCode, Gemini CLI, Amp, Devin, Jules, Kiro | `AGENTS.md` | copy `AGENTS.md` |
| GitHub Copilot | `.github/copilot-instructions.md` | copy the file |
| Anything else with a system prompt | any of the above | paste the body of `CLAUDE.md` |

All four files are generated from the same source by `scripts/sync_guidelines.py`, so they always say the same thing. CI fails if they drift.

## FAQ

**What is a CLAUDE.md file?**
A Markdown file at the root of a repository that Claude Code reads at the start of every session as standing instructions. This repo's `CLAUDE.md` contains the rules and nothing else, so it can be appended to an existing one.

**What is AGENTS.md?**
The cross-tool equivalent of CLAUDE.md, read by OpenAI Codex, OpenCode, Gemini CLI, Amp, Devin, Jules, and others. Same content here, different filename.

**Who is behind this?**
EagleMinds, by [Shankar Venkat](https://github.com/shankar4jazz). The rules, examples, tooling, and tests are original work, released under MIT so you can adapt them freely.

**Will it slow the agent down on small tasks?**
It's designed not to. The first section is a calibration table that tells the agent to skip the ceremony for obvious one-liners.

**Why a rule about reporting?**
Because the most expensive agent failure isn't bad code, it's a confident "done" on code that was never run. The other four rules don't catch that; the fifth does.

**Can I add my own project rules?**
Yes. Append a `## Project-Specific Guidelines` section to the same file with your stack conventions. The rules are deliberately stack-agnostic.

**How do I keep the copies in sync if I edit the skill?**
Edit `skills/eagleminds-guidelines/SKILL.md`, run `python scripts/sync_guidelines.py`. CI fails if any generated file is stale. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT, by EagleMinds ([Shankar Venkat](https://github.com/shankar4jazz)). See [LICENSE](LICENSE). To cite, use the "Cite this repository" button on GitHub or [CITATION.cff](CITATION.cff).
