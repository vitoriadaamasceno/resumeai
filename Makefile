
start-dev:
	@uvicorn main:app --reload

up:
	@docker compose up --build

test:
	@pytest