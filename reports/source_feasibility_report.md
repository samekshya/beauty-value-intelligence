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

### 7. Ulta — robots permissive, terms unverified

| | |
| --- | --- |
| Checked | https://www.ulta.com/robots.txt · 2026-08-22 |

`User-agent: *` disallows only `/community/groups/*` and `/community/groups?*`.
There is no blanket `Disallow: /` and no `Crawl-delay`. Product pages are not
disallowed for general crawlers. A grouped block covering `GPTBot`, `CCBot`,
`Meta-ExternalAgent`, `PerplexityBot`, `ClaudeBot` and `Google-Extended`
disallows `/wishlists/`, `/curbside-alert/`, `/metrics1`–`/metrics3` and the
community paths — but again not product pages.

**Terms of use — unverified.** `https://www.ulta.com/terms-and-conditions`
served a "Be Right Back" waiting-room page, so no clause could be read.

This gap is decisive and must not be glossed. §14 requires checking *terms of
use* **and** robots policy. A permissive robots.txt is not permission — retail
terms commonly prohibit automated extraction regardless of what robots.txt says,
and robots.txt is the weaker signal of the two.

**Verdict:** Cannot be classified. Blocked pending a readable terms page. Do not
treat as approved on robots.txt alone.

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

| Source | Status | Reason |
| --- | --- | --- |
| eBay Browse API | **unverified** | Documentation fetch timed out twice |
| Kroger Products API | **unverified** | Developer portal timed out twice |
| CJ Affiliate product feeds | **unverified** | Product-feeds URL returned 404 |
| Impact.com product catalogue | **partial** | "600M+ products" marketplace confirmed; access terms, cost and fields not public — requires signup to determine |
| Rakuten Advertising feeds | **not assessed** | Not reached |
| UPC/GTIN lookup services | **not assessed** | Relevant to §22 entity resolution, not to primary acquisition |
| Walmart / Target | **not assessed** | Not reached |

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

**Retailer coverage is narrower than hoped.** Sephora is excluded and Ulta is
unresolved, so the prestige and luxury tiers (§10 targets 250 high-end and 100
luxury products) will have to come from brand-owned sites, one brand at a time.

Next step is Task C: measure, rather than estimate, the field coverage of the
shortlisted sources against a fixed set of 20 products spanning tiers and
categories.
