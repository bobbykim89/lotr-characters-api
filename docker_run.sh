#!/bin/sh
set -e

# Stop and remove previous containers (and anonymous volumes)
docker-compose down -v || true

# Build images and start services (attached so you see logs).
# If you prefer detached, change to `docker-compose up -d --build`
docker-compose up --build