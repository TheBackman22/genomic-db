# Genomic Database

Hierarchical storage for genomic data using PostgreSQL.

## Structure

```
Genome (1) ──► Chromosome (many) ──► Gene (many)
```

## Prerequisites

- **Docker runtime** — a Docker-compatible daemon such as [Colima](https://github.com/abiosoft/colima) or [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Docker** — [install instructions](https://docs.docker.com/engine/install/)
- **Docker Compose** (v2 plugin) — typically bundled with Docker Desktop; for standalone installs see [install instructions](https://docs.docker.com/compose/install/)
- **Python 3.11+**

## Quick Start

### 1. Start PostgreSQL

```bash
docker compose up -d
```

This starts a PostgreSQL 16 container on `localhost:5432`.

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
```

### 3. Install the package

```bash
python3 -m pip install -e ".[dev]"
```

### 4. Run database migrations

```bash
# Generate initial migration from models
alembic revision --autogenerate -m "initial schema"

# Apply migrations
alembic upgrade head
```

### 5. Verify it works

```bash
python3 scripts/example_usage.py
```

## Project Structure

```
genomic-db/
├── docker-compose.yml      # Local PostgreSQL
├── Dockerfile              # App container (for deployment)
├── pyproject.toml          # Dependencies
├── alembic.ini             # Migration config
├── alembic/
│   ├── env.py              # Migration environment
│   └── versions/           # Migration files
├── src/
│   └── genomic_db/
│       ├── models/            # SQLAlchemy models
│       │   ├── base.py        # Declarative base
│       │   ├── genome.py      # Genome
│       │   ├── chromosome.py  # Chromosome
│       │   └── gene.py        # Gene
│       └── db/             # Database connection
│           └── connection.py
├── scripts/
│   └── example_usage.py    # Demo script
└── tests/
```

## Configuration

The database URL is configured via environment variable:

```bash
# Default (for local Docker)
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/genomics

# For AWS RDS (example)
DATABASE_URL=postgresql://user:pass@my-db.abc123.us-east-1.rds.amazonaws.com:5432/genomics
```

## Common Commands

```bash
# Start database
docker compose up -d

# Stop database
docker compose down

# Stop and delete data
docker compose down -v

# View logs
docker compose logs -f db

# Connect with psql
docker compose exec db psql -U postgres -d genomics

# Create new migration after model changes
alembic revision --autogenerate -m "description of change"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Run tests
pytest
```

## Adding Fields Later

To add new fields to a model:

1. Edit the model in `src/genomic_db/models/genomic.py`
2. Generate a migration: `alembic revision --autogenerate -m "add field_name to table"`
3. Review the generated migration in `alembic/versions/`
4. Apply: `alembic upgrade head`
