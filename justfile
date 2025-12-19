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
    @echo "Starting PostgreSQL..."
    @docker start postgres-dev 2>/dev/null || docker run --name postgres-dev -e POSTGRES_PASSWORD=password -e POSTGRES_DB=postgres-dev -p 5432:5432 -d postgres:16
    @echo "Waiting for database..."
    @sleep 3
    @echo "Starting app..."
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

frontend:
    uv run textual run --dev frontend/app.py

serve:
    textual serve frontend/app.py