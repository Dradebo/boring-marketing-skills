---
name: positioning-angles
description: Find the angle and the offer that make something sell. Researches what competitors say and pay to say, mines their bad reviews for the fears nobody answers, reads market sophistication, then writes 3-5 angles with one starred, each carrying an offer, a guarantee and a named method. Has a local-service mode (job types, map-pack competitors, trade guarantees). Use when launching a product or service, building an offer or lead magnet, before writing a page, or when marketing isn't converting.
when_to_use: find angles for X, how should I position X, what's the hook, why isn't this selling, we sound like everyone else, make this stand out, differentiate this, what offer should we run, write a guarantee, what makes us different, positioning for my plumbing company
argument-hint: "[product, service or offer to position, plus market or city; blank uses brand memory]"
metadata:
  boring:
    version: 4.0.0
    layer: foundation
    reads: [audience, competitors, voc, voice-profile#voice-summary, learnings]
    writes: [positioning, assets]
    optional-keys: [FIRECRAWL_API_KEY, EXA_API_KEY]
    enhances_with:
      - toolset: web-scrape
        gains: "reads competitor sites, pricing pages and review pages in full instead of from search snippets"
---

# Positioning & Angles

The same product can sell far better with a different angle. Same thing, framed around
a different fear, promise or comparison. This skill finds the frames worth
testing, grounded in what competitors say and pay to say, what customers complain about,
and what the business can actually promise. Done means 3-5 distinct angles with one
starred, each carrying an offer, a guarantee and a named method, written to
`./brand/positioning.md`, plus an optional ad matrix. The method is a floor, not a
ceiling. When the market in front of you argues for a better path, take it and say why
in one line.

## Context

Only if `./brand/`, `./brands/` or `MARKETING.md` exists (nothing to load otherwise), run:
`python3 ${CLAUDE_SKILL_DIR}/../start-here/scripts/brand_context.py --for positioning-angles`
(`${CLAUDE_SKILL_DIR}` is this skill's folder; outside Claude Code use the folder this
file was read from, e.g. `.agents/skills/positioning-angles`. If the script or python3 is
unavailable, read the brand folder directly: `./brands/<slug>/` when `./brands/active`
names one, else `./brand/`; then `MARKETING.md`, `preferences.md` and the files in
`reads:`. If none exist, proceed standalone and ask only for what it is, who buys it, and 2-3 competitors if known; for a local business, also the city or service area.)

If `./brand/positioning.md` already exists, this is an update session. Show the current
angle and date, then offer **refine** (re-run Phase 2, diff the landscape against what's
saved, adjust only where the market moved) or **start fresh**. On save, auto-version the
old file per the brand memory spec. If `learnings.md` holds positioning priors (an angle
or offer that won a test), apply them and say which.

## Phase 1. What's actually being sold

- **The after-state, in the customer's words.** What their life looks like after buying.
  An invoicing app sells "stop chasing clients for money", a running coach sells "a
  faster 10K without getting hurt again", a plumber sells "hot water back by dinner".
  Reviews and testimonials say it better than the founder. If you can't state it in one
  concrete sentence, get it from the user; every angle inherits it.
- **One moment at a time.** Many businesses sell several moments to different buyers: a
  SaaS has use cases, a coach has beginners and veterans, a local trade has emergencies
  and planned projects. Position the one the owner most wants more of, and say which.
- **The real alternatives**, not only competitors: do nothing, DIY, a spreadsheet, hire
  someone, a different category, a direct competitor. Each alternative's worst weakness
  is angle material.
- **What they do that customers never see.** Run the fact-sheet interview in
  `references/angle-frameworks.md` with the founder, owner or whoever delivers the work.
  Mechanisms come out of that interview more often than out of research.

Load `references/dunford-positioning.md` if the problem is bigger than messaging: the
wrong category, the wrong segment, or losing deals on price they should win on value.
That's a positioning problem, and Dunford's five components come before any angle.

## Phase 2. Read the market (parallel fan-out)

Angles from model knowledge are guesses. Identify 3-5 competitors (from `competitors.md`,
the user, or a search for "[category] for [audience]"; for local, see the Local section).
Run one WebSearch in the main thread first; if it's denied, write a `Data: MODEL
KNOWLEDGE` draft instead of fanning out.

We use Exa to find the competitors and "alternatives to" pages a keyword search misses
(free tier, then pay as you go), and Firecrawl to read their first screens, pricing and
review pages in full (free tier of 1,000 credits a month, no card). Without them,
WebSearch and WebFetch do the work, and a page read as a summary is labelled that way in
its evidence pack.

**One subagent per competitor, in parallel.** Each returns an evidence pack, not prose:

```
COMPETITOR: <name> · <url> · <rating + review count if any>
FIRST SCREEN: "<headline>" / "<subhead>" / "<primary CTA>"
PRICE FRAME: <posted prices, tiers, "free estimate", trial terms, or none>
PAID HOOKS: "<ad 1>" / "<ad 2>" (Meta Ad Library or Google Ads Transparency Center, <date>)
GUARANTEE: "<verbatim>" or none
COMPLAINTS: "<verbatim from 1-3 star reviews>" (<source>)
```

What a competitor pays to say is their real positioning; homepages carry old committee
compromises. Pull paid hooks from facebook.com/ads/library and adstransparency.google.com.
If a competitor runs no ads, that's a finding too.

**One complaints and VoC subagent.** If `./brand/voc.md` exists, start there. Otherwise
read the 1-3 star reviews of the top competitors and of the business itself: G2,
Capterra, app stores, Trustpilot or Amazon for products; Reddit threads for the category;
Yelp, BBB or Angi for local. Bad reviews name the exact failure buyers fear ("the
onboarding took three months", "the program ignored my knee injury", "quoted $350,
charged $900"). The most repeated fear is often the angle, and the guarantee in Phase 3
answers it. Skip login-walled hosts (Facebook, Instagram, LinkedIn) and say so.

**The AI-answer check.** Buyers increasingly ask an assistant before they look at any
site. Load `references/aeo-positioning.md` and run its prompts. Treat the consensus
description as saturated territory and its blind spots as white space.

**Merge into the landscape triage:**

- **Saturated.** Claims on 3+ competitor surfaces or in the AI consensus. Dead language
  that can sit in a trust strip but is never the angle.
- **Contested.** Claims 1-2 competitors make. Usable only with more proof or specificity.
- **White space.** A fear or axis nobody answers with a specific promise. Check that
  customers actually care (it shows up in the complaints), and that the business can
  keep the promise, before claiming it.

Label once: `Data: LIVE (n competitors, n ad-library pulls, n reviews read)`, and flag
any leg that fell back to model knowledge.

## Phase 3. The offer, the guarantee and the named method

Two businesses with the same angle can sell very differently because of the offer. Build
three pieces, each from what the business already does or can afford to do.

**The offer** is what the customer gets and on what terms. Run Hormozi's value equation:
raise the dream outcome and the buyer's belief they'll get it, cut the wait and the
effort. Most offers lose on the bottom half (setup time, the four-hour service window,
the 12 weeks before any result). Load `references/hormozi-offer.md` for offer shapes by
business type, including a section for local trades.

**The guarantee** removes the fear the complaints surfaced. Decision rule: it answers the
top complaint, and the owner confirms the business can afford it (refund rate, missed
deadlines, callbacks). A guarantee the business can't keep becomes the next bad review.
Write it as a sentence the owner would sign, with a number, a window and what happens if
they miss.

**The named method** is the HOW that makes the promise believable, the answer to "why
will this work when other things haven't?" Even when nothing is proprietary, there is a
step competitors skip or an ordinary fact nobody explains (Claude Hopkins' Schlitz move).
Name it like a method, give the "because" in two sentences, and test it: could a
competitor say this sentence verbatim? If yes, sharpen it. Load
`references/unique-mechanism.md` when the owner says "we don't really do anything
different".

## Phase 4. Market sophistication (Schwartz)

Detect the stage from Phase 2 evidence, not vibes:

- **Stage 1.** You'd have to explain what the category is; buyers say "I didn't know that
  was possible". Announce the promise.
- **Stage 2.** Similar promises exist and are escalating (faster, more, #1). Be more
  specific than the superlatives.
- **Stage 3.** Ads sound alike and buyers say "I've tried things like this". Explain the
  mechanism.
- **Stage 4.** Competing mechanisms, ads leading with proof. Out-prove them.
- **Stage 5.** Features commoditized, one known brand wins by default. Sell identity or
  rally against an enemy.

Paid hooks are the best signal; homepages lag. AI-adjacent markets compress the ladder:
if the AI-answer check shows assistants already comparing mechanisms and proof, call it
Stage 3-4. Load `references/schwartz-sophistication.md` when the signals conflict or the
user disputes the call.

| Stage | Run first | Also viable | Skip (and why) |
|---|---|---|---|
| 1 | Transformation, Speed/Ease | Specificity | Mechanism, Contrarian. Nothing to answer yet |
| 2 | Specificity, Transformation (with numbers) | Social Proof, Speed/Ease | Contrarian. The market isn't frustrated yet |
| 3 | Mechanism, Contrarian, Specificity, Risk Reversal | Enemy | bare Speed or Transformation. Reads as the hype everyone claims |
| 4 | Mechanism with proof, Social Proof, Risk Reversal | Specificity | anything unproven |
| 5 | Enemy, Specificity as identity ("for people who...") | Contrarian | generic promises. The market stopped listening |

## Phase 5. Generate angles

Run the mapped generators against the after-state, the offer, the method, the landscape
and the customer's words. Generate broadly, keep the 3-5 strongest. Load
`references/angle-frameworks.md` when output feels thin.

The 8 generators (the trigger condition matters more than the template):

1. **Contrarian.** "Stop [common practice]. Here's what works." When the market is
   frustrated with the standard approach.
2. **Unique Mechanism.** "The [Named Method] that [result]." Stage 3 and up.
3. **Transformation.** "From [painful now] to [after-state] in [time]." When the result is
   dramatic and specific and the buyer is problem-aware.
4. **Enemy.** A problem, practice or mindset, never a competitor by name (the surprise
   bill, the setup fee, the cookie-cutter plan). When complaints share a villain.
5. **Speed/Ease.** "[Result] in [short time]" or "without [usual sacrifice]." The most
   claimed angle in most markets; use it only with a number the business keeps.
6. **Specificity.** Narrow the who or the what. "For [specific buyer] who want [specific
   result]." Beats generic incumbents, and it's the default when the brand is absent from
   the AI answers.
7. **Social Proof.** "[Specific result] for [number] [type of people]." When proof is
   strong and trust is the barrier.
8. **Risk Reversal.** The guarantee is the headline. When risk is the top objection and
   the business can afford to keep the promise.

**Quality gate.** Every surviving angle passes all six, or it's cut or sharpened:

1. **Specific?** "Better results" fails. "Paid 11 days sooner" passes.
2. **Differentiated?** Saturated claims and copies of a competitor's paid hook fail.
3. **Believable?** The method or the proof supports it.
4. **Keepable?** The owner confirmed the business delivers it every time.
5. **Right for this buyer and moment?** Checked against audience segments and the
   customer's words.
6. **Repeatable?** It fits a headline, an ad or the side of a van in about ten words, and
   a customer could repeat it to a friend.

About three generate-and-gate passes is the ceiling. Past that the constraint is the offer
or the proof, so present the best honestly and name the test it strains.

## Local service businesses

When the business is a plumber, roofer, HVAC company, dentist, med spa, cleaner or any
business customers call from a map, adjust the method:

- **Split by job type before anything else.** Each wants a different angle.

| Job type | Example | Buyer's state | What decides the call |
|---|---|---|---|
| Emergency | burst pipe, no heat | panicked, phone in hand, calls one or two numbers | someone answers now, can come today, rough price |
| Urgent, can wait a day | failing water heater | annoyed, calls 2-3 businesses | a clear price, an arrival window, reviews |
| Planned project | repipe, new roof | researching for weeks, gets 3 quotes | proof of similar jobs, warranty, financing |

- **The competitors are whoever shows up for "[service] [city]":** the top 3 on the map,
  the Local Services Ads row, and the 2-3 businesses running search ads. Read their first
  screen as a phone visitor sees it. Google Maps pages often don't fetch; use review
  snippets from search, Yelp, BBB or Angi, or ask the user to paste.
- **Saturated in nearly every trade:** "family owned and operated", "licensed and
  insured", "24/7 emergency service", "honest upfront pricing" with no price shown,
  "quality workmanship", "fast and reliable", "free estimates", "satisfaction guaranteed".
  Trust strip only.
- **The offer often outsells the angle.** "The price on the quote is the price on the
  invoice" beats another "upfront pricing" claim. Trade offers and guarantees
  (arrival-window, price-lock, workmanship, clean-home) are in the local section of
  `references/hormozi-offer.md`.
- **Most trades sit at Stage 2-3 on claims.** Emergencies bend the stage table. Speed and
  availability decide, so a proven Speed angle leads at any stage.
- **The unspoken mechanism is the rich vein.** Every plumber runs a camera down a slow
  drain; almost none send the homeowner the video before quoting.

## Output

Present in chat per `start-here/references/output-format.md`: the deliverable header, the landscape
triage, the market read (stage, after-state, primary alternative, top complaint), then 3-5
numbered angles. Each gets a **statement**, **psychology** (the complaint or customer
phrase it answers), **headline**, **offer**, **guarantee** and **best for**. Star exactly
one with 1-2 sentences tied to the stage and the white space, then ask which to keep or
combine.

**On selection, write `./brand/positioning.md`.** Offer, guarantee and mechanism live
inside Chosen Angle, because other skills read only that section:

```markdown
# Positioning
Last updated: <date> by /positioning-angles

## Chosen Angle
Angle: <name>
Segment or moment: <who, which use case or job type>
Statement: <one sentence>
Offer: <what they get, on what terms>
Guarantee: "<the sentence the owner signed off on>"
Mechanism: <named method + the "because">
Psychology: <the fear or desire it answers, with the customer phrase>
Headline direction: "<example>"
Best for: <segments, channels>

## Market Assessment
Category: <the market customers shop in>
Sophistication: Stage <N>
Primary alternative: <what customers do instead>
Top complaint in the market: "<verbatim>" (<source>)
AI consensus: <how assistants frame the category; our descriptor or ABSENT>

## Competitive Landscape (as of <date>)
Saturated: <claims>
Contested: <claim, who uses it>
White space: <gaps>
Data: LIVE (<n> competitors, <n> ad-library pulls, <n> reviews read)

## VoC Language Bank
Verbatim phrases for copy. Quote them, don't paraphrase:
- PAIN: "<phrase>" (<source>)
- DESIRE: "<phrase>" (<source>)
- OBJECTION: "<phrase>" (<source>)

## Angles Explored
### <Angle 1> (selected) / ### <Angle 2> ...
- Statement / Headline / Offer (one line each)
```

Update `brand.yaml`; version any prior file to `./brand/.history/`.

## The 12-ad testing matrix

After the angle is chosen, offer once: "Want the testing matrix? 4 hooks x 3 formats = 12
ads, saved for /creative and /paid-ads." Default yes when the user mentioned ads. Save it
to disk; cell IDs only pay off when downstream skills and /performance-review read them.

The shared contract is `start-here/references/schemas/ad-matrix.schema.json` (`${CLAUDE_SKILL_DIR}/../start-here/references/schemas/ad-matrix.schema.json`). Rows are 4 hooks from the
chosen angle: `direct`, `question`, `proof`, `contrarian`. Columns are 3 formats: `static`,
`video`, `carousel`. Cell IDs are `MA-H{1-4}-{A-C}` (A static, B video, C carousel). Each
cell holds hook text for the format, a one-sentence visual, primary text with a customer
phrase, and a CTA. Write `./campaigns/<campaign-name>/ad-matrix.md` (readable grid plus
per-cell detail) and `ad-matrix.json` (`{ "angle", "campaign", "created", "source":
"positioning-angles", "cells": [ { "id": "MA-H1-A", "hook_type": "direct", "format":
"static", "hook", "visual", "primary_text", "cta" }, ... ] }`, all 12 cells). Append both
to `./brand/assets.md`. Assets get named by cell ID (`MA-H2-B-9x16-v1.mp4`).

## Worked examples (all research illustrative)

**Local service: Hartline Plumbing, Dallas TX (a sample business).** Water heater
replacements, an urgent job type. The plumbers on the map all say "upfront pricing" and
"same-day service"; two advertise "$50 off" an unposted price; none posts an installed
price. Their bad reviews repeat "quoted one price, the bill was double". Stage 3. The crew
already photographs the heater and venting before quoting, and the final bill matched the
quote on almost every job last year, so the guarantee is affordable. Offer: same-day or
next-morning replacement at one flat installed price, haul-away and permit included.
Guarantee: "The price on your quote is the price on your invoice." Method: the
Price-Before-We-Touch-It check. ★ Risk Reversal, headline "Your water heater price in
writing before we touch it." Runner-up: Speed, kept for the matrix's direct hook.

**Online service: bookkeeping for Shopify sellers doing $1-10M.** Four competitors say
"stress-free bookkeeping" and "real-time dashboards" (saturated); two pay for
"catch-up bookkeeping" ads (contested); sellers on Reddit complain "my books say I'm
profitable but my bank account disagrees", and nobody talks about inventory-aware cost
of goods (white space). Stage 3. Offer: monthly close by the 10th with COGS reconciled
to stock counts. Guarantee: "If your P&L and bank balance don't reconcile within 60 days,
we work free until they do." Method: Inventory-Aware Books. ★ Mechanism, headline "Your
books say profit. Your bank says no. Here's the disconnect."

**Creator or coach: an online running coach for runners over 40.** Competitors promise
"PR faster" and "custom plans" (saturated). Complaints in running forums: "every plan
assumes I'm 25", "got hurt in week 6". Stage 4, so proof and a mechanism lead. Offer: 12
weeks, two runs and two 20-minute strength sessions a week, with a weekly video check-in.
Guarantee: "Do the sessions for 6 weeks. If your easy pace hasn't improved, full refund."
Method: the Two-Session Strength Block. ★ Specificity, headline "A faster 10K after 40,
without another injury."

## What's next

- `/direct-response-copy` to write the headlines, offer and page from the chosen angle
  and the VoC bank (~15 min)
- `/landing-page` to build the page for this one offer (~20 min)
- `/paid-ads` to turn the matrix cells into campaigns (~15 min)
- `/lead-magnet` for a top-of-funnel asset that carries the angle; for a local business,
  `/google-business-profile` to put the offer where map searchers see it first (~15 min)
