# COMPLETE MASTER PROJECT HANDOFF

# Beyond the Price Tag

## A Data-Driven Analysis of True Value in Beauty

### Flagship Interactive Product:

# Beauty Value Intelligence Engine

### Core Feature:

# True-Value Dupe Finder

---

# READ THIS ENTIRE DOCUMENT BEFORE MAKING CHANGES

You are taking over a serious portfolio-level data project.

Act simultaneously as:

* Senior Data Analyst
* Data Scientist
* Analytics Engineer
* Data Engineer
* Retail Analytics Consultant
* Machine Learning Engineer
* NLP Engineer
* Product Analyst
* Streamlit/Data App Developer
* Technical Reviewer

Your job is not simply to make something that runs.

Your job is to build a project that would be impressive to:

* data analyst recruiters
* data science recruiters
* retail analytics teams
* ecommerce companies
* beauty companies
* fashion/retail companies
* hiring managers evaluating technical portfolios

The project must feel like a genuine investigation of a retail pricing problem, not a generic Kaggle analysis.

---

# 1. USER / PORTFOLIO CONTEXT

The creator of this project is interested in:

* data analytics
* data science
* AI/ML
* retail
* fashion
* makeup
* beauty
* consumer behaviour

Previous portfolio work already includes:

1. Product Placement Optimisation

   * retail transactions
   * market basket analysis
   * association rules
   * product placement decisions

2. Sephora Review Data Pipeline

   * beauty data
   * review data
   * data pipeline work
   * unstructured/customer data analysis

Therefore this new project MUST NOT feel like:

* another market basket project
* another Sephora reviews project
* another basic sentiment analysis
* another simple recommendation system
* another Power BI dashboard using a downloaded CSV

This project needs to introduce new technical depth.

The strongest differentiators should be:

* multi-source data acquisition
* messy ecommerce data cleaning
* unit normalisation
* entity resolution
* price-per-unit economics
* statistical testing
* retail value modelling
* product similarity
* NLP embeddings
* explainable recommendations
* a polished consumer-facing analytical app

---

# 2. PROJECT TITLE

Use the main title:

# Beyond the Price Tag

Subtitle:

## A Data-Driven Analysis of True Value in Beauty

Interactive application:

# Beauty Value Intelligence Engine

Flagship functionality:

# True-Value Dupe Finder

---

# 3. CORE PROJECT IDEA

Beauty shoppers often compare products based on sticker price.

Example:

Drugstore product:

$12

High-end product:

$35

Most consumers immediately conclude:

> The $12 product is cheaper.

But this may be misleading because beauty products frequently contain dramatically different quantities.

Example:

Drugstore product:

$12 for 2 g

Price per gram:

$6/g

High-end product:

$35 for 10 g

Price per gram:

$3.50/g

The high-end product costs much more at checkout but is actually cheaper per gram.

Therefore the central project question is:

> Are drugstore beauty products actually cheaper than high-end products when we account for how much product consumers receive?

The project should then go further.

Second major question:

> When consumers buy a cheaper alternative or "dupe", are they actually saving money or simply buying less product?

Third major question:

> Can we identify alternatives that are not only similar and cheaper upfront, but genuinely better value after quantity is considered?

---

# 4. PROJECT PHILOSOPHY

Do not design the project to prove:

> Drugstore is better.

Do not design the project to prove:

> High-end is better.

Do not manipulate thresholds, product selection, categories, or comparisons to force a dramatic conclusion.

Let the data answer:

> When does drugstore genuinely provide better value, and when does it not?

Maintain neutrality throughout the analysis.

---

# 5. DEFINITIONS THAT MUST REMAIN SEPARATE

The project must distinguish between several different ideas.

## Affordability

How much money the customer needs to spend at checkout.

Example:

$12 vs $35.

---

## Quantity Value

How much product the customer receives for the money.

Example:

Price per gram or price per millilitre.

---

## Consumer Value

A broader comparison involving factors such as:

* quantity economics
* ratings
* review confidence
* similarity
* popularity

---

## Product Similarity

How closely two products resemble each other based on:

* category
* product form
* finish
* coverage
* shade
* description
* ingredients
* claims

---

## Dupe

A product sufficiently similar to another product.

---

## True-Value Dupe

A product that is:

1. genuinely similar
2. cheaper upfront
3. competitive or better on unit economics
4. reasonably well reviewed

Do not collapse these concepts into one metric.

---

# 6. MAIN RESEARCH QUESTIONS

The project should investigate:

1. Are drugstore products genuinely cheaper per gram or mL?

2. How much does the apparent drugstore saving shrink after correcting for quantity?

3. Which categories have the biggest luxury premium?

4. Which categories show surprisingly small differences between tiers?

5. Do luxury products generally contain more product?

6. Which drugstore products look inexpensive but are expensive per gram/mL?

7. Which high-end products are surprisingly competitive per gram/mL?

8. Which brands give customers the most product for their money?

9. Which brands provide the least product for their money?

10. Does price per unit correlate with customer ratings?

11. Do expensive products actually receive better consumer ratings?

12. Which beauty categories have the greatest variation in unit pricing?

13. Are cult/bestselling products good value?

14. Are popular drugstore alternatives always good value?

15. Do mini products have hidden unit-price premiums?

16. How large is the average "Mini Tax"?

17. Which brands have the largest Mini Tax?

18. Does the prestige premium remain after controlling for category?

19. Does larger product quantity reduce unit cost?

20. Which dupes provide genuine savings?

21. Which dupes are cheaper upfront but worse value after quantity adjustment?

22. Can product similarity and retail economics be combined into a better dupe recommendation system?

---

# 7. INITIAL PROJECT SCOPE

Focus first on makeup.

Do not make skincare the main scope.

Suggested categories:

1. Foundation
2. Concealer
3. Powder blush
4. Liquid blush
5. Cream blush
6. Bronzer
7. Highlighter
8. Setting powder
9. Pressed powder
10. Lip liner
11. Lipstick
12. Liquid lipstick
13. Lip gloss
14. Mascara
15. Brow products
16. Primer
17. Setting spray
18. Eyeshadow singles
19. Eyeshadow palettes

The final category list may be reduced depending on data quality.

Prioritise approximately 10 to 14 categories with strong enough data.

---

# 8. IMPORTANT CATEGORY RULE

Do not directly compare products measured in incompatible units.

Example:

Powder blush measured in grams

versus

Liquid blush measured in mL

These should generally be treated as separate analytical categories.

Do not convert grams into mL unless true product density is known.

Never invent density.

---

# 9. TARGET DATASET SIZE

Do not chase huge row counts just to say the dataset is large.

A clean 800-product dataset is better than a messy 50,000-product dataset.

## Minimum viable dataset

Approximately:

* 600 to 800 products
* 30+ brands
* 10+ categories

## Strong final dataset

Approximately:

* 800 to 1,500 products
* 40 to 75 brands
* 10 to 14 strong categories

## Stretch target

1,500 to 3,000 products if acquisition and validation are reliable.

Do not inflate the dataset with duplicate listings.

---

# 10. IDEAL MARKET-TIER DISTRIBUTION

Aim approximately for:

Drugstore:
300 products

Mid-range:
100 to 150 products

High-end:
250 products

Luxury:
100 products

Exact numbers can vary.

Balanced category representation matters more than perfect tier counts.

---

# 11. SUGGESTED BRANDS

## Drugstore / Mass Market

Potential examples:

* e.l.f.
* Maybelline
* NYX
* L'Oréal Paris
* Milani
* Essence
* Wet n Wild
* Revlon
* CoverGirl
* ColourPop
* Physicians Formula

---

## Mid-Range / Affordable Prestige

Depending on final methodology:

* Morphe
* Juvia's Place
* Pixi
* Kiko Milano
* selected other brands

---

## High-End / Prestige

Potential examples:

* MAC
* NARS
* Rare Beauty
* Fenty Beauty
* Benefit
* Tarte
* Too Faced
* Urban Decay
* Anastasia Beverly Hills
* Huda Beauty
* Makeup by Mario
* Haus Labs
* Saie
* Tower 28

---

## Luxury

Potential examples:

* Dior
* YSL Beauty
* Armani Beauty
* Givenchy
* Tom Ford Beauty
* Chanel if usable data is available
* Guerlain if usable data is available

Do not force brands into the project if data is poor.

---

# 12. MARKET TIER CLASSIFICATION

Do NOT classify products as drugstore/high-end purely based on price.

That would create circular analysis.

Create a separate brand-tier mapping.

Suggested values:

* Drugstore
* Mid-range
* High-end
* Luxury

Classification should consider:

* distribution channel
* retailer positioning
* prestige status
* brand positioning
* market perception

Maintain:

`brand_tier_mapping.csv`

Fields:

* brand
* market_tier
* classification_basis
* source_or_reason
* reviewed_date

Document ambiguous cases.

---

# 13. DATA ACQUISITION STRATEGY

This project should NOT depend exclusively on one outdated Kaggle dataset.

The preferred architecture is:

## Automated Multi-Source Beauty Product Data Pipeline

Use a combination of:

1. current structured beauty/product APIs
2. licensed or authorised product feeds
3. permitted web extraction where allowed
4. official manufacturer websites for validation
5. older public datasets for historical metadata only
6. manual validation for critical products

---

# 14. CRITICAL SCRAPING RULE

Before automatically collecting data from any retailer or website:

Check:

* terms of use
* robots policy where relevant
* permitted automated access
* available public APIs
* affiliate/product-feed availability

Do not build a scraper that requires:

* CAPTCHA bypassing
* anti-bot circumvention
* proxy rotation designed to evade blocks
* browser fingerprint manipulation
* Cloudflare bypass
* authentication circumvention
* rate-limit evasion

If automated extraction is prohibited or blocked, use another legal/authorised source.

Do not make the project dependent on violating retailer terms.

---

# 15. PREFERRED DATA SOURCE TYPES

## Source Type A: Beauty/Product APIs

Prioritise services that provide structured product information such as:

* product name
* brand
* retailer
* price
* original price
* category
* rating
* review count
* size
* ingredients
* stock
* product URL
* variants

Evaluate current services rather than assuming any one source will remain available.

The agent should perform a source feasibility study before building the full pipeline.

---

# 16. SOURCE FEASIBILITY STUDY

Before collecting hundreds of products:

Test approximately 20 products from at least 3 possible data sources.

For each source determine coverage for:

| Field        | Required?          |
| ------------ | ------------------ |
| Product name | Critical           |
| Brand        | Critical           |
| Category     | Critical           |
| Retail price | Critical           |
| Quantity     | Critical           |
| Unit         | Critical           |
| Product URL  | Critical           |
| Retailer     | Critical           |
| Rating       | Strongly preferred |
| Review count | Strongly preferred |
| Description  | Preferred          |
| Finish       | Preferred          |
| Coverage     | Preferred          |
| Ingredients  | Preferred          |
| Shade        | Preferred          |
| UPC/EAN      | Very useful        |

Create:

`source_feasibility_report.md`

Evaluate:

* data quality
* cost
* rate limits
* quantity coverage
* makeup coverage
* retailer coverage
* reliability
* update frequency
* legal/usage constraints

Only then choose the acquisition stack.

---

# 17. HISTORICAL SEPHORA DATASET

An older Sephora public dataset may be used as supplementary data.

It may contain:

* product names
* brand
* categories
* size
* historical price
* ratings
* reviews
* ingredients
* highlights

Use it primarily for:

* bootstrapping product catalogue
* testing cleaning logic
* ingredient data
* historical metadata
* historical price comparison if entity matching is reliable

Do NOT treat old prices as current prices.

Store:

`historical_price`

separately from:

`current_price`

---

# 18. CURRENT DATA OBSERVATION

Every current price record should contain:

* price
* currency
* retailer
* observed_at
* source
* list/sale status

Treat the dataset as a market snapshot.

Example:

> US beauty retail price snapshot, August 2026

Do not pretend prices are permanently valid.

---

# 19. LIST PRICE VS SALE PRICE

Maintain separate columns:

* list_price
* sale_price
* sale_flag

Primary unit-value analysis should use LIST PRICE.

Reason:

Temporary promotions can distort cross-product comparisons.

Sale-price analysis can exist as a secondary feature later.

---

# 20. MULTI-SOURCE DATA ARCHITECTURE

Do not overwrite conflicting retailer records.

Use separate product and offer tables.

Example:

Rare Beauty Product X:

Retailer A:
$25

Retailer B:
$25

Retailer C:
$24

Preserve each observation.

---

# 21. DATABASE ARCHITECTURE

Recommended database:

DuckDB

PostgreSQL is also acceptable if there is a clear reason.

Suggested tables:

## brands

* brand_id
* brand_name
* market_tier
* tier_basis

## categories

* category_id
* category
* subcategory
* preferred_standard_unit

## products

* product_id
* brand_id
* category_id
* product_name
* product_form
* description
* finish
* coverage
* texture
* parent_product_id

## product_variants

* variant_id
* product_id
* shade_name
* shade_family
* undertone
* size_variant
* mini_flag

## product_sizes

* size_id
* product_id
* variant_id
* size_raw
* quantity_raw
* quantity_standard
* standard_unit
* pack_count

## product_offers

* offer_id
* product_id
* retailer
* list_price
* sale_price
* currency
* observed_at
* source_url

## product_reviews

* product_id
* retailer
* rating
* review_count
* recommendation_pct
* observed_at

## product_ingredients

* product_id
* ingredient_text
* source

## product_attributes

* product_id
* finish
* coverage
* texture
* waterproof
* longwear
* vegan
* cruelty_free
* fragrance_free
* claims_text

## product_features

Engineered analytical fields.

## dupe_pairs

* anchor_product_id
* candidate_product_id
* similarity_score
* true_value_score
* value_classification

---

# 22. ENTITY RESOLUTION

The same product may appear differently across sources.

Example:

Source 1:

Rare Beauty Soft Pinch Liquid Blush - Hope

Source 2:

Rare Beauty Soft Pinch Liquid Blush Hope 7.5 mL

Source 3:

Soft Pinch Liquid Blush by Rare Beauty - Hope

Build an entity-resolution layer.

Potential matching hierarchy:

1. exact GTIN / UPC / EAN if available
2. exact normalised brand
3. fuzzy normalised product name
4. category compatibility
5. size compatibility
6. shade compatibility
7. retailer SKU where useful

Create:

`match_confidence`

Example:

97.3%

Do not automatically merge low-confidence matches.

Set thresholds:

* high confidence
* manual review
* reject

Store uncertain matches separately.

---

# 23. TEXT NORMALISATION FOR ENTITY MATCHING

Standardise:

* lowercase
* punctuation
* trademark symbols
* hyphenation
* "mini"
* "travel"
* shade information
* duplicate brand names
* size suffixes
* "by BRAND"
* product-type abbreviations

Do not destroy important identifiers.

---

# 24. CRITICAL RAW DATA FIELDS

## Identification

* product_id
* product_name
* brand
* category
* subcategory
* product_form
* market_tier
* variant
* shade
* parent_product_id

## Pricing

* list_price
* sale_price
* currency
* retailer
* observed_at

## Quantity

* amount_raw
* amount_value_raw
* unit_raw
* standard_quantity
* standard_unit
* pack_count

## Product Information

* finish
* coverage
* texture
* shade_name
* shade_family
* undertone
* description
* claims
* ingredients

## Review Information

* rating
* review_count
* recommendation_percentage

## Retail Information

* bestseller_flag
* cult_product_flag
* product_url
* source_name

## Provenance

* source_url
* source_type
* extraction_method
* collected_at

---

# 25. DATA PROVENANCE

Every important data field should be traceable.

Where practical store:

* source_name
* source_url
* collection timestamp
* acquisition method

For high-value headline findings, verify against an authoritative source.

---

# 26. HERO / ANCHOR PRODUCT DATASET

Create a manually validated subset of approximately:

50 to 100 important beauty products.

These might include:

* cult products
* bestselling products
* famous high-end products
* famous drugstore products
* frequently discussed dupes

For each hero product verify:

* product identity
* price
* quantity
* unit
* category
* tier
* rating
* review count
* product form
* shade where relevant

This subset can be used for:

* showcase analysis
* dupe benchmark
* app demos
* model validation

---

# 27. UNIT PARSING IS A CORE TECHNICAL FEATURE

Beauty sizes are messy.

Examples:

* 1 oz
* 0.04 oz
* 0.05 oz / 1.4 g
* 1 fl oz
* 30 mL
* 0.33 fl oz
* 3.5 g
* 2 x 4 g
* 2 × 4g
* Mini 0.17 oz
* 8.5 mL
* 3 x 0.06 oz

Create a robust parser.

---

# 28. STANDARD UNITS

Weight products:

grams

Volume products:

millilitres

Conversions:

1 weight oz = 28.3495 g

1 US fluid oz = 29.5735 mL

Do not treat weight ounces and fluid ounces as equivalent.

---

# 29. DUAL-UNIT LABELS

If a product provides:

0.05 oz / 1.5 g

Prefer the manufacturer's explicit gram value when available.

Use conversion only when a standard-unit value is not supplied.

Store both raw and standardised quantity.

---

# 30. MULTIPACK PARSING

Example:

2 x 4 g

Should produce:

pack_count = 2

quantity_per_item = 4 g

total_quantity = 8 g

Do not accidentally treat total quantity as 4 g.

---

# 31. CATEGORY UNIT MAPPING

Example:

| Category       | Preferred Unit |
| -------------- | -------------- |
| Foundation     | mL             |
| Concealer      | mL             |
| Liquid blush   | mL             |
| Powder blush   | g              |
| Bronzer        | g              |
| Highlighter    | g where powder |
| Setting powder | g              |
| Pressed powder | g              |
| Lip liner      | g              |
| Lipstick       | g              |
| Lip gloss      | mL             |
| Mascara        | mL             |
| Primer         | mL             |
| Setting spray  | mL             |
| Eyeshadow      | g              |

Document exceptions.

---

# 32. DATA QUALITY FLAGS

Create:

`data_quality_flag`

Possible values:

* valid
* missing_price
* missing_quantity
* ambiguous_unit
* suspected_duplicate
* questionable_price
* incompatible_unit
* incomplete
* manual_review
* excluded_from_unit_analysis

Never silently drop problematic records.

---

# 33. VALIDATION RULES

Automatically validate:

* price > 0
* quantity > 0
* rating within valid scale
* review_count >= 0
* valid currency
* known category
* known unit
* reasonable quantity range
* no accidental duplicate products
* no incompatible mass/volume conversions

---

# 34. MANUAL DATA AUDIT

Randomly sample at least 50 products.

Manually verify:

* product
* brand
* category
* price
* quantity
* unit
* calculated unit price
* market tier

Document results.

Target at least approximately 95% correctness for critical fields before final analysis.

---

# 35. PRIMARY METRIC 1: STICKER PRICE

`sticker_price = list_price`

This represents affordability.

---

# 36. PRIMARY METRIC 2: PRICE PER STANDARD UNIT

Weight:

`price_per_g = price / grams`

Volume:

`price_per_ml = price / millilitres`

Generic field:

`price_per_standard_unit`

Never compare price/g directly with price/mL across incompatible products.

---

# 37. PRIMARY METRIC 3: CATEGORY UNIT PRICE INDEX

Calculate:

`unit_price_index = product_price_per_unit / category_median_price_per_unit`

Interpretation:

1.00 = category median

0.70 = 30% below category median

1.40 = 40% above category median

This allows comparisons across different categories.

---

# 38. PRIMARY METRIC 4: PRICE PREMIUM

`price_premium_pct = ((unit_price / category_median_unit_price) - 1) * 100`

Example:

+70%

means:

70% more expensive per standard unit than the category median.

---

# 39. PRIMARY METRIC 5: QUANTITY INDEX

`quantity_index = product_quantity / category_median_quantity`

This helps investigate whether expensive products contain more product.

---

# 40. RATING ADJUSTMENT

Do not treat:

5 stars from 5 reviews

as equivalent to:

4.8 stars from 20,000 reviews.

Use Bayesian rating adjustment.

Possible formula:

`weighted_rating = ((v / (v + m)) * R) + ((m / (v + m)) * C)`

Where:

R = product rating

v = number of reviews

C = category mean rating

m = minimum confidence threshold

Document final parameters.

---

# 41. RATING-ADJUSTED VALUE

Possible metric:

`rating_value_score = weighted_rating_normalised / unit_price_index`

Rescale 0 to 100 if useful.

Do NOT call this objective quality.

Call it:

* comparative value score
* rating-adjusted value
* consumer value indicator

Clearly document limitations.

---

# 42. COST PER USE

This is a SECONDARY metric.

Do not pretend one usage amount applies to everyone.

For suitable categories create scenarios:

* light use
* standard use
* heavy use

Formula:

`estimated_uses = quantity / estimated_quantity_per_use`

`cost_per_use = price / estimated_uses`

Store assumptions in:

`usage_assumptions.yaml`

Do not hard-code them throughout notebooks.

Clearly label:

> Estimated cost per use based on usage assumptions.

---

# 43. DRUGSTORE ILLUSION INDEX

Create an original analytical concept:

# Drugstore Illusion Index

Purpose:

Identify cases where the apparent checkout saving is much larger than the actual quantity-adjusted saving.

For matched comparable products:

`sticker_ratio = drugstore_price / highend_price`

`unit_ratio = drugstore_unit_price / highend_unit_price`

`illusion_multiplier = unit_ratio / sticker_ratio`

Example:

High-end:

$40 / 10 g = $4/g

Drugstore:

$15 / 2.5 g = $6/g

Sticker ratio:

0.375

Unit ratio:

1.5

Illusion multiplier:

4.0

The drugstore item appears dramatically cheaper at checkout but is worse per gram.

Do not rely only on the multiplier.

Create intuitive classifications.

---

# 44. VALUE CLASSIFICATIONS

Potential categories:

## Genuine Bargain

Low upfront price and strong unit economics.

## Cheap Entry Price

Low checkout price but average unit economics.

## False Economy

Cheaper upfront but more expensive per gram/mL than comparable alternatives.

## Luxury Value

High checkout price but competitive quantity economics.

## Luxury Premium

High checkout price and high unit price.

## Balanced Value

Middle-of-the-market economics.

Thresholds must be transparent and data-informed.

---

# 45. MINI TAX

For matched mini/full-size versions of the SAME product:

`mini_tax_pct = ((mini_price_per_unit / fullsize_price_per_unit) - 1) * 100`

Example:

Full:

$40 / 10 g = $4/g

Mini:

$18 / 2 g = $9/g

Mini Tax:

125%

Analyse:

* median Mini Tax
* mean Mini Tax
* highest Mini Tax
* lowest
* Mini Tax by brand
* Mini Tax by category
* distribution

Do not compare unrelated mini and full-size products.

---

# 46. LOVED / CULT PRODUCT ANALYSIS

Create a curated set of popular/cult products.

Possible criteria:

* bestseller badge
* very high review count
* high rating
* retailer bestseller lists
* documented cult status
* manual curated anchor list

Do not call a product "viral" unless actual social-trend evidence exists.

Prefer:

* cult
* bestselling
* highly reviewed
* popular

when social data is not available.

---

# 47. CULT PRODUCT SHOWDOWNS

For important categories compare:

High-end anchor

vs

Drugstore alternatives.

Show:

* sticker price
* quantity
* unit price
* category unit index
* rating
* weighted rating
* review count
* checkout savings
* quantity-adjusted savings
* final classification

Declare:

* Cheapest Upfront
* Best Quantity Value
* Best Reviewed Value
* Best True Value

These may be different products.

---

# 48. STATISTICAL ANALYSIS

The project must go beyond descriptive visualisations.

Analyse differences between tiers.

Potential tests:

* Mann-Whitney U
* Welch's t-test where appropriate
* bootstrap confidence intervals
* Kruskal-Wallis
* ANOVA where assumptions hold
* post-hoc comparisons

Always inspect distributions first.

Do not report only p-values.

Include:

* effect size
* confidence intervals
* practical interpretation

---

# 49. REGRESSION ANALYSIS

Investigate what predicts unit price.

Potential model:

`log(price_per_unit) ~ market_tier + category + log(quantity) + weighted_rating + log(review_count + 1)`

Questions:

* After controlling for category, what premium remains for prestige/luxury positioning?
* Does higher rating predict higher unit price?
* Does greater quantity lower unit cost?
* Which categories are intrinsically more expensive per unit?

Prefer interpretable regression.

This is primarily explanatory.

---

# 50. PRICE VS RATING ANALYSIS

Analyse:

* sticker price vs rating
* unit price vs rating
* unit-price index vs weighted rating
* tier vs weighted rating

Use:

* Spearman correlation
* scatter plots
* regression where useful

Do not claim:

> expensive products are better

unless the evidence genuinely supports it.

---

# 51. BRAND VALUE ANALYSIS

For brands with sufficient sample size calculate:

* product count
* median sticker price
* median unit-price index
* median quantity index
* weighted rating
* percentage below category unit median
* percentage classified Genuine Bargain
* percentage classified False Economy
* percentage classified Luxury Value/Premium

Set a minimum product-count threshold.

Do not rank brands with 1 or 2 products.

---

# 52. CATEGORY ECONOMICS

For each category calculate:

* median drugstore sticker price
* median prestige sticker price
* sticker premium
* median quantities
* median drugstore unit price
* median prestige unit price
* quantity-adjusted premium
* price dispersion
* quantity dispersion
* percentage of drugstore products more expensive per unit than the high-end category median

Answer:

> Where is drugstore genuinely dominant?

and:

> Where does the prestige premium become unexpectedly small?

---

# 53. DUPE ENGINE

The second major component is a product similarity system.

The purpose is to identify genuinely similar alternatives BEFORE analysing price.

---

# 54. ABSOLUTE DUPE RULE

PRICE MUST NOT BE INCLUDED IN THE SIMILARITY MODEL.

Similarity and value must remain separate.

Store:

`dupe_similarity_score`

separately from:

`true_value_score`

Otherwise the model will learn:

cheap = similar

which is conceptually wrong.

---

# 55. DUPE CANDIDATE FILTERING

Before scoring similarity, restrict candidates to:

* same category
* compatible product form
* compatible usage
* compatible coverage where relevant
* compatible finish where relevant

For colour cosmetics also consider:

* shade family
* undertone
* shade description
* colour data

Do not recommend structurally different products just because their marketing text is similar.

---

# 56. SIMILARITY FEATURES

Possible components:

## Product Text Similarity

Use:

* product name
* description
* claims
* texture
* finish
* coverage

Potential model:

Sentence Transformer embeddings

Similarity:

Cosine similarity

---

## Ingredient Similarity

Where available:

* ingredient-set Jaccard similarity
* ingredient overlap
* weighted ingredient representation

Do not claim identical formulation based solely on overlap.

---

## Shade Similarity

Where reliable data exists:

* shade family
* undertone
* colour descriptors
* HEX/RGB
* perceptual colour distance

Only claim exact shade dupes when shade-level data is trustworthy.

---

## Attribute Similarity

Compare:

* finish
* coverage
* form
* wear claims
* texture
* waterproof
* matte/dewy/satin
* etc.

---

# 57. CATEGORY-SPECIFIC DUPE WEIGHTS

Do not force identical weighting for all categories.

Example:

Lipstick:

Shade similarity is important.

Mascara:

Shade similarity is mostly irrelevant.

Foundation:

Coverage, finish, skin type, shade range may matter more.

Suggested starting framework only:

* semantic/product attributes: 35%
* shade: 25%
* ingredients: 20%
* finish/form/coverage: 20%

Then adjust by category.

Document final weights.

---

# 58. DUPE SCORE

Return:

0 to 100

Example:

`Dupe Similarity: 92/100`

Also provide explainability:

* same product category
* similar finish
* similar coverage
* high text similarity
* similar shade family
* strong ingredient overlap

---

# 59. DUPE ENGINE VALIDATION

Do not build embeddings and call the project finished.

Create a manually reviewed benchmark.

Target:

30 to 50 anchor products minimum.

Evaluate:

* Precision@3
* Precision@5
* category correctness
* product-form correctness
* shade correctness where relevant
* manual judgement

Document failure cases.

---

# 60. EXACT SHADE LIMITATION

If shade-level data quality is insufficient:

Do NOT claim:

> exact dupe

Instead say:

* product-level alternative
* formula alternative
* finish alternative
* similar product
* potential dupe candidate

Be transparent.

---

# 61. TRUE-VALUE DUPE ENGINE

After similarity is calculated, introduce economics.

Example:

High-End Original:

Price: $34

Quantity: 1.2 g

Price/g: $28.33

Candidate A:

Price: $10

Quantity: 0.3 g

Price/g: $33.33

Similarity: 94%

Result:

71% cheaper upfront.

18% more expensive per gram.

Classification:

False Economy.

Candidate B:

Price: $14

Quantity: 0.8 g

Price/g: $17.50

Similarity:

91%

Result:

59% cheaper upfront.

38% cheaper per gram.

Classification:

Genuine Bargain.

---

# 62. TRUE-VALUE SCORE

Potential structure:

65% similarity

25% quantity-adjusted economics

10% rating confidence

These are starting assumptions only.

Test them.

Similarity should dominate.

A cheap product that is not genuinely similar is not a dupe.

Expose component scores in the app.

---

# 63. CONSUMER DECISION OUTPUTS

Keep distinct recommendations:

## Cheapest

Lowest sticker price.

## Best Quantity Value

Lowest category-adjusted unit price.

## Best Reviewed Value

Strong unit economics + strong weighted rating.

## Best Dupe

Highest similarity.

## Best True-Value Dupe

Strong similarity + strong economics.

---

# 64. DATA PIPELINE LAYERS

Use:

## Raw

Immutable source data.

`data/raw/`

## Staging

Parsed/lightly cleaned source-specific data.

`data/staging/`

## Processed

Normalised:

* products
* brands
* categories
* sizes
* prices
* tiers

`data/processed/`

## Analytics

Feature-engineered final analytical data.

`data/analytics/`

Never manually modify raw data.

---

# 65. REPOSITORY STRUCTURE

Recommended:

```text
beauty-value-intelligence/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── config/
│   ├── categories.yaml
│   ├── unit_rules.yaml
│   ├── tier_mapping.yaml
│   ├── usage_assumptions.yaml
│   └── data_sources.yaml
│
├── data/
│   ├── raw/
│   ├── staging/
│   ├── processed/
│   └── analytics/
│
├── database/
│   ├── schema.sql
│   └── beauty_value.duckdb
│
├── src/
│   ├── ingest/
│   ├── cleaning/
│   ├── matching/
│   ├── units/
│   ├── validation/
│   ├── features/
│   ├── analytics/
│   ├── modelling/
│   └── utils/
│
├── sql/
│   ├── category_value.sql
│   ├── brand_value.sql
│   ├── false_economies.sql
│   ├── mini_tax.sql
│   ├── tier_comparison.sql
│   └── hero_products.sql
│
├── notebooks/
│   ├── 01_source_feasibility.ipynb
│   ├── 02_data_collection_audit.ipynb
│   ├── 03_data_cleaning_units.ipynb
│   ├── 04_entity_resolution.ipynb
│   ├── 05_exploratory_analysis.ipynb
│   ├── 06_true_cost_analysis.ipynb
│   ├── 07_statistical_analysis.ipynb
│   ├── 08_mini_tax.ipynb
│   ├── 09_cult_showdowns.ipynb
│   ├── 10_dupe_engine.ipynb
│   ├── 11_dupe_validation.ipynb
│   └── 12_business_insights.ipynb
│
├── app/
│   ├── app.py
│   ├── pages/
│   └── components/
│
├── tests/
│   ├── test_units.py
│   ├── test_matching.py
│   ├── test_features.py
│   ├── test_data_quality.py
│   └── test_dupe_logic.py
│
├── reports/
│   ├── figures/
│   ├── source_feasibility_report.md
│   └── final_insights.md
│
└── docs/
    ├── methodology.md
    ├── data_dictionary.md
    ├── source_documentation.md
    └── limitations.md
```

---

# 66. NOTEBOOK PURPOSES

## 01_source_feasibility

Compare candidate sources.

Do not collect the full dataset before this is complete.

---

## 02_data_collection_audit

Inspect:

* source counts
* brands
* categories
* missing fields
* duplicates
* retailer coverage

---

## 03_data_cleaning_units

Build and validate the quantity parser.

---

## 04_entity_resolution

Match products across sources.

---

## 05_exploratory_analysis

Understand:

* distributions
* category balance
* price
* quantity
* ratings
* tiers

---

## 06_true_cost_analysis

Core unit economics.

---

## 07_statistical_analysis

Tests, effect sizes, regression.

---

## 08_mini_tax

Matched mini/full-size analysis.

---

## 09_cult_showdowns

Selected loved product comparisons.

---

## 10_dupe_engine

Build similarity model.

---

## 11_dupe_validation

Benchmark model.

---

## 12_business_insights

Consolidated final findings.

---

# 67. SQL MUST BE MEANINGFUL

Do not include SQL simply to tick a skill checkbox.

Use SQL for:

* median unit price by category
* tier comparisons
* brand value rankings
* False Economy products
* Genuine Bargains
* Mini Tax
* quantity comparisons
* hero-product retrieval
* multi-retailer price observations
* category unit indexes

Include reusable views where useful.

---

# 68. RECOMMENDED TECH STACK

Use technologies only if they serve a purpose.

## Core

Python

Pandas or Polars

DuckDB

SQL

NumPy

SciPy

Statsmodels

Scikit-learn

Sentence Transformers

Plotly

Streamlit

## Optional

BeautifulSoup / httpx for permitted sources

Power BI if a BI version adds value

PostgreSQL if justified

Do not add Spark, Kafka, Airflow, Docker, LLMs, vector databases, etc. just to make the project sound advanced.

---

# 69. STREAMLIT APPLICATION

The app should look like a real beauty intelligence tool.

Not like a homework dashboard.

Keep it visually clean and polished.

---

# 70. APP PAGE 1: EXECUTIVE OVERVIEW

KPIs:

* products analysed
* brands
* categories
* retailers
* median drugstore price
* median high-end price
* median drugstore unit-price index
* median high-end unit-price index
* percentage Genuine Bargain
* percentage False Economy

Show actual headline insights.

Never use placeholder conclusions in the finished version.

---

# 71. PAGE 2: CATEGORY ECONOMICS

Filters:

* category
* tier
* brand
* retailer

Show:

* sticker-price distribution
* quantity distribution
* unit-price distribution
* median tier comparisons
* category premium
* quantity-adjusted premium

---

# 72. PAGE 3: DRUGSTORE ILLUSION

Highlight cases where:

* upfront price is low
* quantity is small
* unit economics are poor

Show:

* False Economy
* Genuine Bargain
* Cheap Entry Price
* Luxury Value
* Luxury Premium

---

# 73. PAGE 4: MINI TAX

Show:

* median Mini Tax
* highest brands
* highest categories
* paired mini/full comparisons
* search by product

---

# 74. PAGE 5: CULT PRODUCT SHOWDOWN

User selects an anchor product.

Compare alternatives using:

* price
* quantity
* price/unit
* rating
* review count
* similarity
* savings
* classification

---

# 75. PAGE 6: TRUE-VALUE DUPE FINDER

Flagship feature.

User searches:

High-end Product X

Display original:

* brand
* tier
* price
* quantity
* unit price
* rating
* key characteristics

Then top alternatives:

### Candidate

Similarity:
93%

Checkout Saving:
57%

Unit Saving:
31%

Rating:
4.6

True Value:
91/100

Classification:
Genuine Bargain

Alternative case:

Similarity:
95%

Checkout Saving:
68%

Unit Saving:
-12%

Classification:
False Economy

The contrast is essential.

---

# 76. PAGE 7: BRAND VALUE EXPLORER

Compare brands using:

* median unit-price index
* quantity index
* weighted rating
* sample size
* category coverage
* value classifications

---

# 77. PAGE 8: METHODOLOGY

Explain:

* data sources
* collection date
* source restrictions
* tier methodology
* unit conversions
* rating adjustment
* Drugstore Illusion metric
* Mini Tax
* dupe methodology
* model limitations

Transparency is a strength.

---

# 78. KEY VISUALISATIONS

Potential charts:

* box plot: unit price by tier
* box plot: quantity by tier
* scatter: sticker price vs quantity
* scatter: unit price vs weighted rating
* slope chart: sticker premium vs quantity-adjusted premium
* category heatmap
* brand ranking
* mini/full paired chart
* distribution plots
* dupe comparison cards

Every chart should answer a specific question.

Do not add decorative charts.

---

# 79. BUSINESS INTERPRETATION

The final analysis should include both:

## Consumer Perspective

What should shoppers actually compare?

## Retail Perspective

What does package size reveal about pricing strategy?

Possible implications:

* smaller package sizes reduce checkout price
* prestige brands may use quantity strategically
* mini products may operate as high-margin trial products
* high-end brands with strong unit value can market longevity
* mass-market brands can differentiate on genuine unit value
* assortment planners can understand value positioning by category

---

# 80. EXAMPLE FINDINGS TO SEARCH FOR

These are examples of the TYPE of insight to investigate.

Do not fabricate these numbers.

Potential findings:

> Drugstore products are 55% cheaper at checkout but only 30% cheaper per unit.

> Drugstore lip liners contain significantly less product.

> Powder blush has a surprisingly small prestige unit-price premium.

> Mascara maintains a large prestige premium even after quantity adjustment.

> Higher price per gram shows almost no relationship with ratings.

> Mini products cost 80% more per unit on average.

These are hypotheses, not conclusions.

---

# 81. README STORY

The README should explain:

## The Problem

Sticker price is not true cost.

## The Question

Is drugstore actually cheaper?

## Why It Matters

Package sizes vary dramatically.

## What Was Built

* multi-source pipeline
* unit parser
* SQL model
* statistical analysis
* value metrics
* Mini Tax
* Drugstore Illusion
* dupe model
* Streamlit app

## Dataset

Sources, size, scope.

## Methodology

Important formulas.

## Findings

Only real findings.

## True-Value Dupe Finder

Screenshots/demo.

## Tech Stack

## How to Run

## Limitations

## Future Work

---

# 82. PORTFOLIO SUMMARY

The project should eventually be explainable as:

> Beauty consumers usually compare products by sticker price, even though package sizes vary significantly across products and brands. I built a multi-source beauty retail intelligence pipeline that standardised product quantities into comparable units, modelled price-per-unit economics across market tiers, quantified hidden size premiums, and combined semantic product similarity with retail value analytics to determine whether popular alternatives actually provide meaningful savings.

---

# 83. WHAT NOT TO DO

DO NOT:

* build a generic beauty dashboard
* make sentiment analysis the focus
* use one Kaggle CSV as the entire project
* silently use old prices as current prices
* scrape websites that prohibit it
* bypass anti-bot controls
* convert grams to mL
* treat fl oz and oz the same
* ignore pack sizes
* classify brand tier based solely on price
* use price inside dupe similarity
* call products exact shade dupes without reliable data
* call products viral without evidence
* fabricate findings
* fabricate missing quantities
* rank brands with tiny samples
* report p-values without effect sizes
* claim correlation means causation
* make cost-per-use assumptions look factual
* over-engineer
* add AI just because AI sounds impressive

---

# 84. PROJECT PRIORITY ORDER

If scope becomes too large, prioritise:

1. Data-source feasibility
2. Clean current dataset
3. Quantity parser
4. Unit economics
5. Drugstore vs prestige analysis
6. Statistical validation
7. Drugstore Illusion
8. Mini Tax
9. Cult-product comparisons
10. Dupe engine
11. True-Value Dupe scoring
12. Streamlit

The project should already be strong before the dupe engine is built.

---

# 85. MVP DEFINITION

The MVP is complete when:

* current product data exists
* approximately 600+ valid products exist
* 10+ categories exist
* tiers are mapped
* quantities are normalised
* price per unit works
* drugstore vs prestige analysis works
* Drugstore Illusion classifications work
* several strong insights are validated
* a basic Streamlit explorer exists

The ML dupe engine is Phase 2.

---

# 86. FULL PROJECT DEFINITION

The full project is complete when:

* multi-source acquisition works
* entity resolution works
* SQL database exists
* tests exist
* data quality is documented
* statistical analysis is complete
* Mini Tax is complete
* cult showdowns exist
* dupe engine exists
* dupe validation exists
* True-Value ranking works
* polished Streamlit app works
* README is excellent
* methodology and limitations are documented

---

# 87. TESTING REQUIREMENTS

Test at minimum:

## Quantity Parsing

* 1 oz
* 1 fl oz
* 0.04 oz
* 30 mL
* 3.5 g
* 2 x 4 g
* dual-unit labels

## Conversions

Known expected values.

## Metrics

* unit price
* quantity index
* price premium
* Mini Tax
* savings
* Drugstore Illusion metric

## Entity Matching

Known same-product examples.

## Data Quality

Nulls, invalid values, duplicates.

## Dupe Logic

Price must not affect similarity.

---

# 88. SOURCE COVERAGE TARGETS

Aim for approximately:

* price coverage: >98%
* quantity coverage: >90%
* tier coverage: 100%
* category coverage: 100%
* provenance coverage: 100%
* rating coverage: ideally >80%

If coverage is worse, report it honestly.

---

# 89. REPRODUCIBILITY

The project must run from a clean environment.

Include:

* requirements.txt
* setup instructions
* configuration files
* deterministic seeds
* commands to rebuild processed data
* commands to recreate database
* command to run tests
* command to launch app

Avoid hidden manual steps.

---

# 90. FINAL PRESENTATION STORYLINE

Use approximately:

## Slide 1

Is drugstore makeup actually cheaper?

## Slide 2

Why sticker price is misleading.

## Slide 3

Dataset and sources.

## Slide 4

Cleaning messy beauty quantities.

## Slide 5

Sticker price vs unit price.

## Slide 6

Category differences.

## Slide 7

Drugstore Illusion.

## Slide 8

Mini Tax.

## Slide 9

Price vs ratings.

## Slide 10

Loved-product showdowns.

## Slide 11

Why normal dupe finders are incomplete.

## Slide 12

Dupe similarity architecture.

## Slide 13

True-Value Dupe example.

## Slide 14

Retail implications.

## Slide 15

Final answer to the research question.

---

# 91. FINAL DELIVERABLES

The finished project should include:

1. source feasibility study
2. data-source configuration
3. ingestion pipeline
4. raw data archive
5. staging data
6. processed dataset
7. analytical dataset
8. data dictionary
9. SQL schema
10. DuckDB database
11. entity-resolution logic
12. quantity parser
13. data-quality tests
14. SQL analyses
15. EDA
16. unit-economics analysis
17. statistical analysis
18. Drugstore Illusion analysis
19. Mini Tax analysis
20. cult-product showdowns
21. dupe engine
22. dupe benchmark
23. True-Value model
24. Streamlit app
25. methodology document
26. limitations document
27. README
28. final business-insights report
29. screenshots/demo
30. reproducibility instructions

---

# 92. ACCEPTANCE CHECKLIST

## DATA

* [ ] Sources have been tested before large-scale ingestion.
* [ ] Current prices are timestamped.
* [ ] Historical prices are labelled separately.
* [ ] Product provenance exists.
* [ ] Entity resolution is documented.
* [ ] Mass and volume remain separate.
* [ ] Weight oz and fluid oz are parsed correctly.
* [ ] Pack sizes are handled.
* [ ] Tiers are documented.
* [ ] Categories use compatible units.

## ANALYSIS

* [ ] Sticker-price comparison exists.
* [ ] Unit-price comparison exists.
* [ ] Quantity comparison exists.
* [ ] Category-normalised metrics exist.
* [ ] Drugstore vs prestige analysis exists.
* [ ] Effect sizes exist.
* [ ] Confidence intervals exist where useful.
* [ ] Mini Tax uses matched variants.
* [ ] Brand rankings require adequate samples.
* [ ] Findings are not pre-decided.

## DUPE ENGINE

* [ ] Price is excluded from similarity.
* [ ] Candidates are category compatible.
* [ ] Similarity is explainable.
* [ ] Benchmark exists.
* [ ] Precision@K is evaluated.
* [ ] Failure cases are documented.
* [ ] True Value is separate from similarity.

## APP

* [ ] Executive Overview works.
* [ ] Category Economics works.
* [ ] Drugstore Illusion works.
* [ ] Mini Tax works.
* [ ] Cult Showdowns work.
* [ ] True-Value Dupe Finder works.
* [ ] Brand Explorer works.
* [ ] Methodology page works.
* [ ] No placeholder values remain.
* [ ] No broken filters remain.

## REPOSITORY

* [ ] README is complete.
* [ ] Tests pass.
* [ ] Pipeline is reproducible.
* [ ] Code is modular.
* [ ] Data quality is documented.
* [ ] Final insights use actual calculations.

---

# 93. PROJECT SUCCESS DEFINITION

Someone should eventually be able to search:

> Is this $12 drugstore product actually better value than this $35 high-end product?

and receive an evidence-based answer such as:

> The drugstore product costs 66% less at checkout, but contains 72% less product. After quantity adjustment it costs 18% more per gram, so it is classified as a False Economy.

For another product:

> This alternative has 91% similarity, costs 59% less upfront, costs 38% less per gram, and has a comparable weighted rating. It is the strongest True-Value Dupe among the analysed alternatives.

That is the intellectual core of this project.

---

# 94. FIRST TASK FOR THE NEW AI

DO NOT immediately build the dashboard.

DO NOT immediately build the dupe engine.

DO NOT immediately collect thousands of rows.

Start with:

## Phase 0: Project Audit

1. Read this entire specification.
2. Create the proposed repository structure.
3. Identify the minimum required fields.
4. Identify 3 to 5 viable current data-source options.
5. Check their usage/access constraints.
6. Run a source feasibility test using approximately 20 representative beauty products.
7. Compare field coverage.
8. Produce `source_feasibility_report.md`.
9. Recommend the final acquisition architecture.
10. Only after that, begin the production ingestion pipeline.

Do not proceed blindly.

---

# 95. EXPECTED AI WORKING STYLE

When implementing:

* work incrementally
* run code
* inspect outputs
* verify calculations
* test before proceeding
* document assumptions
* preserve provenance
* keep raw data immutable
* prefer simple robust architecture
* explain major decisions
* do not fabricate missing data
* do not silently change project scope
* do not introduce random unnecessary features

If a proposed feature cannot be supported by available data:

Simplify the claim.

Do not fake precision.

---

# 96. OPTIONAL FUTURE EXTENSIONS

Only after the main project is excellent.

Possible future work:

## Historical price analysis

Compare older and current prices.

## Ingredient Intelligence

Compare ingredient profiles.

## Shade Intelligence

Improve colour matching.

## Cross-Market Pricing

US vs UK vs Nepal.

## Nepal Import Premium

Investigate whether international drugstore products still behave like "drugstore" products after import pricing in Nepal.

## Promotion Analysis

Compare regular price and sale-price economics.

## Review NLP

Investigate whether similar products receive similar complaints/praise.

## Price Tracking

Periodic retail-price snapshots.

Do not build these before the core project is complete.

---

# 97. FINAL QUALITY BAR

The project must NOT feel like:

> I downloaded a cosmetics CSV and visualised it.

It should feel like:

> I built a multi-source beauty retail data pipeline, reconciled inconsistent product identities, engineered a robust measurement-normalisation system, investigated the difference between checkout affordability and true unit economics, statistically tested prestige pricing effects, quantified hidden package-size premiums, and combined semantic product similarity with retail economics to identify genuinely valuable beauty alternatives.

That is the standard.

---

# 98. CENTRAL RESEARCH QUESTION

Everything should ultimately return to:

> When consumers pay less for a beauty product, are they actually getting better value, or are they sometimes simply buying less product?

And the application's second question:

> If I want an alternative to this expensive beauty product, which product is not only similar and cheaper at checkout, but genuinely better value?

Do not lose sight of these questions.

---

# 99. FINAL INSTRUCTION

Treat this as a flagship portfolio project.

Prioritise:

1. data reliability
2. correct product matching
3. correct quantity parsing
4. defensible methodology
5. interesting analysis
6. statistical validity
7. clear business interpretation
8. explainable ML
9. polished presentation
10. reproducibility

Technical complexity is only valuable when it improves the project.

Do not over-engineer.

Do not fabricate.

Do not bias the conclusion.

Run everything you build.

Verify the outputs.

Build the project so that every major claim can be defended in an interview.