# <Feature> implementation plan

**Goal:** one sentence.

**Existing options:** the library or repo you checked, its licence, and why it fits or
does not. Required before designing anything new.

**Architecture:** two sentences on the approach.

**Tech stack:** what runs it.

## Task 1: <verb> <object>

**Files:** create `path/to/file.py`, modify `path/to/other.py:41-58`

**Step 1.** Write the failing test in `tests/test_file.py::test_case`.

**Step 2.** Run `pytest tests/test_file.py::test_case -v`. Expected: FAIL, function not
defined.

**Step 3.** Implement the minimum that passes.

**Step 4.** Run the same command. Expected: PASS.

**Step 5.** Run `pytest tests/ -q`. Expected: same count as before plus one.

## Task 2: <verb> <object>

Same shape. Two to five minutes of work per task, one writer per file.
