#!/bin/bash
# LingoGrade Cal.com Deployment Script
# Run from local machine: bash deploy.sh

SERVER="root@65.108.151.198"
SSH_KEY="$HOME/.ssh/id_ed25519_hetzner"
REMOTE_DIR="/opt/calcom"

echo "=== LingoGrade Cal.com Deployment ==="

# 1. Create remote directory
echo "[1/5] Creating remote directory..."
ssh -i "$SSH_KEY" "$SERVER" "mkdir -p $REMOTE_DIR"

# 2. Copy files
echo "[2/5] Copying files to server..."
scp -i "$SSH_KEY" docker-compose.yml "$SERVER:$REMOTE_DIR/"
scp -i "$SSH_KEY" Caddyfile "$SERVER:$REMOTE_DIR/"
scp -i "$SSH_KEY" .env "$SERVER:$REMOTE_DIR/"

# 3. Install Docker if not present
echo "[3/5] Ensuring Docker is installed..."
ssh -i "$SSH_KEY" "$SERVER" 'which docker || (curl -fsSL https://get.docker.com | sh && systemctl enable docker && systemctl start docker)'

# 4. Pull and start
echo "[4/5] Pulling images and starting services..."
ssh -i "$SSH_KEY" "$SERVER" "cd $REMOTE_DIR && docker compose pull && docker compose up -d"

# 5. Verify
echo "[5/5] Verifying..."
sleep 10
ssh -i "$SSH_KEY" "$SERVER" "cd $REMOTE_DIR && docker compose ps"

echo ""
echo "=== Deployment complete ==="
echo "Next steps:"
echo "  1. Point DNS: booking.lingograde.com -> 65.108.151.198"
echo "  2. Wait for SSL certificate (automatic via Caddy)"
echo "  3. Visit https://booking.lingograde.com to set up admin account"
echo "  4. Configure event types, availability, and Stripe in Cal.com UI"
