.PHONY: db db-down db-reset backend install seed lint help

db:
	docker compose up -d

db-down:
	docker compose down

db-reset:
	docker compose down -v && docker compose up -d

backend:
	cd backend && uvicorn main:app --reload

install:
	pip install -r backend/requirements.txt

seed:
	python scripts/seed.py

lint:
	ruff check . --fix
	ruff format .

help:
	@echo "make db          — start MySQL (Docker)"
	@echo "make db-down     — stop MySQL"
	@echo "make db-reset    — wipe DB and restart fresh"
	@echo "make backend     — start FastAPI (uvicorn --reload)"
	@echo "make install     — install Python dependencies"
	@echo "make seed        — populate earthquake data from USGS"
	@echo "make lint        — run ruff linter and formatter"
