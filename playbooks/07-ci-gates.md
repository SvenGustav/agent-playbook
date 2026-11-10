# CI gates that fail closed

A gate is a check that can stop a deploy. A check that only reports its findings is a
dashboard, and dashboards get ignored within a month.

## When to use

Adding CI to a repository, or looking at a pipeline that has been green for months while
defects still ship.

## Order the work by cost

Put the cheapest decision first. A five second job that decides whether the twenty minute
suite runs at all is worth more than any single test inside it. It can skip draft pull
requests, skip a labelled commit, and refuse to run on a conflicted branch.

Use a concurrency group keyed on the branch and cancel superseded runs. Pushing three
times to one branch should not queue three full pipelines.

Inside a run, go mechanical then slow: parse, format, lint, build, then browser or
integration suites, then deploy. A failure at minute one should not wait for minute
eighteen.

## Two classes of gate

Hard gates block the merge or the deploy. Soft gates record a result and never block:
visual diffs, bundle size trends, coverage trends.

Choose per check, write the choice down, and keep it. A soft gate that blocks once a
quarter trains people to bypass gates in general.

## Catch what the toolchain cannot see

The build tells you imports resolve. It says nothing about whether an `href` points at a
page that exists. A validator says the HTML is legal, not that the link is alive.

List the failure modes your stack is blind to, and write one check per mode. Internal link
integrity is the standard example: a broken internal link is invisible to the build, to
the validator, and to every browser test that only visits pages it already knows exist.

The same shape applies anywhere: a schema that accepts a field nobody populates, a
migration that runs twice, an asset referenced from CSS.

## Fail closed, and prove it

For every new gate, break the thing it guards, run the gate, watch it go red, then restore.
A gate that has never failed has never been tested, and its green result is decoration.

Keep the proof in the repository as a selftest target that plants a known defect and
asserts the gate rejects it. Then the proof still holds after the gate is edited.

## Local enforcement

A pre-push hook that runs the suite catches the defect before the commit leaves the
machine, which is the cheapest place to catch it. Three conditions make it real:

- The file mode is 100755. A hook committed as 100644 is skipped with a warning that
  scrolls past, while the hook body still claims it cannot be bypassed. Check with
  `git ls-files -s .githooks/pre-push`.
- Dependencies exist in every worktree. A hook that runs a formatter in a worktree
  without `node_modules` fails for the wrong reason, and the next push uses `--no-verify`.
- One suite, one place. If CI runs the same checks on the same machine, the hook doubles
  the cost inline in every agent turn. Pick one.

Name what the hook protects. A pre-push hook sits before the push. Merge protection is a
separate mechanism, and on a plan without required status checks there is none.

## Cost

Runner minutes are a budget. Measure per job, not per run: cancelled runs look cheap in
wall clock and still bill. Then remove duplicate work, which is usually one PR gate
workflow plus a deploy workflow that only deploys on the default branch.

Report a measured change with the run id that proves it. Anything else is a projection,
and say so.

## Wiring

A gate nobody invokes is decoration. Every check needs a caller: the pull request
workflow, the deploy workflow after the build, and the local hook if it is cheap enough.

Then audit the wiring the way you audit the gate: delete the call, confirm the pipeline
still goes green, and fix that.
