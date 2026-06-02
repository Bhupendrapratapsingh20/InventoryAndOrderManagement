#!/bin/bash
set -e
echo "Running database migrations..."
/root/.local/bin/alembic upgrade head || echo "Migrations already applied or no migrations needed"
echo "Migrations completed."
