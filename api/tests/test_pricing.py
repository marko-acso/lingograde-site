"""
Regression tests for pricing.py — the single source of truth for all prices.

These pin documented business rules so an accidental edit to a price, tier
bound, or currency table is caught immediately:
  - every cents-denominated price ends in .95
  - corporate tiers are contiguous, non-overlapping, and volume-discounted
  - the four supported currencies always carry the same number
  - headline SKU prices match the published catalog
"""

import os
import sys

# pricing.py lives one directory up (api/); make it importable regardless of rootdir.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pricing


def _all_cent_amounts():
    amounts = []
    for pkg in pricing.KIDS_PACKAGES.values():
        amounts.extend(pkg["amounts"].values())
    amounts.extend(pricing.EXPRESS_HIRING_AUDIT["amounts"].values())
    amounts.append(pricing.MEGA_BUNDLE_CENTS)
    for tier in pricing.CORPORATE_ASSESSMENT.values():
        amounts.append(tier["unit_cents"])
    for acc in pricing.ACCESSORY_CATALOG.values():
        amounts.append(acc["amount"])
    return amounts


def test_all_cent_prices_end_in_95():
    for cents in _all_cent_amounts():
        assert cents % 100 == 95, f"{cents} does not end in .95"


def test_headline_sku_prices():
    assert pricing.EXPRESS_HIRING_AUDIT["amounts"]["eur"] == 24995  # EUR 249.95
    assert pricing.MEGA_BUNDLE_CENTS == 29995                       # EUR 299.95
    assert pricing.KIDS_PACKAGES["deep-dive"]["amounts"]["eur"] == 24995


def test_corporate_tier_unit_prices():
    assert pricing.CORPORATE_ASSESSMENT["team"]["unit_cents"] == 11995
    assert pricing.CORPORATE_ASSESSMENT["department"]["unit_cents"] == 9995
    assert pricing.CORPORATE_ASSESSMENT["enterprise"]["unit_cents"] == 7995


def test_corporate_tiers_contiguous_and_bounded():
    team = pricing.CORPORATE_ASSESSMENT["team"]
    dept = pricing.CORPORATE_ASSESSMENT["department"]
    ent = pricing.CORPORATE_ASSESSMENT["enterprise"]
    assert team["min_seats"] == 5
    assert team["max_seats"] + 1 == dept["min_seats"]   # 14 -> 15, no gap/overlap
    assert dept["max_seats"] + 1 == ent["min_seats"]    # 49 -> 50, no gap/overlap
    assert ent["max_seats"] == 200                       # above this -> contact form


def test_corporate_volume_discount_decreases_with_size():
    team = pricing.CORPORATE_ASSESSMENT["team"]["unit_cents"]
    dept = pricing.CORPORATE_ASSESSMENT["department"]["unit_cents"]
    ent = pricing.CORPORATE_ASSESSMENT["enterprise"]["unit_cents"]
    assert team > dept > ent


def test_amounts_equal_across_currencies():
    for b in list(pricing.KIDS_PACKAGES.values()) + [pricing.EXPRESS_HIRING_AUDIT]:
        assert len(set(b["amounts"].values())) == 1, (
            f"{b['name']} differs across currencies: {b['amounts']}"
        )


def test_amounts_cover_exactly_allowed_currencies():
    for b in list(pricing.KIDS_PACKAGES.values()) + [pricing.EXPRESS_HIRING_AUDIT]:
        assert set(b["amounts"].keys()) == pricing.ALLOWED_CURRENCIES


def test_drip_prices_match_catalog():
    assert pricing.HOMEWORK_CHECK == {"discounted": 23.95, "full": 29.95, "currency": "EUR"}
    assert pricing.REASSESSMENT == {"discounted": 118.95, "full": 139.95, "currency": "EUR"}
    assert pricing.DOUBLE_HOMEWORK == {"discounted": 53.95, "full": 59.90, "currency": "EUR"}
