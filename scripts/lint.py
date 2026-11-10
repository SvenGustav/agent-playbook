#!/usr/bin/env python3
"""Check the playbooks against the conventions stated in the README."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

BANNED = {
    "\u2014": "em dash",
    "\u2013": "en dash",
    "\u201c": "curly quote",
    "\u201d": "curly quote",
    "\u2019": "curly apostrophe",
}
MAX_WORDS = 900
LINK = re.compile(r"\]\(([^)#]+)\)")


def check(path: Path, root: Path, require_shape: bool = True) -> tuple[list[str], int]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    problems: list[str] = []

    if require_shape:
        if not lines or not lines[0].startswith("# "):
            problems.append("no title on line 1")
        if "## When to use" not in text:
            problems.append("no '## When to use' section")

    words = len(text.split())
    if words > MAX_WORDS:
        problems.append(f"{words} words, limit {MAX_WORDS}")

    for char, name in BANNED.items():
        if char in text:
            number = next(i for i, line in enumerate(lines, 1) if char in line)
            problems.append(f"{name} on line {number}")

    for target in LINK.findall(text):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if not ((root / target).exists() or (path.parent / target).exists()):
            problems.append(f"link does not resolve: {target}")

    return problems, words


def check_workflow(path: Path) -> list[str]:
    """A workflow template is only useful if it parses and declares its permissions."""
    problems: list[str] = []
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        return [f"does not parse: {str(error).splitlines()[0]}"]
    if not isinstance(document, dict):
        return ["top level is not a mapping"]
    # PyYAML reads a bare `on:` key as boolean True, the same YAML 1.1 quirk that turns
    # an unquoted NO into false.
    present = {"on" if key is True else key for key in document}
    for key in ("name", "on", "jobs"):
        if key not in present:
            problems.append(f"missing '{key}'")
    if "permissions" not in document:
        problems.append("no 'permissions' block, so the token keeps its defaults")
    jobs = document.get("jobs") or {}
    if not isinstance(jobs, dict) or not jobs:
        problems.append("no jobs")
    for name, job in (jobs or {}).items():
        if not isinstance(job, dict):
            problems.append(f"job {name} is not a mapping")
            continue
        if "timeout-minutes" not in job:
            problems.append(f"job {name} has no timeout")
    return problems


def lint(root: Path) -> int:
    failures = 0
    playbooks = sorted((root / "playbooks").glob("*.md"))
    readme = (root / "README.md").read_text(encoding="utf-8")

    for path in playbooks:
        problems, words = check(path, root)
        if path.name not in readme:
            problems.append("not listed in README.md")
        status = "ok  " if not problems else "FAIL"
        print(f"[{status}] {path.relative_to(root)} ({words} words)")
        for problem in problems:
            print(f"       {problem}")
        failures += bool(problems)

    for path in sorted((root / "templates").glob("*.md")):
        problems, words = check(path, root, require_shape=False)
        status = "ok  " if not problems else "FAIL"
        print(f"[{status}] {path.relative_to(root)} ({words} words)")
        for problem in problems:
            print(f"       {problem}")
        failures += bool(problems)

    for pattern in ("ci/*.yml", ".github/workflows/*.yml"):
        for path in sorted(root.glob(pattern)):
            problems = check_workflow(path)
            status = "ok  " if not problems else "FAIL"
            print(f"[{status}] {path.relative_to(root)}")
            for problem in problems:
                print(f"       {problem}")
            failures += bool(problems)

    print(f"\n{len(playbooks)} playbooks, {failures} with problems")
    return 1 if failures else 0


def selftest() -> int:
    """Plant a violation, confirm the linter fails, remove it, confirm it passes."""
    source = Path(__file__).resolve().parent.parent
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw) / "repo"
        shutil.copytree(source, root, ignore=shutil.ignore_patterns(".git", "build"))
        if lint(root) != 0:
            print("selftest FAIL: clean copy does not lint")
            return 1
        target = root / "playbooks" / "01-skills-as-procedural-memory.md"
        target.write_text(target.read_text() + "\nA sentence with an em dash \u2014 here.\n")
        if lint(root) == 0:
            print("selftest FAIL: em dash passed the linter")
            return 1
        print("\nselftest ok: the linter rejects an em dash it should reject")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--root", default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    return lint(Path(args.root))


if __name__ == "__main__":
    sys.exit(main())
