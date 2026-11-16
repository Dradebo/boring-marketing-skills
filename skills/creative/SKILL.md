---
name: creative
description: AI creative production engine for product photos, product video, social graphics, talking heads, and ad creative through one tiered pipeline with a vision-QA loop that scores every asset before you see it. Use whenever visual assets need to be generated, edited, or batch-produced for a brand or campaign.
when_to_use: generate an image, product shot, product video, hero video, social graphic, YouTube thumbnail, talking head, UGC video, lip sync, ad creative, edit my product photo, animate this image, make visuals for this campaign
argument-hint: "[what to make, or blank to be routed]"
metadata:
  boring:
    version: 4.0.0
    layer: execution
    reads: [creative-kit, positioning#chosen-angle, voice-profile#voice-summary]
    writes: [creative-kit]
    optional-keys: [REPLICATE_API_TOKEN, OPENAI_API_KEY, HF_API_KEY_ID, HF_API_KEY_SECRET, ELEVENLABS_API_KEY]
---

# Creative Engine

One engine for every visual asset a brand ships. The judgment: match motion and style
to positioning, spend pennies finding direction before spending dollars on finals, and
never present an asset you haven't looked at yourself. Done = downloaded files,
QA-scored, brand-consistent, named so downstream skills can find them. This is the
floor, not the ceiling. When the situation argues for a better path, take it and say why.

## Context

Only if `./brand/`, `./brands/` or `MARKETING.md` exists (nothing to load otherwise), run:
`python3 ${CLAUDE_SKILL_DIR}/../start-here/scripts/brand_context.py --for creative`
(If the script or python3 is unavailable, read the files named in `reads:` directly,
section-anchored where specified. If none exist, proceed standalone. Ask only for
what the task strictly requires.)

If learnings.md holds creative priors (hook formats, style winners), cite those you apply.

## Setup: 30 seconds, once

1. **Token:** check `$REPLICATE_API_TOKEN` (env or `.env`). Missing → **prompt-only
   mode**, defined in `references/api-workflow.md` §6: same workflow, deliverable is
   the exact prompt + model + settings instead of the file. Never block on the token.
2. **Stack freshness:** if `./brand/creative-stack.md` is missing or older than the registry's
   `ttl-days`, run `bash ${CLAUDE_SKILL_DIR}/scripts/verify_models.sh` before the first
   paid call. It rewrites `./brand/creative-stack.md` (a different file from the `stack.md` that start-here keeps) with a pass/fail table.
3. **Brand kit:** read `./brand/creative-kit.md`. Missing → for a one-off asset,
   proceed and offer to build it after; for campaign work, build it first (below).

## What we use

None of this is required. With no key, prompt-only mode writes the exact prompt, model
and settings for any tool you already have. When you want the files made for you, this is
the stack we run, one pick per job. Keys are listed in TOOLS.md; payloads and per-model
prices live only in `references/MODEL_REGISTRY.md`.

- **Images.** We use GPT Image (OpenAI) where the text or layout has to be exact and for
  edits to a real photo, which are the `image-complex-prompt` and `image-instruct-edit`
  roles. It is pay per image, through the OpenAI API (`OPENAI_API_KEY`) or Replicate.
  Everyday stills stay on `image-default`. Without a key, the prompt-only deliverable
  works in any image tool.
- **Video.** We use Seedance 2.5 (ByteDance) through Higgsfield or Replicate, pay per
  clip. That means 2.5 where your provider lists it, otherwise 2.0. The registry's
  verified rows are Seedance 2.0, and 2.5 sits there as a "newer, verify before use" row
  until it passes the registry's checks. Without a key, you get the prompt and settings
  for any video tool.
- **Voiceover and talking heads.** We use ElevenLabs for the voice, for cloning and a
  consistent voice across a campaign. It has a free tier, then plans (`ELEVENLABS_API_KEY`).
  Without it, the lip-sync model's built-in voice or any quick text-to-speech tool
  covers a script test.
- **One key for many models.** Replicate is the path the registry's payloads and the
  async pattern are written for (`REPLICATE_API_TOKEN`). Higgsfield is the one-key
  alternative: one API for 50+ image and video models, Seedance included, pay as you go
  (`HF_API_KEY_ID` and `HF_API_KEY_SECRET`). On Higgsfield keep the role and the prompt,
  and take the parameters and calls from its own docs.

## References: when to load what

| File | Load when |
|------|-----------|
| `references/model-routing.md` | Before model selection: job→model defaults, the i2v/i2i/t2v decision, style capsules, moodboarding, platform map, when to leave Replicate. |
| `references/MODEL_REGISTRY.md` | Before ANY generation: the only source of payloads and prices. Resolve roles here. |
| `references/api-workflow.md` | First generation of a session: async pattern, download-within-1h, file naming, campaign manifest, QA mechanics, handoffs. |
| `references/VISUAL_INTELLIGENCE.md` | Constructing prompts for anything that matters: visual psychology, anti-slop checklist (Part 4 powers the QA rubric), style taxonomy, consistency techniques. |

## Modes

Route by what's being made. Each mode file carries the craft for that asset type;
they all share the registry, the API workflow, and the QA loop.

| Request smells like | Mode file |
|---------------------|-----------|
| Product stills, e-commerce shots, editing a real product photo | `modes/product-photo.md` |
| Reveals, orbits, demos, any product motion | `modes/product-video.md` |
| Posts, thumbnails, quote cards, content calendars | `modes/social-graphics.md` |
| Presenters, UGC testimonials, spokesperson, lip-sync | `modes/talking-head.md` |
| Paid ads, ad matrix cells, A/B variants | `modes/ad-creative.md` |
| Anything else visual | No mode file: brand kit + registry + this file |

Quick Mode: a specific single-asset request ("16:9 hero shot of the bottle on walnut")
skips mode ceremony. Construct the prompt, generate, QA, deliver, one-line what's-next.

## Routing by ROLE: never by model ID

Load `references/model-routing.md` before model selection. It carries the job→model
judgment and the input-modality (i2v/i2i/t2v) decision. Payloads and prices appear
ONLY in `references/MODEL_REGISTRY.md`; this file and the modes speak in roles, and
the registry's Role Map resolves them at call time. When models change, the registry
changes and nothing else does.

```
STILL IMAGE
├─ default            → image-default (iterate with seeds where supported)
├─ shipping at 4K     → image-premium-4k
├─ editing a real photo / multi-reference fusion → image-default with image_input
├─ complex composition / dense prompt / exact in-scene text → image-complex-prompt
├─ typography-dominant flat graphic (>6 words)   → image-text-render
├─ logo / icon / needs real vector               → image-vector
└─ user names a model → use it (look up its payload in the registry)

VIDEO: the tier pipeline (below) is the default path
├─ drafts             → video-draft
├─ UGC / ad-native (handheld, imperfect-real)    → video-ugc
├─ polished finals    → video-production
├─ character/reference consistency → video-reference
├─ locked-off product shot         → video-locked-camera
└─ explicit "hero"    → video-premium (3-model parallel)

SPEECH
├─ lip-sync default   → lipsync-default
├─ cheap script tests → lipsync-budget
├─ video-production output → lipsync-kling
└─ animate a still photo into a speaker → digital-human
```

Don't ask the user which model to use. Pick the role; tell them what ran and what it
cost in the delivery summary.

## The tier pipeline (default for all video)

Cheap drafts find the direction; production money only follows a chosen direction.

```
1. SOURCE FRAME   Best video starts from an approved still (I2V beats T2V: you
                  control frame one). Generate/approve the image first when practical.
2. DRAFT          3-5 motion variants on the draft tier (draft-tier cost per MODEL_REGISTRY, 720p,
                  ~30s). Different camera moves / energies, not five near-clones.
                  QA each, present pre-ranked.
3. PICK           User picks a direction (or asks for another draft round).
4. PRODUCTION     Regenerate the winner(s) on the production role at full quality.
                  Same prompt skeleton, same seed discipline where supported.
5. PREMIUM        ONLY on an explicit "hero" request: run the premium trio in
                  parallel on the winning prompt, QA all three, present pre-ranked.
                  Never silently escalate to premium.
```

Images skip the tiers: generate on `image-default`, iterate by changing ONE variable
per round, reusing the seed where the model supports it so you can attribute the change.

**Cost discipline:** under $1 total: just generate (no confirmation ritual). $1-2:
state the cost in one line and proceed. **≥$2: confirm before running.** Always record
actual spend in the campaign manifest.

## Vision QA loop: runs after EVERY generation

You look at everything before the user does. No raw URL dumps.

1. **Download immediately** (URLs die in 1 hour; api-workflow.md §1).
2. **Look:** `Read` the image; for video extract first/mid/last frames via ffmpeg
   (mechanics in api-workflow.md §2; thumbnail fallback if ffmpeg is absent).
3. **Score 1-10** against a rubric assembled from: the brand kit's palette/mood/
   avoid-list, the anti-slop checklist (VISUAL_INTELLIGENCE.md Part 4), and the
   request's own spec (ratio, text space, focal point, platform).
4. **Below 7:** name the failure, fix THAT in the prompt, regenerate. About 2 retries is
   the practical ceiling; past that the prompt frame or model family is the constraint,
   so present the best attempt with an honest score history instead of burning budget.
5. **Present** the best asset WITH the critique: score, one strength, one residual
   weakness. Multi-model comparisons arrive pre-ranked with stated reasons.

A 6 honestly labeled beats an unexamined 8. The QA notes per asset go in the manifest
(`qa_score`) so /performance-review can later correlate scores with results.

## Brand kit: `./brand/creative-kit.md`

The visual DNA every mode reads before generating: colors (hex + names), typography
direction, photography/illustration preference, overall mood, the avoid-list, logo
path, and any saved artifacts (style locks, social templates, approved presenters).

Building it: ask for a site/social URL first and propose a kit from what you observe;
fall back to direct questions only for what you can't infer. Writes/updates follow the
brand-memory spec (`${CLAUDE_SKILL_DIR}/../start-here/references/brand-memory.md`: auto-version old file, 3-line change summary, update brand.yaml).

Using it: palette and mood terms are injected into every prompt; avoid-list items are
standing guardrails; saved style locks and presenter specs are reused verbatim rather
than re-explored.

## Style exploration: optional, not a toll booth

For a NEW project with no locked style and real campaign scope, offer (don't impose)
a direction exploration, default five: the category-safe one, its opposite, one
borrowed from another industry, one emotion-first, one convention-breaker; fewer when
the brief is narrow. Generate small, present with strategy/vibe/risk per direction, let
the user pick or combine ("lighting from 2, composition from 4"), then write a **style
lock** (palette, exact lighting phrase, composition rules, technical reference,
anti-patterns) into the campaign directory and reference it in every subsequent prompt.

Skip exploration when: a style lock or template already exists, the request is
specific, it's a follow-up asset, or the user says skip. Quick Mode always skips.

Consistency at scale = brand prefix + locked phrases + fixed seeds + reference images
(techniques: VISUAL_INTELLIGENCE.md Part 10).

## Batch & campaign scale

3+ assets → write the campaign manifest BEFORE generating
(api-workflow.md §4: per-asset role, model, prompt, seed, cost, qa_score, status).
Generate in parallel waves of 5-8 (rate limits), updating the manifest per asset. A
failed batch resumes from the manifest. Skip `done`, retry `failed` once, run
`pending`. Wall-clock for a wave = its slowest member.

## Output

Files-first, per the api-workflow.md conventions: assets under `creative-output/…`
(or the campaign's own tree), versioned names, ad assets named by matrix cell ID,
one line per asset appended to `./brand/assets.md`.

Delivery summary follows the standard contract:

1. `## <DELIVERABLE>` + date/context line
2. The assets, each with its path, what it is, QA score + one-line critique, model that
   ran (named once here, from the registry) and actual cost
3. `**Files saved:**` exact paths with (new)/(updated)
4. `**What's next:**` (below)

If a creative brief came from another skill, return the `creative_delivery` block
(api-workflow.md §5) pointing at the manifest.

## What's next

- `/content-atomizer`: cut the approved assets into platform-native posts (~10 min)
- `/paid-ads`: if these were matrix cells, build the campaigns around them (~15 min)
- `/direct-response-copy`: landing page or email copy to pair with the visuals (~15 min)
- `/performance-review`: after the assets have run, map results back to cells and
  QA scores so the next round is smarter
