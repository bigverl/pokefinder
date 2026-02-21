# PokeFinder

A Pokedex-style team building tool for PokeRogue.

## Features

- **Candidate Finder** — Search for Pokemon by stats, type matchups, and moves
- **Type Coverage Analyzer** — Find your team's offensive and defensive coverage gaps

---

## Installation

### Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager
- [just](https://github.com/casey/just#installation) — Command runner
- [Docker](https://docs.docker.com/get-docker/) — For PostgreSQL

### Quickstart

```bash
# Make sure docker engine is started
just install
just start
```

`just install` sets up dependencies, runs database migrations, and seeds the database. Requires docker engine to be active
`just start` starts the backend and frontend. Open http://localhost:8080 when it's ready.

To stop:

```bash
just stop
```

### Debug Install

To see verbose output during installation (database setup steps, migration details, seed counts per table):

```bash
just install-debug
```

---

## Usage

| Command | Description |
|---------|-------------|
| `just install` | First-time setup |
| `just start` | Start backend, frontend, and database |
| `just stop` | Stop all services |
| `just install-debug` | First-time setup with verbose output |
| `just up` | Docker compose up. Containerized usage (slow) |
| `just down` | Docker compose down. |


---

## Todos

### Features
- [ ] Pokedex

### Architecture
- [ ] Remove database entirely and replace with json fixture
- [ ] Refactor frontend to use React
- [ ] Host on GitHub Pages
