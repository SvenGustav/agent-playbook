# Verification checklist

Run against the artifact, after the work claims to be finished.

- [ ] `git log --oneline -5` shows the commit, `git status` clean for the expected files
- [ ] Every path named in the task exists and contains what was asked for
- [ ] The test command was re-run now, and the counts match the claim
- [ ] The linter was run now, on the current tree
- [ ] Remote state read back: URL fetched, API queried, deployment status checked
- [ ] Any new gate was mutation-tested: the defect makes it fail
- [ ] What is still unverified is named in the report
