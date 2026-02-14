# Database Backups

## Create a backup

```bash
docker compose run --rm backup
```

This saves a timestamped `.sql` file to this directory (e.g. `genomics_20260214_015651.sql`).

## Restore from a backup

```bash
docker compose exec -T db psql -U postgres genomics < backups/<filename>.sql
```

To do a clean restore, truncate existing data first:

```bash
docker compose exec db psql -U postgres genomics -c "TRUNCATE genes, chromosomes, genomes CASCADE"
docker compose exec -T db psql -U postgres genomics < backups/<filename>.sql
```
