.PHONY: lint lint-selftest check

lint:
	python3 scripts/lint.py

lint-selftest:
	python3 scripts/lint.py --selftest

check: lint lint-selftest
