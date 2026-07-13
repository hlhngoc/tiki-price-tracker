# Issue Tree

---

## SCQA

**Situation:**
Tiki ranks #3 in Vietnam's online book market with approximately 3.0% revenue share, behind Shopee (~55.6%) and TikTok Shop (~40.6%).

**Complication:**
This minor 3.0% book market share becomes an urgent vulnerability when viewed against Tiki's prolonged corporate distress at the macro platform level. This financial pressure is demonstrated by two distinct historical milestones: VNG fully writing off its 510B VND investment as early as Q1/2019, and the platform later recording a steep $93M USD operating loss in FY2022 (Note: both events serve as platform-wide corporate context, not book-category specific data). With cash runway severely constrained, the platform faces immediate, compelling pressure to audit unit economics and pricing margins across every single category, including books, to minimize operating losses.

**Question:**
Given its contracted 3.0% book market share and Tiki's platform-wide financial constraints, how should Tiki position and manage its online book category moving forward?

**Answer (initial hypothesis — to be tested against scraped data, not yet verified):**
Based on the platform's macro financial distress, we hypothesize that Tiki is undergoing a defensive retrenchment rather than an aggressive growth play. The platform can no longer afford to subsidize a low-margin 3P book marketplace to chase volume. Instead, our assessment suggests this pressure has driven a strategic pivot toward a lean, self-sustaining 1P model (Tiki Trading) to justify its operational survival.

*Caveat: This Answer is a starting hypothesis, not a conclusion. It must be revised based on findings from Day 9-14 data analysis (data quality audit + hypothesis testing using `seller_type` and pricing data).*

---

## MECE Issue Tree

### Branch A — 1P vs. 3P Internal Mix (Pricing & Margin Dynamics)

**Question:** Within Tiki's book category, what share of internal revenue (GMV proxy) comes from 1P (Tiki Trading) vs. 3P sellers, and how is that mix trending over time?

**Fields used:** `seller_type`, `price`, `quantity_sold` (as GMV proxy)

**Data requirement:** Time-series — requires multiple snapshots spanning enough days to observe a trend, not just a single point-in-time read. Cannot be tested until sufficient data has accumulated (Day 9+).

**Relevance:** Directly tests the initial SCQA hypothesis (defensive retrenchment toward 1P). This is the primary branch for confirming or rejecting the Answer stated in the SCQA section above.

---

### Branch B — Publisher (NXB) Behavior

**Question:** Which publishers maintain the most stable pricing (lowest discount rates), and which discount most aggressively?

**Fields used:** `publisher`, `price`, `discount_rate`

**Data requirement:** Cross-sectional — can be tested with a single well-formed snapshot, since it compares publishers against each other at a point in time rather than tracking change over time. Testable earlier than Branch A/C.

**Relevance:** Surfaces publisher-level pricing discipline patterns; informs which publisher relationships might be more resilient to price-war dynamics.

---

### Branch C — Assortment: Bestseller vs. Long-tail Discounting

**Question:** Do best-selling books get discounted more heavily over time than long-tail (low-volume) titles?

**Fields used:** `title`, `price`, `quantity_sold` (to define bestseller vs. long-tail), tracked across snapshots

**Data requirement:** Time-series — same constraint as Branch A. Requires observing price change over time, not just current discount level, since a book's current discount alone doesn't reveal whether it "became" more discounted or was always priced that way. Cannot be tested until sufficient data has accumulated (Day 9+).

**Relevance:** Tests whether Tiki's discounting behavior differs based on catalog position (bestseller vs. long-tail), which has implications for assortment strategy recommendations later in the project.

---

### Data Gaps (explicitly noted, not silently skipped)

- No data on Tiki's actual wholesale purchase cost from publishers — the ~40-45% discount figure in `market_notes.md` remains a consultant estimate, not verifiable against this dataset.
- No book-category-specific 1P/3P GMV split exists in public market data (only platform-wide, per `market_notes.md` Section 0b) — Branch A's findings will be the first book-category-specific evidence on this question, once enough data has accumulated.

