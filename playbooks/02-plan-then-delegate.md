# Plan, then delegate

Two habits make agent work predictable: the plan lives in a file, and every unit of work
is small enough to finish in one focused pass.

## When to use

Any task that touches more than one file, or that you would not finish in one tool call.
For a single edit, skip this and do it directly.

## Write the plan

Put the plan in the repo, under a directory the agent can find again:
`docs/plans/YYYY-MM-DD-slug.md`.

Each task in the plan names four things: the files it touches, the exact change, the
command that proves it worked, and the expected output of that command. A task that says
"add validation" is not a task. A task that says "add a length check in
`src/auth/password.py:41`, run `pytest tests/test_password.py::test_short`, expect FAIL,
then PASS" is.

Size each task at two to five minutes of focused work. Small tasks are cheap to retry,
cheap to review, and easy to drop when the plan turns out to be wrong. A task that
balloons is a plan defect, and the fix is to split it before dispatch, not during.

Before designing anything new, record what already exists: the library you checked, its
licence, and why it fits or does not. An implementer told to build from scratch will
build from scratch, badly.

## Delegate it

Dispatch one fresh agent per task. Fresh context is the point: it carries no confusion
from the previous task's dead ends.

Give the child the full task text in its prompt. Do not give it the plan path and let it
read the file. The child should not have to reconstruct scope, and a child that reads the
whole plan will pick up tasks that are not its own.

State where the change lands, what the surrounding code does, and the exact verification
command. Children know nothing about the conversation that produced the task.

Assign one writer per file. Parallel agents editing the same file produce a merge that
nobody reviewed.

Let the child report changed paths and command output. The parent reviews the diff,
integrates, and commits. Delegating a commit means nobody checked what went into it.

## Review it twice

First pass: does the change match the specification, no more and no less. Second pass:
is the code good. Run them in that order. Quality review of code that does the wrong
thing wastes both passes.

After the final task, review the whole change as one unit: does it work together, does
anything contradict, do the tests still pass from a clean state.

## Failure modes

A plan written as prose paragraphs cannot be dispatched task by task.

A child that asks a question is blocked, not finished. Answer it, then let it continue.

A plan that keeps growing tasks during execution is being used as a scratchpad. Stop,
rewrite the remaining tasks, then resume.
