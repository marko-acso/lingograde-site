# LingoGrade Deployment Instructions

---

## 1. Fix Cal.com — Enable Public Event Pages

The self-hosted Cal.com at booking.lingograde.com redirects to auth login because the default landing page requires authentication. Public event pages work via direct event URLs.

### Step-by-step:

```bash
# SSH into your Hetzner server
ssh -i ~/.ssh/id_ed25519_hetzner root@65.108.151.198

# Navigate to Cal.com directory
cd /opt/calcom

# Check Cal.com is running
docker compose ps

# Open a shell inside the Cal.com container
docker compose exec calcom sh
```

**Inside the container, check your admin user exists:**
```bash
# Open the database
npx prisma db execute --stdin <<< "SELECT id, username, email FROM users;"
```

Then **exit the container** and do these fixes:

### A. Set a default redirect for the root URL

Edit the Caddyfile on the server so the root of booking.lingograde.com redirects to your main event page instead of showing the login screen:

```bash
cat > /opt/calcom/Caddyfile << 'EOF'
booking.lingograde.com {
    # Root redirect to your main scheduling page
    handle / {
        redir https://booking.lingograde.com/marko.check permanent
    }

    # Everything else goes to Cal.com
    reverse_proxy calcom:3000
    encode gzip

    # Security headers
    header {
        X-Content-Type-Options "nosniff"
        X-Frame-Options "SAMEORIGIN"
        Referrer-Policy "strict-origin-when-cross-origin"
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
    }
}
EOF
```

### B. Restart Caddy to apply

```bash
docker compose restart caddy
```

### C. Verify public access

Open in browser (incognito):
- https://booking.lingograde.com → should redirect to /marko.check
- https://booking.lingograde.com/marko.check → should show your public profile with event types
- https://booking.lingograde.com/marko.check/quick-assessment → should show booking calendar

### D. If your username is different from "marko.check"

Check your username:
```bash
docker compose exec calcom npx prisma db execute --stdin <<< "SELECT username FROM users LIMIT 5;"
```

Replace `marko.check` in the Caddyfile redirect with whatever your actual username is.

### Troubleshooting

If event types don't show publicly:
1. Log into Cal.com admin: https://booking.lingograde.com/auth/login
2. Go to Event Types
3. For each event type, make sure it's NOT set to "Private"
4. Check Availability → make sure you have available slots

If you see "No availability" on public pages:
1. Go to Availability in Cal.com admin
2. Set your working hours
3. Make sure timezone is correct

---

## 2. Deploy Caddyfile.prod (Main Site Security Headers)

This deploys the production Caddyfile for www.lingograde.com with security headers, favicon handling, and bare domain redirect.

**Important:** This assumes the main site is served from a SEPARATE Caddy instance than Cal.com (different server or different Caddy process). If they share the same Caddy, you'll need to merge the Caddyfiles.

### If main site has its OWN Caddy (separate from Cal.com):

```bash
# From your local machine (in lingograde-site/deploy/)
SERVER="root@YOUR_MAIN_SITE_IP"
SSH_KEY="$HOME/.ssh/id_ed25519_hetzner"

# Copy the Caddyfile
scp -i "$SSH_KEY" Caddyfile.prod "$SERVER:/etc/caddy/Caddyfile"

# Restart Caddy on the server
ssh -i "$SSH_KEY" "$SERVER" "systemctl reload caddy"

# Verify
ssh -i "$SSH_KEY" "$SERVER" "caddy validate --config /etc/caddy/Caddyfile"
```

### If main site and Cal.com share the SAME server (65.108.151.198):

You need to merge both Caddyfiles into one. The Cal.com Docker Caddy and the system Caddy can't both bind port 443.

**Option A (recommended): Use system Caddy for everything**

```bash
ssh -i ~/.ssh/id_ed25519_hetzner root@65.108.151.198

# Stop the Docker Caddy (Cal.com's)
cd /opt/calcom
# Edit docker-compose.yml: remove the caddy service entirely
# Change calcom ports from "3001:3000" to expose on localhost only

# Install system Caddy
apt install -y caddy

# Create merged Caddyfile
cat > /etc/caddy/Caddyfile << 'EOF'
www.lingograde.com {
    root * /var/www/lingograde-site
    file_server
    encode gzip
    try_files {path} {path}.html {path}/ /404.html

    handle /favicon.ico {
        rewrite * /assets/mascot/marco-logo-v6.1.png
        file_server
    }

    header {
        X-Content-Type-Options "nosniff"
        X-Frame-Options "SAMEORIGIN"
        Referrer-Policy "strict-origin-when-cross-origin"
        Permissions-Policy "camera=(), microphone=(), geolocation=()"
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://www.google-analytics.com https://app.lingograde.com; frame-src 'none'"
    }
}

lingograde.com {
    redir https://www.lingograde.com{uri} permanent
}

booking.lingograde.com {
    handle / {
        redir https://booking.lingograde.com/marko.check permanent
    }
    reverse_proxy localhost:3001
    encode gzip

    header {
        X-Content-Type-Options "nosniff"
        X-Frame-Options "SAMEORIGIN"
        Referrer-Policy "strict-origin-when-cross-origin"
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
    }
}
EOF

# Validate and restart
caddy validate --config /etc/caddy/Caddyfile
systemctl reload caddy
```

### Verify after deployment:

```bash
# Check security headers
curl -I https://www.lingograde.com 2>/dev/null | grep -E "X-Content|X-Frame|Referrer|Content-Security|Strict-Transport"

# Check favicon
curl -sI https://www.lingograde.com/favicon.ico | head -5

# Check redirect
curl -sI https://lingograde.com | grep Location
```

---

## 3. Stripe Branding Colors

Current wrong colors: #525f7f (grey-blue) / #0074d4 (generic blue)
Target colors: #2563AB (LingoGrade navy) / #27AE60 (LingoGrade green)

### Step-by-step:

1. Go to https://dashboard.stripe.com/settings/branding
2. Under **Colors**:
   - **Brand color** (primary): Change from `#0074d4` to `#2563AB`
     - This is used on payment page buttons, links, and accents
   - **Accent color** (secondary): Change to `#27AE60`
     - This appears on success states and secondary elements
3. Under **Icon**:
   - Verify your LingoGrade icon is uploaded (should already be done)
4. Under **Logo**:
   - Verify your LingoGrade logo is uploaded (should already be done)
5. Click **Save** at the bottom

### Verify:

Open any of your Stripe payment links in incognito:
- https://buy.stripe.com/6oU6oH7Dmdjd0ZeefbgUM01
- The "Pay" button and link colors should now be navy (#2563AB)
- Success/confirmation elements should use green (#27AE60)

### Also update invoice branding:

1. Go to https://dashboard.stripe.com/settings/billing/invoice
2. Under **Appearance** → **Accent color**: Set to `#2563AB`
3. **Save**

### Also update Checkout branding:

1. Go to https://dashboard.stripe.com/settings/checkout
2. Under **Appearance**:
   - **Button color**: `#2563AB`
   - **Button text color**: `#FFFFFF` (white)
3. **Save**

### Other Stripe fixes while you're there:

**Add EIK as Tax ID:**
1. Go to https://dashboard.stripe.com/settings/billing/invoice
2. Under **Default** → **Tax IDs** or **Business details**
3. Add a new Tax ID:
   - Type: Select "Bulgarian Unified Identification Code (BG UIC)" or search "bg_uic"
   - Enter your EIK number
4. Save

**Fix Marco plush description:**
1. Go to https://dashboard.stripe.com/products
2. Find "Marco" plush product
3. Edit description: find "feet)30" → change to "feet). 30" (add space + period)
4. Save

**Rename tip product:**
1. Go to https://dashboard.stripe.com/products
2. Find the tip product (currently "Many students like to say thank you")
3. Change name to: "Tip Your Assessor"
4. Move the Voss line ("Many students like to say thank you...") into the description field
5. Save
