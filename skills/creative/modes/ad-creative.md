# Ad Creative Mode

Paid ad production wired to the shared ad-matrix contract: /positioning-angles writes
the matrix, this mode fills its cells with creative, /paid-ads runs them, and
/performance-review maps results back to the same cell IDs. One taxonomy end to end.
That loop is the point. This is the floor, not the ceiling. When the situation argues
for a better path, take it and say why (the cell-ID naming contract isn't the flexible part).

**Before generating:** resolve roles in `references/MODEL_REGISTRY.md`: statics on
**image-default** (typography-dominant cells on **image-text-render**, dense/exact-text
compositions on **image-complex-prompt**), video cells through the tier pipeline
(**video-draft** → **video-production**; UGC-style cells on **video-ugc**; premium trio
only on explicit hero), carousels = static sets. Job→model judgment and the i2v/i2i
modality call live in `references/model-routing.md`. Load it when the routing isn't
obvious. Follow `references/api-workflow.md` for calls,
QA, manifest. Read `./brand/creative-kit.md` and `./brand/positioning.md#chosen-angle`.

---

## The matrix contract

Schema: `${CLAUDE_SKILL_DIR}/../start-here/references/schemas/ad-matrix.schema.json`. File:
`./campaigns/<name>/ad-matrix.json` (+ a human-readable `.md` twin).

```
4 HOOKS (rows)              3 FORMATS (columns)         12 CELLS
H1-H4, taxonomy:            A = static                  MA-H{1-4}-{A-C}
  direct      plain benefit claim                       e.g. MA-H2-B
  question    opens a loop the ad answers
  proof       specific result/evidence leads
  contrarian  challenges the category's accepted advice
                            B = video
                            C = carousel
```

Every cell carries: `cell_id`, hook + format refs, `headline`, `body_copy`,
`cta_text`, `creative_prompt` (consumed by this mode), `asset_paths`, `status`
(`planned → copy-ready → creative-ready → live → …`).

**Asset naming is the contract:** `{cell_id}-{ratio}-v{N}.{ext}`, for example
`MA-H2-B-9x16-v1.mp4`, `MA-H3-A-1x1-v2.png`, carousel cards
`MA-H1-C-card1-1x1-v1.png`. This exact name is the tracking name: use it as the ad
name in the platform dashboard and the UTM content parameter, so performance data maps
back to cells with zero translation.

## Entry points

1. **Matrix exists** (the normal path): read `ad-matrix.json`, list cells by status,
   generate creative for `planned`/`copy-ready` cells (all 12, a row, a column, or
   named cells; user's call). After each cell: append the file to its `asset_paths`,
   set `status: creative-ready`, update the campaign manifest.
2. **No matrix, campaign-scale ask:** route to `/positioning-angles`. Hooks belong to
   positioning, not creative ("Run /positioning-angles first; it writes the matrix this
   mode fills. ~15 min."). If the user wants to skip it, build a minimal schema-conforming
   matrix yourself (4 hooks from the chosen angle + VoC language, one per class) and say so.
3. **Quick Mode, single ad:** no matrix ceremony. Generate the one ad, QA, deliver;
   name it descriptively and suggest the matrix when they're ready to test seriously.

## Filling a cell

```
1 READ the cell: hook_text + taxonomy + format + creative_prompt (+ headline/cta).
2 BUILD the generation prompt: cell's creative_prompt + brand kit palette/avoid-list
  + platform/safe-zone clauses (below) + format spine.
   - A static: one image per target ratio.
   - B video: source frame → draft pass → production final (tier pipeline). The
     hook must land in the FIRST visible moment: frame one is the ad.
   - C carousel: 2-10 cards, 1:1, consistent lock across cards; card 1 = the hook
     standalone (most viewers never swipe).
3 ON-IMAGE TEXT: the hook in ≤6 rendered words, or clean text-space + composite in
  post. Letter-perfect offers → image-text-render role.
4 GENERATE at the cell's primary ratio first; winning cells get ratio variants
  (1:1, 4:5, 9:16, 16:9) per the format's platforms.
5 QA (standard loop + ad gates below), save under the cell name, update json +
  manifest.
```

Hook-taxonomy visual logic: the image should carry the same psychology as the copy.
**direct** = product/result clean and unmissable · **question** = visual tension or
incomplete state that the headline's question opens · **proof** = the number/result/
before-after made visual · **contrarian** = pattern interrupt, breaks the category's
visual conventions on purpose.

**Worked cell, `MA-H2-B` (question hook × video), sample business Hartline Plumbing, Dallas TX:**

```
Matrix cell:   hook H2 (question): "Is your water heater older than your car?"
               format B (video), platform Meta Reels, dimensions 9x16
1 Source frame: a garage water heater with a rust-streaked base and a dated tag, a car
                in soft focus behind it (the visual question), 9:16
2 Draft pass:   3 motion drafts (draft-tier cost per the registry): slow push to the
                dated tag / rack focus from the car to the tank / a hand wiping rust
                from the base
3 Pick:         rack-focus draft wins (question reads in frame one)
4 Final:        video-production, 5s, silent (Reels gets platform audio), hook text
                overlay zone reserved between the top 14% and the bottom 35%
5 Save:         ./campaigns/hartline-water-heater/ads/MA-H2-B-9x16-v1.mp4
                json: asset_paths += ..., status: creative-ready · manifest updated
```

## Platform specs and safe zones

| Placement | Ratio / size | Safe zone & rules |
|-----------|--------------|-------------------|
| Meta feed | 1:1 or 4:5 (1080 base) | bottom ~10% gets CTA overlay; keep in-image text light: heavy text hurts delivery |
| Meta Stories/Reels | 9:16 (1080×1920) | keep text and logos out of the top ~14%, the bottom ~35% and 6% on each side (Meta's stated zone, see `meta-ads` `references/meta-facts.md`); subject in the middle |
| Meta carousel | 1:1, 2-10 cards | every card standalone AND sequential |
| Google responsive display | 1.91:1 + 1:1 (1200 base) | **NO text in image**: Google overlays text dynamically; clean background, product focal |
| Google display fixed | 300×250, 728×90, 160×600, 320×50 | must read at actual pixel size; high contrast, brutal simplicity |
| YouTube thumbnail/end | 16:9 (1280×720) | bottom-right ~30% of end screens = subscribe overlay |
| LinkedIn sponsored | 1.91:1 or 1:1 | professional restraint; insight > urgency; no hype language |
| TikTok in-feed | 9:16 | top ~130px, bottom ~170px, right ~80px are UI → subject center-left in middle 70%; native > produced |

Cross-platform adaptation = re-composition + tone shift, not resizing: Meta→Google
strips baked text; Meta→LinkedIn swaps emotional urgency for data/insight; Meta→TikTok
strips polish and moves the subject center-left; everything→9:16 recomposes.

### Placement prompt templates

```
META FEED PRODUCT        [Product] commercial advertising photography, prominently
                         displayed in [lifestyle/studio] setting, [brand palette],
                         soft professional lighting, space at [top/bottom] for
                         headline, scroll-stopping, 4:5, sharp focus on product

META FEED UGC STYLE      Authentic-feeling social content, person [demographic]
                         genuinely using [product], natural casual lighting,
                         real-life setting, candid not over-produced, warm
                         trustworthy, 4:5, genuine expression

META FEED TYPOGRAPHY     Bold text-driven graphic, text "[HOOK ≤6 words]" in heavy
                         condensed font, [brand color] background, high contrast,
                         supporting visual element secondary, strong hierarchy, 1:1

META STORIES             [Product/subject], vertical 9:16 immersive, content clear of
                         the top 14% and bottom 35% of the frame, bold engaging, native-stories feel
                         with commercial quality, visual flow downward toward CTA

GOOGLE RESPONSIVE        [Product] clean commercial photography, NO text overlays,
                         product as clear focal point, clean uncluttered background,
                         studio lighting, survives cropping to multiple ratios,
                         [1:1 / 1.91:1]

GOOGLE BANNER            [Product] horizontal banner layout, ultra-wide, product on
                         [left/right] with open text space opposite, high contrast,
                         must read at 728x90 actual size, brutal simplicity, 21:9
                         then crop

LINKEDIN                 [Product/concept] professional B2B visual, sophisticated
                         restraint, thought-leadership positioning, credible not
                         salesy, space for headline, 1.91:1 or 1:1

TIKTOK IN-FEED           [Product] authentic TikTok-native style, NOT corporate,
                         phone-camera aesthetic with good lighting, subject
                         center-left, middle 70% of frame, trend-aware, feels like
                         organic content, 9:16
```

### Artifact formats: ads that don't look like ads

A reliably strong static family renders a believable ARTIFACT instead of an ad
layout: napkin math (handwritten before/after numbers on a photographed napkin),
a handwritten note, a sticky-note task board, a meme, a chat or post screenshot.
Two rules of the genre: (1) image models over-polish, and polish is exactly what
breaks the illusion. Counter explicitly in the prompt: "slightly messy natural
handwriting, not calligraphy", "screenshot quality, not professional", "raw,
slightly low quality". Memes get no CTA button (memes don't have CTAs; a small URL
at most). (2) screenshot-style artifacts carry policy risk: no fake platform UI on
TikTok, and invented engagement metrics or fabricated conversations presented as
real social proof fail the honesty bar everywhere. Run these through the policy
gate before spending.

### Carousel narrative structures

```
META (conversion):    1 hook/scroll-stopper → 2 problem → 3 solution → 4 proof →
                      5 CTA with urgency
LINKEDIN (insight):   1 provocative stat → 2 hidden problem → 3 your methodology →
                      4 results/proof → 5 CTA with value proposition
```

Every card must survive standalone (cards get seen out of order) AND advance the
sequence. One visual lock across all cards.

## Algorithm-assembled placements (Advantage+ / Performance Max)

These systems assemble ads from an asset library. Generate components, not one
"perfect" ad: 3-5 product shots + 3-5 lifestyle/contextual + 2-3 bold graphic
variants, EACH at 1:1, 4:5, 9:16, 16:9. Rules: no baked-in text (the algorithm adds
it), clean backgrounds (overlay legibility), product survives any crop, genuine visual
diversity (five near-identical images give the optimizer nothing to learn). Pair with
text assets: 5 short headlines, 5 descriptions, 5 primary texts, varied angles.

## A/B variants: one variable, or you learn nothing

After results identify winning cells (via /performance-review or pasted platform
data), generate variants that change EXACTLY one variable: background treatment,
product angle, expression, text treatment, color temperature, composition, CTA text,
or headline. Same base prompt verbatim, one clause swapped; fixed seed where the model
supports it so the change is attributable. Naming: `{cell_id}-{ratio}-var-{variable}-{option}-v1.png`
(e.g. `MA-H2-A-4x5-var-bg-warm-v1.png`). This keeps lineage to the cell. Judge nothing
under ~1000 impressions per variant.

## Batch freshness: recurring generation

Per-batch uniqueness is not freshness; repetition creeps in ACROSS batches. When this
mode runs on a cadence (daily/weekly cell fills, always-on asset feeds), check the
last ~7 days of generated concepts before writing new ones and hold three guardrails:
don't reuse a format from the last ~3 days or an angle from the last ~5 unless it's a
deliberate iteration of a proven winner; never open a hook with the same first three
words as a recent hook; every concept states a one-line novelty reason: if you can't
write one, it's a rerun. Default daily mix: ~40% proven family (winning format/angle,
new hook + visual treatment), ~40% adjacent test (swap exactly one of format or
angle), ~20% new bet (fresh motif from competitor gaps or new inspiration). Read
performance signals with recency decay. Avoid what the data has turned against, not
what got one bad reaction.

## Policy gates: check BEFORE generating

Violations cost launch days. The recurring offenders:

- **Meta:** no personal-attribute call-outs ("Are you overweight?" → "Looking to get
  fit?"); no unrealistic before/after or health/income promises; creative must match
  the landing page.
- **Google:** editorial rules: no ALL-CAPS gimmicks, "$$$", or vague CTAs; display
  images sharp at real size; responsive images text-free.
- **LinkedIn:** verifiable claims, stats attributed, professional tone; hype reads as
  spam here.
- **TikTok:** no fake UI elements or platform-logo watermarks; native or it dies;
  synthetic media disclosed.
- **AI content (all platforms):** apply the platform's AI label where required;
  AI-generated people are never presented as real customers (full rules:
  talking-head mode's disclosure section); keep prompts/assets on record (the manifest does
  this).

Flag the relevant gate per cell in the delivery summary: `policy: clean` or
`policy: review [issue]`.

## Ad copy fields

When the matrix's copy fields are empty (or Quick Mode), write them with the asset.
The hook taxonomy carries through the copy:

- **Meta:** primary text (first 125 chars do the work), headline ~40 chars,
  description ~30, CTA button from the platform's fixed set.
- **Google responsive display:** up to 5 short headlines (≤30), 1 long headline (≤90), up to 5 descriptions (≤90). Google Ads help lists the current limits.
- **LinkedIn:** intro text ~150 chars, outcome-focused headline ≤70.
- **TikTok:** ≤100 chars, native voice.

Deeper persuasion work belongs to `/direct-response-copy`. Hand off, don't duplicate.

## QA additions for this mode

Standard loop plus the ad gates: hook legible in the first glance at feed size ·
safe-zone collision check against the placement table · policy gate · brand
palette/avoid-list · (video) hook lands before the skip/scroll moment · (carousel)
card 1 stands alone · cell-name correctness (downstream tracking depends on it).

## Output

Assets under `./campaigns/<campaign>/ads/` (or `creative-output/ad-creative/<campaign>/`
when no campaign dir exists), named by cell ID; `ad-matrix.json` updated
(`asset_paths`, `status: creative-ready`); version the old json per the brand-memory
spec (`${CLAUDE_SKILL_DIR}/../start-here/references/brand-memory.md`); manifest + `./brand/assets.md` per asset. Delivery = standard contract with a
cell-status table (cell, hook taxonomy, format, files, QA score, policy flag).

**What's next:** `/paid-ads` to build campaigns from the creative-ready cells ·
`/performance-review` after spend to map results back to cells · `/direct-response-copy`
for the landing page the ads point at.
