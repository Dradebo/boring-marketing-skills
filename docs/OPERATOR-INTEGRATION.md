# Operator integration — marketing execution front

This fork is **an execution toolkit, not a new go-to-market source of truth**.

## Authority and handoff

- Strategy and source-of-truth documents remain in **Sean OS — GTM & Living Portfolio**, beginning with **00 — SEAN GTM SOURCE OF TRUTH** and its existing Offers/Economics, Fishing, Content, Outreach, Public Surfaces, Experiments and Proof ledgers. Link to those records; do not recreate them here.
- Scheduling, next actions and obligations remain in **Time Radar**. A skill may propose an action, but never imply it has updated Time Radar without a confirmed write.
- This fork owns only *its own skill instructions, research notes, draft assets, execution evidence and measured learnings*. Work already completed elsewhere remains valid input.
- One active paid wedge and at most one contrasting prospecting pond per review; expand only on real responses. No new content or prospecting quotas by default.

## Existing fronts: where the skills plug in

| Current front | Relevant skills | Handoff (not duplicated strategy) |
| --- | --- | --- |
| **Fly Fisher / Operation Graveyard** | `find-local-clients` → `first-screen-check` → `pitch-the-fix` | One economically meaningful buyer problem, dated evidence, plausible payer, one small fix, one explicit GO/HOLD/KILL |
| **Personal presence / LinkedIn / portfolio repair** | `social-content`, `content-atomizer`, `performance-review` | Work-backed proof and one platform-native asset; no invented credentials, client outcomes or generic AI commentary |
| **Shelf Pulse and other commercial-ready products** | `positioning-angles`, `landing-page`, `ai-search` | One offer and measurable customer task; organic AI mentions are **not** paid ChatGPT ads |
| **ChatGPT discovery and ad-market investigation** | `ai-search` (organic) + separate, verified paid-ad research | Label discovery vs advertising, keep claims and access limits explicit; never imply the generic ad skills can buy ChatGPT placements |
| **Client operations / evidence-first consulting** | `audience-research`, `competitive-intel`, `performance-review` | Buyer language, baseline, delivered artifact and observed outcome |

## Operator loop

`Signal → Conversation → Diagnosis → Economics → Artifact → Offer → Delivery → Proof → Distribution → Learning`

The default action is the **smallest verified commercial next step**, not a new launch. Prefer a useful artifact to a meeting request. Public posts are a distribution channel for proof, not proof themselves. A reply is a signal; it is not a sale. Measured outcomes must retain sample size, source and date.

**Before running a campaign**

1. Read the relevant existing GTM record and `MARKETING.md` in the working campaign workspace.
2. State the current paid offer, target buyer, evidence of the problem and one success measure. Mark missing fields as unknown.
3. Pick the smallest sequence of existing skills. Don't auto-create a full content engine.
4. Stage research and drafts locally; require a human approval for contact, publishing, ad spend, account changes or customer-data transfer.
5. After action, preserve actual results separately from inferred opportunity.

## Time Radar handoff: minimum record

Use this as a *proposed interoperability contract*, not a claim about Time Radar's current database schema. Map into its real schema before writing.

| Field | Meaning |
| --- | --- |
| `campaign_id` | Stable ID; link existing campaign if it already exists |
| `source_record` | Canonical GTM/project record or dated research evidence |
| `offer_and_buyer` | Buyer task and the one thing offered |
| `stage` | observed / diagnosed / drafted / approved / contacted / replied / delivered / measured / parked |
| `artifact_path` | Exact local work file or live proof URL |
| `next_action` | Single action; null when there is no justified next step |
| `due_at` | Optional explicitly agreed deadline, never invented |
| `outcome` | Direct observation; human reply, paid job, rejection, or none |
| `evidence` | Source, date, sample size / denominator when relevant |
| `approval` | Required approval and whether it actually occurred |

Don't copy sensitive customer contact details into a shared marketing summary or an automation prompt. Prospect data stays inside the campaign workspace with appropriate access control.

## Practical first pass

Take one existing, evidenced offer from the canonical ledger. Audit up to ten relevant potential buyers (no bulk or guessed emails), shortlist three with one fixable leakage point each, prepare one-to-one draft approaches, obtain approval before contact, and record what *actually* happens. If the underlying problem cannot be confirmed, log HOLD or NONE rather than filling the pipeline with fiction.

## Fork maintenance

Keep original MIT attribution and upstream history. Keep operator-specific changes visibly scoped and easy to cherry-pick after upstream updates. Rerun tests and check diffs before merging. The repository's Claude hooks are a convenience guard, **not** a security boundary; file permissions, separate workspaces, and an approvals policy remain necessary.
