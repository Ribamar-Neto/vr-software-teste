local/start:
	uvicorn src.main:app --port 8008 --reload

test: # Executa os testes e retorna os erros e porcentagens de coverage.
	pytest --cov=src --cov-report=term-missing --cov-report=html --cov-report=xml --cov-branch

test-async: # Executa apenas testes assíncronos com pytest-asyncio.
	pytest --cov=src --cov-report=term-missing --cov-report=html --cov-report=xml --cov-branch -m async

test-async-complete: # Executa testes assíncronos completos com pytest-asyncio.
	pytest --cov=src --cov-report=term-missing --cov-report=html --cov-report=xml --cov-branch -m async -v --tb=short --strict-markers --disable-warnings --durations=10

test-all-async: # Executa todos os testes incluindo assíncronos com pytest-asyncio.
	pytest --cov=src --cov-report=term-missing --cov-report=html --cov-report=xml --cov-branch --asyncio-mode=auto -v --tb=short

lint:
	@echo
	ruff format .
	@echo
	ruff check --silent --exit-zero --fix .
	@echo
	ruff check .
	@echo
	mypy .
