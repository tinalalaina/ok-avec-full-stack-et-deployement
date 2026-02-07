#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

copy_if_missing() {
  local source_file="$1"
  local target_file="$2"

  if [[ -f "$target_file" ]]; then
    echo "[skip] $target_file existe déjà"
    return 0
  fi

  cp "$source_file" "$target_file"
  echo "[ok] créé: $target_file"
}

BACKEND_EXAMPLE="$ROOT_DIR/backend/.env.example"
BACKEND_ENV="$ROOT_DIR/backend/.env"
LEGACY_BACKEND_ENV="$ROOT_DIR/backend/env"
FRONTEND_EXAMPLE="$ROOT_DIR/frontend/.env.example"
FRONTEND_ENV="$ROOT_DIR/frontend/.env"

if [[ ! -f "$BACKEND_EXAMPLE" ]]; then
  echo "[error] Fichier introuvable: $BACKEND_EXAMPLE" >&2
  exit 1
fi

if [[ ! -f "$FRONTEND_EXAMPLE" ]]; then
  echo "[error] Fichier introuvable: $FRONTEND_EXAMPLE" >&2
  exit 1
fi

copy_if_missing "$BACKEND_EXAMPLE" "$BACKEND_ENV"
copy_if_missing "$FRONTEND_EXAMPLE" "$FRONTEND_ENV"

if grep -q '^SECRET_KEY=change-me$' "$BACKEND_ENV"; then
  GENERATED_SECRET_KEY="$(python3 - <<'PY'
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
PY
)"
  sed -i "s#^SECRET_KEY=change-me$#SECRET_KEY=${GENERATED_SECRET_KEY}#" "$BACKEND_ENV"
  echo "[ok] SECRET_KEY générée automatiquement dans backend/.env"
fi

if [[ -f "$LEGACY_BACKEND_ENV" ]]; then
  while IFS= read -r line; do
    [[ -z "$line" || "$line" =~ ^# ]] && continue
    key="${line%%=*}"
    if ! grep -q "^${key}=" "$BACKEND_ENV"; then
      echo "$line" >> "$BACKEND_ENV"
      echo "[ok] variable migrée depuis backend/env: $key"
    fi
  done < "$LEGACY_BACKEND_ENV"
fi

echo "\nTerminé. Vérifie ensuite les valeurs de production dans:"
echo "- backend/.env"
echo "- frontend/.env"
