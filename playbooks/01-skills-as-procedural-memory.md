# Skills as procedural memory

An agent starts every session with no memory of the last one. A skill file is the part
that survives.

## When to use

You are about to explain the same procedure for the second time, or the agent got a task
right yesterday and wrong today on the same kind of work. Both are signs the procedure
belongs in a file.

## Shape

One skill is one markdown file with four parts.

1. A description line that names the trigger: `Use when <situation>. <what it does>.`
2. When to use, plus the neighbouring tasks that belong somewhere else.
3. The procedure, numbered, with the commands that actually ran.
4. Pitfalls, each with the rule that prevents it.

## Rules

Name the trigger in the first sentence of the description. If the description does not
mention a situation the agent will recognise, the file never gets loaded and the work
does not improve.

Write one rule per line and give the reason. `Run the check twice, because the first run
warms the cache` survives paraphrasing. `Be careful with caches` does not.

Record commands, not descriptions of commands. The next session should not have to
rediscover the flag that made it work.

Put the pitfall in the file in the same turn you hit it. A lesson that lives in a chat
transcript is gone by the next session.

Keep project facts out of the procedure. Paths, credentials and customer names change;
the shape of the work does not. If a fact is needed, put it in a reference file next to
the skill and link it from the procedure.

Update rather than append. A skill with three overlapping sections about the same
problem teaches the agent nothing. Delete the stale rule when you replace it.

## Test

The check is mechanical. Start a fresh session, give the agent a task in the trigger
category, and watch whether it loads the skill without being told. If it does not, the
description is wrong, not the agent.

## Failure modes

A skill that describes values instead of actions (`be rigorous`, `write clean code`)
changes nothing.

A skill copied from a blog post without the pitfalls is a summary of someone else's
work, and the agent will follow it into the same wall that blog post hit.

A skill that grows by appending turns into a pile of exceptions. Rewrite it flat when it
passes about 150 lines.
