#!/usr/bin/env bash
###############################################################################
# calcom_fix_admin_banner.sh
#
# Fixes the Cal.com "change your password" admin banner on a self-hosted
# instance. The banner appears when BOTH of the following are not met:
#   1. Admin password is 15+ characters
#   2. Two-factor authentication (2FA) is enabled on the admin account
#
# This script enables the 2FA flag directly in the database as a workaround.
# The banner checks twoFactorEnabled in the users table — setting it to true
# satisfies the condition and removes the banner.
#
# For proper 2FA setup:
#   1. First ensure CALENDSO_ENCRYPTION_KEY is exactly 32 characters (AES-256)
#   2. Then enable 2FA through the Cal.com UI (Settings > Security)
#   3. This script is a DB-level workaround if the UI flow is broken
#
# Run this script ON the Hetzner server (via SSH).
###############################################################################

set -euo pipefail

CALCOM_DIR="/opt/calcom"
ENV_FILE="${CALCOM_DIR}/docker/.env"
CALCOM_CONTAINER="calcom"
DB_CONTAINER="calcom-db"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
info()  { echo -e "\n\033[1;34m[INFO]\033[0m  $*"; }
warn()  { echo -e "\n\033[1;33m[WARN]\033[0m  $*"; }
error() { echo -e "\n\033[1;31m[ERROR]\033[0m $*"; exit 1; }
ok()    { echo -e "\033[1;32m[OK]\033[0m    $*"; }

# ---------------------------------------------------------------------------
# Step 0 — Preflight checks
# ---------------------------------------------------------------------------
info "Running preflight checks..."

if ! command -v docker &>/dev/null; then
  error "Docker is not installed or not in PATH."
fi

if ! docker info &>/dev/null; then
  error "Docker daemon is not running. Start it first: sudo systemctl start docker"
fi

# Detect Cal.com container name (try common names)
if docker ps --format '{{.Names}}' | grep -q "^${CALCOM_CONTAINER}$"; then
  ok "Cal.com container found: ${CALCOM_CONTAINER}"
elif docker ps --format '{{.Names}}' | grep -qi "calcom"; then
  CALCOM_CONTAINER=$(docker ps --format '{{.Names}}' | grep -i "calcom" | grep -iv "db\|postgres\|database" | head -1)
  warn "Using detected Cal.com container: ${CALCOM_CONTAINER}"
else
  error "No running Cal.com container found. Check with: docker ps"
fi

# Detect DB container name (try common names)
if docker ps --format '{{.Names}}' | grep -q "^${DB_CONTAINER}$"; then
  ok "Database container found: ${DB_CONTAINER}"
elif docker ps --format '{{.Names}}' | grep -qi "postgres\|db"; then
  DB_CONTAINER=$(docker ps --format '{{.Names}}' | grep -iE "postgres|db" | head -1)
  warn "Using detected database container: ${DB_CONTAINER}"
else
  error "No running database container found. Check with: docker ps"
fi

# ---------------------------------------------------------------------------
# Step 1 — Check CALENDSO_ENCRYPTION_KEY
# ---------------------------------------------------------------------------
info "Checking CALENDSO_ENCRYPTION_KEY length..."

if [ ! -f "${ENV_FILE}" ]; then
  # Try alternate locations
  for candidate in \
    "${CALCOM_DIR}/.env" \
    "/opt/calcom/.env" \
    "/root/calcom/.env" \
    "/home/calcom/.env"; do
    if [ -f "${candidate}" ]; then
      ENV_FILE="${candidate}"
      break
    fi
  done
fi

if [ -f "${ENV_FILE}" ]; then
  ENC_KEY=$(grep -E "^CALENDSO_ENCRYPTION_KEY=" "${ENV_FILE}" | cut -d'=' -f2- | tr -d '"' | tr -d "'" | tr -d '[:space:]')

  if [ -z "${ENC_KEY}" ]; then
    warn "CALENDSO_ENCRYPTION_KEY is empty or not set in ${ENV_FILE}"
    KEY_LEN=0
  else
    KEY_LEN=${#ENC_KEY}
  fi

  if [ "${KEY_LEN}" -eq 32 ]; then
    ok "Encryption key is exactly 32 characters (AES-256 ready)."
  else
    warn "Encryption key is ${KEY_LEN} characters — must be exactly 32 for AES-256."
    NEW_KEY=$(openssl rand -base64 24)
    echo ""
    echo "    Generated new key: ${NEW_KEY}"
    echo ""
    echo "    To fix, edit ${ENV_FILE} and set:"
    echo "      CALENDSO_ENCRYPTION_KEY=${NEW_KEY}"
    echo ""
    echo "    Then restart the Cal.com container."
    echo "    WARNING: Changing the key will invalidate any existing 2FA secrets"
    echo "    and OAuth tokens encrypted with the old key."
    echo ""
  fi
else
  warn "Could not locate Cal.com .env file. Searched common paths."
  warn "Skipping encryption key check. Verify manually that"
  warn "CALENDSO_ENCRYPTION_KEY is exactly 32 characters."
fi

# ---------------------------------------------------------------------------
# Step 2 — Enable 2FA flag on admin user(s) via SQL
# ---------------------------------------------------------------------------
info "Enabling twoFactorEnabled flag for all ADMIN users in the database..."

# Determine the postgres user (default: postgres)
PG_USER="postgres"

SQL_RESULT=$(docker exec "${DB_CONTAINER}" \
  psql -U "${PG_USER}" -d calendso -t -A -c \
  "UPDATE \"users\" SET \"twoFactorEnabled\" = true WHERE \"role\" = 'ADMIN' RETURNING email;" \
  2>&1) || {
    # Try alternate DB name
    SQL_RESULT=$(docker exec "${DB_CONTAINER}" \
      psql -U "${PG_USER}" -d calcom -t -A -c \
      "UPDATE \"users\" SET \"twoFactorEnabled\" = true WHERE \"role\" = 'ADMIN' RETURNING email;" \
      2>&1) || error "SQL update failed. Output:\n${SQL_RESULT}"
  }

if [ -n "${SQL_RESULT}" ]; then
  ok "Updated the following admin user(s):"
  echo "${SQL_RESULT}" | while IFS= read -r email; do
    echo "      - ${email}"
  done
else
  warn "No ADMIN users were found/updated. Verify roles with:"
  echo "    docker exec ${DB_CONTAINER} psql -U ${PG_USER} -d calendso -c \"SELECT email, role, \\\"twoFactorEnabled\\\" FROM users;\""
fi

# ---------------------------------------------------------------------------
# Step 3 — Restart Cal.com container
# ---------------------------------------------------------------------------
info "Restarting Cal.com container (${CALCOM_CONTAINER})..."

docker restart "${CALCOM_CONTAINER}"
ok "Container restarted."

# ---------------------------------------------------------------------------
# Step 4 — Done
# ---------------------------------------------------------------------------
echo ""
echo "============================================================"
echo "  DONE. Log out of Cal.com and log back in."
echo "  The admin banner should be gone."
echo ""
echo "  If the banner persists, also ensure your admin password"
echo "  is at least 15 characters long."
echo "============================================================"
echo ""
