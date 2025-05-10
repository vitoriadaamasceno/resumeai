
start-dev:
	@uvicorn main:app --reload

up:
	@docker compose up --build

lint:
	@ruff check . --fix

test:
	@pytest