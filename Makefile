.PHONY: install dev test lint check compile

install:
	python -m pip install -e .

dev:
	python -m pip install -e '.[dev]'

test:
	pytest -q

lint:
	ruff check src tests

compile:
	python -m compileall -q src

check: lint test compile
