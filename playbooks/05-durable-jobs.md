# Durable jobs

Work that must outlive the conversation belongs in a scheduler, with a log you can read
afterwards.

## When to use

A task has to run on a schedule, survive a closed laptop or a new session, or finish
after the session that started it ends. Anything that only has to happen now does not
need this.

## Shape

A scheduled job needs four things: a schedule, a definition of done, a durable log, and
an owner to notify.

Write the definition of done as an observable outcome. `Post the digest` is a wish.
`Write the file, then confirm it contains one entry per source` is checkable by whatever
runs next.

Keep the log outside the agent's memory. A row per run, with start time, end time, exit
status and the artifact path. When someone asks whether the job ran, the answer comes
from that table, not from a configuration file.

## Verifying a schedule

Three separate facts, often confused:

- The job is configured, with the schedule you think it has.
- The job is enabled. A configured job can be paused.
- The job ran, at a time after the change you are asking about.

Check all three. A schedule entry and a success from last week are not proof of a run
today.

## Long runs

Anything that takes more than about a minute goes in the background with a completion
notification, and the session keeps working. A foreground call that blocks for minutes
burns the turn and teaches you nothing until it ends.

For jobs that never exit, notify on a pattern instead: a line in the log that means ready.

## Idempotency

Assume every job runs twice. A cron entry that overlaps with a previous run, a retry
after a timeout, a manual trigger during a schedule: all normal. Writes keyed on a stable
id, and a guard that skips work already recorded, turn a double run into a no-op.

Backfills are the same problem at volume. Run them against a copy, or against a partition
the job owns, before pointing them at production rows.

## Failure modes

A job that fails silently because nothing watches its exit code.

A job whose output a human reads only when they remember to open a folder.

A retry loop with no ceiling, which turns one failure into a bill.
