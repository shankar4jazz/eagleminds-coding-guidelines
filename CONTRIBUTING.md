# Contributing

The guidelines live in one file: `skills/eagleminds-guidelines/SKILL.md`. Everything else that repeats them (`CLAUDE.md`, `AGENTS.md`, the Cursor rule, the Copilot instructions) is generated.

1. Edit `skills/eagleminds-guidelines/SKILL.md` (or `references/examples.md`, or `skills/eagleminds-review/SKILL.md`).
2. Run `python scripts/sync_guidelines.py`.
3. Commit the source and the regenerated files together. CI rejects PRs where they disagree.

What gets merged:

- Fixes to examples that don't demonstrate what they claim.
- Guidance backed by a transcript or a before/after run showing the failure it prevents. Say what you observed.
- Shorter wording that keeps the meaning.

What doesn't:

- New principles without evidence of a failure the existing five miss.
- Tool-specific files that duplicate the generated ones. Add a generator target to `scripts/sync_guidelines.py` instead.
- README translations that aren't kept in sync with `README.md` (the Chinese one is maintained; others are welcome if you commit to updating them).

Apply the guidelines to your own PR: one change per PR, every hunk traceable to the PR title, and say what you ran.
