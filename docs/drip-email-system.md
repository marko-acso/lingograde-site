# LingoGrade Drip Email System — Camp + Voss Sequence

**Version 1.0 — Confidential Internal Document**
**"The most important communication is the one you don't send."**

---

## Table of Contents

1. [Philosophy](#1-philosophy)
2. [Architecture & Triggers](#2-architecture--triggers)
3. [Segmentation](#3-segmentation)
4. [The 5-Day Sequence](#4-the-5-day-sequence)
5. [Day 0 — The Report (No Sell)](#5-day-0--the-report)
6. [Day 1 — The Homework Anchor](#6-day-1--the-homework-anchor)
7. [Day 3 — Voss Label + Camp Vision](#7-day-3--voss-label--camp-vision)
8. [Day 5 — Thaler Friction + Kahneman Frame](#8-day-5--thaler-friction--kahneman-frame)
9. [Day 7 — Camp Pure](#9-day-7--camp-pure)
10. [Day 10 — Silence](#10-day-10--silence)
11. [Day 30 — Value Newsletter](#11-day-30--value-newsletter)
12. [Week 8 — Reassessment Window](#12-week-8--reassessment-window)
13. [Partner Onboarding Sequence](#13-partner-onboarding-sequence)
14. [Subscriber Welcome + Schedule](#14-subscriber-welcome--schedule)
15. [Homework Delivery Email](#15-homework-delivery-email)
16. [24-Language Matrix](#16-24-language-matrix)
17. [Discount Ladder](#17-discount-ladder)
18. [Personalisation Variables](#18-personalisation-variables)
19. [Automation Rules](#19-automation-rules)
20. [Anti-Patterns](#20-anti-patterns)
21. [Metrics & Success Criteria](#21-metrics--success-criteria)

---

## 1. Philosophy

Every email LingoGrade sends must pass three tests:

1. **The Friend Test:** Would a friend send this? If it sounds weird over coffee, rewrite it.
2. **The Camp Test:** Does this push, or does it present? If it pushes, rewrite it.
3. **The Silence Test:** Is this email necessary? Would the student's experience be worse without it? If no, don't send it.

### Core Principles

- **Day 0 is sacred.** The report arrives alone. No upsell. No CTA beyond "here is your report." The student needs space to absorb what they received.
- **Drip, don't pour.** One email per touchpoint. Never stack. Never "just wanted to follow up."
- **Discounts decay.** The discount ladder goes 20% → 15% → 10% → 0%. Prices never decrease after the ladder ends. This is structural, not artificial — early action genuinely costs less.
- **Silence is a message.** After Day 10, we stop. The absence communicates: "We don't need you to buy. We're here if you want us."
- **Max 2 emails per week.** Even during the active drip sequence. If Day 3 and Day 5 fall in the same week, that's the cap. No newsletter stacks on top.

### What We Never Send

- "We miss you!" (Guilt framing. We don't miss their wallet.)
- "Last chance!" (Unless a real, published deadline exists.)
- "You left something behind!" (Cart abandonment guilt.)
- "Don't forget!" (Implies they're forgetful. Patronising.)
- Any email with more than one CTA. One email, one action, one decision.
- Any email longer than 200 words in the body.

### Lozanov Language Rule

Every email is student-facing copy. The same language rules that govern reports apply here:

- **Never use "error," "mistake," "wrong," "fail," or "weakness."** Use "pattern," "focus area," "developing structure," or "growth point."
- **Never frame the student's level as a deficit.** "Your B1 assessment" — not "You scored B1" or "You're still at B1."
- This applies to all 24 language variants. Translators must be briefed: the target-language equivalent of "error" is equally banned.
- If `{specific_pattern_reference}` or `{one_specific_finding}` pulls text containing banned words from the report system, the variable must be filtered before injection. Fallback to generic phrasing rather than sending banned language.

### Berne Tone Rule

Every email operates from **Adult ego state** — factual, calm, respectful of the reader's autonomy. The reader is addressed as an equal making their own decisions, never as a child being guided.

| Banned (Parent → Child) | Required (Adult → Adult) |
|--------------------------|--------------------------|
| "We're so proud of your progress!" | "Your patterns have shifted." |
| "Don't worry if you're not ready yet." | "Available whenever you decide." |
| "We know this can feel overwhelming." | "Take your time with it." |
| "Great job booking your assessment!" | "Your session is confirmed." |

If an email draft reads like a teacher praising a student or a parent reassuring a child, rewrite it. The student is an adult. Speak to them like one.

---

## 2. Architecture & Triggers

### Trigger Events

| Event | Sequence Started | Delay |
|-------|-----------------|-------|
| Assessment completed | 5-Day Post-Assessment | Immediate (Day 0) |
| Homework purchased | Homework Delivery | On completion (55 min) |
| Reassessment window opens | Week 8 Nudge | 8 weeks post-assessment |
| No activity for 30 days | Value Newsletter | Day 30 |
| Partner signup | Partner Onboarding | Immediate |
| Subscription started | Welcome + Schedule | Immediate |

### Suppression Rules

- **If student purchases:** Suppress all remaining drip emails for that product. Never advertise what they already own.
- **If student unsubscribes:** Full stop. No "are you sure?" No re-engagement sequence. Respect the decision.
- **If student books reassessment:** Suppress Week 8 nudge. They already acted.
- **If student has active subscription:** Suppress all individual product emails. Subscriber gets separate communication track.
- **Max 1 email per 48 hours** across all sequences. If two triggers fire on the same day, the higher-priority email sends; the other is suppressed entirely (not delayed).

### Priority Hierarchy

1. Transactional (report delivery, booking confirmation, receipt)
2. Active drip sequence (Days 1-7)
3. Milestone (Week 8 reassessment)
4. Value newsletter (Day 30+)

Transactional always sends. All others respect the 48-hour minimum gap.

---

## 3. Segmentation

### Primary Segments

| Segment | Trigger | Drip Variation |
|---------|---------|----------------|
| **Individual — Quick** | Booked Quick Assessment | Upsell path: HW → Full → Reassess |
| **Individual — Full** | Booked Full Assessment | Upsell path: HW → Reassess → Lessons |
| **Individual — DeepDive** | Booked DeepDive | Upsell path: HW → Reassess → Subscription |
| **Corporate** | Company booking | ROI framing, team language, invoice mention |
| **Kids** | Age < 16 | Parent-addressed, different tone, no direct upsell |
| **Returning** | Has previous assessment | Progress comparison framing |

### Secondary Personalisation

- **CEFR level** — A1/A2 get encouragement-heavy copy; B2/C1 get precision-focused copy
- **Language assessed** — Subject lines and examples reference the actual language
- **Assessor name** — "Marco noted..." or assessor's real name if preferred
- **Session type** — 15 min vs 25 min vs 40 min affects what products make sense to mention

---

## 4. The 5-Day Sequence — Overview

| Day | Purpose | Discount | Tone | WISE Lens |
|-----|---------|----------|------|-----------|
| 0 | Report delivery | — | Calm, factual | — |
| 1 | Homework anchor | 20% off HW | Observational | Thaler (nudge) |
| 3 | Reassessment vision | 15% off Reassess | Empathetic | Voss (label) + Camp (vision) |
| 5 | Double HW bundle | 10% off 2x HW | Practical | Thaler (friction) + Kahneman (loss) |
| 7 | Lesson introduction | 0% (full price) | Warm, final | Camp pure (zero need) |
| 10 | Nothing | — | — | Silence (the message IS nothing) |
| 30 | Value article | — | Generous | Give without asking |
| 56 | Reassessment window | — | Curious | Camp (no-oriented question) |

---

## 5. Day 0 — The Report

**Timing:** Immediately upon report generation (within assessment SLA).

**Subject line:** `Your {language} assessment report is ready`

**Body:**

```
Hi {first_name},

Your report is attached. Take your time with it — there's a lot in there.

If any questions come up after you've read through it, reply to this email. We'll get back to you within 24 hours.

{assessor_first_name}
LingoGrade
```

**Rules:**
- No product mention. None.
- No "we hope you enjoyed your session."
- No social media links.
- Report attached as PDF. No "click here to view" (friction).
- Plain text preferred. Minimal HTML if needed for PDF attachment rendering.
- Sender: assessor's name, not "LingoGrade Team."

---

## 6. Day 1 — The Homework Anchor

**Timing:** 24 hours after Day 0.

**Discount:** 20% off Homework Check (29.95 → 23.95).

**Subject line template (by segment):**

| Segment | Subject |
|---------|---------|
| Quick/Full | `One pattern from your {language} session` |
| DeepDive | `A detail from your {language} analysis` |
| Corporate | `One finding from {first_name}'s assessment` |
| Kids | `A note for {first_name}'s parents` |

**Body structure:**

```
Hi {first_name},

In your report, you'll notice {specific_pattern_reference}.

This is one of the most common patterns at {cefr_level} — and one of the most responsive to targeted practice.

If you'd like to work on it between now and your next session, the homework check gives you a written exercise built around your specific patterns, with detailed corrections returned within 55 minutes.

This week: {currency} {discounted_price} (regular {currency} {full_price}).

If the report itself gives you enough to work with, that's completely fine too.

{assessor_first_name}
LingoGrade
```

**Rules:**
- `{specific_pattern_reference}` must be pulled from the actual report, not generic. If the system cannot populate this, use: "you'll notice some patterns in your verb usage" (vague but honest).
- Price stated once. No "only" or "just."
- BYAF close: "completely fine too."
- One link. One CTA. No secondary offers.

---

## 7. Day 3 — Voss Label + Camp Vision

**Timing:** 72 hours after Day 0.

**Discount:** 15% off Reassessment (139.95 → 118.95).

**Subject line template:**

| Segment | Subject |
|---------|---------|
| Quick/Full | `It sounds like {language} matters to you` |
| DeepDive | `The patterns we discussed on {session_day}` |
| Corporate | `{first_name}'s {language} trajectory` |
| Returning | `How {language} has changed since last time` |

**Body structure:**

```
Hi {first_name},

It seems like you've been thinking about where your {language} stands — that's why you booked the assessment in the first place.

The report gives you a snapshot. What it can't show is how those patterns change over time.

The reassessment at eight weeks gives you a before-and-after comparison — same assessor, same methodology, clear progress data.

This week: {currency} {discounted_price} (regular {currency} {full_price}).

If you'd rather focus on the report for now and decide later, the reassessment is always available.

{assessor_first_name}
LingoGrade
```

**Technique breakdown:**
- **Line 1:** Voss label — names the emotion/motivation without assuming it. "It seems like..." is a label, not a statement. If wrong, the student corrects it internally. If right, they feel understood.
- **Line 2:** Camp vision — "how those patterns change over time" paints a future without prescribing it.
- **Close:** BYAF + safety valve. "Always available" removes urgency.

---

## 8. Day 5 — Thaler Friction + Kahneman Frame

**Timing:** 120 hours after Day 0.

**Discount:** 10% off 2x Homework Bundle (59.90 → 53.95).

**Subject line template:**

| Segment | Subject |
|---------|---------|
| All (except Kids) | `Easier now than later` |
| Corporate | `{first_name}'s development path` |

**Body structure:**

```
Hi {first_name},

Most language patterns are easier to address while they're fresh in your awareness.

The double homework check gives you two targeted exercises — one for your strongest pattern, one for your developing area — with corrections returned within 55 minutes each.

This week: {currency} {discounted_price} for both (regular {currency} {full_price}).

If you'd prefer to work at your own pace, the report has everything you need.

{assessor_first_name}
LingoGrade
```

**Technique breakdown:**
- **Subject:** Kahneman loss-frame. "Easier now than later" implies cost of delay without creating urgency. It is a true statement about memory and pattern awareness.
- **Thaler friction reduction:** "Two exercises" with one link is simpler than deciding on one exercise twice. Bundling reduces decision count.
- **Safety valve:** "Report has everything you need" — the free option remains valid.

---

## 9. Day 7 — Camp Pure

**Timing:** 168 hours after Day 0.

**Discount:** 0%. Full price.

**Subject line template:**

| Segment | Subject |
|---------|---------|
| All | `When you're ready` |

**Body structure:**

```
Hi {first_name},

Your report has the full picture. If you want to take it further — lessons, homework, reassessment — it's all there whenever you decide.

No rush from our side.

{assessor_first_name}
LingoGrade
```

**Rules:**
- This is the last active email. It must communicate finality without saying "last chance."
- No product links in the body. If they want to act, they know where to find LingoGrade.
- No price mention. No discount. Pure Camp: zero need.
- "No rush from our side" is the most important sentence. It communicates that LingoGrade does not need this sale.
- Maximum 40 words in the body.

---

## 10. Day 10 — Silence

**Timing:** Never.

**What happens:** Nothing. No email is sent.

The absence is the message. The student has received four emails in ten days. Now they receive nothing. The contrast communicates:

1. LingoGrade is not desperate.
2. The drip had a structure — it was not infinite.
3. The student's inbox is respected.
4. If they come back, it will be because they chose to.

**Implementation:** This is not a "placeholder email set to draft." There is literally no Day 10 email in the system. The sequence ends at Day 7.

---

## 11. Day 30 — Value Newsletter

**Timing:** 30 days after assessment, if no purchase has been made.

**Discount:** None.

**Subject line:** `{language} insight: {topic_title}`

**Body structure:**

```
Hi {first_name},

{Short, genuinely useful language insight — 80-120 words. A tip about the specific language they were assessed in. Something they can use today, for free, without buying anything.}

Your report and all available tools are in your dashboard whenever you want them.

LingoGrade
```

**Rules:**
- This is a gift, not a funnel entry. No product mention beyond the dashboard reference.
- The insight must be real, specific to their language, and actually useful.
- If we cannot generate a quality insight for their language, do not send. Silence is better than filler.
- Sender: "LingoGrade" — not the assessor. Enough time has passed that personal tone from the assessor would feel contrived.

### Topic Bank (Examples by Language)

| Language | Topic |
|----------|-------|
| German | "The one preposition rule that fixes 60% of case errors" |
| French | "Why your brain fights the subjunctive — and what to do about it" |
| Spanish | "Ser vs estar: the trick that textbooks don't teach" |
| Italian | "Congiuntivo in conversation: when native speakers actually use it" |
| Russian | "Aspect pairs: the shortcut to sounding natural" |
| Portuguese | "Why Brazilian and European Portuguese feel like different languages" |

---

## 12. Week 8 — Reassessment Window

**Timing:** 56 days after original assessment.

**Discount:** None (reassessment is already priced as a follow-up at 139.95).

**Subject line:** `Would it be wrong to find out?`

**Body structure:**

```
Hi {first_name},

Eight weeks ago, your {language} assessment showed {one_specific_finding}.

Patterns like that tend to shift with time — sometimes faster than you'd expect.

Would it be wrong to see how they've changed?

The reassessment uses the same methodology and gives you a direct before-and-after comparison.

Book when you're ready: {booking_link}

If now isn't the right time, your original report and data stay in your dashboard indefinitely.

{assessor_first_name}
LingoGrade
```

**Technique breakdown:**
- **Subject:** Camp no-oriented question. The natural answer is "No, it wouldn't be wrong."
- **Line 1:** Personalised reference to actual assessment data.
- **"Tend to shift":** Observational. Not "you've improved" (presumptuous) or "you might not have improved" (deflating).
- **Booking link:** One link. No "Book Now" button. Just a link.
- **Safety valve:** "Your original report and data stay... indefinitely." No pressure. No expiry.

---

## 13. Partner Onboarding Sequence

**Trigger:** Partner signup completed.

**Timing:** Immediately upon partner account activation.

### Email 1 — Welcome + Dashboard Access (Day 0)

**Subject line:** `Your partner dashboard is live`

**Body:**

```
Hi {first_name},

Your partner account is active. Here is your dashboard: {dashboard_link}

Inside you will find:
- Your personal referral link (live now — share it anywhere)
- Sticker order tracking (if applicable)
- Earnings and referral history

Your referral link works immediately. Every assessment booked through it is tracked and credited to your account.

If anything in the dashboard is unclear, reply to this email.

{partner_manager_name}
LingoGrade Partners
```

**Rules:**
- One CTA: the dashboard link. No product upsells.
- No "congratulations" or "welcome aboard" — Adult-to-Adult. They signed up; now here are the tools.
- Sender: partner manager name, not "LingoGrade Team."

### Email 2 — First Referral Tips (Day 3)

**Subject line:** `Three ways partners get their first referral`

**Body:**

```
Hi {first_name},

Partners who earn first tend to do one of three things:

1. Share the referral link in a class group chat (WhatsApp, Telegram, or similar).
2. Mention LingoGrade during a lesson when a student asks about their level.
3. Place a sticker where students wait — lobby, hallway, co-working space.

Your link: {referral_link}

None of these require a pitch. The link does the explaining.

If you have questions about how referrals are tracked, reply here.

{partner_manager_name}
LingoGrade Partners
```

**Rules:**
- Practical, not motivational. No "you've got this" or "we believe in you."
- Three concrete actions, not abstract strategy.
- BYAF implied: the list is a menu, not a mandate.

### Email 3 — Sticker Placement Guide (Day 7)

**Subject line:** `Where stickers work best`

**Body:**

```
Hi {first_name},

If you ordered stickers, here is what the data shows:

- Eye-level surfaces near seating (cafés, waiting areas) get the most scans.
- Smooth, clean surfaces hold longest — glass, laminate, painted walls.
- One sticker per location is enough. Clustering reduces scans.

Your sticker tracking is live in your dashboard. Every scan is logged with location and timestamp.

If you did not order stickers, your referral link covers the same ground digitally.

{partner_manager_name}
LingoGrade Partners
```

**Rules:**
- Only sent if partner has sticker order OR after Day 3 email. Suppressed if partner unsubscribed.
- No pressure to order stickers. Digital referral link is positioned as equally valid.
- Data-driven framing ("what the data shows"), not opinion.
- This is the last partner onboarding email. Sequence ends here. Further communication is monthly partner newsletter only.

---

## 14. Subscriber Welcome + Schedule

**Trigger:** Subscription started (Weekly or Complete tier).

**Timing:** Immediately upon subscription activation.

### Email 1 — Welcome + What Happens Next (Day 0)

**Subject line:** `Your {subscription_tier} subscription is active`

**Body:**

```
Hi {first_name},

Your {subscription_tier} subscription is now active. Here is what happens next:

{if Weekly}
- One session per week, same assessor, same time slot.
- Your first session is {first_session_date} at {first_session_time}.
- Homework is included — it arrives within 55 minutes of each session.
- Flashcard app premium access is active in your dashboard.
{/if}

{if Complete}
- Sessions scheduled per your selected cadence.
- Full assessment + homework + flashcard premium + reassessment — all included.
- Your first session is {first_session_date} at {first_session_time}.
- Your reassessment is pre-booked at the 8-week mark.
{/if}

Calendar invite attached. Your dashboard shows your full schedule: {dashboard_link}

If you need to reschedule, reply to this email at least 24 hours before your session.

{assessor_first_name}
LingoGrade
```

**Rules:**
- Conditional content based on subscription tier. Only show what applies.
- Calendar invite attached as .ics file — reduce friction, do not make them find the booking manually.
- Sender: assigned assessor, not "LingoGrade Team." The subscriber has a named person.
- No upsell. They already bought the top tier. Respect the purchase.
- One CTA: dashboard link.

### Email 2 — After First Session (Day 1 post-session)

**Subject line:** `Your first session report`

**Body:**

```
Hi {first_name},

Your report from {session_date} is attached.

{if homework_included}
Your homework exercise is in progress and will arrive within 55 minutes.
{/if}

Your next session: {next_session_date} at {next_session_time}.

If anything in the report needs clarification, reply here.

{assessor_first_name}
LingoGrade
```

**Rules:**
- Transactional. Report delivery + next session reminder.
- No commentary on performance. The report speaks for itself.
- This template repeats after every session in the subscription. Keep it identical — predictability is a feature.
- Maximum 60 words in body.

---

## 15. Homework Delivery Email

**Trigger:** Homework exercise completed by assessor (within 55-minute SLA).

**Timing:** Immediately upon homework completion.

**Subject line:** `Your {language} homework corrections`

**Body:**

```
Hi {first_name},

Your homework corrections are attached.

The exercise focused on {homework_focus_area}. The corrections include specific notes on each pattern — read through them at your own pace.

If anything in the corrections is unclear, reply to this email. We will clarify within 24 hours.

{assessor_first_name}
LingoGrade
```

**Rules:**
- Transactional only. No upsell. No "ready for more?" No mention of other products.
- `{homework_focus_area}` pulled from the homework record — e.g., "dative prepositions" or "subjunctive usage." If unavailable, use: "the patterns identified in your assessment."
- Corrections attached as PDF. No "click here to view."
- Sender: the assessor who corrected the homework.
- Maximum 80 words in body.
- Lozanov rule applies: corrections document must never use "error," "mistake," or "wrong." Use "pattern," "focus area," "alternative structure."
- No follow-up email after this. The homework is delivered; the student works with it on their own terms.

---

## 16. 24-Language Matrix

All emails are sent in the student's native language (not the assessed language). The assessed language is referenced by name within the email.

### Supported Languages

| # | Language | Code | Formality | Tip Amounts |
|---|----------|------|-----------|-------------|
| 1 | German | de | Informal (du) | 20/10/5 |
| 2 | English | en | Neutral | 20/10/5 |
| 3 | French | fr | Formal (vous) | 20/10/5 |
| 4 | Spanish | es | Informal (tú) | 20/10/5 |
| 5 | Italian | it | Informal (tu) | 20/10/5 |
| 6 | Portuguese | pt | Informal (você) | 20/10/5 |
| 7 | Russian | ru | Informal (ты) | 20/10/5 |
| 8 | Ukrainian | uk | Informal (ти) | 20/10/5 |
| 9 | Serbian | sr | Informal (ти) | 20/10/5 |
| 10 | Croatian | hr | Informal (ti) | 20/10/5 |
| 11 | Bulgarian | bg | Informal (ти) | 20/10/5 |
| 12 | Romanian | ro | Informal (tu) | 20/10/5 |
| 13 | Polish | pl | Informal (ty) | 20/10/5 |
| 14 | Turkish | tr | Formal (siz) | 20/10/5 |
| 15 | Hungarian | hu | Formal (Ön) | 20/10/5 |
| 16 | Dutch | nl | Informal (je) | 20/10/5 |
| 17 | Swedish | sv | Informal (du) | 20/10/5 |
| 18 | Norwegian | no | Informal (du) | 20/10/5 |
| 19 | Danish | da | Informal (du) | 20/10/5 |
| 20 | Finnish | fi | Informal (sinä) | 20/10/5 |
| 21 | Chinese | zh | Formal (您) | 88/18/8 |
| 22 | Japanese | ja | Formal (です/ます) | 20/10/5 |
| 23 | Korean | ko | Formal (존댓말) | 20/10/5 |
| 24 | Arabic | ar | Formal (أنتم) | 20/10/5 |

### Translation Rules

- **Emails are in the student's native language.** A German speaker assessed in English receives emails in German.
- **Product names stay in English.** "Homework Check," "Quick Assessment," "DeepDive" — these are brand names, not translated.
- **Currency matches geo:** EUR for Europe, USD for US, CHF for Switzerland, GBP for UK. Same number, different symbol.
- **Chinese market exception:** Lucky number tip amounts (8/18/88). Bundle pricing uses 288.95.
- **Formality must match the site.** If the website uses informal (du/tú/ты), the email uses informal. If the site uses formal (vous/您), the email uses formal. No mixing.
- **RTL support:** Arabic emails must render right-to-left. Test before launch.
- **Unicode compliance:** All character sets must render correctly in all major email clients. Test Cyrillic, CJK, Arabic script in Gmail, Outlook, Apple Mail minimum.

### Translation Process

1. English master copy written and approved
2. Professional translation (not machine) for all 24 languages
3. Native speaker review for tone, formality, and cultural fit
4. Technical QA for character rendering, RTL, link placement
5. A/B test subject lines in top 5 languages (de, en, fr, es, it) before rolling out

---

## 17. Discount Ladder

| Day | Product | Discount | Example (EUR) |
|-----|---------|----------|---------------|
| 1 | Homework Check | 20% | 29.95 → 23.95 |
| 3 | Reassessment | 15% | 139.95 → 118.95 |
| 5 | 2x Homework Bundle | 10% | 59.90 → 53.95 |
| 7 | Lesson intro | 0% | 89.95 (full price) |
| 30+ | Everything | 0% | Full price permanently |

### Ladder Rules

- **Discounts never return.** Day 1's 20% is gone on Day 2. No "we extended it." No "one more chance."
- **No discount codes.** The discounted price is applied automatically via the link in the email. No copy-paste codes (friction + feels like a coupon site).
- **Discount applies to first purchase only.** Subsequent purchases of the same product are full price.
- **Discounts are per-assessment.** A student who takes a second assessment gets a fresh ladder.
- **Never mention the full-price future in the email.** "This week: 23.95" is enough. Do not write "normally 29.95, but this week only 23.95!" That's scarcity framing.
- **Corporate segment:** No discounts. Corporate pricing is already structured. The drip still runs but without the discount ladder.

### Price Display Rules

- State the price once, factually.
- Format: `{currency_symbol} {amount}` — e.g., `€ 23.95`, `$ 23.95`, `CHF 23.95`
- Never: "only," "just," "starting at," "from," "as low as"
- Never: strikethrough pricing (~~29.95~~ 23.95) — feels like a clearance sale
- The discounted price and regular price appear on the same line, factually: `This week: € 23.95 (regular € 29.95).`

---

## 18. Personalisation Variables

### Required Variables (must populate or suppress email)

| Variable | Source | Example |
|----------|--------|---------|
| `{first_name}` | Booking form | "Anna" |
| `{language}` | Assessment record | "German" |
| `{cefr_level}` | Report | "B1" |
| `{assessor_first_name}` | Session record | "Marco" |
| `{currency}` | Geo-detection | "€" |

### Optional Variables (enhance if available, skip if not)

| Variable | Source | Example |
|----------|--------|---------|
| `{specific_pattern_reference}` | Report JSON | "a recurring pattern in your use of dative prepositions" |
| `{session_day}` | Booking record | "Tuesday" |
| `{one_specific_finding}` | Report JSON | "your spoken fluency outpaced your grammatical accuracy by approximately one CEFR band" |
| `{discounted_price}` | Ladder calculation | "23.95" |
| `{full_price}` | Product catalog | "29.95" |
| `{booking_link}` | System-generated | URL |

### Fallback Rules

If a required variable cannot be populated:
- `{first_name}` missing → use "Hi there" (never "Dear Customer")
- `{language}` missing → suppress email entirely (cannot send a drip without knowing what was assessed)
- `{cefr_level}` missing → suppress Day 1 email (pattern reference depends on level context)
- `{assessor_first_name}` missing → use "Your assessor" (never "The LingoGrade Team" as sender during drip)

---

## 19. Automation Rules

### Sequence Entry

```
WHEN assessment_status = "completed"
AND report_status = "delivered"
AND student_email IS NOT NULL
AND student_unsubscribed = FALSE
THEN start_sequence("post_assessment", student_id)
```

### Suppression Logic

```
WHEN student purchases product_X
THEN suppress all emails mentioning product_X in active sequences

WHEN student.active_subscription = TRUE
THEN suppress all drip sequences
AND start_sequence("subscriber_welcome", student_id)

WHEN student.unsubscribed = TRUE
THEN suppress ALL sequences immediately
AND log("unsubscribe", student_id, timestamp)

WHEN student.age < 16
THEN route to "kids" segment
AND address all emails to parent_email
AND remove all discount mentions (parent, not child, makes purchase decisions)
```

### Rate Limiting

```
MAX 1 email per 48 hours per student (across all sequences)
MAX 2 emails per 7 days per student (across all sequences)
MAX 7 emails per 30 days per student (across all sequences)

IF rate_limit_exceeded:
  suppress lower-priority email (see Priority Hierarchy in Section 2)
  DO NOT delay — suppress entirely
```

### Link Tracking

- UTM parameters on all product links: `?utm_source=drip&utm_medium=email&utm_campaign=day{N}&utm_content={segment}`
- Click tracking: yes, for conversion measurement
- Open tracking: optional (Apple MPP makes it unreliable; do not make decisions based on open rates alone)
- Unsubscribe link: every email, above the fold, visible without scrolling. Legal requirement (GDPR, CAN-SPAM) and Camp requirement (freedom to leave).

---

## 20. Anti-Patterns

### Things That Will Never Exist in This System

| Anti-Pattern | Why It's Banned |
|--------------|-----------------|
| "We miss you!" re-engagement | Guilt framing. We don't miss their wallet. |
| Cart abandonment emails | "You left something behind" implies obligation to complete a transaction they chose to leave. |
| Countdown timers in email | Fake urgency. Even if the discount is real, the timer creates anxiety that violates Camp. |
| "Other students like you bought..." | Social pressure via comparison. Cialdini weaponised. |
| "Your discount is expiring!" as subject | Fear + scarcity. The discount structure is stated once; we don't chase with it. |
| Multi-CTA emails | Decision fatigue. One email, one action. |
| Embedded video autoplay | Bandwidth disrespect + spam filter trigger. |
| "Reply YES to confirm" | Command disguised as engagement. |
| Post-unsubscribe "are you sure?" | They're sure. Respect it. |
| A/B testing subject lines with fear variants | Even testing fear-based copy normalises it internally. Only test neutral vs warm. |
| Emoji in subject lines | LingoGrade is a premium brand. 🔥 and 😱 belong to Duolingo. |
| ALL CAPS in subject lines | Shouting. |
| "Exclusive offer" language | Nothing in our drip is exclusive. The discount ladder is structural and transparent. |

### The Duolingo Inversion

Duolingo's retention model is built on guilt, streaks, and FOMO. LingoGrade's model is built on the opposite: respect, silence, and the assumption that adults can manage their own learning. Every design decision in this email system should be testable against the question: "Is this something Duolingo would do?" If yes, reconsider.

---

## 21. Metrics & Success Criteria

### What We Measure

| Metric | Target | Notes |
|--------|--------|-------|
| Delivery rate | > 98% | Below this = infrastructure problem |
| Unsubscribe rate | < 0.5% per email | Above this = content/frequency problem |
| Spam complaint rate | < 0.01% | Above this = stop everything and investigate |
| Click-through rate (Day 1) | 8-15% | Homework is lowest-commitment CTA |
| Click-through rate (Day 3) | 5-10% | Reassessment is higher commitment |
| Click-through rate (Day 7) | 2-5% | Full price, lowest expected CTR |
| Conversion rate (click → purchase) | 15-25% | Below 15% = landing page friction |
| Day 30 open rate | 20-30% | Lower bar; they haven't heard from us in 3 weeks |
| Week 8 conversion | 10-20% | Primary long-term revenue metric |

### What We Don't Optimise For

- **Open rate.** Apple Mail Privacy Protection inflates it. Not a reliable signal.
- **Email volume.** Sending more emails does not produce more revenue. It produces more unsubscribes.
- **Speed to purchase.** A student who buys on Day 30 is as valuable as one who buys on Day 1. We do not pressure early conversion.

### Quarterly Review

Every quarter, review:
1. Is the unsubscribe rate stable or climbing?
2. Are spam complaints at zero?
3. Which language segments have the highest/lowest conversion?
4. Is the Day 30 newsletter generating any measurable return visits?
5. What percentage of Week 8 reassessment emails convert?

Adjust copy, timing, or sequence only based on data. Never based on "I think we should send more emails."

---

## Appendix A: Email Technical Specifications

| Spec | Requirement |
|------|-------------|
| Format | HTML with plain-text fallback |
| Width | 600px max (email client compatibility) |
| Images | Logo only. No hero images. No stock photos. |
| Font | System font stack (no web fonts in email) |
| Sender name | Assessor's first name (Days 0-7), "LingoGrade" (Day 30+) |
| Reply-to | Assessor's LingoGrade email (Days 0-7), support@lingograde.com (Day 30+) |
| Unsubscribe | One-click (List-Unsubscribe header + visible link) |
| Preheader | First sentence of body, no separate preheader text |
| Dark mode | Test and support. No white-background-only designs. |
| Accessibility | Alt text on logo. Sufficient contrast. No information conveyed by colour alone. |

---

## Appendix B: Email Template — Visual Structure

```
┌─────────────────────────────────────┐
│  [LingoGrade logo — small, left]    │
│                                     │
│  Hi {first_name},                   │
│                                     │
│  {Body — 80-200 words max}          │
│                                     │
│  {Single CTA link — text, not       │
│   button. "View homework options"   │
│   not "BUY NOW"}                    │
│                                     │
│  {Assessor first name}              │
│  LingoGrade                         │
│                                     │
│  ─────────────────────────────────  │
│  Unsubscribe | Privacy              │
└─────────────────────────────────────┘
```

**No buttons.** Text links only. Buttons create visual urgency. A calm text link says "here if you want it." A bright button says "CLICK ME."

---

## Appendix C: Subject Line Bank (English Master)

These are the master English versions. All 24 languages are translated from these.

| Day | Subject | Backup A | Backup B |
|-----|---------|----------|----------|
| 0 | Your {language} assessment report is ready | Your {language} report | Your assessment results |
| 1 | One pattern from your {language} session | A detail from your {language} report | Something from your {language} assessment |
| 3 | It sounds like {language} matters to you | The patterns we noticed in your {language} | Your {language} trajectory |
| 5 | Easier now than later | While it's fresh | Your {language} patterns are still recent |
| 7 | When you're ready | Everything is here | Your {language} tools |
| 30 | {language} insight: {topic} | A {language} tip | Something useful for your {language} |
| 56 | Would it be wrong to find out? | Eight weeks later | Your {language}, eight weeks on |

---

*"All outcomes are good. We're here if you want us."*

**Document maintained by LingoGrade Operations. For questions or edge cases, contact the product lead directly.**
