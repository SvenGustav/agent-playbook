.PHONY: lint lint-selftest links links-selftest check

lint:
	python3 scripts/lint.py

lint-selftest:
	python3 scripts/lint.py --selftest

links:
	python3 bin/check_links.py --dist tests/fixture/dist --redirects tests/fixture/redirects.json --warn-only

links-selftest:
	python3 bin/check_links.py --selftest

check: lint lint-selftest links-selftest
