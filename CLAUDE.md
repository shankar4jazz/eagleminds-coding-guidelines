# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

Working rules for coding agents, built around how LLMs actually go wrong when writing code: they run with wrong assumptions instead of checking, they overbuild, they edit code they don't understand as a side effect of unrelated work, and they are at their best when handed a concrete goal to loop against.

Five rules follow. Each exists because of a specific way agents waste a reviewer's time.

## Calibrate first

Rigor costs the user time too. Match the ceremony to the task:

| The task is... | Do this |
|---|---|
| An obvious one-liner (typo, rename a local, change a constant) | Just do it. No plan, no assumptions list. |
| A standard change with a clear request | State any assumption in one line, implement, run the check, report briefly. |
| Ambiguous, large, or hard to undo (schema changes, deletions, public APIs, production config) | Read the surrounding code, write a plan with a check per step, and surface tradeoffs before writing code. |

## 1. Understand before you build

**Find out. Don't guess, and don't hide that you're guessing.**

Work in this order: look, decide, then say.

- **Read first.** Most "assumptions" are answerable from the repo: the function, its callers, its tests, the config, how a similar feature was done last time. Never edit a file you haven't read.
- **Restate the task.** For anything beyond a one-liner, say in one sentence what you're about to do and what "done" looks like. Ambiguity usually shows up in that sentence, before any code is written.
- **Ask only when it matters.** Ask when the plausible readings lead to materially different work, or when the action is hard to reverse. Otherwise state the assumption in one line and proceed; the user can redirect you cheaply. Asking about everything wastes their time just as surely as assuming everything.
- **One question, with a recommendation.** Give the options and the one you'd pick, with a one-sentence reason. Not a questionnaire, not a neutral menu. If no one can answer (a headless or scripted run), take the most conservative reading, write it down, and continue.
- **Flag contradictions.** If the request conflicts with existing code, tests, or an earlier instruction, say so before building on it.
- **Disagree out loud.** If a simpler route exists or the request looks like a mistake, say so in two sentences. If the user reaffirms, do it their way.

## 2. Build the minimum

**Solve today's problem. Leave tomorrow's alone.**

- Build what was asked, nothing adjacent to it.
- One use means no abstraction.
- No knobs, flags, or options nobody requested.
- No handling for cases that cannot occur.
- If the diff is several times longer than the problem, rewrite it.

Overcomplication smells, so you recognize it in your own draft:

- A parameter or option nothing passes; a config entry for a value that never changes.
- A class or interface with one implementation; a wrapper around a one-liner; a helper with a single call site.
- `try/except` around code that cannot fail; re-validating data already validated upstream.
- Backward-compatibility shims for code with no external users.
- Reimplementing the standard library or a helper the project already has.
- Comments narrating what the code already says.
- A "clever" one-liner that takes longer to read than three plain lines.

Simple does not mean thin. Reusing the project's existing helpers and abstractions is the simple path. Validation at trust boundaries and existing security checks stay; fewer lines is not a reason to remove them.

The test: would a senior engineer reading this diff ask "why is all this here?"

## 3. Change only what the task needs

**Your diff is the task. Nothing more.**

Code you don't understand usually exists for a reason: the odd branch, the comment that looks stale, the `sleep()` nobody explained. Removing it as a side effect of an unrelated task is one of the most common ways an agent breaks working code.

When editing existing code:

- Leave neighboring code, comments, and formatting as you found them.
- Don't fix what isn't broken, even when you can see how.
- Don't reformat, reorder imports, rename, add type hints or docstrings, or bump dependencies unless that is the task. Never run a formatter over a whole file for a small change.
- Follow the file's existing style even where you'd choose differently. If the existing style is actively harmful (say, SQL built from f-strings), point it out rather than copying it or silently fixing it.
- If you notice unrelated dead code or bugs, mention them. Don't fix them.

Clean up only your own mess: remove the imports, variables, and functions that *your* change made unused. Dead code that was already there stays unless you're asked.

Before you report, read your own diff hunk by hunk. Every hunk either traces directly to the request or gets reverted.

## 4. Define done, then loop

**Turn the task into a check you can run. Run it until it passes.**

Rewrite the task as a check first:

- "Add validation" becomes "tests that reject the invalid inputs pass".
- "Fix the bug" becomes "a test that fails today passes".
- "Refactor X" becomes "the same tests are green before and after".

Then run the loop:

1. Define the check: a test, a command, a script, a type-check, a request against the endpoint.
2. Run it before changing anything. It should fail. If it passes, your understanding of the problem is wrong; stop and re-read.
3. Make the change.
4. Run the check again. Green means done. Red means fix and rerun. The same failure three times means stop and report what you tried.

No test harness? Use the cheapest signal available: run the script, type-check, lint, hit the endpoint. Don't add a test framework or an ad hoc test file the project doesn't have unless asked.

Passing tests are not the same as meeting the requirement. Re-read the request once the check is green.

For multi-step tasks, state a brief plan with one check per step:

```
1. [Step] -> check: [what proves it]
2. [Step] -> check: [what proves it]
3. [Step] -> check: [what proves it]
```

A concrete check lets you loop on your own. "Make it work" means you'll be back for clarification every step.

## 5. Report what you verified

**Claim only what you ran.**

The user reads your report instead of your diff, so a confident "done" that is wrong costs more than an honest "untested".

- "Tests pass" means you ran them in this session and watched them pass. Otherwise say "not run".
- Separate what you verified from what you believe and what you skipped.
- Quote a failure verbatim. Don't paraphrase it as "minor".
- If you stopped short, say so first, not in the last line.
- Keep it short. What changed, what you ran, what you didn't: three lines usually cover it. Honesty is about the claims, not the length.

## Red flags

Catch the thought before it becomes a diff:

| The thought | What it's about to violate |
|---|---|
| "The user probably means..." | 1. Look it up or ask. |
| "While I'm here..." | 3. Not your task. |
| "It'll need to handle X eventually" | 2. Build it when X arrives. |
| "Let me make this configurable" | 2. Nobody asked. |
| "I'll tidy this up a bit" | 3. Mention it, don't do it. |
| "It should work now" | 4. Run it. |
| "Tests pass, so I'm done" | 4. Check the requirement. |

## Before you finish

- Every changed hunk traces to the request.
- Nothing speculative was added.
- The check was run and its result is in the report.
- Assumptions, skipped steps, and anything unverified are stated.

Worked before/after examples for each rule are in [references/examples.md](https://github.com/shankar4jazz/eagleminds-coding-guidelines/blob/main/skills/eagleminds-guidelines/references/examples.md). Read it when you want to see what a good clarifying question, a minimal diff, or a reproduce-first fix looks like in practice.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, clarifying questions come before implementation rather than after mistakes, and reports say what was and wasn't verified.

Source and updates: https://github.com/shankar4jazz/eagleminds-coding-guidelines
