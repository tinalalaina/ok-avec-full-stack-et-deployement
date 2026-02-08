#!/usr/bin/env bash
set -euo pipefail

BACKEND_URL="${BACKEND_URL:-}"
FRONTEND_URL="${FRONTEND_URL:-}"

if [[ -z "$BACKEND_URL" || -z "$FRONTEND_URL" ]]; then
  echo "Usage: BACKEND_URL=https://api.example.com FRONTEND_URL=https://app.example.com $0"
  exit 1
fi

BACKEND_HEALTH_URL="${BACKEND_URL%/}/healthz/"

printf "[1/3] Checking backend health endpoint: %s\n" "$BACKEND_HEALTH_URL"
curl --fail --silent --show-error "$BACKEND_HEALTH_URL" >/tmp/backend-health.json
cat /tmp/backend-health.json

printf "\n[2/3] Checking frontend URL: %s\n" "$FRONTEND_URL"
curl --fail --silent --show-error -I "$FRONTEND_URL" | head -n 5

printf "\n[3/3] Basic API reachability: %s\n" "${BACKEND_URL%/}/api/users/login/"
curl --silent --show-error -o /dev/null -w "HTTP %{http_code}\n" "${BACKEND_URL%/}/api/users/login/"

echo "Smoke check finished successfully."
