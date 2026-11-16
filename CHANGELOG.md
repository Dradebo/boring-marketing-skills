# Changelog: Boring Marketing Skills

## 4.0.0 (2026-11-16)

Free marketing skills for your AI agent: research, positioning, copy, pages, SEO, AI search, ads, email and content, plus a local-business pack. 31 skills (19 carried from 3.1.1, 12 new). MIT licensed.

### Renamed
- The library is now **Boring Marketing Skills**: plugin `boring-marketing`, frontmatter key `metadata.boring`. Install with `npx skills add boringmarketer/boring-marketing-skills` (any agent) or `/plugin install boring-marketing@boring-marketing-skills` (Claude Code).

### New: the local-business pack (6 skills)
- `google-business-profile`: checks the Google profile against the top 3 in the map pack and writes a month of posts.
- `local-seo-plan`: decides which services and towns get a page, a section, or nothing.
- `service-area-pages`: town and service pages that aren't the same page with the city swapped.
- `reviews`: where reviews stall, the owner replies, and the ask after every job.
- `first-screen-check`: the site on a phone the way a customer sees it (number, promise and proof on the first screen).
- `speed-to-lead`: missed calls and slow replies, then the text-back and follow-up.

### New: ads, agency and long-form (6 skills)
- `google-ads-tracking`: Google Ads counting calls and form fills, so it bids on real leads.
- `ads-incrementality-check`: a pause test against the phone log, to see whether ads add calls or only take credit.
- `meta-ads`: Meta API setup, campaign launch and proof the tracking fires.
- `find-local-clients` and `pitch-the-fix`: the agency path. Pick a trade and a town, rank the businesses losing the most customers, then write a short email about one broken thing with a fix you can sell.
- `long-form-article`: a long guide with real numbers and named sources, under any byline.

### Upgraded
- `start-here`: a **lite first run** is now the default. It reads the site and what customers say (Google reviews for a local business, review sites for software and shops) in about 3 minutes, writes the core brand files and names one first move. The four-agent foundation (about 15 minutes) is opt-in: say "deep". Routing covers all 31 skills in plain words, with the local pack and the agency path ("new client", "find clients") as branches. It still works for any business.
- `positioning-angles`, `competitive-intel`, `ai-search`, `keyword-research`, `landing-page`, `direct-response-copy`, `lead-magnet`, `paid-ads`, `email-sequences`, `performance-review`, `social-content`, `programmatic-seo`: sharper methods and local worked examples (a sample business, Hartline Plumbing in Dallas), with the free path first in every one.
- `creative`: the model registry and routing re-verified on 2026-11-13. Sora 2 is gone (its API ended 2026-09-24), so UGC video routes to Seedance 2.0 with Veo 3.1 as the alternate; GPT Image 2 got cheaper and lost transparent backgrounds; Seedance 2.0 is cheaper without video inputs; newer models are listed for the next refresh.

### Works in more agents
- Skills installed with `npx skills add` (Claude Code, Codex, Cursor and others) now load the brand files. The CLI copies skill folders only (each skill to `.agents/skills/<name>/`, with `.claude/skills/<name>` linked to it), so `_system/` never arrived and the brand-context loader silently failed outside the Claude Code plugin. The shared runtime (`brand_context.py`, `capability.py`, `route.py`) now ships inside `start-here/scripts/`, and every skill calls it as a sibling. If python3 or the script is missing, a skill reads the brand folder directly.
- Every skill now sees the business facts in `brand.yaml` (category, services, and for a local business the phone, town, service area and rating).
- `route.py` gains local goals (`found`, `chosen`, `calls`, `clients`) and `--request "<plain words>"`, which ranks skills by their trigger phrases.

### Checks
- New tests: trigger routing for all 31 skills (no model calls), portability across the three install layouts (plus an opt-in run of the real `npx skills` CLI), the banned-terms rules, the 31-skill catalog against the README, and strict-YAML-safe frontmatter (the `npx skills` CLI skips a skill whose description holds an unquoted `: `).
- `check_banned.sh` bans private names, author paths and real-looking ad account or conversion IDs, and allows the author's own tool (boringfunnels) only on a line that says it is made by the author of this library.
- `doctor.sh` checks the shared runtime copies and flags frontmatter that strict YAML parsers reject.

### Release cleanup
- Shared files ship inside `start-here/references/` (output format, schemas, brand memory), so skills installed with `npx skills add` can read them.
- Examples from real campaigns keep the lesson and drop the figures. Illustrative examples are labeled as such, and sample quotes are no longer attributed to real people.
- Plain words in every skill: no em dashes, and no product plugs beyond the one disclosed house tool.

## Earlier versions

- **3.x (2026):** brand memory shared across skills, a creative engine with a model registry, and research that never comes back empty.
- **2.0 (2026) and 0.1 (2025):** the first skill sets.
