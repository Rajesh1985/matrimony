#!/usr/bin/env bash
set -euo pipefail

# Change these if needed
APP_USER="www-data"
APP_GROUP="www-data"
ENV_ROOT="/srv/uploads"
ENV="prod"
BASE="$ENV_ROOT/$ENV"

# Create directories
sudo mkdir -p "$BASE"/{files,thumbs,pdfs}
sudo mkdir -p "$ENV_ROOT/quarantine"
sudo mkdir -p "$ENV_ROOT/derivatives"
sudo mkdir -p "$ENV_ROOT/secure"   # for encrypted sensitive files

# Create app user/group if missing (safe to run even if exists)
if ! id -u "$APP_USER" >/dev/null 2>&1; then
  sudo useradd --system --no-create-home --group "$APP_GROUP" "$APP_USER" || true
fi

# Set ownership and permissions
sudo chown -R "$APP_USER":"$APP_GROUP" "$ENV_ROOT"
sudo find "$ENV_ROOT" -type d -exec chmod 750 {} \;
sudo find "$ENV_ROOT" -type f -exec chmod 640 {} \;

# Tighten secure folder more strictly
sudo chown -R root:"$APP_GROUP" "$ENV_ROOT/secure"
sudo chmod 750 "$ENV_ROOT/secure"

echo "Directories created under $ENV_ROOT and owned by $APP_USER:$APP_GROUP"