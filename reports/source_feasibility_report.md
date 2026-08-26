# Source Feasibility Report

**Project:** Beyond the Price Tag — Beauty Value Intelligence Engine
**Stage:** Phase 1 · Stage 1.0 — Feasibility
**Status:** All measurements complete (Open Beauty Facts and Google Shopping titles measured 2026-08-26). Decision memo written — final section. Branch decision pending at Gate 1.0.
**All source checks performed:** 2026-08-22 (Open Beauty Facts export measured 2026-08-26)

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
3. **Drugstore brands do not publish product size.** Measured across 1,098
   drugstore products from five brand storefronts: **zero** carry a quantity,
   uniformly across every brand, confirmed by a second method. Overall
   coverage from permitted sources is 11.4% — 380 products of 3,333 — and
   none of them are drugstore. Every US retailer that sells mass-market makeup
   (Sephora, Ulta, Target, Walmart) is closed on terms or at the edge. The
   only identified route to structured quantity, Open Beauty Facts, is
   untested. The §98 research question is currently unanswerable.

---

## Source assessments

### 1. Open Beauty Facts — open data, barcodes

| | |
| --- | --- |
| Access | Bulk exports: MongoDB dump, JSONL/NDJSON, Parquet (Hugging Face), CSV. Live JSON/XML API v2 and v3. |
| Auth | None for bulk exports |
| Cost | Free |
| Licence | Open Database License (structure); Database Contents License (records); Creative Commons Attribution ShareAlike (images) |
| **Size field** | **Structured** — `product_quantity` + `product_quantity_unit`, with the raw label in `quantity`. Measured 2026-08-26: usable fill rate, negligible US-makeup volume. See *Open Beauty Facts — measured*. |
| Checked | https://world.openbeautyfacts.org/data · 2026-08-22 · export measured 2026-08-26 |

**Legal status — exact directives read.**
`https://world.openbeautyfacts.org/robots.txt` (2026-08-22) contains:

```
User-agent: *
Disallow: /api
Disallow: /cgi
Disallow: /facets
```

followed by blanket `Disallow: /` blocks for roughly 45 named third-party
crawlers — SEO tools, scrapers, and the crawlers of several LLM companies.

`https://static.openfoodfacts.org/robots.txt` (2026-08-22) carries the same
named-crawler blanket blocks, with `/data/` not disallowed for
`User-agent: *`.

Two distinct things must not be conflated:

- **Crawling the site** is disallowed for the named crawlers, and `/api` is
  disallowed for *all* crawlers. The live API is therefore off-limits as a
  crawl target.
- **The bulk exports** are published deliberately under ODbL for reuse. That is
  a licensed distribution channel, not crawling, and is the only route worth
  considering.

No workaround was sought or is proposed. The consequence is simply that the
schema could not be confirmed: `data-fields.txt` is hosted only on domains
where automated fetching for this study was refused.

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
declare crawler policy is not served to automated requests. The site is behind
bot protection that refuses them at the edge.

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
are not disallowed. A grouped block naming six third-party crawlers (search
and LLM-company bots) disallows `/wishlists/`, `/curbside-alert/`,
`/metrics1`–`/metrics3` and the community paths — again, not product pages.

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
| **Size field** | **Embedded at best** — measured 2026-08-26: a size appears in at least one listing title for 12 of 20 drugstore products, in 5.1% of listing titles overall, and the figures disagree across listings. See *Google Shopping titles via SerpApi — measured*. |
| Checked | https://serpapi.com/pricing · 2026-08-22 · probe run 2026-08-26 |

Returns search-results data — titles, prices, merchant, link. Size is present
only when a merchant happens to put it in the listing title, so coverage is
inherited from other retailers' title conventions and cannot be relied on.

**Verdict:** Viable paid fallback for breadth and for cross-retailer price
observations (§20). Not a solution to the size problem. The free tier's 250
searches is enough to measure coverage in Task C without spending anything.

#### Google Shopping titles via SerpApi — measured

Run 2026-08-26 with `python src/ingest/feasibility_serpapi_probe.py`. Every
figure is from `data/raw/feasibility/_serpapi_summary.json`; the twenty raw
responses are in `data/raw/feasibility/serpapi/` with provenance and the key
scrubbed.

*Design.* Twenty drugstore products, four per brand whose storefront probe
succeeded (ColourPop, essence, Milani, Physicians Formula, Wet n Wild), taken
in handle order with sets, kits, tools and non-makeup skipped — the rule was
fixed before the first query. Engine `google_shopping`, `gl=us`, `hl=en`,
one search per product. The size rule is the strict regex and magnitude
bounds of the storefront pass, imported from that script rather than
re-typed, so the two figures are measured the same way. A listing counts as
brand-matched when the brand name appears in its title.

*Budget.* 20 searches of the free tier's 250. One call in the first run was
charged but never answered; that product was re-queried in a resumed run
that reused the six responses already saved.

| Brand | Products with ≥ 1 sized listing title | Sized titles / brand-matched titles |
| --- | ---: | ---: |
| ColourPop | 0 / 4 | 0 / 150 |
| essence | 2 / 4 | 10 / 81 |
| Milani | 4 / 4 | 6 / 114 |
| Physicians Formula | 3 / 4 | 5 / 131 |
| Wet n Wild | 3 / 4 | 6 / 54 |
| **All** | **12 / 20** | **27 / 530 (5.1%)** |

Every product returned brand-matched listings (13–40 each). Only **1 of 20**
had a size in its *first* brand-matched listing.

*Reading.* A size can be found for most drugstore products, but only by
sifting ten to forty third-party listings per product for the one to six
that print one — and those do not agree. The Milani Amore Satin Matte Lip
Crème listings say 0.21 oz, 0.22 oz and 6 g; the Wet n Wild Big Poppa
Mascara listings say 8 ml, 10 ml and 0.33 fl oz. Each figure is a retailer's
transcription, not a manufacturer label, and deciding which is right means
looking at the product — which is manual capture with a search engine as a
hint. ColourPop, whose listings are its own storefront and resellers of it,
shows zero, consistent with the storefront measurement.

*Verdict, measured.* Google Shopping titles are a **size-hint source, not a
size source**: 60% of drugstore products get at least one candidate figure,
5% of listings carry one, and the candidates conflict. It can shorten
manual capture; it cannot replace it, and nothing from it should enter the
dataset unverified. At one search per product, 600 products is roughly
three months of the free tier or one month of the $25 plan.

*Operational note.* One of the twenty calls hung for roughly 54 minutes past
its nominal 60-second timeout before the first run failed — `requests`
bounds each socket read, not the call. The probe now bounds every call by
wall clock (90 s), caps the run at eight minutes, never retries within a
run, and resumes from saved responses; the resumed run completed its
fourteen calls in about five minutes with none abandoned.

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

### 11. Target — excluded (terms prohibit it)

| | |
| --- | --- |
| Terms | https://www.target.com/c/terms-conditions/-/N-4sr7l · 2026-08-22 · actual document, last updated 2026-04-15 |
| robots.txt | https://www.target.com/robots.txt · 2026-08-22 |

Target was the most promising fix for the drugstore quantity hole: mass-market
makeup sells there, and its product pages carry specification tables with net
contents. The terms settle it.

**Terms of use — verbatim clauses.** The licence is:

> "a limited license to access and make personal use of the Site and the
> Content for NONCOMMERCIAL PURPOSES ONLY"

Users agree not to:

> "Use or attempt to use any engine, software, tool, agent, data or other device
> or mechanism (including browsers, spiders, robots, avatars or intelligent
> agents) to navigate or search the Site other than the search engine and
> search agents provided by Target"

> "Make any use of data extraction, scraping, mining or other data gathering
> tools, or create a database by systematically downloading or storing Site
> content"

> "Make any commercial use of the Site or its Content, including making any
> collection or use of any product listings, descriptions, prices or images"

and:

> "Accessing, downloading, printing, posting, storing or otherwise using the
> Site or any of the Content for any commercial purpose ... constitutes a
> material breach."

**robots.txt — separately.** `User-agent: *` only. Roughly 100 disallowed paths
covering `/admin`, `/Checkout`, `/account/`, `/cart`, search parameters and
legacy paths. **Product pages (`/p/`) are not disallowed.** No blanket
`Disallow: /` for any agent, no `Crawl-delay`.

**robots ≠ permission, again.** Target's robots.txt would let any crawler read
every product page. Its terms prohibit three separate things this project would
do: using an agent to navigate the site, using data extraction tools, and
creating a database by systematically storing content. The "create a database
by systematically downloading or storing Site content" clause describes the
project's `data/raw/` layer exactly.

**Verdict: Excluded.** No workaround sought.

---

### 12. Walmart — excluded (terms unreadable behind CAPTCHA; prohibition corroborated)

| | |
| --- | --- |
| Terms attempted | `walmart.com/help/article/walmart-com-terms-of-use/…fae5f0`, `…fae5a0`, `business.walmart.com/help/article/walmart-business-terms-of-use/…` · 2026-08-22 |
| Result | **CAPTCHA interstitial on all three**, across two domains |
| robots.txt | https://www.walmart.com/robots.txt · 2026-08-22 |
| Corporate terms | https://corporate.walmart.com/terms-of-use · 2026-08-22 · governs corporate site only |

**Terms of use — not readable.** Three distinct URLs on two Walmart domains all
served a bot-verification page ("Activate and hold the button to confirm that
you're human") rather than the document. Walmart's *terms of use* are themselves
behind a CAPTCHA. Per §14 that ends the inquiry — the site refuses automated
access at the threshold, and solving a CAPTCHA to read the policy is exactly
the circumvention §14 prohibits.

**Corroborating text, secondary.** The corporate-site terms (readable, but
governing `corporate.walmart.com` only) prohibit using "any engine, software,
tool, agent or other device or mechanism (including without limitation
browsers, spiders, robots, avatars or intelligent agents) to navigate or search
this Site." Secondary sources quote the retail-site terms as prohibiting use of
"any robot, spider, site search/retrieval application or other manual or
automatic device to retrieve, index, 'scrape,' 'data mine' or otherwise gather
any Materials ... without Walmart's express prior written consent." That
wording is **not recorded as verified** — it was not read from the retail
site's own page — but it is consistent with the corporate terms and with the
CAPTCHA behaviour.

**Developer route checked.** `developer.walmart.com` lists APIs for Marketplace
sellers, 1P suppliers, carriers and advertisers. No public product-lookup API
for non-sellers is offered. Walmart's affiliate programme runs through
Impact.com, which was dropped earlier by decision.

**robots.txt — separately.** `User-agent: *` disallows `/account/`, `/api/`,
`/search`, `/store/ajax/`, `/typeahead/` and wildcard API paths. Product pages
(`/ip/`) are not disallowed. No blanket `Disallow: /`. Only Yahoo's `Slurp` has
a `Crawl-delay: 5`. Again permissive at the robots level; again not permission.

**Verdict: Excluded.** On access behaviour alone — terms unreadable without
CAPTCHA — with the prohibition corroborated but not primary-verified.

---

**Consequence of 11 and 12.** Walmart and Target were the last two candidates
that sell mass-market makeup *and* publish net contents. Both are excluded on
terms. With Sephora and Ulta already out, **every US retailer that carries
drugstore makeup is closed to this project.** The drugstore quantity hole cannot
be filled from any retailer. That leaves Open Beauty Facts and manual capture.

| Source | Status | Reason |
| --- | --- | --- |
| CJ Affiliate product feeds | **unverified** | Product-feeds URL returned 404 |
| Impact.com product catalogue | **dropped** | Dropped by decision — approval latency unbounded, fields not documented publicly |
| Rakuten Advertising feeds | **not assessed** | Not reached |
| UPC/GTIN lookup services | **not assessed** | Relevant to §22 entity resolution, not to primary acquisition |

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
| CoverGirl | Other | `Allow: /`; several third-party crawlers named and permitted | Yes |
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
| Fenty Beauty | Shopify | Permissive; named third-party crawlers explicitly granted access | Yes |
| Tarte | Shopify | Permissive (blocks Nutch, Amazonbot) | Yes |
| Anastasia Beverly Hills | Shopify | Permissive; named third-party crawlers explicitly allowed | Yes |
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

## MEASURED field coverage — Task C results

Probed 2026-08-22. All figures below are counted from retrieved responses, not
estimated. Raw responses and provenance are in `data/raw/feasibility/`.

**Method.** Fetched the public product JSON from 20 brand-owned Shopify
storefronts whose `robots.txt` permits product paths, identifying honestly as
`beauty-value-intelligence/0.1`, with a 2-second delay between requests.
Reached **19 of 20** brands and retrieved **3,333 products**. e.l.f. returned
`404` on `products.json` — the endpoint is disabled there, so e.l.f. needs a
different route despite its permissive robots.

### §16 critical fields — measured across 3,333 products

| Field | Coverage | Note |
| --- | --- | --- |
| Product name | **100.0%** | |
| Brand | **100.0%** | `vendor` |
| Retail price | **100.0%** | `variants[].price` |
| Product URL | **100.0%** | from `handle` |
| Retailer | **100.0%** | implicit — the brand's own store |
| Category | **81.8%** | `product_type`, but see below |
| **Quantity** | **11.4%** | **fails the screening criterion** |
| **Unit** | **11.4%** | same field |
| Rating | **0%** | absent from this source |
| Review count | **0%** | absent |
| UPC/EAN | **0%** | absent |
| Ingredients | **0%** | absent |
| Finish / Coverage | **0%** | absent |

Category nominally reaches 81.8%, but the values are not a usable taxonomy:
606 products carry an empty `product_type`, and the populated values mix
granularities and casing — `Lips`, `Eyes`, `eye`, `face`, `Face`,
`Foundations & Concealers`, `Makeup Set`, `Bundle`, `Fragrance`, `Skincare
Bundle`. Mapping these onto the 19 categories in `config/categories.yaml` is
real work, and some rows cannot be mapped at all.

### Tier breakdown — the disclosure asymmetry as a finding

Re-measured with the strict plausibility rules (magnitude bounds from
`config/unit_rules.yaml`, case-sensitive units, no script blocks). The stricter
pass moves overall coverage from 12.3% to **11.4%** — the earlier regex had
accepted a small amount of junk. The strict figure is the one to cite.

"With qty" counts a plausible size in a structured slot: variant title, product
option, or product title. Sizes appearing only in description prose are shown
separately and **not** counted, because prose can describe a bundle component or
a recommended product rather than the item itself.

| Tier | n | With qty | Coverage | Body-only |
| --- | ---: | ---: | ---: | ---: |
| **Drugstore** | 1,098 | **0** | **0.0%** | 22 |
| Mid-range | 593 | 12 | 2.0% | 20 |
| High-end | 1,471 | 225 | 15.3% | 135 |
| Luxury | 171 | 143 | 83.6% | 6 |
| **All** | **3,333** | **380** | **11.4%** | |

**Drugstore, by brand — the zero is uniform, not an average.**

| Brand | n | With qty | Coverage |
| --- | ---: | ---: | ---: |
| ColourPop | 250 | 0 | 0.0% |
| Essence | 233 | 0 | 0.0% |
| Milani | 161 | 0 | 0.0% |
| Physicians Formula | 204 | 0 | 0.0% |
| Wet n Wild | 250 | 0 | 0.0% |

Five brands, 1,098 products, zero structured sizes. Not one brand is dragging
down an otherwise non-zero average; every drugstore storefront probed behaves
identically. (ColourPop's 22 body-only hits are bundle listings naming component
sizes, which is why prose is excluded from the count.)

**The finding.** Drugstore brands, as a class, do not disclose net quantity on
their own storefronts. Non-drugstore brands sometimes do. That asymmetry is a
result about market behaviour, not an artefact of collection — the same
endpoint, the same method and the same rules were applied to every brand, and
the drugstore result was confirmed by a second retrieval method on e.l.f. and
Wet n Wild product pages.

It is also a result with an obvious interpretation that must *not* be asserted
on this evidence: that mass-market brands withhold size because it would make
per-unit comparison easy. The data shows the disclosure gap; it says nothing
about intent. The claim this supports is narrower — *size disclosure on
brand-owned storefronts is tier-dependent, and absent at the mass-market end.*

**The caveat that keeps it honest.** Non-drugstore coverage is poor too. The
15.3% high-end figure is almost entirely MAC (213 of 225), and the 83.6% luxury
figure is Tom Ford Beauty alone. **Excluding those two brands, non-drugstore
coverage is 24 of 1,814 — 1.3%.** Anastasia Beverly Hills, Tarte, Saie, Tower 28,
Haus Labs, Juvia's Place and Morphe are all at exactly 0.0%, indistinguishable
from drugstore.

So the defensible statement is not "prestige discloses, drugstore doesn't." It
is: *drugstore disclosure is categorically zero; prestige disclosure is near-zero
with two exceptions.* The asymmetry survives, but it is between 0% and 1.3%, not
between 0% and 15%. Stated at its true size it is still a finding — a clean
categorical zero across 1,098 products is not noise — but it is a much smaller
one than the tier table suggests at a glance.

### Why — the mechanism, confirmed

Shopify variant titles carry size **only when a product is sold in more than one
size**. Inspecting the structures directly:

- Tom Ford Beauty exposes an explicit `Size` option, with variants like
  `"151 Iconic Nude / 0.07 oz"`. Genuine size data.
- Wet n Wild and Milani expose `options=['Title']` and
  `variants=['Default Title']`. One variant, no size. The shade sits in the
  product name (`"Photo Focus Dewy Foundation | Classic Beige"`).

Drugstore products are overwhelmingly single-size, so their variant slot encodes
nothing. **The 0.0% is not a parsing failure — the data is absent.**

### Is size merely JavaScript-rendered? No.

Because the products.json result was ambiguous, 21 product detail pages were
fetched across seven brands and searched for size in the rendered HTML.

A first pass matched 18 of 21 pages, but those matches were **noise** —
`029g`, `0MG`, `5Ml`, `7G` — hash and identifier fragments inside minified
scripts. Counting them would have manufactured a coverage figure. After
stripping `<script>`, `<style>` and `<noscript>`, requiring a plausible size
shape and applying the magnitude bounds in `config/unit_rules.yaml`:

| Measurement | Result |
| --- | --- |
| Plausible size in **visible page text** | **2 / 21 (9.5%)** |
| Plausible size in **JSON-LD** | 2 / 21 (9.5%) |
| Plausible size **anywhere incl. script blocks** | 6 / 21 (28.6%) |

The 6 script-block hits do not rescue it. The values are **identical across all
three pages of a given brand** — ABH returns `0.9 g, 18 g, 30 mL, 7 mL` on every
page, ColourPop `0.95 fl oz, 28 mL, 5.8 fl oz` on every page — which is site-wide
boilerplate from navigation and recommendation blocks, not each product's own
size.

**Essence, Milani, Physicians Formula, Saie and Wet n Wild returned zero
plausible size tokens anywhere in the HTML, including scripts.** Size is not
hidden behind JavaScript on these sites. It is not published.

**Independently confirmed by a second method.** Two product pages were fetched
through a separate retrieval path and read directly rather than pattern-matched:

- e.l.f. *Halo Glow Liquid Filter* — price `$15` shown; **no size, net weight or
  volume displayed anywhere on the page.**
- Wet n Wild *Photo Focus Dewy Foundation, Classic Beige* — price `$6.89` shown;
  **no size displayed anywhere on the page.**

This also closes the e.l.f. gap left by its `404` on `products.json`. e.l.f. is
the largest drugstore brand in the §11 roster, and it does not publish size on
its own storefront either. Two independent methods agree: the drugstore result
is a genuine absence of published data, not an artefact of how it was measured.

### The `grams` trap, quantified

Shopify's variant `grams` field is populated on **55.7%** of products — over four
times the real size coverage. It is shipping weight including packaging, and it
is the single most dangerous field in this dataset: using it would produce
price-per-gram figures for 1,857 products that look entirely reasonable and are
all wrong. No validation rule in §33 would flag them.

### Verdict against §88

§88 targets quantity coverage above 90%. Measured coverage from brand-owned
Shopify storefronts is **11.4% overall and 0.0% for drugstore**. §88 says to
report honestly rather than adjust the target, so: this source cannot support
the central research question on its own. The tier the question is *about* has no
size data at all.

---

## Recommendation

### The finding that overrides everything else

The drugstore tier — the subject of the §98 central research question — has
**zero measured quantity coverage** from the only permitted, authoritative source
found. Drugstore brands do not publish product size on their own storefronts.
This is not a parsing gap the Stage 1.2 parser can close: there is nothing to
parse. Two independent methods agree, across nine brands, including e.l.f.

Every architecture below is shaped by that one fact.

### Primary acquisition architecture

**Brand-owned Shopify storefronts as the product spine, with quantity supplied
from a second source.**

*Why this and not something else.* The storefronts deliver product name, brand,
list price, product URL and retailer at **100%** on 3,333 products across 19
brands, free, permitted, no auth, and manufacturer-authoritative — satisfying §13
item 4 and §19's list-price requirement directly. Nothing else verified comes
close on the critical fields it *does* cover. Its failure is confined to one
field. So the right move is to keep it for what it is good at and solve quantity
separately, rather than abandon the one source that works.

*What the spine does not provide.* Rating, review count, UPC/EAN, ingredients,
finish and coverage are absent entirely. The §16 "strongly preferred" and
"preferred" tiers cannot be filled from the primary source at all.

*Why it is only partially selected.* `config/data_sources.yaml` records
`quantity_source: UNRESOLVED`. The primary cannot be declared complete until
quantity has a named source with measured coverage. That is the gate.

### The quantity source — the decision that is actually pending

*This section is the framing written before the export was measured. The
result is in "Open Beauty Facts — measured" below: outcome 3, in a specific
form — the fill rate is usable, the volume is not.*

**Open Beauty Facts is the only identified route to structured net quantity,
and it is untested.** Its schema could not be confirmed because the hosts
refuse automated fetching, and no workaround was sought. Three outcomes are
possible, and Stage 1.0 cannot close until one of them is measured:

1. **OBF carries a parsed numeric `product_quantity` with a unit, at a usable
   US-makeup fill rate.** Then it becomes the quantity source, joined to the
   spine by barcode — which also supplies UPC/EAN for §22 entity resolution.
   Best case.
2. **OBF carries a raw `quantity` label string at a usable fill rate.** Then it is
   *embedded*, the §27–31 parser does the work, and the join is still by
   barcode. Workable.
3. **OBF's US makeup fill rate is too low.** Then no identified source supplies
   drugstore quantity, and the project has to choose between the fallback
   below and a scope change.

Testing it requires a bulk-export download, which is a licensed ODbL
distribution channel rather than a crawl, and `User-agent: *` permits `/data/`.
That decision sits with the project owner.

### Open Beauty Facts — test design, ready to run

The query is written and self-tested: `sql/obf_feasibility.sql`, run via
`python src/ingest/obf_feasibility.py --site-total N`. It executes end-to-end
against a synthetic export, and its integrity gate was proven to halt on a
deliberately truncated file (exit code 3, nothing downstream reported).

**Which export flavour, and why — both Parquet and CSV.**

Parquet is the analytical flavour: typed columns, list-typed `countries_tags`
and `categories_tags` that DuckDB reads natively, and the fastest load. It is
the one the measurement runs on.

CSV is downloaded *as well*, for one reason only: **integrity**. Two
independently generated exports of the same database should agree on row count
and share nearly every barcode. If they disagree materially, at least one is
broken, and that check needs no external reference number. This is the primary
sanity check. It is stronger than comparing to a site-advertised total, because
the advertised figure is itself just another number of unverified provenance.

JSONL and the MongoDB dump are not requested. JSONL is the flavour reported as
dropping from ~4M to ~0.7M across days; the MongoDB dump needs a MongoDB
instance to read and adds a dependency the project does not otherwise need.

**Fields measured.** Both quantity fields, separately, because they answer
different questions:

| Field | Type | What it is | What it decides |
| --- | --- | --- | --- |
| `quantity` | string | Raw label text — `"30 ml"`, `"0.14 oz / 4 g"` | Embedded coverage. What the §27–31 parser would have to eat. |
| `product_quantity` | string | Pre-parsed numeric, as text — `"30"` | Structured coverage. The number Stage 1.1 is waiting on. |
| `product_quantity_unit` | string | Unit for the above — `"ml"` | Whether structured means *usable* structured. |
| `code` | string | EAN/UPC barcode | Joinability, and the §22 tier-1 match key. |
| `brands` | string | Free text | Tier mapping against §11. |
| `countries_tags` | list | `['en:united-states', …]` | US filter. |
| `categories_tags` | list | `['en:lipsticks', …]` | Makeup filter and §7 category mapping. |

The schema is taken from the sibling Open Food Facts Parquet dataset on Hugging
Face (read 2026-08-22), which shares the Product Opener schema. All three
quantity fields are typed **string**, including `product_quantity` — so even
the "structured" field needs `try_cast` and cannot be assumed numeric. Part 0.4
of the query verifies every required column exists in the actual file before
anything else runs; if one is missing, the assumption was wrong and the query
stops.

Their *disagreement* is also measured: rows with raw `quantity` but no
`product_quantity` are ones OBF's own parser gave up on, which calibrates how
much Stage 1.2 parser work remains even on the structured path.

**How US makeup is identified in a global cosmetics database.** Two filters,
applied independently and intersected, with every funnel stage reported so
each filter's contribution is auditable.

- *US:* `countries_tags` contains `en:united-states`. This is contributor-
  entered "where is it sold", not a manufacturer field, so it **under-counts**
  — a US product entered by a French contributor may carry only `en:france`.
  Under-counting is the safe direction: it shrinks *n* without polluting the
  sample. No attempt is made to infer US-ness from brand or barcode prefix,
  which would do the opposite.
- *Makeup:* `categories_tags` contains a tag whose stem matches one of the §7
  categories — `en:lipstick%`, `en:mascara%`, `en:foundation%`, and so on,
  prefix-matched so sub-categories are included. The broad `en:make-up` tag is
  reported for context but is **not** sufficient on its own: it also covers
  brushes, removers and tools. The query dumps the actual tag vocabulary on
  the US-makeup rows so stems the filter missed can be added by hand.

**Sanity check design — Route 2 primary, Route 1 corroboration.**

Part 0 runs first and gates everything else:

1. Both flavours must have ≥ 1,000 rows — below that is a known truncation
   signature.
2. Row counts must agree within 5%. Material disagreement means re-download
   both; it does not mean pick the bigger one.
3. Barcode overlap between flavours is reported. Two complete exports should
   share nearly every `code`.
4. Duplicate-barcode rate is reported; > 5% duplicates is a warning.
5. *Route 1:* if a site-read product count is supplied (`--site-total`), the
   Parquet row count must agree with it within 5%.

Any FAIL halts the run. Parts 1–4 are never reported on a suspect export, so
a low fill rate cannot be mistaken for a database property when it is an export
defect.

**What the query reports once Part 0 passes.** The funnel (all → US → makeup →
US makeup); the category-tag and brand vocabularies actually present; the
quantity fill rate at each funnel stage for raw, parsed, and parsed-with-unit;
the unit vocabulary; raw/parsed disagreement; **fill rate by §11 tier and by
drugstore brand**; and the joinable ceiling — rows with brand, name and
quantity all present. The single decisive number is
`obf_by_tier.drugstore.parsed_with_unit_pct`.

**What is needed from the project owner.**

1. Download the Parquet export to `data/raw/obf/obf.parquet`.
2. Download the CSV export to `data/raw/obf/obf.csv`.
3. Read the product count shown on the site and supply it as `--site-total`.
4. Run `python src/ingest/obf_feasibility.py --site-total <N>`.

Both files are git-ignored (large, ODbL-licensed, re-downloadable). The query
is read-only on `data/raw/` and writes its scoped subset to
`data/staging/obf_us_makeup.parquet` for inspection.

*Delivered 2026-08-26, with two differences from the list above: the files
keep their published names (`beauty.parquet`, `en.openbeautyfacts.org.products.csv`,
passed with `--parquet` / `--csv`), and the site count was not read — the
row count the publisher advertises for the same Parquet file was used as the
external total instead. Provenance and verification are recorded in
`data/raw/obf/PROVENANCE.md`.*

### Open Beauty Facts — measured

Run 2026-08-26. Every figure below is from
`data/raw/feasibility/_obf_measurement.txt`, produced by
`python src/ingest/obf_feasibility.py --parquet data/raw/obf/beauty.parquet --csv data/raw/obf/en.openbeautyfacts.org.products.csv --site-total 73747 --total-source "…"`.

**Integrity check — stated first, as required.** Verdict: **WARN, not PASS.**

| Check | Result |
| --- | --- |
| Parquet rows / distinct barcodes | 73,747 / 73,747 |
| CSV rows / distinct barcodes | 64,237 / 64,237 |
| Flavour disagreement | 12.9% — **above the 5% tolerance** |
| Newest edit in Parquet / in CSV | 2026-08-24 / 2026-05-07 — a 108-day gap |
| Barcodes in both flavours | 60,902 (94.8% of the CSV's barcodes are in the Parquet) |
| External total (publisher's advertised row count for this Parquet file) | 73,747 — **exact match**, and the file's byte size matches too (59,406,016) |

The row-count check failed as designed, and the failure was diagnosed rather
than waived. The CSV export the project publishes is a snapshot from 7 May;
the Parquet is current. Both files were downloaded on the same day, so a
re-download would return the same stale CSV. The disagreement is snapshot
age, not truncation: the Parquet is the larger and newer flavour, it holds
94.8% of the older flavour's barcodes, and it agrees with the publisher's
own row count to the byte. The gate was extended so that this case — and
only this case: a flavour at least 30 days staler *and* an external total
that corroborates the Parquet — downgrades to a WARN that is printed and
carried forward; an unexplained disagreement still halts. All figures below
are from the Parquet alone. The site-advertised product count was not read,
so Route 1 rests on the publisher's dataset API rather than the website.

**Schema.** All eight required columns are present. `product_quantity` is
text and needs `try_cast`, as anticipated. There is **no price field** of any
kind in the 111-column schema; OBF's role was always quantity and barcodes,
and that is confirmed.

**Funnel.** Two makeup scopes are reported. *Strict* requires a tag naming a
§7 product type (`en:lipsticks`, `en:mascara`, `en:Volumizing mascaras`…).
*Broad* adds OBF's makeup family tags (`en:makeup`, `en:face-makeup`,
`en:eyes-makeup`, `en:lip-makeup`), which say "makeup" without saying which
type. The first run used a case-sensitive prefix filter and found 15 US rows;
the tag vocabulary showed why, and the filter was corrected before anything
was concluded.

| Stage | Rows |
| --- | ---: |
| All rows | 73,747 |
| Tagged `en:united-states` | 4,806 |
| — of which carrying no category tag at all | 2,377 (49.5%) |
| Makeup, strict, any country | 344 |
| Makeup, broad, any country | 942 |
| **US makeup, strict** | **24** |
| **US makeup, broad** | **57** |

Half of the US-tagged rows are invisible to any category filter, so the US
makeup counts are a floor. They are not a floor with a large ceiling above
it: the US-tagged brand list is Dove, Aveeno, Neutrogena, CeraVe — this is a
hygiene-and-skincare corpus with a makeup fringe.

**Fill rates.** `parsed_with_unit` is the structured field with a unit; `raw`
is the label string.

| Scope | n | Raw label | Parsed numeric | Parsed + unit |
| --- | ---: | ---: | ---: | ---: |
| All rows | 73,747 | 41.8% | 32.1% | 21.9% |
| US, all products | 4,806 | 21.4% | 17.9% | 14.8% |
| Makeup, any country | 344 | 49.4% | 35.5% | 28.8% |
| US makeup, strict | 24 | 58.3% | 45.8% | 45.8% |
| **US makeup, broad** | **57** | **64.9%** | **56.1%** | **49.1%** |

Units on the US makeup rows: g 16, ml 12, no unit 4. Raw versus parsed on
the 57: both present 32, raw only 5, parsed only 0, neither 20 — OBF's own
parser handled 32 of 37 label strings, and the 5 it dropped are strings like
`1`, `5`, `250` with no unit, which no parser should accept. Other §16
fields on the 57: brand 48 (84.2%), product name 48 (84.2%), barcode 57
(100%), category 100% by construction, price 0.

**By tier — the number Stage 1.1 was waiting on.** US-tagged rows, broad
scope, matched to the §11 brand list with a word-bounded brand match.

| Tier | Rows | Strict | With parsed quantity + unit | Rate |
| --- | ---: | ---: | ---: | ---: |
| Drugstore | 16 | 13 | 10 | 62.5% |
| Mid-range | 0 | 0 | 0 | — |
| High-end | 1 | 1 | 0 | 0.0% |
| Luxury | 0 | 0 | 0 | — |

Drugstore, by brand: L'Oréal Paris 6 (2 with quantity), Maybelline 5 (4),
CoverGirl 3 (2), e.l.f. 1 (1), Milani 1 (1). NYX, Revlon, ColourPop,
Wet n Wild, Physicians Formula and essence: no US-tagged makeup rows at all.
ColourPop has no rows in the database under any country.

The 62.5% clears the 50% switch trigger written in the fallback section. That
trigger was written for a *rate*, on the unstated assumption that there would
be rows to apply it to. There are ten. Against a §10 target of 300 drugstore
products, the rate is not the finding; the volume is.

**With the country filter removed.** Because the US tag is
contributor-entered and under-counts, the same table was run on every row
regardless of country. Drugstore §11 brands: **165 rows, 11 brands, 65 with
parsed quantity + unit** — Maybelline 60 (16 with quantity; tagged
Netherlands 29, France 28), essence 45 (28; Netherlands 37), NYX 15 (7),
L'Oréal Paris 14 (3), Wet n Wild 12 (0; Türkiye 10), e.l.f. 7 (7; Netherlands
6), Revlon 5 (0), CoverGirl 3 (2), Physicians Formula 2 (0), Milani 1 (1).
Mid-range 13 rows (4 with quantity), high-end 10 (5), luxury 8 (5).

These are not US quantities. Most come from a Dutch drugstore-chain import
and French contributors; a row tagged to another market carries that
market's pack size, and pack sizes differ across markets for the same product
name. With no barcode on the spine side (measured absent in Task C), such a
quantity cannot be verified as the US size. The 165 is a ceiling on what OBF
holds, not a supply of usable US figures.

**Joinability.** Of the 57 US makeup rows, 32 have brand, name and quantity
together. The spine has no barcodes, so the join would be by normalised brand
plus fuzzy name (§22 tiers 2–3), not by barcode. Thirty-two candidates.

**Verdict.** Open Beauty Facts is a real, structured, well-parsed quantity
source with essentially no US makeup in it. It resolves the pending decision
as outcome 3: no identified source supplies drugstore quantity at scale.
What OBF can still contribute is small and specific — a barcode-keyed
reference set of roughly 65 drugstore quantities (any market) to test the
§27–31 parser against, and at most ten US-tagged drugstore rows for spot
joins. It cannot carry a tier.

### Fallback architecture, and when to switch

**Fallback: manual quantity capture for a curated product set.**

§26 already specifies a manually validated hero/anchor set of 50–100 products.
If no structured source emerges, that set expands: pick products
category-by-category, read the size from packaging or the manufacturer's
product page where it exists, record provenance per §25, and build the
quantity-adjusted analysis on a smaller, fully verified dataset.

*Switch trigger:* OBF measured US-makeup quantity fill rate for drugstore brands
below roughly 50%. At that point barcode-joining gets most rows nothing, and
manual capture is faster and more defensible than patching a sparse join.
*Measured 2026-08-26:* 62.5%, on sixteen rows. The trigger asked the wrong
question — the rate passed and the volume failed — and the fallback is
reached regardless.

*Cost of switching:* the dataset shrinks far below §9's 600–800 minimum. The
analysis stays honest — every number traceable — but the scale claims in §82
and §97 have to be rewritten. A "multi-source pipeline" that delivers 150 hand-
verified products is a different project from the one specified, and the README
would need to say so rather than imply otherwise.

### Realistic dataset-size ceiling

| Scenario | Products with verified quantity | Against §9 |
| --- | --- | --- |
| Spine only, as measured today | **380** (11.4% of 3,333), **0 drugstore** | Below minimum, and structurally useless for the research question |
| + OBF, as measured 2026-08-26 | 380 + at most 10 US-tagged drugstore rows with quantity (32 US makeup join candidates in total) | Below minimum; drugstore still effectively absent |
| + OBF ignoring the country tag | + up to 65 drugstore quantities from other markets, not verifiable as US pack sizes | Not usable as US data |
| Manual fallback | 150–300, hand-verified | Far below minimum; a different project |

The 3,333 retrievable products are a catalogue ceiling, not a dataset ceiling.
Without quantity they are names and prices, which the project explicitly exists
to go beyond.

Tier damage from the brand sweep compounds this: luxury has two reachable brands
(Tom Ford Beauty, Armani Beauty) against a §10 target of 100 products. See the
platform-reachability risk above.

### Fields no source can supply, and what that means downstream

| Field | §16 priority | Best available source | Consequence |
| --- | --- | --- | --- |
| **Quantity / unit (drugstore)** | Critical | None at source. OBF: 10 US-tagged rows. Google Shopping titles: a candidate figure for 12 of 20 products, unverified and conflicting | **Blocks the central comparison until resolved** — measured 2026-08-26, still unresolved |
| Rating | Strongly preferred | Kaggle historical only (prestige brands, stale) | §40 Bayesian rating, §41 rating-adjusted value and §50 price-vs-rating cannot run on current data. At best they run on the historical Sephora subset, clearly labelled. |
| Review count | Strongly preferred | Same | Same. §51 brand value analysis loses its rating dimension. |
| UPC / EAN | Very useful | OBF, if usable | Without it, §22 entity resolution falls back to fuzzy name matching with lower `match_confidence`. |
| Ingredients | Preferred | Kaggle historical; OBF possibly | Phase 3 ingredient Jaccard (§56) is limited to products present in those sources. |
| Finish / Coverage | Preferred | Must be derived from description text | Phase 3 candidate filtering (§55) depends on text extraction, not structured attributes. |
| Multi-retailer offers | §20 | None — no multi-brand retailer is permitted | `product_offers` becomes one row per product. Cross-retailer dispersion is out of scope. Dataset represents manufacturer list price, not street price. |

The honest summary for the README: the project can measure **quantity-adjusted
list-price economics across tiers** for whatever subset has verified quantity.
It cannot, with current sources, relate those economics to consumer ratings on
current data, and it cannot measure retailer-level price variation at all.

### The three paths, reassessed after Tasks 1–3

The options were first laid out under the platform-reachability risk, when the
problem looked like "luxury is thin." Tasks 1–3 changed the problem: every US
retailer selling drugstore makeup is closed, and drugstore brands publish no
size. The options are the same three; their weights are not.

**Path A — Narrow to prestige-only.**
Drop the drugstore tier and compare mid-range / high-end / luxury on the 380
products with measured quantity.
*For:* It is buildable today, from permitted sources, with no further decisions.
The unit-economics machinery, the Mini Tax and the dupe engine all work on it.
*Against:* The 380 are **not a prestige sample — they are a MAC-and-Tom-Ford
sample**: 213 MAC, 143 Tom Ford, 24 everything else. A two-brand dataset cannot
support tier claims, brand rankings under §51's minimum-sample rule, or any
cross-brand finding. And the §98 question is *about* drugstore; answering a
different question is a reframe wearing narrower clothes, not a narrowing.

**Path B — Manual capture on an expanded anchor set.**
Pick 150–300 products across all four tiers, read the net quantity from
packaging or a manufacturer page where one exists, record provenance per §25,
and build the full analysis on a small, fully verified dataset.
*For:* It is the only path that puts a *measured* drugstore number next to a
prestige one and therefore the only one that answers §98 as written. Every row
is hand-verified, which is stronger provenance than any scraped source. §26
already specifies this set; it grows rather than being invented.
*Against:* It falls far below §9's 600–800 minimum and §82's "multi-source
pipeline" framing — the README has to say "hand-verified set of N" and mean it.
Sample selection becomes the methodology risk: with ~40 products per tier, which
products get picked decides the answer, and the selection rule must be written
*before* any quantity is read, or §4's neutrality is gone. It is also labour,
and labour that cannot be re-run by a stranger from a clean clone (§89) — only
re-audited.

**Path C — Reframe around the disclosure asymmetry.**
Make the measured finding the headline: across 1,098 drugstore products from
five brands, net quantity is disclosed on **zero**, against 380 of 2,235
non-drugstore products. The project becomes an investigation of *what
mass-market beauty does not tell you*, with quantity-adjusted economics
computed wherever disclosure permits.
*For:* It is entirely true and entirely measured — the cleanest result in the
study. It is genuinely interesting to the retail-analytics audience §1 names.
It requires no more data. And it converts the blocking problem into the
subject, which is honest rather than clever.
*Against:* It abandons §98 as the question and §93 as the success definition.
The asymmetry is strong as a *measurement* and weak as a *story*: five brands,
one channel (their own storefronts), one mechanism (Shopify variant slots). It
says nothing about packaging, retailer listings or intent, and a reader will
reach for the intent reading immediately. Overclaiming from it is its own
fabrication. And prestige disclosure is 1.3% outside two brands — the contrast
is 0% against 1.3%, which is a real categorical zero but not the dramatic gap
the framing invites.

**What OBF changes.** Only Path B's cost and Path A's relevance. If OBF has
real drugstore fill — the threshold in the fallback section is 50% — then the
drugstore tier becomes measurable at scale, Path B shrinks to the §26 anchor set
it was always meant to be, and Path A becomes unnecessary. If OBF is thin, Path
B is the only route to a drugstore number, and the choice is between B and C.
Path C's finding is true regardless of OBF and could accompany either.

No path is chosen here. The OBF measurement is the last piece of evidence that
materially moves the choice, and it is one download away.

*Measured 2026-08-26: OBF is thin — ten US-tagged drugstore rows with
quantity. Path A is unchanged, Path B does not shrink, and the choice is
between B and C. The decision memo at the end of this report restates the
three paths with the measured ceiling.*

### What Stage 1.0 has and has not delivered

Against the roadmap gate:

- **Primary source named** — yes, with a documented hole.
- **Fallback named** — yes.
- **Legal status documented per source with the exact clause** — yes, for every
  source reached. Ulta's clause is quoted verbatim; Sephora's and the five
  luxury houses' refusals are recorded as HTTP 403 with no circumvention sought.
- **Real quantity coverage measured, not assumed** — yes: 11.4% overall, 0.0%
  drugstore, from 3,333 products, confirmed by a second method.

What it has not delivered is a **quantity source for the drugstore tier**. That
is the open decision, and it is the project owner's to make, because the
candidate that could resolve it requires a retrieval decision and the
alternatives change the project's scope.

### Historical note

The earlier draft of this report, written before measurement, said the parser
had become "the component that determines whether a dataset exists." That was
half right. The parser is still essential for the embedded sizes that do exist.
But measurement showed the larger problem is upstream of any parser: for the
tier that matters most, the size is not published. No parser fixes an absence.

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

---

## Decision memo — Stage 1.0 gate

Written 2026-08-26, after every planned measurement. Everything above this
line is evidence; this section is the choice the project owner has to make.
**No path is chosen here.** The figures are from this repository's own
output: `data/raw/feasibility/_tier_breakdown.json`,
`_pdp_strict_analysis.json`, `_obf_measurement.txt` and
`_serpapi_summary.json`.

### The revised ceiling — products with a verified net quantity

| Source, permitted | Products with verified quantity | Of which drugstore |
| --- | ---: | ---: |
| Brand-owned storefronts, 3,333 products retrieved | **380** (11.4%) — 213 MAC, 143 Tom Ford Beauty, 24 all other brands | **0** of 1,098 |
| Open Beauty Facts, US-tagged rows | 32 join candidates with brand, name and quantity (no barcode on the storefront side, so a fuzzy join) | 10 |
| Open Beauty Facts, any market | 65 drugstore quantities — Dutch, French and Turkish pack sizes, not verifiable as US | 0 usable |
| Google Shopping titles via SerpApi, 20 drugstore products probed | a candidate figure for 12 of 20, from 5% of listings, conflicting across listings, unverified | 0 verified |
| Every US multi-brand retailer (Ulta, Sephora, Target, Walmart, Amazon) | excluded — terms, edge blocks, or a dead API | — |

So: roughly **380 plus a few dozen** products can carry a quantity-adjusted
price today, and the drugstore share of that is **ten**, against §10's
target of 300 and §9's floor of 600–800 products across 30+ brands. The
storefront zero is not sampling noise: five drugstore brands, 1,098
products, no structured size on any of them, confirmed by a second method.

### The three paths

**A — Narrow to prestige only.** Keep the 380 and build the full pipeline
on them.
*§9:* fails the 600 floor; two brands supply 94% of the rows, so "30+ brands"
is not met in any meaningful sense. *§10:* drugstore 0 of 300; luxury carried
by one brand. *§98:* cannot be answered — the question is about paying less,
and the cheap tier is absent. The honest name for this is a MAC-versus-Tom
Ford unit-economics study. Buildable today with no further decisions.

**B — Hybrid: automated spine plus manual quantity capture for drugstore.**
Keep the 3,333-product storefront spine for names, prices and categories;
read net quantity by hand from packaging or a manufacturer page for a
pre-registered drugstore set — and for the prestige brands at 0%, so the
comparison is like-for-like — each row with photo or URL provenance per
§25. Google Shopping titles supply a candidate figure for about 60% of
products to verify against, not to trust.
*§9:* partially reachable — hand capture of 150–300 drugstore products plus
the 380 lands near 550–700 with quantity, a thin pass or a near miss;
30+ brands is reachable. *§10:* drugstore becomes measurable at scale for
the first time; luxury stays at two brands. *§98:* the only path that puts a
measured drugstore number next to a measured prestige one and answers the
question as written. *Costs:* labour a stranger cannot re-run from a clean
clone (§89 — re-auditable, not reproducible); selection risk — the product
list must be fixed before any size is read, or §4's neutrality is gone; OBF
adds at most ten spot-check rows and a 65-row parser test set.

**C — Reframe around the disclosure asymmetry.** Make the measured finding
the headline: on their own storefronts, drugstore brands disclose net
quantity on 0 of 1,098 products, prestige brands on 1.3% outside MAC and
Tom Ford; compute quantity-adjusted economics wherever disclosure permits.
*§9:* the catalogue (3,333) meets the row targets, but the analysis rows are
the same 380 as Path A. *§10:* moot — tiers become the subject, not the
sample frame. *§98:* abandoned as the question, replaced by "what does
mass-market beauty not tell you?" — true, measured, and interesting to §1's
audience, but a measurement more than a story: one channel, one mechanism,
and intent must not be asserted from it. Requires no new data.

### What the measurements settle, and what they do not

- Open Beauty Facts is **not** a drugstore quantity source at scale (ten
  US-tagged rows). Path B does not shrink.
- Google Shopping titles carry a size for 12 of 20 drugstore products, but
  on 5% of listings, from third-party retailers, with conflicting figures
  for the same product. Path B's manual capture can be *guided* by them —
  a hint per product to check against packaging — not replaced by them.
- Nothing measured makes Path A answer §98, and nothing makes Path C need
  more data. The choice is between B's labour and C's reframe, or a
  combination: C's finding is true under every path and can accompany B.

### Stage 1.0 gate checklist (ROADMAP)

- Primary source named — brand-owned storefronts (Shopify `products.json`
  and permitted product pages), with the quantity hole documented.
- Fallback named — manual quantity capture on a pre-registered set.
- Real quantity-field coverage measured, not assumed — storefronts 11.4%
  strict, drugstore 0.0%; Open Beauty Facts 49.1% on 57 US makeup rows and
  62.5% on 16 drugstore rows; Google Shopping titles 12 of 20 products,
  5.1% of listings.
- Legal status documented per source with the governing clause — Ulta,
  Target, Walmart, Sephora, Amazon, Open Beauty Facts and SerpApi, each in
  its section.

Gate condition met. Decision pending: **A, B, or C.**
