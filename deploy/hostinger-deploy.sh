#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR=${PROJECT_DIR:-/opt/rupaykg-enterprise}
COMPOSE_FILE="$PROJECT_DIR/deploy/docker-compose.hostinger.yml"

cd "$PROJECT_DIR"

if [ ! -f .env ]; then
  echo "Missing .env file. Copy .env.example and update production values before deploying."
  exit 1
fi

docker compose -f "$COMPOSE_FILE" pull mongo nginx || true
docker compose -f "$COMPOSE_FILE" up -d --build

echo "Deployment finished."
echo "Check services: docker compose -f $COMPOSE_FILE ps"
