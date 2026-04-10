"""
pricing.py — Single source of truth for all LingoGrade prices.
All amounts in cents. All prices end in .95 (business rule).
"""

# ── Bot Assessment ──
BOT_ASSESSMENT_CENTS = 4995  # EUR 49.95

# ── Kids Packages ──
KIDS_PACKAGES = {
    "quick": {
        "name": "Kids Quick Check",
        "description": "15-minute assessment for ages 6-17. Pre-A1 to B2. Visual report with parent summary.",
        "amounts": {"eur": 8995, "usd": 8995, "gbp": 8995, "chf": 8995},
    },
    "full": {
        "name": "Kids Full Picture",
        "description": "25-minute assessment for ages 6-17. Pre-A1 to B2. Full report with parent guide + homework.",
        "amounts": {"eur": 12995, "usd": 12995, "gbp": 12995, "chf": 12995},
    },
    "deep-dive": {
        "name": "Kids Deep Dive",
        "description": "40-minute assessment (15+25 with break) for ages 6-17. Comprehensive report + parent consultation.",
        "amounts": {"eur": 24995, "usd": 24995, "gbp": 24995, "chf": 24995},
    },
}

# ── Mega Bundle ──
MEGA_BUNDLE_CENTS = 29995  # EUR 299.95

# ── Accessories ──
ACCESSORY_CATALOG = {
    "cap": {
        "name": "LingoGrade Cap",
        "description": "Embroidered Marco logo on navy cotton twill. Adjustable strap.",
        "amount": 2995,  # EUR 29.95
    },
    "bracelet": {
        "name": "Marco Bracelet",
        "description": "Woven fabric bracelet with Marco silhouette clasp. LingoGrade blue with gold accent thread.",
        "amount": 1495,  # EUR 14.95
    },
    "pin": {
        "name": "Marco Enamel Pin",
        "description": "Hard enamel pin of Marco with mortarboard. Gold-plated metal. Butterfly clutch backing.",
        "amount": 1295,  # EUR 12.95
    },
}

# ── Drip email prices (upsell) ──
HOMEWORK_CHECK = {"discounted": 23.95, "full": 29.95, "currency": "EUR"}
REASSESSMENT = {"discounted": 118.95, "full": 139.95, "currency": "EUR"}
DOUBLE_HOMEWORK = {"discounted": 53.95, "full": 59.90, "currency": "EUR"}

# ── Allowed currencies ──
ALLOWED_CURRENCIES = {"eur", "usd", "gbp", "chf"}
