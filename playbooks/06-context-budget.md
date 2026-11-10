# Context budget

Every tool call re-reads the conversation so far. Long output is not free once; it is
paid again on every later call in the session.

## When to use

Always. This is the constraint that decides whether a long session stays fast.

## What costs what

A few hundred lines of stack trace stays in context for the rest of the session. A full
file dump does the same. On a laptop-class setup, a session that reaches six figures of
tokens adds roughly twenty seconds to every call, and the work does not get better.

The model is not slower because it is thinking harder. It is slower because there is more
to read before it can start.

## Rules

Filter at the source. Redirect a build to a file and grep it, use `--jq` on JSON, `--stat`
on a diff, `head -40` on a log. Print the three lines that matter and keep the rest on
disk.

Read the file you need, at the offset you need. A whole-file read of a 2,000-line file to
change one function is a choice to carry 2,000 lines for the rest of the session.

Batch independent calls in one turn. Five lookups in one turn cost one round trip of
history; five turns cost five.

Run slow work in the background and keep going. A build, a test suite and a crawl all
outlive the patience of a foreground call.

Start a fresh session per topic. When a task is finished, the context that solved it is
dead weight for the next one.

## Failure modes

Pasting a stack trace into the prompt without the command that produced it. The next
session can read the error but cannot reproduce it.

Re-reading a file you just wrote to confirm the write. The tool confirms writes; the
check costs a full file in context.

Letting a subagent return its raw transcript. Ask for the artifact path and the numbers.

## The trade

Cutting context is not about saving tokens for their own sake. It keeps the model close
to the part of the work that matters, and it keeps the session usable for the hour after
the next one.
