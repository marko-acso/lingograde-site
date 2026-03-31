-- =============================================================================
-- Cal.com: Set Marco Mascot Images on Event Types
-- =============================================================================
--
-- HOW TO RUN:
--   1. SSH into the Hetzner server:
--        ssh root@<HETZNER_IP>
--   2. Exec into the postgres container:
--        docker exec -it <postgres_container> bash
--   3. Run this script:
--        psql -U calcom -d calcom < calcom_set_mascot_images.sql
--
-- This script sets a mascot image URL in the metadata JSONB column for each
-- Cal.com event type, matched by slug. Existing metadata keys are preserved.
-- =============================================================================

BEGIN;

-- ---------------------------------------------------------------------------
-- Step 1: Show current state of all event types before any changes
-- ---------------------------------------------------------------------------
SELECT
    id,
    slug,
    title,
    metadata
FROM "EventType"
ORDER BY id;

-- ---------------------------------------------------------------------------
-- Step 2a: Deep Dive Assessment → marco-reading.png
-- Uses COALESCE so that if metadata is NULL we start from an empty object
-- rather than losing the whole value. jsonb_set merges the new key in.
-- ---------------------------------------------------------------------------
UPDATE "EventType"
SET metadata = jsonb_set(
    COALESCE(metadata, '{}'::jsonb),
    '{mascotImage}',
    '"https://lingograde.com/assets/mascot/marco-reading.png"'::jsonb
)
WHERE slug ILIKE '%deepdive-assessment%';

-- ---------------------------------------------------------------------------
-- Step 2b: Full Assessment → marco-thumbsup.png
-- ---------------------------------------------------------------------------
UPDATE "EventType"
SET metadata = jsonb_set(
    COALESCE(metadata, '{}'::jsonb),
    '{mascotImage}',
    '"https://lingograde.com/assets/mascot/marco-thumbsup.png"'::jsonb
)
WHERE slug ILIKE '%full-assessment%';

-- ---------------------------------------------------------------------------
-- Step 2c: Quick Assessment → marco-alarm.png
-- ---------------------------------------------------------------------------
UPDATE "EventType"
SET metadata = jsonb_set(
    COALESCE(metadata, '{}'::jsonb),
    '{mascotImage}',
    '"https://lingograde.com/assets/mascot/marco-alarm.png"'::jsonb
)
WHERE slug ILIKE '%quick-assessment%';

-- ---------------------------------------------------------------------------
-- Step 3: Verify the updates — show final state
-- ---------------------------------------------------------------------------
SELECT
    id,
    slug,
    title,
    metadata
FROM "EventType"
ORDER BY id;

COMMIT;
