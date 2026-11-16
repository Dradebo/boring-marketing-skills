---
name: service-area-pages
description: Writes town and service-area pages for a local business that each say something true and specific about that town, folds the towns that can't into one honest areas-we-serve page, and checks the set for duplicates before anything ships. Use when a plumber, roofer, HVAC company or other service-area business needs city pages, wants to fix town pages that are all the same, or has a local SEO plan that calls for them.
when_to_use: write city pages, service area pages, location pages for my business, town pages, a page for every city we serve, our city pages are all the same, fix duplicate city pages, areas we serve page, local landing pages for each town, near me pages for each suburb
argument-hint: "[business or site] [towns, or 'from plan']"
metadata:
  boring:
    version: 4.0.0
    layer: execution
    reads: [voice-profile, positioning#chosen-angle, voc, competitors#competitor-profiles, brand-manifest]
    writes: []
    optional-keys: [FIRECRAWL_API_KEY, GOOGLE_APPLICATION_CREDENTIALS, GSC_SITE_URL]
    enhances_with:
      - toolset: web-scrape
        gains: "full reads of the site's existing town pages and the competitor pages that win each town"
      - toolset: search-console
        gains: "a per-page baseline, and which old town pages earn nothing and should be merged"
---

# Service Area Pages

A town page earns its place only when it says something true about the business in that town that the other town pages can't. Google's spam policies name the alternative directly: "multiple domain names or pages targeted at specific regions or cities that funnel users to one page" is doorway abuse. This skill decides which towns qualify, writes those pages, folds the rest into one honest areas-we-serve page, and proves the set isn't duplicates before anyone publishes it. The method is a floor. The no-invented-facts rule and the duplicate check don't flex.

## Context

Only if `./brand/`, `./brands/` or `MARKETING.md` exists (nothing to load otherwise), run:
`python3 ${CLAUDE_SKILL_DIR}/../start-here/scripts/brand_context.py --for service-area-pages`
(`${CLAUDE_SKILL_DIR}` is this skill's folder; outside Claude Code use the folder this file was read from, e.g. `.agents/skills/service-area-pages`. If the script or python3 is unavailable, read the brand folder directly: `./brands/<slug>/` when `./brands/active` names one, else `./brand/`; then `MARKETING.md`, `preferences.md` and the files in `reads:`. If none exist, proceed standalone and ask only for what the task needs.)

If `./campaigns/local-seo/plan.md` exists, read it first. Its market map already says which towns get a page, which get a line, and why. Don't redo that work. Use its capability ledger as the source of every claim.

## Modes

| Situation | Mode |
|---|---|
| No town pages yet | **NEW SET**, all phases |
| Town pages exist and look alike, or slid in rankings | **FIX EXISTING**, start with the duplicate check in Phase 6 on the live pages, then Phases 1-7 |
| One named town | **SINGLE PAGE**, Quick Mode: qualify that town, write it, run the duplicate check against the existing pages |

## Phase 1. Qualify each town

A town gets its own page only when all three hold:

1. **The business really serves it.** Job addresses, the Google profile's service areas and an honest drive time from the base. Google's own limit for a profile's service area is about 2 hours of driving from the base, and a page for a town the crew won't drive to is a doorway page by definition.
2. **There is something to win.** Demand evidence for the service in that town and no page of the business winning it (from the plan, or a quick check: the town and state in the query, the map pack checked from the town).
3. **There is real local proof.** At least one element from the list below. Two is a good default for a full page.

Local proof that counts:
- jobs done in the town, by type, from the job records;
- reviews that name the town or a neighborhood in it, quoted verbatim with the date;
- cleared job photos from the town;
- a crew member based there, or an honest response time from the base;
- a local condition that changes the work, from a source you fetched: the city's water quality report, its permit rules for the job, the age of the housing stock, a past freeze or flood, an HOA or utility rule, a utility rebate;
- a pricing difference (a trip fee zone, for example).

Gather the sourced conditions with one research subagent per town, in parallel (Task tool, `general-purpose` when the plugin's research type is unavailable), each fetching the city's own pages and returning facts with URLs, within the research budget (40 fetches, 8 minutes).

We use Firecrawl for these reads: it returns clean markdown of the city's own pages and can crawl a city site for the permit rule or the water report (free tier of 1,000 credits a month, no card). Without it, WebFetch reads the same pages as summaries, and each fact still carries its URL.

What doesn't count: "proudly serving", population, founding year, landmarks, a list of neighborhoods nobody asked about, and anything you can't source. Census trivia that doesn't change the job is padding.

A town that fails gets a line on the areas-we-serve page, listed in the output with the reason and what would unlock a page ("3 more jobs and one review naming Rowlett").

## Phase 2. Plan the set

- **One areas-we-serve hub.** It lists every served town with one true line each and links to the town pages that exist. Unqualified towns live here.
- **Town pages** only for the towns that qualified.
- **Service pages stay the parents.** A service × town page (water heater repair in Garland) needs the plan's proof threshold for that exact combination. Never multiply services × towns because a template makes it easy.
- **One page per query.** The homepage should not target "[service] [town]" for a town that has its own page. Two pages chasing one query split the signal.
- **Links.** Town page to the services done there and to the hub. Service pages to the towns where the jobs actually happened.

## Phase 3. Spec each page before writing it

Write a short spec per page in the output file:

| Field | Example (sample business) |
|---|---|
| URL | `/areas/garland-tx/` (stable slug, no dates) |
| Create or improve | Create |
| The question it answers first | "Who can fix a leaking water heater in Garland today?" |
| Local proof | 31 water heater jobs in 12 months; 4 reviews naming Garland; attic installs in 1970s ranch homes; city permit required |
| Different from its siblings because | Older housing stock, attic gas units, the permit step, its own reviews |
| Who wins now | The three businesses observed in the Garland map pack, by name |
| CTA | Call or text, with hours |

The "different from its siblings" line is the doorway test written down. If you can't fill it with something true, the town goes back to the hub.

## Phase 4. Write the page

Load `references/page-anatomy.md` before writing. Default section order:

1. **Answer first.** 40-80 words that answer the page's question: what, where, how fast, how to reach them, with one real fact about this town.
2. **The work done here.** The job types from the ledger for this town, each with the substance of the work: what fails, how it's diagnosed, what the fix involves, what it costs the homeowner in time or damage if it waits. This is true in every town and specific to the trade, which makes it the safest thing to write at length.
3. **What's different about this town.** Only sourced conditions that change the work.
4. **Proof.** Reviews that name the town, a job story, real photos.
5. **Coverage and response.** Honest drive times, hours, emergency availability exactly as the owner confirms it.
6. **Pricing.** The structure (trip fee, minimum, free estimates or not). Dollar amounts only if the owner publishes them.
7. **Questions.** Only real ones, from calls, reviews or the questions Google shows for that town's searches. Skip the section if there are none.
8. **Call to action.** Tap to call, text if they answer texts, hours.

**The filler trap.** Tell a writer, human or AI, "never invent a fact" and it fills the space with procedure: what to have ready when you call, what happens after you book, questions like "What areas do you serve?". It reads as safe and says nothing. When a service business rebuilt its copied town pages and retired the rest with redirects, both drafting rounds drifted into this filler.
What fixed it was pointing the writer at the substance of the work itself. If a paragraph would make sense on a page for a different trade, cut it.

## Phase 5. Technical checks

Load `references/technical-checks.md`, which carries the commands that settle each check. In brief:
- One business entity in the markup, with the real address or none at all for a business that hides its address. Town pages say where the business works (`areaServed`). Never a separate LocalBusiness per town with an invented address.
- No star ratings in your own markup, and no prices, hours or claims in markup that the visible page doesn't show.
- Title and H1 name the service and the town once, plainly.
- Images sized for phones. A hero image of several megabytes on a page meant for someone with a burst pipe is a lost call.
- Every retired or renamed URL redirects in one hop to a page that loads.

## Phase 6. Quality gate (before anything ships)

1. **Duplicate check.** Run it across the new pages and every existing town page:
   `python3 ${CLAUDE_SKILL_DIR}/scripts/overlap.py <pages-dir-or-files> --names "Dallas,Garland,Mesquite,Richardson"`
   It masks the town names, then reports the share of sentences any two pages have in common. Default bar: under 30% for every pair. Over the bar, fix the template or the proof behind it, never one page by hand, because the same defect sits on every sibling. If proof can't close the gap, the town goes back to the hub.
2. **The read test.** Pick two town pages at random. Would someone who read the first learn something on the second? If not, they are one page.
3. **Claim trace.** Every factual claim maps to the ledger, a fetched source, or the owner-confirm list. Anything else comes out.
4. **Markup matches the page.** Nothing in the JSON-LD that a visitor can't see.

Rewrite and re-check up to three rounds. If the set still fails, ship fewer pages and say so. Eight real pages beat twenty where twelve are padding.

## Phase 7. Publish, retire and measure

- Publish the hub and the 3-5 strongest town pages first. Add more when those are indexed and showing impressions.
- **FIX EXISTING:** for each old town page, rebuild it (it qualifies), merge it into the hub with a 301, or redirect it to the nearest real town page. One hop, then update internal links and the sitemap. Town pages that are literal copies of each other tend to lose ground first when rankings drop, so fix the copies before a drop, not after.
- Record a baseline per page in Search Console (with `GOOGLE_APPLICATION_CREDENTIALS` and `GSC_SITE_URL` set, read it directly; otherwise ask for a Performance export). After 60-90 days indexed, a page with no impressions gets more proof, a merge into the hub, or a redirect. Leaving it costs the pages that work.

## Output

Write `./campaigns/service-area-pages/<YYYY-MM-DD>-pages.md`, the handoff for the owner or the developer:

1. `## SERVICE AREA PAGES for <business>` with the date and the data label.
2. The qualify table: every served town, qualified or not, the reason, and the unlock for those that aren't.
3. The set: hub, town pages, service-page links, and the redirect list for FIX EXISTING.
4. Per page: the spec, the full copy, and its JSON-LD block.
5. The duplicate check output and the read-test notes.
6. Owner to confirm: every claim that needs a yes before publishing.
7. Measurement baseline.

If the project has a codebase, also write the pages into it, the way the project already builds pages, and list the paths. Never publish. Append one line to `./brand/assets.md`.

## What's next

- `/first-screen-check` on each new page, on a phone, before traffic goes to it (~10 min).
- `/google-business-profile` so the profile's services and links match the pages (~20 min).
- `/reviews` to keep fresh reviews coming in. The proof on these pages ages, and Google's rules forbid scripting what customers write (~15 min).
- `/performance-review` at 60-90 days to read the baseline and decide what to merge (~10 min).
