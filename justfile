install:
    @echo "=> Installing dependencies..."
    @uv sync --all-groups 2>&1 | tail -n 0
    @echo "   Done"
    @echo ""
    @echo "Install complete. Run 'just start' to launch."

start:
    @echo "=> Starting backend..."
    @uv run litestar --app backend.src.app:app run --reload > /dev/null 2>&1 &
    @sleep 2
    @echo "   done"
    @echo "=> Starting frontend..."
    @cd frontend && npm run dev > /dev/null 2>&1 &
    @echo "   done"
    @echo ""
    @echo "Open http://localhost:5173 in your browser"

stop:
    @echo "=> Stopping frontend..."
    @-lsof -ti:5173 | xargs kill 2>/dev/null
    @echo "   done"
    @echo "=> Stopping backend..."
    @-lsof -ti:8000 | xargs kill 2>/dev/null
    @echo "   done"
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

test-frontend:
    cd frontend && npm run test

test-all:
    just test-unit
    just test-component
    just test-frontend

check:
    scripts/static_analysis.sh

commit:
    just check
    just test-all

frontend:
    cd frontend && npm run dev

backend:
    litestar --app=backend.src.app:app run --debug --reload
