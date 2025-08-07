local/start:
	uvicorn src.main:app --port 8008 --reload

test:
	pytest --cov-report=term-missing --cov-report=html --cov-report=xml --cov-branch --cov src/

lint:
	@echo
	ruff format .
	@echo
	ruff check --silent --exit-zero --fix .
	@echo
	ruff check .
	@echo
	mypy .
