---
name: keyword-research
description: Maps what people search for and ask about a business as a topic map rather than a 5,000-row keyword list, using free autocomplete and Search Console first, covering both Google searches and the questions people put to AI assistants, going deep only on the topics worth acting on, and ending in ready-to-write briefs. Use when planning content, choosing what to write about, finding content gaps, or building an SEO and AI-search plan, for an online business or a local one.
when_to_use: keyword research for X, content strategy for X, what should I write about, what topics should I cover, SEO strategy, topic clusters, topic map, content gaps, competitor keywords, content plan, what do people search for in my industry, what questions do customers ask about X
argument-hint: "[topic, niche, or seed keywords]"
metadata:
  boring:
    version: 4.0.0
    layer: strategy
    reads: [positioning#chosen-angle, audience#watering-holes, competitors#competitor-profiles, voc]
    writes: [keyword-plan]
    optional-keys: [DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD, TREG_TOKEN, FIRECRAWL_API_KEY, GOOGLE_APPLICATION_CREDENTIALS, GSC_ACCESS_TOKEN]
    enhances_with:
      - toolset: search-console
        gains: "the site's own queries, striking-distance pages and unserved demand, the best keyword data there is"
      - toolset: web-scrape
        gains: "full reads of ranking pages for word counts, structure and schema instead of snippets"
---

# Keyword Research

The unit of this work is the topic, and the win is being the page or the source that answers it. Keywords are evidence that a topic has demand, nothing more. This skill turns a business into a topic map: families of related searches and questions, each with its demand evidence, a verdict, and a ready brief for the ones worth doing now. Done means a short decision queue (NOW, NEXT, HOLD, DROP) another person could defend from the evidence, and briefs /seo-content can write from without researching again. The method is a floor. When the business in front of you argues for a better path, take it and say why in one line.

## Context

Only if `./brand/`, `./brands/` or `MARKETING.md` exists (nothing to load otherwise), run:
`python3 ${CLAUDE_SKILL_DIR}/../start-here/scripts/brand_context.py --for keyword-research`
(`${CLAUDE_SKILL_DIR}` is this skill's folder; outside Claude Code use the folder this file was read from, e.g. `.agents/skills/keyword-research`. If the script or python3 is unavailable, read the brand folder directly: `./brands/<slug>/` when `./brands/active` names one, else `./brand/`; then `MARKETING.md`, `preferences.md` and the files in `reads:`. If none exist, proceed standalone and ask only what you sell, who you serve, the site, and the goal: traffic, leads, sales or authority.)

Positioning shapes how you write about a topic, never which topics you target. A brand positioned as "the anti-agency" writes about "marketing strategy" with an anti-agency angle. It doesn't target "anti-agency" as a keyword.

## Modes

- **Full research** (no `./brand/keyword-plan.md`): all phases.
- **Refresh** (a plan exists): re-run Rung 2 on the existing NOW and NEXT families only, diff against the old plan, version the old copy, and summarize what moved. Don't rebuild unless asked.
- **Briefs only** (the user names the keywords): Quick Mode. Skip to Rung 3 for those topics.
- **Local business:** everything below applies, plus the Local branch. Questions about which services and towns get pages belong to /local-seo-plan; this skill maps the topics (guides, cost and symptom content, comparisons) around them.

## Phase 0. Data sources

Detect what's available and say what you found in one line.

| Source | Detection | What it gives |
|---|---|---|
| Google autocomplete | always (`scripts/suggest.py`) | Real phrasings people type, free |
| Search Console | `GOOGLE_APPLICATION_CREDENTIALS` or `GSC_ACCESS_TOKEN`, or `gcloud auth application-default print-access-token` works with the Search Console scope, or a user export | The site's own queries and pages |
| Google Ads Keyword Planner | user has an Ads account | Volume ranges by location, free |
| DataForSEO (what we use) | `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`, or a volume tool you already pay for | Real monthly search volumes (any one volume source is enough) |
| Firecrawl (what we use) | `FIRECRAWL_API_KEY` or MCP tools | Full page and results scraping |

We use DataForSEO for volumes and SERP data: real monthly search volumes instead of autocomplete and live checks alone, pay as you go with no subscription ($50 minimum top-up that does not expire, plus a $1 trial credit on sign-up). Without it, autocomplete, Search Console and the live results rank the topics without volumes. If you'd rather not open another account, treg (one token for many data APIs, pay per call) reaches SEO and SERP data too. We use Firecrawl to read the ranking pages in full (free tier of 1,000 credits a month, no card). Without it, WebFetch reads them as summaries and the plan says so.

**Search Console pull** (whenever access exists). Query the last 90 days, dimensions `["query","page"]`. A plain `gcloud auth login` token lacks the Search Console scope, so set up application-default credentials once: `gcloud auth application-default login --scopes=https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform`. A service account must be added as a user on the property. URL-encode the site (`sc-domain%3Aexample.com` for a domain property, the encoded address for a URL-prefix one).

```
curl -s -X POST \
  -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  -H "x-goog-user-project: <your-project-id>" \
  -H "Content-Type: application/json" \
  "https://searchconsole.googleapis.com/webmasters/v3/sites/{encoded-siteUrl}/searchAnalytics/query" \
  -d '{"startDate":"<90d ago>","endDate":"<today>","dimensions":["query","page"],"rowLimit":5000}'
```

Pull out two lists. **Striking distance:** queries with 50 or more impressions at an average position of 8 to 30. Google already half-likes a page for these, so improving it beats writing something new. **Unserved demand:** queries with real impressions and no page genuinely about them.

**Data label.** Every deliverable carries one line: `Data: LIVE (suggest + N result pages + Search Console)` or `Data: MODEL KNOWLEDGE (verify before spending)`. Without a volume source, print no volume numbers. Use demand evidence (autocomplete richness, Search Console impressions, how much competitors invest) and prefix any estimate with `~`.

## Two query spaces

Treat both as first-class from the first seed:

1. **Search-visible demand.** What people type into Google: autocomplete, Search Console, volume tools.
2. **AI-native questions.** The longer, conversational questions people ask ChatGPT, Perplexity, Gemini or Google's AI Mode ("is a proposal tool worth it if I only send three proposals a month?"). Many show near zero Google volume and still decide who gets recommended. Free sources: the question forms autocomplete returns (`--mode questions`), the questions Google shows in results, forum and Reddit threads, long queries in Search Console (six words or more are often conversational), `voc.md`, support tickets, sales call notes and reviews.

The two spaces disagree, and that disagreement is signal. A family that is strong in AI-native questions but modest on Google can outrank a high-volume head term for a business that wants to be the cited answer. Without a paid AI-volume source, record AI-native demand as "observed phrasing, no volume". Never invent a number for it.

## Phase 1. Seed with the six circles

Default: 20 to 30 seeds from six lenses. Each lens exists because teams reliably skip it and then wonder why the plan looks like their navigation menu. Example business: a proposal-software product for freelancers.

1. **What you sell.** The category words buyers use, not internal names. "proposal software", "proposal templates", "client contracts"
2. **Problems you solve,** phrased the way people who have them phrase them. "client ghosting after proposal", "how long should a proposal take", "scope creep"
3. **Outcomes you deliver.** "win more clients", "raise freelance rates"
4. **Your positioning** (from `positioning#chosen-angle`). Seeds where your angle is the answer. Angle "close on the call" gives "live proposal walkthrough".
5. **Adjacent topics,** where the audience already spends attention (`audience#watering-holes`). "freelance pricing", "first client onboarding"
6. **Entities to be named next to:** tools, frameworks, people, competitors. AI answers work by association, so the entities you consistently appear beside shape which conversational questions cite you. "value-based pricing", named competitors for comparison pages

Label each seed with its circle and its likely intent (informational, commercial, transactional). Group the seeds into 4 to 8 **topic family candidates**: areas broad enough for one hub piece and 3 to 7 supporting pieces. They are hypotheses until Rung 1 tests them.

## Phase 2. The depth ladder

Go only as deep as a decision needs. Depth is spent on topics you'll act on, never on every keyword. **Tripwire:** if you are about to fetch result pages for every keyword, or enrich every row of the tail, stop. You've rebuilt the pipeline this skill exists to replace.

### Rung 1. Infer the terrain (every family, cheap)

For each family's head term and its strongest one or two seeds:

`python3 ${CLAUDE_SKILL_DIR}/scripts/suggest.py "<keyword>" --format json`

It queries Google's suggest endpoint across alphabet, question, preposition and comparison probes (about 50 requests, free, no key). Use `--mode questions,prepositions` for secondary seeds. Harvest: phrasings you didn't think of, recurring modifiers, question forms (for the AI-native space), year modifiers, brand mentions. Match the families against Search Console rows if you have them.

Record per family: autocomplete richness, Search Console impressions, the AI-native questions found, and any volume figures with their source. Then cut. Families with no demand evidence in either space drop here, before anything expensive happens.

**Spot patterns from a sample.** A programmatic shape ("X for [industry]", "[tool A] vs [tool B]", "[service] in [town]") needs at least two different observed substitutions of the same frame. Record the shape and its examples. Never enumerate the missing substitutions to prove it.

### Rung 2. Test the promising few (at most 5 families)

One research subagent per promising family, all in parallel (Task tool, `general-purpose` when the plugin's research type is unavailable), each under the research budget (40 fetches, 8 minutes, no sub-agents of its own). Write the plan from what they return. No second research pass.

Each subagent, for its family:
1. **Results capture.** For the 5 to 10 strongest keywords, fetch the results page (Firecrawl search if available, else WebSearch), then the top 3 to 5 ranking pages. Record URL, title, content type, published or updated date, word count, structured data, from the fetched page, never from the snippet. Record the result features present and the questions Google shows, verbatim.
2. **AI-surface capture.** Whether an AI Overview appears, whether it fully answers the query, which domains it cites. Then ask the conversational version through web search and note who gets cited for that phrasing.
3. **Competitor coverage.** `site:{domain}` searches per family for the domains in `competitors#competitor-profiles`: what they cover, how well, what they skip.

Pack format per subagent: `{family, keywords: [{kw, suggest_hits, results: [...], features, questions: [...], ai_overview: {present, fully_answers, cited_domains}, competitor_coverage}], ai_native_questions: [...], discoveries: [...]}`.

Merge the packs and surface the 3 to 5 discoveries that change a decision ("a Reddit thread ranks third for X and no good article exists", "competitor A has nothing on Y").

### Rung 3. Go deep on what you commit to

Briefs, full outlines and the coverage map (every sub-question, the entities to name, the answer each heading must give) only for NOW families. That is Phase 4.

## Local branch

Apply when the business serves customers in places: a trade, a clinic, a shop. Sample business: Hartline Plumbing, Dallas TX.

1. **Pages for services and towns are /local-seo-plan's decision.** Keep this skill on the topics around them: cost guides, symptom and how-to questions, comparisons ("tankless vs tank in North Texas"), seasonal content.
2. **Every results check names the place.** Put the city and state in the query, or set the search location. A national check for a local business is mislabeled evidence and gets labeled as such.
3. **Demand finds opportunities. Proof that the business does the work authorizes the claim.** A family about a service the business doesn't deliver is HOLD at any volume. "Gas line repair" for a plumber without the license waits for the license.
4. **Read local numbers carefully.** Metro, city and county volumes overlap, so never add them. Close variants returning the same number are one intent. No estimate isn't zero, and the lowest reporting tier isn't a count. Cost per click describes the ad auction, not ranking difficulty. Read the monthly series, because trades are seasonal. (The full rules live in /local-seo-plan's `references/reading-local-data.md`.)
5. **"Near me" searches resolve in the map pack.** Their volume is metro-wide and the winner is decided by the Google profile, so route that gap to /google-business-profile rather than writing content for it.
6. **AI-native questions for a local business are full of place and urgency** ("who can fix a water heater in Garland today that takes weekend calls?"). Collect them from call notes, texts and reviews first. That's where the customer's exact words are.

Six-circle seeds for the sample plumber: sell ("water heater replacement"), problems ("water heater leaking from bottom"), outcomes ("hot water back same day"), positioning ("upfront pricing plumber"), adjacent ("Texas winter freeze pipes"), entities (brands they install, the city's permit office).

## Phase 3. Cluster and validate

**Cluster** the surviving keywords inside each family, intent first and wording second. "best crm software" and "what is a crm" share words but are different pages. Attach each cluster's questions (they become H2s), result evidence, AI Overview status and competitor coverage.

**Programmatic check.** A cluster with a substitutable slot, at least 10 slot values with demand evidence, and a dataset that makes each page genuinely different is tagged `route: /programmatic-seo`. Town and service-area variants for a local business are tagged `route: /service-area-pages` instead. Variants that need different arguments per page stay `route: /seo-content`.

**Validate each family** with Rung 1 and 2 evidence. A family failing two or more checks becomes a single article or drops, however on-brand it feels.

1. **Demand evidence**, ranked by strength: Search Console impressions, then a volume source, then autocomplete richness (30 or more distinct completions suggests real demand, 2 doesn't), then visible competitor investment. AI-native questions count when observed. No signal in either space fails.
2. **Market, not product.** "Our methodology" and "[your tool] tutorials" fail. "[category] strategy" and "[problem] solutions" pass. Nobody searches your product name unless you're famous.
3. **Competitive reality.** Dominant brands across fresh, thorough results: find an adjacent or longer-tail family. A mix of big and niche sites: winnable with better content. Thin, dated or generic results: opportunity. Reddit or forums in the top 5 is the strongest gap signal there is, since no adequate article exists and Google is rewarding first-hand experience. Check `references/facts.md` for which AI engines currently cite those threads.
4. **Proprietary advantage.** Original data, method or practitioner experience competitors can't copy. With it, prioritize hard; first-party data is also the strongest AI-citation driver. Without it, the family can pass but can't lead.

Record per family: `demand PASS/FAIL (evidence) · market PASS/FAIL · competitive PASS/FAIL (results evidence) · advantage YES/NO (what)` and the verdict. A calibrated example:

```
Family: Proposal Methodology (the founder's own framework)
demand FAIL: 3 autocomplete completions, no Search Console impressions, no AI-native questions found
market FAIL: product-centric; the market searches "how to write a proposal"
competitive PASS: thin results, trivially, because nobody searches it
advantage YES: original framework
VERDICT: DROP as a family. Fold the framework into "how to write a proposal" as its angle.
```

That last move is the recurring judgment. A failed family with a real advantage doesn't die. It becomes the angle inside a family the market actually searches.

## Phase 4. Prioritize and brief

Score each surviving family on three axes.

**Business value** (high, medium, low): closeness to revenue. Commercial and bottom-funnel families outrank awareness topics even at a tenth of the demand.

**Competitive opportunity** (high, medium, low): from Phase 3, plus striking-distance status. A page already at position 8 to 30 is the fastest win available.

**AI visibility**, three fields per family:
- `zero_click_risk` HIGH, MED or LOW. HIGH means an AI Overview fully answers the query (a definition, a quick fact) and the click rarely happens.
- `citation_path` YES or NO. YES when the current citations are beatable on format or data, or the conversational phrasing has no settled answer. NO when the citations are locked to major authorities and you bring nothing original.
- `conversational_targets`: 2 or 3 AI-style phrasings the brand should be cited for. They go into briefs as answer blocks.

A high-demand informational family with `zero_click_risk: HIGH` and `citation_path: NO` drops to HOLD whatever its volume: it would be traffic-free content. A modest family with a clear citation path moves up, because AI-referred visitors convert better and few competitors are working for those citations yet. (Current figures: /ai-search's `references/aeo-facts.md`.)

**The decision queue:**

| Business value | Opportunity | AI visibility | Verdict |
|---|---|---|---|
| High | High | LOW risk or citation path | **NOW** |
| any | striking distance | any | **NOW** (fixing beats writing) |
| High | Medium | citation path YES | NEXT |
| Medium | High | LOW risk | NEXT |
| High | Low | citation path YES | NEXT (a citation play) |
| any | any | HIGH risk and no citation path | HOLD |
| Low | any | any | HOLD |
| fails validation, or a service the business can't deliver | | | DROP or HOLD with its unlock |

NOW and NEXT are few by design. Commitment is the user's move, and the queue hands them exactly that decision instead of a calendar pretending ten topics start at once.

**Backlog.** An ordered list, not dated slots: rank, piece title, family, route, a one-line reason, status `planned`. Striking-distance fixes rank above new pieces of equal value.

**Briefs** for every NOW family routed to /seo-content, written to `./campaigns/content-plan/{keyword-slug}.md` following the content-brief schema when the folder `${CLAUDE_SKILL_DIR}/../start-here/references/schemas/` is present (otherwise the same fields as plain markdown): results analysis (top results with fetched word counts, strengths, weaknesses, `content_gap`), the questions verbatim, recommended structure, search intent and the call to action. Leave out monthly volume unless a real number came from Search Console or a volume tool.

Brief craft that separates a usable brief from a keyword with headers:
- The content type follows the results. If the top 5 are all comparisons, a long guide won't rank. Match the format and beat it on substance.
- Target length is the median of the fetched top results, plus or minus 20%.
- Questions become H2s phrased as the question. Open with a 40 to 60 word direct answer to the main query.
- `must_include` carries the advantage from Phase 3 and the `conversational_targets` as answer blocks.
- `content_gap` is specific ("no result shows real numbers from a finished project"), never "could be more comprehensive".

For families routed to /programmatic-seo or /service-area-pages, write one routing note instead of briefs: the frame, the slot, the observed examples, the data source, the demand evidence.

## Output

Write `./brand/keyword-plan.md` (version the old copy first). Sections: business context; sources and data label; the topic map (each family with its hub, clusters, both demand spaces, validation and verdict); a table under the heading `## Cluster Priorities` with priority (NOW maps to high, NEXT to medium, HOLD to low), intent, route, `zero_click_risk` and `citation_path` (keep that heading exactly; /performance-review reads it by anchor); competitor gaps; the ordered backlog; the brief index. Append one line per brief to `./brand/assets.md`.

In chat, following the four-section output contract: the family verdicts, the 3 to 5 discoveries, the top of the backlog, and one **start here** recommendation with its evidence, then **Files saved** and **What's next**.

## What's next

- `/seo-content` writes the first NOW piece from its brief (~20 min).
- `/programmatic-seo` or `/service-area-pages` if a family was routed there.
- `/ai-search` if several families showed a citation path, to check who AI assistants name today (~20 min).
- `/local-seo-plan` for a local business, to decide which services and towns get pages (~30 min).
