install:
    uv sync --all-groups

dev:
    python src app.py

up:
    docker-compose up -d --build

down:
    docker-compose down

test-unit:
    TEST_MODE=unit uv run pytest -m unit

test-integration:
    TEST_MODE=integration uv run pytest -m integration

test-all:
    TEST_MODE=unit uv run pytest -m unit
    TEST_MODE=integration uv run pytest -m integration