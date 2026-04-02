-- =============================================================================
-- Cal.com: Set website back-link on user profile
-- =============================================================================
--
-- HOW TO RUN:
--   1. SSH into the Hetzner server:
--        ssh -i ~/.ssh/id_ed25519_hetzner root@65.108.151.198
--   2. Exec into the postgres container:
--        docker exec -it $(docker ps -qf name=calcom-db) bash
--   3. Run this script:
--        psql -U calcom -d calcom < /tmp/calcom_add_backlink.sql
--
-- Or one-liner from SSH:
--   docker exec -i $(docker ps -qf name=calcom-db) psql -U calcom -d calcom < calcom_add_backlink.sql
--
-- This sets bio + metadata.website so booking pages show:
--   1. A "Visit website" clickable link back to lingograde.com
--   2. Bio text with brand description
-- =============================================================================

BEGIN;

-- Set bio text (appears on profile)
UPDATE "users"
SET bio = 'LingoGrade — Professional Language Assessment | www.lingograde.com'
WHERE username = 'marco';

-- Set metadata.website for clickable "Visit website" link
-- Cal.com reads metadata->>'website' to render a back-link on public pages
UPDATE "users"
SET metadata = COALESCE(metadata, '{}'::jsonb) || '{"website": "https://www.lingograde.com"}'::jsonb
WHERE username = 'marco';

-- Verify
SELECT username, bio, metadata->>'website' AS website FROM "users" WHERE username = 'marco';

COMMIT;
