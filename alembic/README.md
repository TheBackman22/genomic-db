# Alembic Migrations

Alembic is a database migration tool for SQLAlchemy. It tracks changes to your models and generates scripts that alter the database schema to match, without losing existing data.

## Why use migrations?

Without migrations, adding a column to a model would require manually writing `ALTER TABLE` SQL or dropping and recreating tables (losing all data). Alembic automates this by comparing your SQLAlchemy models to the current database schema and generating the necessary SQL.

## How it works

1. You modify a model in `src/genomic_db/models/`
2. Run `alembic revision --autogenerate -m "description of change"` to generate a migration script
3. Review the generated script in `alembic/versions/`
4. Run `alembic upgrade head` to apply it

Alembic applies incremental `ALTER TABLE` statements (adding columns, changing types, adding indexes, etc.) so existing data stays intact. No truncation or container restarts needed.

## Common commands

```bash
# Generate a migration after model changes
alembic revision --autogenerate -m "add description to genes"

# Apply all pending migrations
alembic upgrade head

# Rollback the last migration
alembic downgrade -1

# Show current migration version
alembic current

# Show migration history
alembic history
```

## Key files

- `alembic.ini` — connection string and logging config (project root)
- `alembic/env.py` — imports your models so autogenerate can detect changes
- `alembic/versions/` — generated migration scripts
