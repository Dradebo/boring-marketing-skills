# Output Format

Every skill follows this contract. It is short on purpose: the contract is four sections,
a Quick Pick block for choices, and Quick Mode for specific requests. Everything else is
restraint.

---

## Principles

1. **Markdown-native.** Claude Code renders markdown. So do Notion, Slack exports, and
   every editor the deliverable lands in. Use headings, bold labels, tables, and lists.
   Never Unicode box-art, ASCII dividers, or fixed line widths. Output that needs a
   monospace font to look right is broken everywhere else.

2. **Files first, output second.** The deliverable lives on disk (`./brand/`,
   `./campaigns/<name>/`) BEFORE it is summarized in chat. Long content (full articles,
   complete sequences, detailed briefs) belongs in files; chat shows what was saved, the
   key decisions, and the route forward. Append one line per asset to `./brand/assets.md`
   (Quick Mode skips this and never creates `./brand/` for a one-off asset).

3. **Scannable in five seconds.** The deliverable name, the recommended option, and the
   next step are each findable without scrolling or hunting. Predictable section order
   does most of this work.

4. **Professional restraint.** No emoji. No exclamation marks. No "Great news!" filler.
   No preamble ("Here is your...", "I've created..."). The output starts at the header.
   The output is the deliverable; present it and move on.

5. **Recommended option visible immediately.** When presenting multiple options, the
   pick comes first (Quick Pick block), details after.

---

## The four-section contract

Every skill output has these sections, in this order. If one is genuinely not applicable
(rare), include it with a one-line note saying why.

### 1. Header

```markdown
## LANDING PAGE COPY: Spring Launch
Generated Jun 10, 2026 · angle: "The Anti-Dashboard" · voice profile loaded
```

An `##` heading naming the deliverable (the output type, not the skill name), then one
line of date + context (which brand files / angle / data mode shaped this run).

### 2. Content

The deliverable summary or the deliverable itself if it is short. Clean markdown:
- Headings for structure, bold for labels, lists for items.
- Tables only for genuinely enumerable facts (keyword metrics, send schedules,
  variant comparisons), never for single-column status lists.
- Research-backed skills include the one-line data label here:
  `Data: LIVE (6 sources)` or `Data: MODEL KNOWLEDGE (verify before spending)`.
  Estimated numbers carry `~`.

### 3. Files saved

```markdown
**Files saved:**
- ./campaigns/spring-launch/landing-page.md (new)
- ./brand/positioning.md (updated)
- ./brand/assets.md (1 entry appended)
```

Exact relative paths with `(new)` / `(updated)` / `(n entries appended)` markers. Every
skill that writes files shows what it wrote: the user never hunts for output. If nothing
was written (analysis-only), say `No files written (analysis-only output).`

### 4. What's next

```markdown
**What's next:**
- /email-sequences: turn this page into a 5-email welcome flow (~15 min)
- /creative: hero image for the page from your creative kit (~10 min)
- /content-atomizer: promote it across your 2 priority platforms (~10 min)

Or tell me what you're working on and I'll route you.
```

2 to 4 concrete `/skill` suggestions, each with a reason and a rough time estimate. End with
the routing fallback line. If this completes a workflow, say so and point at
`/start-here` for a status review.

**Conditional /creative suggestion:** suggest a visual build step only when BOTH are
true: Replicate is connected (key present in `.env` / stack.md) AND the asset type
actually benefits from a visual (landing page hero, ad creative, social graphic; not a
keyword plan or an email sequence). When suggested, it is a listed option, never an
auto-advance.

---

## Quick Pick block

When a skill presents multiple options (angles, concepts, headline variants), the
recommendation appears at the top, before the detailed options:

```markdown
**Quick Pick: ★ Option 2: The Question Hook**
"What if your proposal template is the reason you're stuck at, say, $5k months?"
Best for: cold traffic, skeptical buyers. All options below.
```

One ★ pick, the option number so the user can find it in the full list, a one-line
rationale or copy excerpt. If there is no clear winner, skip the block: do not fake a
recommendation.

---

## Quick Mode

When the user makes a specific, single-asset request ("write me a LinkedIn post about
X", "give me 5 subject lines", "generate a product photo"), skip the ceremony and
deliver:

- No project status scan, no multi-step workflow proposal, no gap analysis, no
  missing-file warnings.
- Just the asset (still saved to disk per the files-first principle), then a one-line
  what's-next.

**Quick Mode wins over any "scan first" rule.** If a skill's own instructions say to
audit context, propose a plan, or check the brand foundation before generating, a
specific single-asset request overrides that. Deliver first.

**Not Quick Mode:** "help me with...", "where should I start", "set up my...", anything
exploratory gets the full experience.

---

## Status indicators

Three indicators, used sparingly inside content sections:

| Mark | Meaning |
|------|---------|
| ✓ | present / passed / saved |
| ✗ | missing / failed |
| ★ | recommended option |

That is the whole palette. No progress spinners, no circled numbers, no star-rating
rows, no tree-view glyphs.

---

## Anti-patterns

- **No box-drawing or divider art.** No `━━━`, `───`, `┌─┐` boxes, `├──` trees, or
  `①②③` numerals. Use markdown headings, lists, and ordered lists.
- **No character counting.** No fixed line widths, no aligned columns built from
  spaces, no indent diagrams. Write normal markdown and let the renderer work.
- **No preamble, no postamble.** Start at the header; end at what's-next.
- **No emoji**, anywhere in output.
- **No dumped deliverables.** A 2,000-word article pasted into chat instead of saved to
  `./campaigns/` is a bug, even if it is also saved.
- **No orphaned output.** Missing files-saved or what's-next sections are bugs.
- **No fabricated metrics.** Examples that need numbers mark them as illustrative
  ("say 2.1%"); estimates carry `~` and the data label says where they came from.

---

## Worked example (complete output shape)

```markdown
## SUBJECT LINE VARIANTS: Welcome Email 1
Generated Jun 10, 2026 · voice profile loaded · Data: MODEL KNOWLEDGE

**Quick Pick: ★ Option 1: proof + specificity**
"I booked 3 clients with this proposal template"

1. ★ "I booked 3 clients with this proposal template", proof + specificity
2. "Your proposal template is broken (here's mine)", curiosity + pattern interrupt
3. "The 3-email sequence that books calls", utility, clear value

Recommended A/B test: 1 vs 2. Applied prior: learnings.md 2026-05-12: question
subjects underperformed proof subjects for this list.

**Files saved:**
- ./campaigns/welcome-flow/subject-lines.md (new)
- ./brand/assets.md (1 entry appended)

**What's next:**
- /email-sequences: write the full email behind the winner (~10 min)

Or tell me what you're working on and I'll route you.
```
