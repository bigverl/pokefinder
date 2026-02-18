install:
    @echo "=> Installing dependencies..."
    @uv sync --all-groups 2>&1 | tail -n 0
    @echo "   Done"
    @echo ""
    @just init-db
    @echo ""
    @echo "=> Seeding database..."
    @just seed-db
    @echo ""
    @echo "=> Stopping database..."
    @-docker stop pokefinder-db > /dev/null 2>&1
    @echo "   Done"
    @echo ""
    @echo "Install complete. Run 'just start' to launch."

install-debug:
    @echo "=> Installing dependencies..."
    @VERBOSE=1 uv sync --all-groups
    @echo "   Done"
    @echo ""
    @VERBOSE=1 just init-db
    @echo ""
    @echo "=> Seeding database..."
    @VERBOSE=1 just seed-db
    @echo ""
    @echo "=> Stopping database..."
    @-docker stop pokefinder-db 2>&1
    @echo "   Done"
    @echo ""
    @echo "Install complete. Run 'just start' to launch."

init-db:
    @VERBOSE=${VERBOSE:-0} scripts/reset_db.sh

seed-db:
    @VERBOSE=${VERBOSE:-0} python3 scripts/seed_db.py

start:
    @echo "=> Starting database. This will take a few seconds...  "
    @docker start pokefinder-db > /dev/null 2>&1 || docker run --name pokefinder-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=pokefinder-db -p 5432:5432 -d postgres:16 > /dev/null 2>&1
    @sleep 3
    @echo "done"
    @echo "=> Starting backend...     "
    @uv run litestar --app backend.src.app:app run --reload > /dev/null 2>&1 &
    @sleep 2
    @echo "done"
    @echo "=> Starting frontend...    "
    @uv run textual serve --dev frontend/app.py --port 8080 > /dev/null 2>&1 &
    @echo "done"
    @echo ""
    @echo "Open http://localhost:8080 in your browser"

stop:
    @echo "=> Stopping frontend...   done"
    @-lsof -ti:8080 | xargs kill 2>/dev/null
    @echo "=> Stopping backend...    done"
    @-lsof -ti:8000 | xargs kill 2>/dev/null
    @echo "=> Stopping database... done"
    @-docker stop pokefinder-db > /dev/null 2>&1
    @echo ""
    @echo "Stopped all services"

up:
    docker-compose up -d --build
    @echo ""
    @echo "Open http://localhost:8080 in your browser"
    @echo ""

down:
    docker-compose down

test-unit:
    uv run pytest -m unit

test-component:
    uv run pytest -m component

test-all:
    uv run just test-unit
    uv run just test-component

check:
    scripts/static_analysis.sh

frontend:
    uv run textual run --dev frontend/app.py

serve:
    textual serve --dev frontend/app.py --port 8080

backend:
    litestar --app=backend.src.app:app run --debug --reload
