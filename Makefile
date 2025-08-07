local/start: # Executa um server FastAPI
	uvicorn src.main:app --port 8008 --reload

test: # Executa os testes e retorna os erros e porcentagens de coverage.
	pytest --cov-report term-missing --cov-report html --cov-branch --cov .

lint: # Executa o lint para formatar e verificar erros.
	@echo
	ruff format .
	@echo
	ruff check --silent --exit-zero --fix .
	@echo
	ruff check .
