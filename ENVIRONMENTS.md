# Environments

This project runs two isolated Postgres databases via Docker Compose profiles. Both can run simultaneously without conflict.

## Overview

| | Dev | Local Prod |
|---|---|---|
| **Purpose** | Sandbox for development, experimentation, testing | Sensitive genomic computations that cannot run on AWS |
| **Container** | `genomics-db-dev` | `genomics-db-prod` |
| **Host port** | 5432 | 5433 |
| **Database name** | `genomics_dev` | `genomics_prod` |
| **Config file** | `.env.dev` (committed) | `.env.prod` (gitignored) |
| **Branch restriction** | None | `main` only |
| **Docker volume** | `postgres_data_dev` | `postgres_data_prod` |

## Getting Started

### Dev environment

```bash
./db.sh dev up
```

Starts the dev database on port 5432. Works from any git branch.

### Local prod environment

```bash
# Must be on the main branch
git checkout main
./db.sh prod up
```

The `db.sh` wrapper enforces a git branch guard: the prod database can only be started when the current branch is `main`. This prevents accidentally running untested code against production data.

## db.sh Reference

All database operations go through `db.sh`:

```bash
./db.sh <env> <command> [args...]
```

| Command | Description | Example |
|---|---|---|
| `up` | Start the database container | `./db.sh dev up` |
| `down` | Stop the database container | `./db.sh prod down` |
| `logs` | View container logs | `./db.sh dev logs -f` |
| `backup` | Create a SQL backup in `backups/` | `./db.sh prod backup` |
| `migrate` | Run Alembic migrations | `./db.sh dev migrate upgrade head` |

Any other command is passed through to `docker compose` with the appropriate profile.

## Migrations (Alembic)

Both environments share the same set of migration files in `alembic/versions/`. Each database independently tracks which migrations have been applied via its own `alembic_version` table.

### Typical workflow

1. **Develop and test migrations against dev:**

   ```bash
   # Generate a migration from model changes
   ./db.sh dev migrate revision --autogenerate -m "add samples table"

   # Apply it
   ./db.sh dev migrate upgrade head

   # Check current state
   ./db.sh dev migrate current
   ```

2. **Apply to local prod when ready:**

   ```bash
   git checkout main
   ./db.sh prod migrate upgrade head
   ```

3. **Roll back if needed:**

   ```bash
   ./db.sh dev migrate downgrade -1
   ```

### How the URL is resolved

- `db.sh migrate` reads credentials from the matching `.env.<env>` file and sets `DATABASE_URL` before calling Alembic.
- Running `alembic` directly (without `db.sh`) uses the default in `alembic.ini`, which points to the dev database.
- `alembic/env.py` checks for a `DATABASE_URL` environment variable and overrides `alembic.ini` if set.

## Python Application Code

`connection.py` reads `DATABASE_URL` from the environment, defaulting to the dev database:

```python
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/genomics_dev"
)
```

To point your application at prod:

```bash
source .env.prod
export DATABASE_URL="postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5433/${POSTGRES_DB}"
python your_script.py
```

## Configuration Files

| File | Committed | Description |
|---|---|---|
| `docker-compose.yml` | Yes | Defines both database services and backup services using profiles |
| `.env.dev` | Yes | Dev credentials (safe defaults) |
| `.env.prod` | No | Prod credentials (gitignored -- change the password) |
| `alembic.ini` | Yes | Alembic config, default URL points to dev |
| `db.sh` | Yes | Wrapper script with branch guard and environment routing |

## Data Isolation

- Each environment uses a **separate Docker volume** (`postgres_data_dev` / `postgres_data_prod`), so `docker compose down -v` on one environment does not affect the other.
- Running `docker compose --profile dev down -v` destroys only the dev volume.
- The prod volume persists independently and is only affected by explicit prod commands.
