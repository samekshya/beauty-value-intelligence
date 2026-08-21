# Source Feasibility Report

**Project:** Beyond the Price Tag — Beauty Value Intelligence Engine
**Stage:** Phase 1 · Stage 1.0 — Feasibility
**Status:** Task B complete (desk research). Task C (measured testing) not started.
**All source checks performed:** 2026-08-22

---

## How sources are graded

Per spec §16 every source is graded against 16 fields. Per the project's
primary screening criterion, one field decides admission:

> A source that cannot reliably return product **size** (quantity + unit) is
> unusable for this project regardless of catalogue breadth, price accuracy,
> or cost.

Size availability is graded on three levels, because the difference decides
how much of the §27–31 parser is load-bearing:

| Level | Meaning |
| --- | --- |
| **Structured** | A dedicated quantity field carrying a value and its unit. |
| **Embedded** | Size exists only inside free text (usually the product title). Needs the parser. |
| **Absent** | Not available at usable reliability. Disqualifying. |
| **Unknown** | Not measured. Never assumed. |

### Evidence standard

Every claim below comes from a page fetched on 2026-08-22, with the URL
recorded. Where a page could not be read, the row says **unverified** and says
why. Nothing here is written from recall — several of these services changed
materially in ways that contradict widely repeated assumptions, and two of the
most commonly recommended sources turned out to be dead ends.

---

## Headline findings

Three results change the shape of the acquisition plan:

1. **Amazon's Product Advertising API v5 is deprecated and already returns
   `403 Forbidden`.** Its replacement gates access behind an active sales
   requirement. Amazon is not a viable source for this project.
2. **Google's Shopping Content API is the wrong direction of data flow.** It
   uploads *your own* catalogue to Merchant Center. It cannot query other
   retailers' products. It is not a candidate at all.
3. **Structured size data is scarce.** Not one source verified so far exposes a
   dedicated, unit-bearing quantity field for US makeup. The single candidate
   that plausibly does could not be verified, because its robots policy blocks
   this agent. Size will most likely arrive **embedded in text** and have to be
   parsed — which promotes the §27–31 parser from "hardest technical piece" to
   "the thing the dataset's existence depends on".

---

## Source assessments

### 1. Open Beauty Facts — open data, barcodes

| | |
| --- | --- |
| Access | Bulk exports: MongoDB dump, JSONL/NDJSON, Parquet (Hugging Face), CSV. Live JSON/XML API v2 and v3. |
| Auth | None for bulk exports |
| Cost | Free |
| Licence | Open Database License (structure); Database Contents License (records); Creative Commons Attribution ShareAlike (images) |
| **Size field** | **Unknown — unverified** |
| Checked | https://world.openbeautyfacts.org/data · 2026-08-22 |

**Legal status — exact directives read.**
`https://world.openbeautyfacts.org/robots.txt` (2026-08-22) contains:

```
User-agent: *
Disallow: /api
Disallow: /cgi
Disallow: /facets
```

and separate blanket blocks:

```
User-agent: ClaudeBot
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: Claude-Web
Disallow: /
```

`https://static.openfoodfacts.org/robots.txt` (2026-08-22) carries the same
`ClaudeBot` / `anthropic-ai` blanket `Disallow: /`, with `/data/` not
disallowed for `User-agent: *`.

Two distinct things must not be conflated:

- **Crawling the site** is disallowed for this agent, and `/api` is disallowed
  for *all* agents. The live API is therefore off-limits as a crawl target.
- **The bulk exports** are published deliberately under ODbL for reuse. That is
  a licensed distribution channel, not crawling, and is the only route worth
  considering.

No workaround was sought or is proposed. The consequence is simply that the
schema could not be confirmed: `data-fields.txt` is hosted only on domains that
block this agent.

**Why the size field is unverified.** Secondary sources describe a `quantity`
field holding "the net quantity or size of the product". That is plausible and
consistent with the sibling Open Food Facts schema, but it is second-hand and
is **not** recorded as fact. Two things remain genuinely unknown and both are
decisive:

1. Whether `quantity` is raw label text (`"50 ml"`) or a parsed numeric with a
   separate unit field. This is the difference between *structured* and
   *embedded*.
2. **US makeup coverage and fill rate.** Open Beauty Facts is contributor-driven
   and historically strongest on European groceries. Its makeup catalogue depth
   for US-market products, and how often `quantity` is actually populated on
   those rows, is unmeasured. A schema that supports a field says nothing about
   how often it is filled.

**Verdict:** Highest-value candidate to test, and the only plausible route to
*structured* size. Must be resolved in Task C by downloading a bulk export and
measuring US makeup rows directly — no site crawling required.

---

### 2. Amazon Product Advertising API — rejected

| | |
| --- | --- |
| Status | **Deprecated** |
| Checked | https://webservices.amazon.com/paapi5/documentation/ · 2026-08-22 |

The documentation URL `302`-redirects to a deprecation notice at
`https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation`,
which states:

> "PA-API 5 is no longer the recommended way to access Amazon's product catalog."

and that applications calling it "receive an HTTP `403 Forbidden` response". No
sunset date is given because access is *already* restricted. The successor is
the **Creators API**, "a REST-based API that provides programmatic access to
Amazon's product catalog data for publishers, influencers, and affiliate
partners."

**Eligibility — unverified from primary source.** Amazon's own Creators API
page (`https://affiliate-program.amazon.com/creatorsapi`) `302`-redirects to a
sign-in wall, so its terms could not be read. Multiple secondary sources
(affiliate-marketing publications, 2026) state access requires an approved
creator account plus **at least 10 qualifying sales in the past 30 days**, up
from 3 under PA-API 5, with access suspended if the threshold lapses. Treated as
**unconfirmed**, but directionally consistent with the deprecation page's
framing around "publishers, influencers, and affiliate partners".

**Verdict: Rejected.** Even at the low end, access is conditioned on running an
active affiliate business with continuous qualifying sales. That is not
satisfiable for a portfolio data project, and a source that can be revoked for
insufficient sales cannot underpin a reproducible pipeline (§89).

---

### 3. Google Shopping Content API — rejected, not a candidate

| | |
| --- | --- |
| Checked | https://developers.google.com/shopping-content/guides/quickstart · 2026-08-22 |

The API's direction of data flow is the opposite of what this project needs. It
exists to "Upload products", "Manage inventory", and "Manage Merchant Center
accounts" — pushing *your own* catalogue into Google. It requires your own
Merchant Center account and provides no facility to query other retailers'
listings.

**Verdict: Rejected.** This is a frequent misconception worth recording: the
name suggests a shopping search index, but it is a merchant-side publishing
API. It was never a candidate.

---

### 4. Brand-owned Shopify storefronts — e.l.f., Rare Beauty

| | |
| --- | --- |
| Access | Public storefront JSON; published XML sitemaps |
| Auth | None |
| Cost | Free |
| **Size field** | **Embedded** (see below) |
| Checked | robots.txt for both · 2026-08-22 |

**Legal status.** Both are Shopify storefronts with permissive robots policies.

`https://www.elfcosmetics.com/robots.txt` — `User-agent: *` disallows admin and
account areas (`/admin`, `/account`), cart and checkout (`/cart`, `/carts`,
`/checkout`, `/checkouts/`), `/orders`, `/policies/`, parameterised `/search`,
and theme-preview parameters. `AhrefsBot` gets a 10-second crawl delay; `Nutch`
is blocked. Product paths and JSON endpoints are **not** disallowed.
`Sitemap: https://www.elfcosmetics.com/sitemap.xml`.

`https://www.rarebeauty.com/robots.txt` — `User-agent: *` disallows `/admin`,
`/services`, `/sf_*`, `/cart/`, `/checkout`, `/checkouts/`, `/orders`,
`/account` (except login), `/cart.js`, `/recommendations/products`, and
filter/sort parameter permutations. The file states that "Public product,
collection, page, blog, policy, cart, and localized HTML is crawlable."
`Sitemap: https://www.rarebeauty.com/sitemap.xml`.

**The size problem — an important trap.** Shopify's product JSON exposes a
variant `weight` field, which looks like exactly what this project needs. It is
not.

- `weight` is **shipping weight**, which includes packaging. A 30 mL
  foundation's variant weight reflects the glass bottle, pump and carton, not
  the 30 mL of product. Using it as net quantity would silently corrupt every
  price-per-unit figure in the project — and would do so *plausibly*, which is
  worse than an obvious error.
- The Ajax product reference shows no `weight_unit` at variant level, so even
  the shipping weight arrives without a documented unit.
- Actual product size appears in variant `title` / `option1`–`option3` as text
  (the same slots that carry "Small/Medium/Large" for apparel).

Size is therefore **embedded**, and must come from the §27–31 parser applied to
variant titles and product names — never from `weight`.

*(Verified against Shopify's public documentation only. Whether e.l.f. and Rare
Beauty actually populate variant titles with sizes is a Task C measurement, not
an assumption.)*

**Verdict:** Strong candidate. Permitted, free, no auth, authoritative
(manufacturer-published, satisfying §13 item 4), and covers tiers at both ends.
Its ceiling is brand-by-brand breadth, not legality.

---

### 5. Maybelline — conditional

| | |
| --- | --- |
| Checked | https://www.maybelline.com/robots.txt · 2026-08-22 |

A single `User-agent: *` block disallows `/api/*`, `/sitecore/content`,
`/cdn-cgi/*`, `/formbuilder`, tracking parameters (utm, gclid, fbclid, msclkid,
ttclid), search/filter parameters — and notably the locale paths `/en/`,
`en-us/`, `en-US/`. Four `Sitemap:` directives are published.

Product pages are not disallowed as a class, but the disallowed locale prefixes
need care: if US product URLs resolve under a disallowed locale path, they are
off-limits. **Unresolved** — determining the live US product URL pattern is a
Task C check.

**Verdict:** Conditional. Not usable until the locale-path question is settled.
Not a blocker; Maybelline is one brand, not an architecture.

---

### 6. Sephora — excluded

| | |
| --- | --- |
| Checked | https://www.sephora.com/robots.txt · 2026-08-22 |

`robots.txt` itself returned **HTTP 403 Forbidden** — the file that exists to
declare crawler policy is not served to this agent. The site is behind bot
protection that refuses automated requests at the edge.

Per §14 and the project's rules of engagement: a source that blocks automated
access is recorded and set aside. No circumvention was attempted, evaluated, or
is proposed.

**Verdict: Excluded as a live source.** Note the consequence for scope —
Sephora is a primary US prestige and luxury retailer, so the high-end and luxury
tiers must be built from brand-owned sites and other retailers.

---

### 7. Ulta — excluded (terms prohibit it)

| | |
| --- | --- |
| robots.txt | https://www.ulta.com/robots.txt · 2026-08-22 |
| Terms | https://www.ulta.com/company/terms-and-conditions · 2026-08-22 |

**Correction to an earlier draft of this report.** The terms were initially
recorded as unreadable. That was a wrong URL, not a blocked page:
`/terms-and-conditions` serves a "Be Right Back" waiting-room interstitial,
while the actual document lives at `/company/terms-and-conditions` and loads
normally. Ulta is now fully resolved.

**robots.txt.** `User-agent: *` disallows only `/community/groups/*` and
`/community/groups?*`. No blanket `Disallow: /`, no `Crawl-delay`. Product pages
are not disallowed. A grouped block covering `GPTBot`, `CCBot`,
`Meta-ExternalAgent`, `PerplexityBot`, `ClaudeBot` and `Google-Extended`
disallows `/wishlists/`, `/curbside-alert/`, `/metrics1`–`/metrics3` and the
community paths — again, not product pages.

**Terms of use — verbatim clauses.** The terms grant only:

> "a limited license to access and make personal use of the Site and Site
> content only for noncommercial purposes"

and that licence expressly excludes:

> "any resale or commercial use of the Site; any collection and use of any
> product listings, descriptions, or prices; any derivative use of the Site"

It further prohibits:

> "any use of data mining, robots, or similar data gathering and extraction
> tools"

and:

> "The Site may not be reproduced, duplicated, copied, sold, resold, visited, or
> otherwise exploited for any commercial purpose without the express written
> consent of Ulta."

**Verdict: Excluded.** This is decisive on two independent grounds. The general
prohibition on "data mining, robots, or similar data gathering and extraction
tools" rules out automated collection, and the licence carve-out for "any
collection and use of any product listings, descriptions, or prices" names
precisely what this project would collect — so even manual collection of
listings and prices falls outside the granted licence.

**This is the case study for why robots.txt is not permission.** Ulta's
robots.txt is among the most permissive of any retailer checked: product pages
are open to every crawler including this one. Its terms nonetheless prohibit the
activity outright. §14 requires checking both, and where they disagree the terms
govern. Had only robots.txt been consulted, Ulta would have looked like the best
retailer source available.

**Consequence.** Ulta was the highest-value unresolved candidate because it
carries mass and prestige brands under one roof. Losing it, on top of Sephora,
means **no US multi-brand beauty retailer is available**, and all product data
must come from brand-owned sites one brand at a time. That also removes the
easiest route to multi-retailer price observations for the same product (§20).

---

### 8. SerpApi — commercial SERP/product API

| | |
| --- | --- |
| Access | REST API, API key |
| **Free tier** | 250 searches/month, 50/hour |
| Paid | $25/mo → 1,000 · $75/mo → 5,000 · $150/mo → 15,000 · $275/mo → 30,000 · $725/mo → 100,000 |
| **Size field** | **Embedded at best** |
| Checked | https://serpapi.com/pricing · 2026-08-22 |

Returns search-results data — titles, prices, merchant, link. Size is present
only when a merchant happens to put it in the listing title, so coverage is
inherited from other retailers' title conventions and cannot be relied on.

**Verdict:** Viable paid fallback for breadth and for cross-retailer price
observations (§20). Not a solution to the size problem. The free tier's 250
searches is enough to measure coverage in Task C without spending anything.

---

### 9. Historical Sephora dataset (Kaggle) — supplementary only

| | |
| --- | --- |
| Content | ~9,800 products across ~21 variables, including size, price, brand, category, rating, review count, ingredients |
| Checked | Kaggle dataset listings · 2026-08-22 |

Per §17 this is usable for bootstrapping the product catalogue, testing cleaning
logic, ingredient data, and historical metadata — and it does carry a size
column, which makes it genuinely useful for **developing and testing the
quantity parser before any live data exists**.

Its prices are historical and must be stored as `historical_price`, never as
`current_price` (§17, §83). Exact row counts and licence per specific dataset
are **unverified** — Kaggle dataset pages did not render for automated fetching,
so figures above come from secondary descriptions.

**Verdict:** Supplementary, never primary. High value as parser test material.

---

### 10. Not yet assessed

Recorded honestly rather than assumed. None of these are ruled in or out.

**eBay Browse API — partially verified, not recommended.**
Free, with a default application-level limit of **5,000 calls/day**; an
"Application Growth Check" (free, on request) raises it substantially. Auth is
OAuth via a developer account. **Size fields could not be confirmed** — the API
documentation timed out on three separate attempts and the field reference was
never read. Set aside on suitability rather than access: eBay listings are
seller-authored marketplace text, so brand, size and category are inconsistent
by construction, and prices reflect resale rather than retail. That fails §18's
"US beauty retail price snapshot" framing regardless of what the schema offers.

**Kroger Products API — unverified.**
The developer portal timed out on four separate attempts across two URLs, and
the documentation is JavaScript-rendered so search results could not extract the
field list either. A Products API exists; whether it exposes a structured size
field, its rate limits, and its cost are all **unknown**. Kroger's makeup
assortment is also mass-market only, so it could not serve the prestige or
luxury tiers even if it verified well.

| Source | Status | Reason |
| --- | --- | --- |
| CJ Affiliate product feeds | **unverified** | Product-feeds URL returned 404 |
| Impact.com product catalogue | **dropped** | Dropped by decision — approval latency unbounded, fields not documented publicly |
| Rakuten Advertising feeds | **not assessed** | Not reached |
| UPC/GTIN lookup services | **not assessed** | Relevant to §22 entity resolution, not to primary acquisition |
| Walmart / Target | **not assessed** | Not reached |

---

## Brand-level source coverage

Every brand named in spec §11, checked individually on 2026-08-22. Status is
from that brand's own `robots.txt` unless noted.

**Status key** — `Shopify`: Shopify storefront, product paths permitted ·
`SFCC`: Salesforce Commerce Cloud (Demandware) · `Other`: another platform ·
`BLOCKED`: robots.txt returned HTTP 403, so policy could not be read and the
site refuses automated requests · `PDP disallowed`: robots.txt explicitly
disallows product detail pages.

Note that platform is *not* the same question as permission. Both are recorded
because Shopify storefronts expose a consistent public product JSON structure,
which matters for how much per-brand work each source costs.

### Drugstore — 11 of 11 reachable

| Brand | Platform | robots status | Usable |
| --- | --- | --- | --- |
| e.l.f. | Shopify | Permissive | Yes |
| Milani | Shopify | Permissive | Yes |
| Essence | Shopify | Permissive | Yes |
| Wet n Wild | Shopify | Permissive | Yes |
| Revlon | Shopify | Permissive (blocks only `-remote` variant URLs) | Yes |
| ColourPop | Shopify | Permissive | Yes |
| Physicians Formula | Shopify | Permissive | Yes |
| CoverGirl | Other | `Allow: /`; ClaudeBot named and permitted | Yes |
| L'Oréal Paris | Other (Sitecore) | Permissive; blocks filter parameters only | Yes |
| NYX | SFCC | Permissive; PDPs not disallowed | Yes |
| Maybelline | Other (Sitecore) | Conditional — disallows `/en/`, `en-us/`, `en-US/` | Verify |

### Mid-range — 4 of 4 reachable

| Brand | Platform | robots status | Usable |
| --- | --- | --- | --- |
| Morphe | Shopify | Permissive | Yes |
| Juvia's Place | Shopify | Permissive | Yes |
| Pixi | Shopify | Permissive | Yes |
| Kiko Milano | Other | Permissive; blocks `/sku`. US storefront presence unconfirmed | Verify |

### High-end — 11 of 14 clean, 1 conditional, 2 blocked

| Brand | Platform | robots status | Usable |
| --- | --- | --- | --- |
| MAC | Shopify | Permissive | Yes |
| Rare Beauty | Shopify | Permissive | Yes |
| Fenty Beauty | Shopify | Permissive; ClaudeBot explicitly granted access | Yes |
| Tarte | Shopify | Permissive (blocks Nutch, Amazonbot) | Yes |
| Anastasia Beverly Hills | Shopify | Permissive; AI crawlers explicitly allowed | Yes |
| Huda Beauty | Shopify | Permissive | Yes |
| Makeup by Mario | Shopify | Permissive | Yes |
| Haus Labs | Shopify | Permissive | Yes |
| Saie | Shopify | Permissive | Yes |
| Tower 28 | Shopify | Permissive | Yes |
| NARS | SFCC | Permissive; PDPs allowed | Yes |
| Urban Decay | SFCC | Conditional — `Disallow: */Product-Get*`, `Crawl-delay: 5` | Verify |
| Benefit | — | **BLOCKED** (403) | No |
| Too Faced | — | **BLOCKED** (403) | No |

### Luxury — 2 of 7 reachable

| Brand | Platform | robots status | Usable |
| --- | --- | --- | --- |
| Tom Ford Beauty | Shopify | Permissive | Yes |
| Armani Beauty | SFCC | Permissive; PDPs allowed | Yes |
| YSL Beauty | SFCC | **`Disallow: */Product-Show`** — PDPs disallowed | No |
| Dior | — | **BLOCKED** (403) | No |
| Givenchy Beauty | — | **BLOCKED** (403) | No |
| Guerlain | — | **BLOCKED** (403) | No |
| Chanel | — | **BLOCKED** (403) | No |

### Damage to the §10 tier targets

| Tier | §10 target | Brands usable | Assessment |
| --- | --- | --- | --- |
| Drugstore | 300 | 11 (10 clean + 1 verify) | **Comfortable.** ~30 products/brand clears it. |
| Mid-range | 100–150 | 4 (3 clean + 1 verify) | **Tight but workable.** Needs ~30/brand from a thin roster; §11 already invited "selected other brands" here. |
| High-end | 250 | 12 (11 clean + 1 verify) | **Comfortable.** |
| Luxury | 100 | **2** | **At risk.** 50 products/brand from two brands. |

Luxury is the only tier in real trouble, and the failure is not random. Every
blocked or restricted luxury brand is a conglomerate-owned European house —
Dior, Givenchy and Guerlain (LVMH), Chanel, and YSL (L'Oréal Luxe). The two
survivors are Tom Ford Beauty, which runs a Shopify storefront, and Armani
Beauty, whose SFCC robots.txt happens to permit PDPs. §11 already anticipated
part of this by hedging Chanel and Guerlain with "if usable data is available";
the answer is that it is not.

---

## RISK: platform-reachability bias in tier composition

**Named risk. Unresolved — decision required.**

### The concern

If reachable brands skew toward DTC/Shopify-native companies, then a finding
reported as "drugstore vs prestige" is partly measuring "DTC vs legacy" — a
different question, and a direct threat to the §98 central research question.
Package-size strategy plausibly differs by business model: a DTC brand
controlling its own margin and shipping economics has different incentives on
fill volume than a legacy brand selling through wholesale retail.

### What the data actually shows

The concern is real but **narrower than "DTC vs legacy"**, and the distinction
matters for choosing a response.

Reachability does *not* track DTC status at the drugstore or high-end tiers.
Revlon, CoverGirl, L'Oréal Paris, NYX, Maybelline and Physicians Formula are all
legacy wholesale brands, and all are reachable. MAC and NARS are
conglomerate-owned prestige brands (Estée Lauder, Shiseido), and both are
reachable. Several legacy mass brands have simply migrated to Shopify, so
"Shopify" is not a proxy for "DTC-native".

The bias is concentrated almost entirely in **one tier and one corporate
cohort**: European luxury houses under LVMH, Chanel and L'Oréal Luxe. Those
brands block automated access, and they are exactly the brands defining the
luxury tier.

So the accurate statement of the risk is not "the sample skews DTC" but:

> **The luxury tier cannot be sampled representatively. What survives is two
> brands that happen to be reachable, which is a selection mechanism unrelated
> to the pricing behaviour being measured — but plausibly correlated with it,
> since a house that refuses automated access may also price and package
> differently from one that runs an open storefront.**

Drugstore, mid-range and high-end tiers do not have this problem in any severe
form.

### Options — tradeoffs, not a recommendation

**Option A — Accept and document.**
Keep all four tiers. Report luxury findings with an explicit caveat naming the
two brands and the blocked five, and treat luxury n as too small for inference.

*For:* Preserves the §10 four-tier structure and the §6 research questions
unchanged. Costs nothing. Honest, if the caveat is prominent rather than buried
in limitations.
*Against:* A two-brand tier will still be read as "luxury" by anyone skimming
the app or README. Any luxury-tier statistical test would be underpowered and
arguably shouldn't be run at all, which makes the tier decorative. Risks the
appearance of rigour without the substance — the failure mode §97 warns against.

**Option B — Narrow the tier claims.**
Merge luxury into high-end, or relabel the tier to what it can actually support
(for example "prestige — accessible sample"). Report three tiers.

*For:* Every reported tier then has a defensible sample. Statistical claims stay
sound. Removes the most likely interview criticism before it is raised.
*Against:* Loses the most rhetorically striking comparison — a $70 Chanel
lipstick against a $6 e.l.f. one is the example that makes the project land.
Deviates from §10 and §11, requiring documented justification. The prestige
premium at the very top end goes unmeasured, which is where it is largest.

**Option C — Reframe the question around what is measurable.**
Make reachability part of the analysis rather than a limitation of it. State the
scope as US makeup brands with publicly accessible product data, and note that
the brands refusing automated access cluster at the luxury end — an observation
about the market, not merely about the dataset.

*For:* Turns the constraint into a finding and is fully honest about the sample
frame. Data-access asymmetry across market tiers is genuinely interesting to
retail analytics audiences. Nothing is hidden.
*Against:* Changes the headline question, which §98 says not to lose sight of.
The observation is real but thin — five blocked domains is an anecdote, not
evidence about industry practice, and overclaiming from it would be its own
fabrication. Risks looking like rationalisation of a data-collection failure.

### What is not in question

Whichever option is chosen, tier assignment still comes from brand positioning
and never from price (§12), and the drugstore/mid/high-end comparisons remain
sound. This risk is about the luxury tier's representativeness, not about the
integrity of the central research question at the tiers where sampling works.

---

## Where this leaves the acquisition plan

**The bottleneck is size, and it is worse than the spec's §88 target assumes.**
§88 sets a quantity-coverage target of >90%. Nothing verified so far offers
structured, unit-bearing quantity for US makeup. The realistic architecture is:

- **Text-embedded size, parsed** — from brand-owned storefronts, where the
  manufacturer publishes the size and the data is authoritative.
- **Structured size, if it exists at all** — Open Beauty Facts bulk export,
  unconfirmed on both schema and US makeup fill rate.

This raises the stakes on the §27–31 parser considerably. It is no longer merely
"the hardest technical piece" of Stage 1.2 — it is the component that determines
whether a dataset exists. It also makes the Shopify `weight` trap the single
most dangerous available shortcut, because it yields a plausible number that is
wrong in a way no downstream check would catch.

**No US multi-brand beauty retailer is available.** Sephora blocks automated
requests at the edge; Ulta's terms prohibit collection of product listings and
prices outright. eBay is accessible but unsuitable, and Kroger is both unverified
and mass-market only. Every product must therefore come from a **brand-owned
site, one brand at a time** — which is more work but yields manufacturer-
authoritative data (§13 item 4).

**One consequence deserves flagging now, because it constrains Phase 2.**
§20 specifies preserving multiple retailer observations per product, and §18
requires a `retailer` field. With no multi-brand retailer available, nearly every
product will have exactly **one** offer, from the brand itself. The
`product_offers` table stays correct by design but will be effectively one row
per product, and cross-retailer price dispersion cannot be analysed. Brand-owned
pricing is also list pricing, which suits §19's requirement that unit-value
analysis use list price — but it means the dataset represents manufacturer RRP,
not street prices, and the README and methodology must say so plainly.

Next step is Task C: measure, rather than estimate, the field coverage of the
shortlisted sources against a fixed set of 20 products spanning tiers and
categories.
