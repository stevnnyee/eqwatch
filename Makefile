.PHONY: db db-down db-reset backend install seed lint help

# Prefer python3 when available (typical on macOS/Homebrew); otherwise `python`.
# Override anytime: make seed PYTHON=python
PYTHON ?= $(shell command -v python3 >/dev/null 2>&1 && echo python3 || echo python)

db:
	docker compose up -d

db-down:
	docker compose down

db-reset:
	docker compose down -v && docker compose up -d

backend:
	cd backend && $(PYTHON) -m uvicorn main:app --reload

install:
	$(PYTHON) -m pip install -r backend/requirements.txt

seed:
	$(PYTHON) scripts/seed.py

lint:
	$(PYTHON) -m ruff check . --fix
	$(PYTHON) -m ruff format .

help:
	@echo "make db          — start MySQL (Docker)"
	@echo "make db-down     — stop MySQL"
	@echo "make db-reset    — wipe DB and restart fresh"
	@echo "make backend     — start FastAPI (uvicorn --reload)"
	@echo "make install     — install Python deps ($(PYTHON) -m pip)"
	@echo "make seed        — populate earthquake data from USGS"
	@echo "make lint        — run ruff linter and formatter"
