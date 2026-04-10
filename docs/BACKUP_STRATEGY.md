# LingoGrade Backup Strategy

## Supabase (PostgreSQL)
- **Automatic**: Supabase Pro plan includes daily backups with 7-day retention
- **Manual**: Weekly `pg_dump` via cron on Hetzner server
  ```bash
  # Add to crontab: 0 3 * * 0 /opt/lingograde-api/scripts/backup-db.sh
  pg_dump "$DATABASE_URL" | gzip > /var/backups/lingograde/db-$(date +%Y%m%d).sql.gz
  ```
- **Retention**: Keep 4 weekly + 3 monthly snapshots
- **Restore**: `gunzip -c backup.sql.gz | psql "$DATABASE_URL"`

## Reports (PDF files)
- **Location**: `/var/data/lingograde/reports/` on Hetzner
- **Backup**: Rsync to secondary storage nightly
  ```bash
  # 0 4 * * * rsync -az /var/data/lingograde/ /var/backups/lingograde/files/
  ```
- **Retention**: Indefinite (PDFs are small, ~200KB each)

## Invoices
- **Location**: `/var/data/lingograde/invoices/` on Hetzner
- **Backup**: Same rsync job as reports
- **Retention**: 10 years (Bulgarian accounting law)

## Cal.com
- **Type**: SaaS — managed by Cal.com
- **Export**: Monthly manual export of booking data via Cal.com API
- **Stripe**: Stripe retains all payment records indefinitely

## Static Site
- **Source of truth**: Git repository
- **Hosting**: Vercel (rebuilt from git on every deploy)
- **No backup needed** — git history is the backup

## Sticker Selfies
- **Location**: `/var/data/lingograde/stickers/` on Hetzner
- **Backup**: Same rsync job
- **Retention**: 1 year after verification

## Recovery Playbook
1. **DB lost**: Restore from latest `pg_dump` or Supabase point-in-time recovery
2. **Server lost**: Provision new Hetzner VPS, clone repo, restore files from backup, run deploy
3. **Vercel down**: Serve static files from Caddy on Hetzner as fallback
