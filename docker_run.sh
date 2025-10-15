#!/bin/sh
set -eu

# ------------------------
# setup_qdrant.sh
# - Stops & removes existing containers for this compose project
# - Starts DRF with runserver commande
# ------------------------

# Choose docker-compose command (support docker-compose or docker compose)
if command -v docker-compose >/dev/null 2>&1; then
  DC="docker-compose"
elif docker compose version >/dev/null 2>&1; then
  DC="docker compose"
else
  echo "ERROR: neither 'docker-compose' nor 'docker compose' found in PATH."
  exit 1
fi

echo "Using: $DC"

# Load environment variables from docker.env if present, exporting them
if [ -f ./docker.env ]; then
  echo "Loading variables from ./docker.env"
  # export everything in docker.env
  # shellcheck disable=SC1091
  set -a
  . ./docker.env
  set +a
else
  echo "No docker.env file found in project root — continuing without sourcing it."
fi

# Ensure we run from repo root where docker-compose.yml exists
if [ ! -f docker-compose.yml ] && [ ! -f docker-compose.yaml ]; then
  echo "ERROR: docker-compose.yml not found in current directory. Run this script from the repo root."
  exit 2
fi

echo "Stopping and removing compose services (if any)..."
# Stop and remove containers, networks, volumes created by compose in this folder
$DC down -v --remove-orphans || true

# Start DRF service
echo "Starting DRF service (detached)..."
$DC up -d api

echo "Done. DRF service is up and running. If you want to stop everything, run: ${DC} down -v"