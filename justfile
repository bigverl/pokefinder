install:
    uv sync --all-groups

init-db:
    scripts/reset_db.sh

seed-db:
    python3 scripts/seed_db.py

go:
    just install
    just init-db
    just seed-db

run:
    uv run litestar --app backend.src.app:app run --reload

up:
    docker-compose up -d --build

down:
    docker-compose down

test-unit:
    uv run pytest -m unit

test-api:
    scripts/test_api.sh

test-unit-postgres:
    uv run pytest tests/unit/test_candidate_finder_postgres.py

test-integration:
    uv run pytest -m integration

test-all:
    just test-unit
    just test-integration
    just test-unit-postgres
