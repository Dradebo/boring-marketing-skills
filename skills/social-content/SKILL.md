---
name: social-content
description: Writes original X and LinkedIn posts from the user's own best posts and real numbers, not generic hooks. Builds a per-user pattern library (what wins in their niche plus their own canon), then drafts one finished post, scores it 0 to 100 against a calibrated rubric (70 ships), checks it for the tells that make posts sound written by AI, and runs quote-post, reply and weekly modes. Use for writing original social posts; to repurpose existing long-form content use /content-atomizer.
when_to_use: write me a tweet, draft an X post, write a LinkedIn post, set up my content system, what should I post, score this post, score this tweet, quote tweet this, QT this, reply to this post, weekly content plan, social posts for this week, build my social canon, make this post better
argument-hint: "[topic/insight/link to draft from | post to score | post URL to QT | 'setup' | 'week']"
metadata:
  boring:
    version: 4.0.0
    layer: distribution
    reads: [social-canon, voice-profile, positioning#chosen-angle, learnings, algo-cache]
    writes: [social-canon, assets]
    optional-keys: [FIRECRAWL_API_KEY, SCRAPECREATORS_API_KEY, X_BEARER_TOKEN, TREG_TOKEN, ZERNIO_API_KEY, BUFFER_ACCESS_TOKEN]
    enhances_with:
      - toolset: social-data
        gains: "extracts the social canon from documented X coverage"
      - toolset: social-api
        gains: "ranks the user's own posts by real engagement instead of asking them to pick"
---

# Social Content

Original posts for X and LinkedIn that earn reach because their structure is proven in the user's niche and their substance is verifiably theirs. It works the same for a SaaS founder, a creator or agency owner, and a local business owner: the patterns come from their niche, the proof comes from their work.

Structure is learnable, because you can extract it from accounts that win. Credibility is not, because it comes only from the user's real numbers and stories. And a post earns its reach when it hands the reader something worth saving. The default ship bar is a calibrated 70 out of 100. This is a floor, not a ceiling. A better path for the post in front of you beats the recipe; take it and say why in one line.

This is the original-content system. `/content-atomizer` repurposes existing content, `/long-form-article` writes the long piece, and a local business's posts on its own Google profile belong in `/google-business-profile`.

## Context

Only if `./brand/`, `./brands/` or `MARKETING.md` exists (nothing to load otherwise), run:
`python3 ${CLAUDE_SKILL_DIR}/../start-here/scripts/brand_context.py --for social-content`
(`${CLAUDE_SKILL_DIR}` is this skill's folder; outside Claude Code use the folder this file was read from, e.g. `.agents/skills/social-content`. If the script or python3 is unavailable, read the brand folder directly: `./brands/<slug>/` when `./brands/active` names one, else `./brand/`; then `MARKETING.md`, `preferences.md` and the files in `reads:`. If none exist, proceed standalone and ask only for what the task strictly requires.)

Voice-profile governs how drafts sound; positioning#chosen-angle governs what they argue; learnings entries tagged `[social-content]` override default pattern weights. Cite any prior you apply. Platform mechanics (link handling, format ranking, timing) are perishable: check `./brand/algo-cache.md` first, else `references/platform-facts.md`, and refresh per its header if stale.

`./brand/social-canon.md` is this skill's memory: pattern library, personal canon, replay ledger. Every mode except SETUP reads it.

## What a finished post is

Six craft rules. They decide what gets drafted, before the rubric decides how well. Load `references/post-craft.md` before the first draft of a session; it has an example of each across a SaaS founder, a creator or agency, and a local business, plus the full list of tells.

1. **One finished post per request.** Hand over the single best post, finished. Plans, series and variants come when asked. A file of five drafts and a content plan makes the user do the choosing, which was the job.
2. **Something to save.** Before drafting, name what a reader would come back to this post for: a message to paste, steps to copy, a checklist, a breakdown, a real number. If the only answer is the opinion, go back to the source and find the usable part.
3. **The reader's tool before your receipts.** Give them the thing to use first. Your own test results make a good post of their own. Anything a post hands out has to work: run the prompt, send the text message to yourself, click the setting.
4. **A plain first line, then what to do.** Line one says what happened or what's true, the way you'd tell a colleague. Line two says what the reader should do about it. A clever first line that needs decoding loses to a plain one.
5. **A real screenshot before a designed image.** The default image is the primary source with the key line highlighted: the help page, the dashboard, the ad, the review. A designed graphic is the exception.
6. **Wording that matches the source.** Check every verb and superlative against the source before delivering. If the source says "may limit", the post doesn't say "kills". "One of the fastest" is not "the fastest".

## Modes

| Mode | Trigger | Needs canon? |
|---|---|---|
| **SETUP** | "set up my content system", first run by agreement | Builds it |
| **DRAFT** | A topic, insight, or link to post about | Best with; degrades gracefully |
| **SCORE** | "score this" + a draft they wrote | Best with |
| **QT/REPLY** | A post (paste or URL) to respond to | Best with |
| **CADENCE** | "this week's posts", weekly ritual | Yes, run SETUP first |

If `./brand/social-canon.md` doesn't exist and the request is a specific draft, **Quick Mode wins**: draft now using the generic archetype weights in `references/pattern-extraction.md` and the voice profile, mark credibility gaps with placeholders, and offer SETUP in one line at the end. Never block "write me a post about X" behind a 20-minute setup.

---

## Mode: SETUP

Builds the user's content system in three phases. Output: `./brand/social-canon.md`. Phases A and B run in parallel where inputs allow; the whole thing is one session.

### Phase A: niche pattern scrape

1. **Get the account list.** The user names 5 to 10 accounts whose content wins in their niche, or names the niche and you find candidates (web search for top accounts in the category; check each is active and actually in the niche). Mix sizes on purpose: include about two accounts under 10K followers. Small accounts that punch above their weight are the purest structural signal; big accounts win partly on status (see the attribution method in `references/pattern-extraction.md`). Confirm the list with the user before scraping.

2. **Fan out parallel subagents, one per account** (Task/Agent tool, `boring-marketing:research` type; `general-purpose` only when that type is unavailable). Sourcing order per agent: X API v2 if `X_BEARER_TOKEN` is set (user timeline, sorted by engagement); otherwise, when `SCRAPECREATORS_API_KEY` is set, only the X endpoints ScrapeCreators documents at docs.scrapecreators.com; otherwise WebFetch/WebSearch on public profiles and posts (Firecrawl for fuller page reads when its key is available), or report the gap. The merge step asks the user to paste 5 to 10 standout posts for any account that couldn't be fetched. LinkedIn profiles rarely scrape; for LinkedIn-first niches, expect pasted input and say so up front. If you would rather hold one key than one per provider, treg (`TREG_TOKEN`) is the one-key alternative. It is one token for many data APIs, social data among them, pay per call. Check its catalog for the platform you need before counting on it.

   Each subagent loads `references/pattern-extraction.md` (taxonomy and attribution method) and returns a **structured evidence pack of structural descriptions, never reusable content**:

   ```
   ACCOUNT: handle · platform · follower count (for normalization)
   POSTS ANALYZED: n, date range, source method
   TOP POSTS (8-15), each:
     engagement (raw + per-follower rate) · archetype (from taxonomy)
     hook shape (question/claim/number/story/POV; quote 10 words max)
     body shape (list / story / image-payload / aphorism / long-form essay)
     length bucket · format (text/image/carousel/video/doc)
     how credentials appear (inline number / story / none)
     what a reader would save (template / steps / number / none)
     closer type (cold stop / question / CTA / open loop)
   PATTERN TALLY: archetype counts across the sample
   LUCK/STATUS FLAGS: posts whose numbers structure can't explain
   ```

   **Hard rule:** extract shapes, never sentences. No full post text is stored anywhere, not in evidence packs and not in the canon. A hook fragment of 10 words or fewer, for classification, is the ceiling. The system learns why posts work; it never builds a swipe file to paraphrase.

3. **Merge.** Normalize all engagement by follower count before comparing anything. A pattern earns weight when it (a) recurs across 2 or more accounts, (b) wins on engagement rate, and (c) survives the luck and status filter. Output: the niche pattern table, each archetype with a weight (high, medium or low for this niche), the evidence behind it, and the format mix the niche rewards. Label it `Data: LIVE (n accounts, m posts)`.

### Phase B: personal canon

Input, most reliable first: the user pastes their 10 to 30 best past posts (ask for "the posts you're proudest of plus your top performers; they're often not the same list"); or scrape their own profile through the same sourcing chain; or, for a new account with no history, interview instead: "Give me 3 to 5 true, specific numbers or outcomes from your work. Real ones. These become the proof in every post." Mark an interview-built canon `seed mode` so DRAFT knows the credential bank is thin.

Extract into four banks:

- **Coinages and signature phrases:** terms they invented or own by repetition. Reuse them; don't coin knockoffs next to them.
- **Credential bank:** every verifiable proof point (dollar amounts, timeframes, counts, named outcomes), each tagged with its source post or interview answer. This is the only place draft numbers may come from.
- **Stories:** retellable first-person stories (what happened, the turn, the outcome).
- **Stances:** positions they've taken publicly. Drafts don't contradict these unless the user explicitly reverses one.

Also derive the **format fingerprint** (length distribution, casing habit, list style, emoji policy; defer to voice-profile where they conflict and note it) and the **owned-topics ledger**: their highest-engagement themes. Owned topics are replay risk: a new post there needs a genuinely new angle or it competes with their own greatest hits.

### Phase C: write the canon

Write `./brand/social-canon.md` (auto-version any existing copy per brand-memory):

```
# Social Canon: {brand}
updated: YYYY-MM-DD · accounts analyzed: n · own posts ingested: m · mode: full|seed

## Niche pattern library
{archetype → weight → evidence (accounts, engagement-rate basis) → format notes}

## Format mix the niche rewards
{text/image/carousel split, length distribution, cadence norms observed}

## Personal canon
### Coinages and signature phrases
### Credential bank          {claim · source · verified date}
### Stories
### Stances

## Owned topics (replay ledger)
{topic · best prior post (date, structural description) · extension-only}

## Format fingerprint
## Content sources           {recurring inputs for CADENCE: what they're building,
                              what they read, communities they're in}
```

Update `brand.yaml`, append one line to `./brand/assets.md`. Close with the three strongest niche patterns and the single best untapped match between a niche pattern and their credential bank. That match is their first post.

---

## Mode: DRAFT

Input: a topic, an insight, a link, or a piece of work to post about.

1. Load social-canon.md and the platform facts (algo-cache, else `references/platform-facts.md`; refresh if stale and say so in one line). Confirm the platform only if it's genuinely unclear.
2. **Find the save first** (craft rule 2). Write it down in one line: "the reader saves this for ___". If the source has no usable part, say so and ask for one rather than drafting an opinion post.
3. **Explore, then pick.** Work 2 or 3 archetypes privately (at least one from the niche's high-weight patterns, no two with the same shape). If learnings.md has `[social-content]` priors, they override niche weights; cite the entry. Score them all. Deliver the best one, finished, and name the runner-up's archetype in one line so the user can ask for it.
4. Platform judgment:

   **X:** long posts are standard; don't compress an idea that needs 800 characters, and don't pad a two-liner. External links default to a first reply (body links carry a reach penalty; see platform-facts), and the post stands without them. Stay in the user's topical lane: the ranker rewards focused accounts, so an off-lane hit costs more than it earns. Frame disagreement constructively; combative posts get suppressed. When the payload is a checklist, a template or a screenshot, write it as an artifact drop: caption of two sentences at most, the image carries the value, and the draft says exactly what the image shows (a real screenshot by default, per craft rule 5).

   **LinkedIn:** when the idea has 3 or more separable points, the default variant is a carousel outline; documents and carousels are the top format. The first two lines (before "see more") are the whole hook. LinkedIn drafts ship with a **first-hour comment plan** by default: 2 or 3 discussion comments the user posts themselves, plus the instruction to answer every reply fast.

5. **Credibility.** Numbers, client results and stories come from the credential bank only. A draft that needs proof the bank doesn't hold gets `[NEEDS REAL NUMBER: what to supply]`, never an invented stat. A post with a real number beats a better-written post without one.
6. **Score and check.** Run the draft through SCORE. Below the 70 default bar: rewrite the weakest dimension and rescore, up to about three passes, then present the best with its honest score history. Then the three pass-or-fail checks below; a post that fails one doesn't ship at any score.
7. Present:

   ```
   ### {label}
   Platform: X | LinkedIn ·  Archetype: {primary} · Runner-up: {archetype}, ask for it
   Score: {total} ({dimension breakdown} - {tell penalties})
   Checks: save ✓ ({what they save}) · source match ✓ · tool works ✓ | n/a
   Replay check: NEW | EXTENSION of {owned topic} | REPLAY (killed)
   Canon used: {credential/coinage/story drawn on}
   [the post, line breaks preserved]
   {If artifact drop: what the image shows. If LinkedIn: carousel outline + comment plan.}
   Self-critique: one line on what makes it work, one on the remaining risk
   ```

8. Save to `./campaigns/social/drafts/{YYYY-MM-DD}-{slug}.md`; append to assets.md.

---

## Mode: SCORE

Load `references/pattern-extraction.md` (the 45 against 85 calibration example) and `references/post-craft.md` (the tells) before the first scoring pass of any session. Uncalibrated scoring drifts generous.

Six dimensions, 0 to 100 total:

| Dimension | Max | What earns it |
|---|---|---|
| Hook strength | 20 | The first line forces the continue decision: an open loop, a surprising number, a stake. 15+ only if it works out of context in a feed |
| Specificity | 20 | Concrete numbers, named tools, exact timeframes, real artifacts. Abstractions score 8 or less |
| Earned credibility | 15 | Claims traceable to the credential bank or the user's visible work. Unverifiable flexes score 0 here regardless of polish |
| Rhythm and scannability | 15 | Line breaks where the eye needs them, varied sentence length, no wall of text, list style matches the fingerprint |
| Pattern integrity | 15 | Cleanly runs one archetype. Half-shapes (a listicle wearing a story's hook) read as noise |
| Native-format fit | 15 | Right length and format for the platform per platform-facts; link placement right; the LinkedIn opener survives the fold |

**Tell penalty: -5 per distinct tell, capped at -25.** The full list with examples is in `references/post-craft.md`. The short version covers a slogan where a sentence belongs (balanced pairs, "X is your new Y", stacked fragments, "isn't X. It's Y." by reflex); a closer that sums up or lands a punchline; a staged opening; a sentence every reader already believes; a colon that sets up a reveal; a list of three by reflex; homework for the reader; an abstraction as the payoff; several quoted fragments from one source; fine print in the post; em dashes; "Let that sink in" and "Here's the thing"; hype words (game-changer, unlock, delve, leverage); engagement bait ("Agree?"); emoji-led openers; hollow superlatives; fake humility.

**Pass-or-fail checks** (not scored; a fail blocks shipping):
- **Save:** you can name what a reader saves this post for.
- **Source match:** every verb, superlative and number matches its source.
- **Tool works:** anything handed out (a prompt, a text to send, a setting) was tried once. Mark n/a when nothing is handed out.

**Replay check** (a separate verdict): search social-canon's owned-topics ledger and, when available, the user's post history for the draft's 2 or 3 most distinctive phrases. NEW is clear. EXTENSION is an owned topic with a genuinely new angle, allowed and flagged. REPLAY restates a prior winner and is killed by default; reviving a greatest hit needs the user's explicit ask.

**Reading the score: 70 and up is the default ship bar, 50 to 69 is solid but not a priority, under 50 is rewrite or kill.** Judgment can override either way with a stated reason. Score honestly: a competent first draft usually lands 55 to 70. If everything you score clears 80, recalibrate against the reference example. When the user submits their own draft, show the full breakdown, name the cheapest dimension to lift (usually specificity; one real number is worth 6 to 10 points), and offer one rewrite.

---

## Mode: QT/REPLY

Input: a post that's moving in the user's niche, pasted (preferred) or a URL (fetch it; if the fetch fails, ask for a paste plus the author and rough engagement).

1. **Freshness.** Quote posts work inside about 7 days of the original; replies inside about 48 hours. Early replies the author engages with get a large ranking boost, so speed is the whole reply game. Stale original: warn, and let the user decide.
2. Say what the original claims and whether it touches the user's lane. Off-lane: recommend skipping; borrowed reach off-topic costs topical focus.
3. Quote-post angles come **only from the three families that add something**:
   - **Data-add:** the original makes a claim; the user has a credential-bank number that confirms, sizes or complicates it.
   - **Disagree with receipts:** disagree with the specific mechanism, not the person, and bring evidence. Constructive framing.
   - **Extension:** "yes, and here's what that means for {the user's audience}", taken somewhere concrete the original didn't go.
   A quote post that rephrases or merely agrees adds nothing; don't draft it.
4. Score quote posts with the full rubric (the original supplies context, not credibility). Replies get a lighter bar: the tell check plus the add test, two sentences or fewer preferred, and written so the author can answer it.
5. Present the best quote post and the best reply, with scores and the freshness verdict. Other angles on request.

---

## Mode: CADENCE

The weekly ritual: 3 to 5 posts from real inputs, one file, ready to schedule. Requires a canon. This is the plan the user asked for, so craft rule 1 holds per post: each slot is one finished post.

1. **Gather sources** (don't invent topics): the canon's content-sources list; recent `[social-content]` learnings; this week's shipped work from assets.md; one question to the user ("what did you build, learn, fix or argue about this week?"); optionally a quick search for what the niche debated this week (a quote-post or reply slot).
2. **Plan the slots.** The default week: 3 to 5 posts, no archetype twice, at most one disagreement post (rationed, or the account becomes a take machine), at least one high-weight niche pattern, at least one post the reader saves for a tool, a carousel if LinkedIn is active, optionally one quote post of a live niche conversation. Spread across the week; daily volume the user can't sustain is a plan that fails by Wednesday.
3. Draft every slot through DRAFT and SCORE. Slots that can't reach 70 from this week's material get cut, not padded. A 4-post week of 70+ beats a 5-post week with a 58 in it.
4. Write `./campaigns/social/{YYYY}-W{ww}.md`: the plan table (day · platform · archetype · score), then each full post with its image note, carousel outline or comment plan. Append to assets.md.
5. After the user posts a week, nudge once: real engagement numbers go to `/performance-review`, which writes the priors that recalibrate pattern weights here.

---

## Queueing the drafts

Drafts are files first. When you want them posted on a schedule, we use Zernio: one API
and MCP that posts and schedules across about 18 platforms (`ZERNIO_API_KEY`), priced by
plan. Buffer is the free option for a few channels (its free plan covers 3 channels and
includes an API key). Without either, paste each draft into the platform's own scheduler.
Whatever the tool, show the exact final text, platform and time first, and queue nothing
without a yes for that batch.

## Output

Per the output contract: deliverable header, content, **Files saved** (`./brand/social-canon.md`, `./campaigns/social/...` with new or updated markers), **What's next**. Files are written before the chat summary. Cite applied learnings priors by entry.

## What's next

- `/performance-review`: after 1 or 2 weeks of posting, feed real numbers back; pattern weights without performance data are guesses (~15 min)
- `/content-atomizer`: a 70+ post that worked is seed content for every other platform (~10 min)
- `/long-form-article`: when a post keeps getting saved, the long version is the next piece (~45 min)
- `/brand-voice`: if drafts keep failing on voice rather than structure, the profile needs work, not the drafts (~20 min)
