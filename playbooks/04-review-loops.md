# Review loops

Self review that produces a list of observations is theatre. The output of a review loop
is a smaller diff, a measured number, or a named gap.

## When to use

After shipping something you care about, and before asking a human to look at it.

## Three rounds

Round one attacks the change. Read your own diff as a hostile reviewer. Look for data
that gets dropped silently, branches that can never run, empty results with no message,
and copy that promises something the code does not do.

Round two attacks the system around the change. The largest defects usually sit next to
your edit: two components that disagree about a matching rule, a filter that hides more
than intended, a cache keyed on the wrong field. Measure this round with real data.

Round three attacks the cost. Anything you made slower or more expensive gets a number in
milliseconds or in currency. A change that is correct and ten times slower is a different
kind of bug, and it is invisible without a measurement.

Each round ends with a fix and a re-run of the same check. Three rounds that end in
analysis have not closed anything.

## Evidence

Measure with a throwaway probe that prints counts and timings and asserts nothing, then
delete it before committing.

Every claim of improvement carries before and after numbers from that probe.

When a measurement exposes a pre-existing gap that is bigger than your change, say so and
scope it as its own task. Quietly widening the change is how a review loop becomes a
rewrite nobody reviewed.

Close the report with what is still unverified. A review that ends in silence about the
untested paths is worse than no review, because it reads as coverage.

## Gates

Mutation-test every new check. Break the thing it guards, run the gate, confirm red,
restore. A file copy taken before the mutation is safer than `git checkout -- file`, which
throws away the uncommitted work the mutation was testing.

Sweep the worst case, not the initial state. A check that only exercises the default path
passes while the longest input or the largest page collides with something.

## Failure modes

A review that rewrites working behaviour without saying which behaviour changed.

A round that finds the same defect twice because the first fix was never re-tested.

Numbers in the commit message that came from a run predating the final edit.
