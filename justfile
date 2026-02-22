install:
    @echo "=> Installing dependencies..."
    @uv sync --all-groups 2>&1 | tail -n 0
    @echo "   Done"
    @echo ""
    @echo "Install complete. Run 'just start' to launch."

start:
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
