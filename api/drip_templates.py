"""
drip_templates.py — LingoGrade drip email template library.

Each function returns {"subject": str, "html": str, "text": str}.

Copy rules:
- Never use "error", "mistake", "wrong", "fail", "weakness"
- Use "pattern", "focus area", "developing structure", "growth point"
- Never frame CEFR level as deficit
- Adult-to-Adult ego state — factual, calm, no praise, no reassurance
- Max 200 words body, one CTA per email
- Sender name in signatures, never "LingoGrade Team"
- All HTML is inline (no external CSS)
"""

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

LANGUAGE_NAMES = {
    "en": "English",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "bg": "Bulgarian",
    "hr": "Croatian",
    "ro": "Romanian",
    "pl": "Polish",
    "zh": "Chinese",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ar": "Arabic",
}

# (topic_title, insight_text)
LANGUAGE_INSIGHTS = {
    "en": (
        "Verb-preposition collocations",
        (
            "In English, verb-preposition combinations don't follow logical rules — they're fixed pairs "
            "that have to be learned as units. 'Depend on', 'apologise for', 'consist of', 'agree with' "
            "— changing the preposition changes meaning or makes the phrase wrong. At B2, roughly 40% of "
            "common patterns involve wrong preposition choice after a verb. The most effective approach is "
            "to learn three new verb-preposition pairs per week in full sentences, not as isolated "
            "vocabulary. Context makes them stick; lists don't."
        ),
    ),
    "de": (
        "The movement vs location preposition rule",
        (
            "In German, preposition choice often determines case. The nine two-way prepositions — in, an, "
            "auf, über, unter, vor, hinter, neben, zwischen — take accusative when movement is implied, "
            "dative when location is described. One test: ask yourself 'going somewhere?' (accusative) or "
            "'already there?' (dative). Ich gehe in den Garten (accusative — movement) vs Ich sitze im "
            "Garten (dative — location). This single rule covers roughly 60% of preposition case "
            "decisions at B1 and above."
        ),
    ),
    "fr": (
        "The subjunctive — when it actually matters",
        (
            "The subjunctive in French appears most after expressions of doubt, emotion, or necessity — "
            "'je veux que', 'il faut que', 'bien que'. French speakers use it inconsistently in casual "
            "speech, but written French and formal registers require it. At B1, focus on the ten most "
            "common trigger phrases and the subjunctive forms of être and avoir — these cover most "
            "real-world use. The rest follows the same pattern once those are solid."
        ),
    ),
    "es": (
        "Ser vs estar — the decision that matters most",
        (
            "Spanish has two verbs for 'to be', and the choice between them shapes meaning in ways that "
            "articles or tenses don't. Ser describes identity and permanent characteristics; estar "
            "describes states and conditions. But native speakers bend this rule: 'estar muerto' (to be "
            "dead) uses estar despite death being permanent. The practical shortcut: if the situation "
            "could change tomorrow, use estar. If it defines what something is, use ser. Exceptions "
            "exist, but this rule handles 80% of decisions correctly."
        ),
    ),
    "it": (
        "The congiuntivo — when to use it, when not to",
        (
            "Italian's congiuntivo sounds more complex than it is in practice. It appears after verbs of "
            "wanting, doubting, or believing when the subject changes: 'voglio che tu venga' (I want you "
            "to come). In everyday spoken Italian, many native speakers replace it with the indicative "
            "and are widely understood. At B1-B2, prioritise using it correctly in writing and in formal "
            "speech — start with 'che' clauses after pensare, credere, sperare, and volere. These four "
            "verbs cover the majority of natural congiuntivo use."
        ),
    ),
    "pt": (
        "European vs Brazilian Portuguese — why they feel different",
        (
            "European and Brazilian Portuguese share grammar but diverge sharply in rhythm, vowel "
            "reduction, and vocabulary. European Portuguese reduces unstressed vowels almost to silence "
            "— 'obrigado' sounds like 'brigadu'. Brazilian Portuguese is more open and syllable-timed. "
            "If you were assessed in European Portuguese, focus on consonant precision and reduced vowel "
            "sounds. If in Brazilian, open vowel pronunciation and 'você' (rather than 'tu') is your "
            "baseline. Grammar is largely shared; pronunciation and register diverge most."
        ),
    ),
    "ru": (
        "Aspect pairs — the shortcut to sounding natural",
        (
            "Russian verbs come in pairs — imperfective and perfective — and the choice between them "
            "carries meaning that English handles with tense. Imperfective describes ongoing or repeated "
            "action; perfective describes completed action with a result. 'Читать / прочитать' (to read / "
            "to finish reading). A practical approach: when the result matters — use perfective. When the "
            "process or habit matters — use imperfective. Learning verbs in pairs from the start is "
            "faster than correcting habit later."
        ),
    ),
    "bg": (
        "Article placement — what makes Bulgarian different",
        (
            "Bulgarian is unusual among Slavic languages in having a definite article — but it attaches "
            "as a suffix, not a separate word. 'Книга' (a book) becomes 'книгата' (the book). The form "
            "varies by gender and grammatical role. The practical focus at A2-B1: master the four article "
            "forms (masculine, feminine, neuter, plural) and the rule that adjectives in a noun phrase "
            "take the article, not the noun itself — 'хубавата книга' not 'хубава книгата'. This single "
            "rule eliminates the most common article patterns."
        ),
    ),
    "zh": (
        "Measure words — the pattern behind them",
        (
            "Chinese measure words (量词) feel arbitrary but follow patterns. 条 is for long, flexible "
            "things (fish, rivers, roads, trousers). 张 is for flat surfaces (paper, tables, faces). "
            "本 is for bound items (books, notebooks). 把 is for things with handles. Learning the "
            "category behind each measure word is faster than memorising each individually. At HSK 3-4, "
            "the ten most common measure words — 个, 条, 张, 本, 把, 只, 匹, 块, 件, 双 — cover roughly "
            "70% of daily usage."
        ),
    ),
}

# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

_BASE_WRAPPER = (
    '<div style="font-family: Georgia, serif; max-width: 580px; margin: 0 auto; '
    'color: #1A1A1A; font-size: 15px; line-height: 1.6;">'
    "{content}"
    "<br>"
    '<p style="color: #888; font-size: 13px; margin-top: 32px;">'
    'LingoGrade — <a href="https://www.lingograde.com" style="color: #2563AB;">lingograde.com</a>'
    "</p>"
    "</div>"
)


def _wrap(content: str) -> str:
    """Wrap content in the standard base HTML wrapper."""
    return _BASE_WRAPPER.format(content=content)


def _p(text: str) -> str:
    """Return a paragraph HTML element."""
    return f"<p>{text}</p>"


def _a(href: str, label: str) -> str:
    """Return an inline anchor styled as a CTA link."""
    return (
        f'<a href="{href}" style="color: #2563AB; font-weight: bold;">{label}</a>'
    )


def _sig(name: str, org: str = "LingoGrade") -> str:
    """Return HTML and text signature block."""
    return f"<p>{name}<br>{org}</p>"


# ---------------------------------------------------------------------------
# Post-assessment sequence
# ---------------------------------------------------------------------------


def post_assessment_day1(
    first_name: str,
    cefr_level: str,
    specific_pattern: str,
    discounted_price,
    full_price,
    currency: str,
    assessor_name: str,
    language: str,
) -> dict:
    """
    Day 1 — sent immediately after report delivery.
    Highlights one specific pattern and offers the homework check.
    """
    subject = f"One pattern from your {language} session"

    text = (
        f"Hi {first_name},\n\n"
        f"In your report, you'll notice {specific_pattern}.\n\n"
        f"This is one of the most common patterns at {cefr_level} — and one of the most "
        "responsive to targeted practice.\n\n"
        "If you'd like to work on it between now and your next session, the homework check "
        "gives you a written exercise built around your specific patterns, with detailed "
        "corrections returned within 55 minutes.\n\n"
        f"This week: {currency} {discounted_price} (regular {currency} {full_price}).\n\n"
        "If the report itself gives you enough to work with, that's completely fine too.\n\n"
        f"{assessor_name}\n"
        "LingoGrade\n\n"
        "https://www.lingograde.com/shop#homework"
    )

    content = (
        _p(f"Hi {first_name},")
        + _p(f"In your report, you'll notice {specific_pattern}.")
        + _p(
            f"This is one of the most common patterns at {cefr_level} — and one of the most "
            "responsive to targeted practice."
        )
        + _p(
            "If you'd like to work on it between now and your next session, the homework check "
            "gives you a written exercise built around your specific patterns, with detailed "
            "corrections returned within 55 minutes."
        )
        + _p(
            f"This week: {currency} {discounted_price} (regular {currency} {full_price})."
        )
        + _p("If the report itself gives you enough to work with, that's completely fine too.")
        + _p(
            _a("https://www.lingograde.com/shop#homework", "Homework check — book here")
        )
        + _sig(assessor_name)
    )

    return {"subject": subject, "html": _wrap(content), "text": text}


def post_assessment_day3(
    first_name: str,
    language: str,
    discounted_price,
    full_price,
    currency: str,
    assessor_name: str,
    segment: str = "full",
) -> dict:
    """
    Day 3 — follows up on the assessment, pitches the reassessment at 8 weeks.
    segment param is retained for future A/B use; copy is consistent across segments.
    """
    subject = f"It sounds like {language} matters to you"

    text = (
        f"Hi {first_name},\n\n"
        f"It seems like you've been thinking about where your {language} stands — that's why "
        "you booked the assessment in the first place.\n\n"
        "The report gives you a snapshot. What it can't show is how those patterns change "
        "over time.\n\n"
        "The reassessment at eight weeks gives you a before-and-after comparison — same "
        "assessor, same methodology, clear progress data.\n\n"
        f"This week: {currency} {discounted_price} (regular {currency} {full_price}).\n\n"
        "If you'd rather focus on the report for now and decide later, the reassessment is "
        "always available.\n\n"
        f"{assessor_name}\n"
        "LingoGrade\n\n"
        "https://www.lingograde.com/shop#reassessment"
    )

    content = (
        _p(f"Hi {first_name},")
        + _p(
            f"It seems like you've been thinking about where your {language} stands — "
            "that's why you booked the assessment in the first place."
        )
        + _p(
            "The report gives you a snapshot. What it can't show is how those patterns "
            "change over time."
        )
        + _p(
            "The reassessment at eight weeks gives you a before-and-after comparison — "
            "same assessor, same methodology, clear progress data."
        )
        + _p(
            f"This week: {currency} {discounted_price} (regular {currency} {full_price})."
        )
        + _p(
            "If you'd rather focus on the report for now and decide later, the reassessment "
            "is always available."
        )
        + _p(
            _a(
                "https://www.lingograde.com/shop#reassessment",
                "Book the reassessment",
            )
        )
        + _sig(assessor_name)
    )

    return {"subject": subject, "html": _wrap(content), "text": text}


def post_assessment_day5(
    first_name: str,
    discounted_price,
    full_price,
    currency: str,
    assessor_name: str,
) -> dict:
    """
    Day 5 — promotes the double homework check bundle.
    """
    subject = "Easier now than later"

    text = (
        f"Hi {first_name},\n\n"
        "Most language patterns are easier to address while they're fresh in your awareness.\n\n"
        "The double homework check gives you two targeted exercises — one for your strongest "
        "pattern, one for your developing area — with corrections returned within 55 minutes each.\n\n"
        f"This week: {currency} {discounted_price} for both (regular {currency} {full_price}).\n\n"
        "If you'd prefer to work at your own pace, the report has everything you need.\n\n"
        f"{assessor_name}\n"
        "LingoGrade\n\n"
        "https://www.lingograde.com/shop#homework-bundle"
    )

    content = (
        _p(f"Hi {first_name},")
        + _p(
            "Most language patterns are easier to address while they're fresh in your awareness."
        )
        + _p(
            "The double homework check gives you two targeted exercises — one for your strongest "
            "pattern, one for your developing area — with corrections returned within 55 minutes each."
        )
        + _p(
            f"This week: {currency} {discounted_price} for both (regular {currency} {full_price})."
        )
        + _p(
            "If you'd prefer to work at your own pace, the report has everything you need."
        )
        + _p(
            _a(
                "https://www.lingograde.com/shop#homework-bundle",
                "Double homework check — book here",
            )
        )
        + _sig(assessor_name)
    )

    return {"subject": subject, "html": _wrap(content), "text": text}


def post_assessment_day7(
    first_name: str,
    assessor_name: str,
) -> dict:
    """
    Day 7 — soft close, no CTA link.
    """
    subject = "When you're ready"

    text = (
        f"Hi {first_name},\n\n"
        "Your report has the full picture. If you want to take it further — lessons, homework, "
        "reassessment — it's all there whenever you decide.\n\n"
        "No rush from our side.\n\n"
        f"{assessor_name}\n"
        "LingoGrade"
    )

    content = (
        _p(f"Hi {first_name},")
        + _p(
            "Your report has the full picture. If you want to take it further — lessons, "
            "homework, reassessment — it's all there whenever you decide."
        )
        + _p("No rush from our side.")
        + _sig(assessor_name)
    )

    return {"subject": subject, "html": _wrap(content), "text": text}


def post_assessment_day30(
    first_name: str,
    language: str,
) -> dict:
    """
    Day 30 — value-add insight email. No CTA, sender is LingoGrade not assessor.
    language should be a language code (e.g. "en", "de") from LANGUAGE_INSIGHTS,
    or a full language name string (fallback generic insight used if not found).
    """
    # Resolve language code
    lang_key = language.lower()
    if lang_key not in LANGUAGE_INSIGHTS:
        # Try to match by full name
        for code, name in LANGUAGE_NAMES.items():
            if name.lower() == lang_key:
                lang_key = code
                break

    lang_display = LANGUAGE_NAMES.get(lang_key, language)

    if lang_key in LANGUAGE_INSIGHTS:
        topic_title, insight_text = LANGUAGE_INSIGHTS[lang_key]
    else:
        topic_title = "A note on language development"
        insight_text = (
            "Consistent, focused practice over short daily sessions outperforms irregular "
            "long study blocks for most adult learners. Twenty minutes of deliberate practice "
            "— targeting a specific pattern — produces faster progress than an hour of general "
            "review. Your report identifies which patterns are most productive to focus on first."
        )

    subject = f"{lang_display} insight: {topic_title}"

    text = (
        f"Hi {first_name},\n\n"
        f"{insight_text}\n\n"
        "Your report and all available tools are in your dashboard whenever you want them.\n\n"
        "LingoGrade"
    )

    content = (
        _p(f"Hi {first_name},")
        + _p(insight_text)
        + _p(
            "Your report and all available tools are in your dashboard whenever you want them."
        )
        + _sig("LingoGrade", "")
    )

    return {"subject": subject, "html": _wrap(content), "text": text}


def post_assessment_day56(
    first_name: str,
    language: str,
    one_specific_finding: str,
    booking_link: str,
    assessor_name: str,
) -> dict:
    """
    Day 56 (8 weeks) — reassessment push using Voss "would it be wrong" framing.
    """
    subject = "Would it be wrong to find out?"

    text = (
        f"Hi {first_name},\n\n"
        f"Eight weeks ago, your {language} assessment showed {one_specific_finding}.\n\n"
        "Patterns like that tend to shift with time — sometimes faster than you'd expect.\n\n"
        "Would it be wrong to see how they've changed?\n\n"
        "The reassessment uses the same methodology and gives you a direct before-and-after "
        "comparison.\n\n"
        f"Book when you're ready: {booking_link}\n\n"
        "If now isn't the right time, your original report and data stay in your dashboard "
        "indefinitely.\n\n"
        f"{assessor_name}\n"
        "LingoGrade"
    )

    content = (
        _p(f"Hi {first_name},")
        + _p(
            f"Eight weeks ago, your {language} assessment showed {one_specific_finding}."
        )
        + _p(
            "Patterns like that tend to shift with time — sometimes faster than you'd expect."
        )
        + _p("Would it be wrong to see how they've changed?")
        + _p(
            "The reassessment uses the same methodology and gives you a direct "
            "before-and-after comparison."
        )
        + _p(f"Book when you're ready: {_a(booking_link, booking_link)}")
        + _p(
            "If now isn't the right time, your original report and data stay in your "
            "dashboard indefinitely."
        )
        + _sig(assessor_name)
    )

    return {"subject": subject, "html": _wrap(content), "text": text}


# ---------------------------------------------------------------------------
# Partner onboarding sequence
# ---------------------------------------------------------------------------


def partner_onboarding_day0(
    first_name: str,
    dashboard_link: str,
    partner_manager_name: str,
) -> dict:
    """
    Partner Day 0 — account activation confirmation with dashboard link.
    """
    subject = "Your partner dashboard is live"

    text = (
        f"Hi {first_name},\n\n"
        f"Your partner account is active. Here is your dashboard: {dashboard_link}\n\n"
        "Inside you will find:\n"
        "- Your personal referral link (live now — share it anywhere)\n"
        "- Sticker order tracking (if applicable)\n"
        "- Earnings and referral history\n\n"
        "Your referral link works immediately. Every assessment booked through it is tracked "
        "and credited to your account.\n\n"
        "If anything in the dashboard is unclear, reply to this email.\n\n"
        f"{partner_manager_name}\n"
        "LingoGrade Partners"
    )

    content = (
        _p(f"Hi {first_name},")
        + _p(
            f"Your partner account is active. Here is your dashboard: "
            f"{_a(dashboard_link, dashboard_link)}"
        )
        + "<p>Inside you will find:<br>"
        + "— Your personal referral link (live now — share it anywhere)<br>"
        + "— Sticker order tracking (if applicable)<br>"
        + "— Earnings and referral history</p>"
        + _p(
            "Your referral link works immediately. Every assessment booked through it is "
            "tracked and credited to your account."
        )
        + _p("If anything in the dashboard is unclear, reply to this email.")
        + _sig(partner_manager_name, "LingoGrade Partners")
    )

    return {"subject": subject, "html": _wrap(content), "text": text}


def partner_onboarding_day3(
    first_name: str,
    referral_link: str,
    partner_manager_name: str,
) -> dict:
    """
    Partner Day 3 — three practical first-referral tactics.
    """
    subject = "Three ways partners get their first referral"

    text = (
        f"Hi {first_name},\n\n"
        "Partners who earn first tend to do one of three things:\n\n"
        "1. Share the referral link in a class group chat (WhatsApp, Telegram, or similar).\n"
        "2. Mention LingoGrade during a lesson when a student asks about their level.\n"
        "3. Place a sticker where students wait — lobby, hallway, co-working space.\n\n"
        f"Your link: {referral_link}\n\n"
        "None of these require a pitch. The link does the explaining.\n\n"
        "If you have questions about how referrals are tracked, reply here.\n\n"
        f"{partner_manager_name}\n"
        "LingoGrade Partners"
    )

    content = (
        _p(f"Hi {first_name},")
        + _p("Partners who earn first tend to do one of three things:")
        + (
            "<ol style='margin: 0; padding-left: 20px;'>"
            "<li>Share the referral link in a class group chat (WhatsApp, Telegram, or similar).</li>"
            "<li>Mention LingoGrade during a lesson when a student asks about their level.</li>"
            "<li>Place a sticker where students wait — lobby, hallway, co-working space.</li>"
            "</ol>"
        )
        + _p(f"Your link: {_a(referral_link, referral_link)}")
        + _p("None of these require a pitch. The link does the explaining.")
        + _p("If you have questions about how referrals are tracked, reply here.")
        + _sig(partner_manager_name, "LingoGrade Partners")
    )

    return {"subject": subject, "html": _wrap(content), "text": text}


def partner_onboarding_day7(
    first_name: str,
    referral_link: str,
    partner_manager_name: str,
    has_stickers: bool = True,
) -> dict:
    """
    Partner Day 7 — sticker placement guidance (or digital-only note if no stickers).
    """
    subject = "Where stickers work best"

    if has_stickers:
        text = (
            f"Hi {first_name},\n\n"
            "If you ordered stickers, here is what the data shows:\n\n"
            "- Eye-level surfaces near seating (cafés, waiting areas) get the most scans.\n"
            "- Smooth, clean surfaces hold longest — glass, laminate, painted walls.\n"
            "- One sticker per location is enough. Clustering reduces scans.\n\n"
            "Your sticker tracking is live in your dashboard. Every scan is logged with "
            "location and timestamp.\n\n"
            "If you did not order stickers, your referral link covers the same ground digitally.\n\n"
            f"{partner_manager_name}\n"
            "LingoGrade Partners"
        )

        content = (
            _p(f"Hi {first_name},")
            + _p("If you ordered stickers, here is what the data shows:")
            + (
                "<ul style='margin: 0; padding-left: 20px;'>"
                "<li>Eye-level surfaces near seating (cafés, waiting areas) get the most scans.</li>"
                "<li>Smooth, clean surfaces hold longest — glass, laminate, painted walls.</li>"
                "<li>One sticker per location is enough. Clustering reduces scans.</li>"
                "</ul>"
            )
            + _p(
                "Your sticker tracking is live in your dashboard. Every scan is logged with "
                "location and timestamp."
            )
            + _p(
                "If you did not order stickers, your referral link covers the same ground digitally."
            )
            + _sig(partner_manager_name, "LingoGrade Partners")
        )
    else:
        text = (
            f"Hi {first_name},\n\n"
            "Your referral link is just as effective as physical stickers for reaching "
            "potential students digitally.\n\n"
            f"Your link: {referral_link}\n\n"
            "Sharing it in the right context — a group chat, a direct message after a "
            "lesson, a social post — produces the same result as a well-placed sticker.\n\n"
            "Every click and booking through your link is tracked in your dashboard.\n\n"
            f"{partner_manager_name}\n"
            "LingoGrade Partners"
        )

        content = (
            _p(f"Hi {first_name},")
            + _p(
                "Your referral link is just as effective as physical stickers for reaching "
                "potential students digitally."
            )
            + _p(f"Your link: {_a(referral_link, referral_link)}")
            + _p(
                "Sharing it in the right context — a group chat, a direct message after a "
                "lesson, a social post — produces the same result as a well-placed sticker."
            )
            + _p("Every click and booking through your link is tracked in your dashboard.")
            + _sig(partner_manager_name, "LingoGrade Partners")
        )

    return {"subject": subject, "html": _wrap(content), "text": text}


# ---------------------------------------------------------------------------
# Subscriber sequence
# ---------------------------------------------------------------------------


def subscriber_welcome_day0(
    first_name: str,
    subscription_tier: str,
    first_session_date: str,
    first_session_time: str,
    assessor_name: str,
    dashboard_link: str,
    homework_included: bool = True,
    reassessment_date: str = None,
) -> dict:
    """
    Subscriber welcome — sent immediately on subscription activation.
    subscription_tier: e.g. "Weekly Lesson", "Complete Programme"
    first_session_date: e.g. "Tuesday 8 April"
    first_session_time: e.g. "18:00 CET"
    reassessment_date: optional, e.g. "Tuesday 3 June" (shown if provided)
    """
    subject = f"Your {subscription_tier} subscription is active"

    # Determine tier class
    tier_lower = subscription_tier.lower()
    is_complete = "complete" in tier_lower or "programme" in tier_lower

    # Homework line
    if homework_included:
        homework_line = (
            "Homework is included in your subscription. After each session, you'll receive "
            "a written exercise targeting the patterns from that lesson. Corrections are "
            "returned within 55 minutes."
        )
        homework_line_html = homework_line
    else:
        homework_line = None
        homework_line_html = None

    # Reassessment line
    if reassessment_date:
        reassessment_line = (
            f"Your reassessment is scheduled for {reassessment_date} — same assessor, "
            "same methodology, clear before-and-after data."
        )
        reassessment_line_html = reassessment_line
    elif is_complete:
        reassessment_line = (
            "The reassessment at eight weeks is included in your programme. "
            "Your assessor will confirm the date after your third session."
        )
        reassessment_line_html = reassessment_line
    else:
        reassessment_line = None
        reassessment_line_html = None

    # Build text
    lines = [
        f"Hi {first_name},",
        "",
        f"Your {subscription_tier} subscription is active.",
        "",
        f"First session: {first_session_date} at {first_session_time}.",
        "Add it to your calendar — a .ics file is attached to this email.",
        "",
    ]
    if homework_line:
        lines += [homework_line, ""]
    if reassessment_line:
        lines += [reassessment_line, ""]
    lines += [
        f"Your dashboard: {dashboard_link}",
        "",
        f"{assessor_name}",
        "LingoGrade",
    ]
    text = "\n".join(lines)

    # Build HTML
    html_parts = [
        _p(f"Hi {first_name},"),
        _p(f"Your {subscription_tier} subscription is active."),
        _p(
            f"First session: <strong>{first_session_date}</strong> at "
            f"<strong>{first_session_time}</strong>.<br>"
            "Add it to your calendar — a .ics file is attached to this email."
        ),
    ]
    if homework_line_html:
        html_parts.append(_p(homework_line_html))
    if reassessment_line_html:
        html_parts.append(_p(reassessment_line_html))
    html_parts.append(
        _p(f"Your dashboard: {_a(dashboard_link, dashboard_link)}")
    )
    html_parts.append(_sig(assessor_name))

    return {"subject": subject, "html": _wrap("".join(html_parts)), "text": text}


def subscriber_post_session(
    first_name: str,
    session_date: str,
    next_session_date: str,
    next_session_time: str,
    assessor_name: str,
    homework_included: bool = True,
) -> dict:
    """
    Transactional post-session email. Sent after each completed session.
    session_date: e.g. "Tuesday 8 April" — used in subject and body
    next_session_date: e.g. "Tuesday 15 April"
    next_session_time: e.g. "18:00 CET"
    """
    subject = f"Your session report — {session_date}"

    if homework_included:
        homework_block = (
            "Your homework exercise for this session has been sent in a separate email. "
            "Complete it before your next session for the best results — corrections come "
            "back within 55 minutes of submission."
        )
        homework_block_html = homework_block
    else:
        homework_block = None
        homework_block_html = None

    lines = [
        f"Hi {first_name},",
        "",
        f"Your session report for {session_date} is now in your dashboard.",
        "It includes the patterns covered, notes from the session, and recommended focus areas.",
        "",
    ]
    if homework_block:
        lines += [homework_block, ""]
    lines += [
        f"Next session: {next_session_date} at {next_session_time}.",
        "A calendar reminder was sent when you first subscribed. "
        "Reply here if you need to reschedule.",
        "",
        f"{assessor_name}",
        "LingoGrade",
    ]
    text = "\n".join(lines)

    html_parts = [
        _p(f"Hi {first_name},"),
        _p(
            f"Your session report for {session_date} is now in your dashboard. "
            "It includes the patterns covered, notes from the session, and recommended "
            "focus areas."
        ),
    ]
    if homework_block_html:
        html_parts.append(_p(homework_block_html))
    html_parts.append(
        _p(
            f"Next session: <strong>{next_session_date}</strong> at "
            f"<strong>{next_session_time}</strong>.<br>"
            "Reply here if you need to reschedule."
        )
    )
    html_parts.append(_sig(assessor_name))

    return {"subject": subject, "html": _wrap("".join(html_parts)), "text": text}
