install:
    uv sync --all-groups

run:
    uv run litestar --app backend.src.app:app run --reload

up:
    docker-compose up -d --build

down:
    docker-compose down

test-unit:
    uv run pytest -m unit

test-unit-postgres:
    uv run pytest tests/unit/test_candidate_finder_postgres.py

test-integration:
    uv run pytest -m integration

test-all:
    just test-unit
    just test-integration
    just test-unit-postgres