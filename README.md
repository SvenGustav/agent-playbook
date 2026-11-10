# agent-playbook

Procedures for working with a coding agent on real code: how to plan, how to delegate,
how to verify, how to review. Seven short playbooks you can copy into any repository.

They come from daily use of an agent on production code. Everything tied to a job, a
client or a codebase has been removed, so what is left is the part that transfers.

## The seven

- `playbooks/01-skills-as-procedural-memory.md`: write the procedure down, so the next session starts where this one ended.
- `playbooks/02-plan-then-delegate.md`: put the plan in a file, keep tasks small, give each child its own context.
- `playbooks/03-verification-gates.md`: treat a summary as a claim and read back the artifact.
- `playbooks/04-review-loops.md`: attack your own work in three rounds and land fixes with numbers.
- `playbooks/05-durable-jobs.md`: move anything that must outlive the session into a scheduler with a log.
- `playbooks/06-context-budget.md`: keep the session short enough to stay fast.
- `playbooks/07-ci-gates.md`: order the work by cost, classify each gate as hard or soft, and prove every gate can fail.

## How to use it

Copy `START-HERE.md` next to your code and point your agent at it. Or paste the single
playbook that matches the task into the agent's context.

Start with `03` and `02`. Verification and delegation change behaviour on the first day.
The rest compound over weeks.

The templates in `templates/` are the shapes that survived: a skill file, a plan, a
delegated task, a verification checklist.

## What is here

```
playbooks/     seven procedures, one topic each
templates/     copyable shapes for a skill, a plan, a task, a check
bin/           check_links.py, a working internal link gate
ci/            pr-gate.yml, a workflow template with a gate, checks and deploy
tests/fixture/ a built site with one dead link, used to prove the gate fails
START-HERE.md  the pointer file for an agent
scripts/lint.py  checks the playbooks and the workflow for the conventions below
```

## The link gate

`bin/check_links.py` is the smallest complete example of the gap a CI pipeline usually
leaves open. A build succeeds while an internal link points at a page nobody generated.

```bash
python3 bin/check_links.py --dist tests/fixture/dist --redirects tests/fixture/redirects.json
python3 bin/check_links.py --selftest
```

The selftest plants a dead link, confirms exit 1, adds the missing page, confirms exit 0,
then adds a needless trailing slash and confirms exit 1 again. Standard library only, no
network, so it runs the same in CI and on a laptop.

## Conventions

Every playbook has a title, a `When to use` section, and fewer than 900 words. No
typographic dashes, no curly quotes. Links resolve. `make lint` enforces this in CI, and
a lint that has never failed has not been tested, so `make lint-selftest` breaks it on
purpose.

## Scope

Seven procedures, one working gate, no framework. There is no orchestration code and no
prompt library tied to one model. The playbooks work with any agent that reads files and
runs commands.

Written from practice, not from benchmark. Where a number appears, it was measured on the
setup the procedure came from.

MIT licensed.
