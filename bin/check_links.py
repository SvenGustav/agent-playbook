#!/usr/bin/env python3
"""Internal link integrity for a built static site.

The build fails on broken imports. It does not fail on an href that points at a page
which was never generated. This check reads the built directory and the redirect file
and reports links with no target.

Usage:
    python3 bin/check_links.py --dist dist --redirects vercel.json
    python3 bin/check_links.py --dist dist --warn-only
    python3 bin/check_links.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

SKIP_PREFIXES = ("#", "mailto:", "tel:", "data:", "javascript:", "blob:", "//", "/api/")
LINK = re.compile(r'(?:href|src)="([^"]+)"')


def walk(directory: Path) -> list[Path]:
    return sorted(p for p in directory.rglob("*") if p.is_file())


def served_paths(dist: Path) -> tuple[set[str], set[str]]:
    """Return (paths served directly, paths that only exist behind a trailing slash)."""
    served: set[str] = set()
    slash_only: set[str] = set()
    for path in walk(dist):
        rel = "/" + path.relative_to(dist).as_posix()
        if rel.endswith("/index.html"):
            base = rel[: -len("/index.html")] or "/"
            served.add(base)
            served.add("/" if base == "/" else base + "/")
        elif rel.endswith(".html"):
            served.add(rel[: -len(".html")])
            served.add(rel)
            if not rel.endswith("/index.html"):
                slash_only.add(rel[: -len(".html")] + "/")
        else:
            served.add(rel)
    return served, slash_only


def redirect_sources(path: Path | None) -> list[re.Pattern[str]]:
    """Literal and :param redirect sources from a vercel.json style file."""
    if path is None or not path.exists():
        return []
    entries = json.loads(path.read_text()).get("redirects", [])
    patterns = []
    for entry in entries:
        source = entry["source"]
        pattern = re.sub(r":[A-Za-z_][A-Za-z0-9_]*", r"[^/]+", re.escape(source).replace(r"\:", ":"))
        patterns.append(re.compile("^" + pattern + "$"))
    return patterns


def links_in(path: Path) -> list[tuple[int, str]]:
    found = []
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for target in LINK.findall(line):
            if target.startswith(SKIP_PREFIXES) or not target.startswith("/"):
                continue
            found.append((number, target))
    return found


def scan(dist: Path, redirects: Path | None) -> tuple[list[str], list[str]]:
    served, _ = served_paths(dist)
    patterns = redirect_sources(redirects)
    dead: list[str] = []
    hops: list[str] = []

    for page in [p for p in walk(dist) if p.suffix == ".html"]:
        for number, target in links_in(page):
            clean = target.split("#")[0].split("?")[0]
            if not clean:
                continue
            where = f"{page.relative_to(dist).as_posix()}:{number}"
            if clean in served:
                continue
            if any(p.match(clean) for p in patterns):
                continue
            if clean.endswith("/") and clean.rstrip("/") in served:
                hops.append(f"{where} -> {target} (extra redirect)")
                continue
            dead.append(f"{where} -> {target}")

    return dead, hops


def report(dist: Path, redirects: Path | None, warn_only: bool) -> int:
    if not dist.is_dir():
        print(f"no build directory at {dist}", file=sys.stderr)
        return 2

    dead, hops = scan(dist, redirects)
    pages = len([p for p in walk(dist) if p.suffix == ".html"])
    for line in dead:
        print(f"dead link    {line}")
    for line in hops:
        print(f"redirect hop {line}")

    print(f"\n{pages} pages, {len(dead)} dead links, {len(hops)} needless redirects")
    if warn_only:
        return 0
    return 1 if dead or hops else 0


def selftest() -> int:
    """Plant a dead link, confirm the check fails, fix it, then plant a redirect hop."""
    source = Path(__file__).resolve().parent.parent / "tests" / "fixture"
    failures = 0
    with tempfile.TemporaryDirectory() as raw:
        dist = Path(raw) / "dist"
        shutil.copytree(source / "dist", dist)

        code = report(dist, source / "redirects.json", warn_only=False)
        print(f"selftest: fixture with a dead link exits {code}")
        failures += code != 1

        (dist / "missing.html").write_text("<!doctype html><title>Now it exists</title>")
        code = report(dist, source / "redirects.json", warn_only=False)
        print(f"selftest: same fixture with the page added exits {code}")
        failures += code != 0

        index = dist / "index.html"
        index.write_text(index.read_text().replace('<a href="/about">About</a>',
                                                  '<a href="/about/">About</a>'))
        code = report(dist, source / "redirects.json", warn_only=False)
        print(f"selftest: fixture with a needless trailing slash exits {code}")
        failures += code != 1

    print("\nselftest ok" if not failures else "\nselftest FAILED")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=Path("dist"))
    parser.add_argument("--redirects", type=Path, default=Path("vercel.json"))
    parser.add_argument("--warn-only", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    if args.selftest:
        return selftest()
    redirects = args.redirects if args.redirects.exists() else None
    return report(args.dist, redirects, args.warn_only)


if __name__ == "__main__":
    sys.exit(main())
