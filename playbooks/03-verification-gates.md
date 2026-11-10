# Verification gates

The most expensive failure in agent work is a confident summary of work that did not
happen.

## When to use

Every time a delegated task reports completion, every time a remote write reports
success, and before you tell a human that something is done.

## The rule

A summary is a claim. The working tree, the process log and the URL are evidence.
Confident prose costs the model nothing, so a paragraph describing a commit, a test run
and an upload proves none of the three.

## Checklist

Read back the artifact, not the report about the artifact.

- Commit landed: `git log --oneline -5` shows the message, and `git status` is clean for
  the files you expected.
- Files exist: the exact path named in the task returns content.
- Tests moved: re-run the suite yourself and compare counts. A log written before the
  last source edit is stale, whatever its numbers say.
- Lint clean: run the linter. `clean` in a summary is a string.
- Remote state changed: fetch the URL or query the API. An upload, a comment, a pull
  request and a deployment are four different facts.
- Service running: the process is up, the port answers, and the health endpoint returns
  the value you expect.

If one check fails, the task is open. Report the level you actually proved: files
written, tests passing locally, commit pushed, deployed.

## When verification fails

Do not re-dispatch the same prompt and hope. Same model, same scope, same wall clock,
same failure.

Split the task. Reduce it until one pass can finish it.

Or do it yourself. Deterministic work such as templating, renaming and running a script
is usually faster to execute than to delegate, and the artifact is guaranteed to land.

Or rescope: ship the smaller correct version and name what is missing.

## Timestamps

Compare times, not just states. A test log older than the source file it claims to test
is evidence of nothing. The same applies to a passing pipeline that ran before the push
you are asking about.

## Gates that fail closed

A gate is only a gate if a defect makes it fail. For every new check, break the thing it
guards and confirm the run goes red. A validation step that has never failed has never
been tested, and its green result is decoration.

## Failure modes

Marking a task complete from the child's word.

Accepting `tests pass` without a count.

Treating a local commit, a pushed commit and a merged pull request as the same event.

Reporting the plan as delivered when the artifact was never read back.
