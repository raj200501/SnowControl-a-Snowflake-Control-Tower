.PHONY: bootstrap verify test lint typecheck docs demo

bootstrap:
	python -m pip install -e ".[dev]"

verify: lint typecheck test docs

test:
	pytest

lint:
	ruff format --check .
	ruff check .

typecheck:
	mypy src

docs:
	mkdocs build -f docs/mkdocs.yml

demo:
	snowcontrol demo
