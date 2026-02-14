#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

usage() {
    echo "Usage: ./db.sh <env> <command> [args...]"
    echo ""
    echo "Environments:"
    echo "  dev     Development database (port 5432)"
    echo "  prod    Local production database (port 5433, requires main branch)"
    echo ""
    echo "Commands:"
    echo "  up        Start the database container"
    echo "  down      Stop the database container"
    echo "  logs      Show container logs"
    echo "  backup    Create a database backup"
    echo "  migrate   Run alembic migrations (pass alembic args after, e.g. 'upgrade head')"
    echo "  Any other docker compose command is passed through."
    echo ""
    echo "Examples:"
    echo "  ./db.sh dev up"
    echo "  ./db.sh prod up"
    echo "  ./db.sh dev backup"
    echo "  ./db.sh dev migrate upgrade head"
    echo "  ./db.sh prod migrate current"
    echo "  ./db.sh prod down"
    exit 1
}

check_branch() {
    local branch
    branch="$(git branch --show-current)"
    if [ "$branch" != "main" ]; then
        echo "ERROR: Production database can only be started from the 'main' branch."
        echo "Current branch: $branch"
        echo ""
        echo "Switch to main first:  git checkout main"
        exit 1
    fi
}

get_database_url() {
    local env_file=".env.$1"
    local port="$2"
    # Source the env file to get POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
    # shellcheck disable=SC1090
    source "$env_file"
    echo "postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${port}/${POSTGRES_DB}"
}

if [ $# -lt 2 ]; then
    usage
fi

ENV="$1"
CMD="$2"
shift 2

case "$ENV" in
    dev)
        PROFILE="dev"
        ;;
    prod)
        check_branch
        PROFILE="prod"
        ;;
    *)
        echo "ERROR: Unknown environment '$ENV'. Use 'dev' or 'prod'."
        exit 1
        ;;
esac

case "$CMD" in
    up)
        docker compose --profile "$PROFILE" up -d "$@"
        echo ""
        echo "$ENV database is running."
        if [ "$ENV" = "dev" ]; then
            echo "Connect: postgresql://postgres:postgres@localhost:5432/genomics_dev"
        else
            echo "Connect: postgresql://postgres:<see .env.prod>@localhost:5433/genomics_prod"
        fi
        ;;
    down)
        docker compose --profile "$PROFILE" down "$@"
        ;;
    logs)
        docker compose --profile "$PROFILE" logs "$@"
        ;;
    backup)
        TOOLS_PROFILE="${PROFILE}-tools"
        docker compose --profile "$TOOLS_PROFILE" run --rm "backup-${ENV}" "$@"
        ;;
    migrate)
        if [ $# -lt 1 ]; then
            echo "Usage: ./db.sh $ENV migrate <alembic command> [args...]"
            echo "Example: ./db.sh $ENV migrate upgrade head"
            exit 1
        fi
        if [ "$ENV" = "dev" ]; then
            DB_URL="$(get_database_url dev 5432)"
        else
            DB_URL="$(get_database_url prod 5433)"
        fi
        DATABASE_URL="$DB_URL" alembic "$@"
        ;;
    *)
        docker compose --profile "$PROFILE" "$CMD" "$@"
        ;;
esac
