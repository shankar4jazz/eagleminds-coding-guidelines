---
name: eagleminds-review
description: Review a diff against the EagleMinds coding guidelines before committing or opening a pull request. Use whenever the user asks to review their changes, check a diff, asks "is this overcomplicated", "did I change too much", "is this ready to commit", or runs /eagleminds-review - and on your own work at the end of any non-trivial coding task. Flags hunks that don't trace to the request, speculative code, drive-by edits, and claims that were never verified.
license: MIT
---

# EagleMinds Review

A diff review that checks the five EagleMinds guidelines instead of general code quality: did the change stay inside the request, stay simple, stay surgical, get verified, and get reported honestly. Use it as the last step before a commit or PR, on your own diff or the user's.

## Steps

1. **Get the diff.** Prefer, in order: what the user points at, `git diff` (unstaged), `git diff --cached` (staged), `git diff <base>...HEAD` for a branch. Say which one you reviewed.
2. **Establish the request.** The review is relative to what was asked. Take it from the conversation, the commit message, or the PR description. If none exists, ask for it in one line before reviewing; you cannot judge "drive-by" without knowing the target.
3. **Classify every hunk.** Four labels, nothing else:
   - **Required**: directly implements the request.
   - **Orphan cleanup**: removes something the required change made unused. Allowed.
   - **Drive-by**: reformatting, renames, type hints, docstrings, "improvements" to adjacent code, dependency bumps. Not asked for.
   - **Speculative**: options nobody passes, abstractions with one implementation, handling for cases that can't happen, backward-compat shims with no users.
4. **Check verification.** What check proves the change works, and was it run in this session? Look for test runs, commands, outputs. "Should work" counts as not verified.
5. **Check the report.** If there is a summary or PR description, does it claim only what was run? Does it state assumptions and anything skipped?

## Output

Keep it short. The reviewer's job is to point, not to rewrite.

```
Reviewed: <diff source> against request: "<one line>"

Hunks: N required, N orphan cleanup, N drive-by, N speculative

Drive-by (revert or split into a separate commit):
- path:line - what it does and why it isn't the request

Speculative (remove until needed):
- path:line - what it adds and what would justify it

Verification: <check that was run and its result> | not run
Report: <claims that outrun the evidence, or "matches">

Verdict: ready | ready after reverting the drive-by hunks | not verified
```

Omit any section that is empty. A clean review is three lines: reviewed, verification, verdict.

## Judgment calls

- A hunk can be required even if it looks like a refactor, when the request can't be implemented without it. Say so rather than flagging it.
- Matching the file's existing style is not drive-by. Changing the file's style is.
- Adding one test for the change is required work. Adding tests for untouched code is drive-by.
- If the diff is clean, say so in one line. Don't invent findings to look thorough.
