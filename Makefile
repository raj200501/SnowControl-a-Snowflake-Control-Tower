.PHONY: bootstrap verify test demo dev-api

bootstrap:
	@echo "No external dependencies required for demo mode."

verify: test

test:
	./scripts/verify.sh

dev-api:
	PYTHONPATH=apps/api python -m app.main
