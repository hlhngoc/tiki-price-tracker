# API Notes — Books Category (Nhà Sách Tiki)

## Endpoint & Category

- Endpoint: `https://tiki.vn/api/personalish/v1/blocks/listings`
- `category_id = 8322` (Nhà Sách Tiki — root category)
- Decision: scrape the entire `8322` category, no filtering by subcategory (Literature, Manga, Economics, etc.)
  - Rationale: keeps the scraper simple, at the cost of mixing product types with different pricing behavior
  - Implication: analysis later needs to re-segment using `primary_category_path` or `category_l2_name`

## Fields of interest

| Field | Location in JSON | Notes |
|---|---|---|
| `author_name` | top-level | Mostly empty in the sampled data — needs a NULL-rate audit across subcategories before deciding if it's usable |
| `original_price` | top-level | The book's fixed cover price (a stable anchor) — distinct from `price`. Not yet verified against a real physical book's printed price |
| `price` | top-level | Displayed/selling price on the website |
| `seller_id` | top-level | Mostly observed as `1` in initial samples — exact percentage not yet audited |
| `seller_type` | `visible_impression_info.amplitude` | e.g. `OFFICIAL_STORE` — not yet confirmed whether `seller_id = 1` reliably maps to first-party (Tiki Trading) |
| Publisher (NXB) | **no dedicated field** — embedded inside `name`, pattern `"<Book title> - NXB <Publisher>"` | Not all products follow this pattern → will produce high NULL rate if parsed. Decision: store `name` as-is, unparsed, at scrape time; parsing happens later in `analysis/` (keeps the "don't invent data" principle) |
| `quantity_sold` | top-level | Polymorphic: `{"text": "Đã bán 67", "value": 67}` — needs consistent handling |
| `primary_category_path` | top-level | e.g. `1/2/8322/316/1084` — used to re-segment by subcategory during analysis |

## Data gaps identified

1. `author_name` is frequently empty at the root category level — exact NULL rate not yet measured, to be audited later
2. Publisher has no dedicated field; must be parsed from `name` — expect a high NULL rate for titles that don't follow the `- NXB ...` pattern
3. `seller_id` / `seller_type` only spot-checked on a few products — actual distribution not yet audited

## Open items for next steps

- Verify `original_price` matches the actual printed cover price on a physical book
- Audit NULL rate of `author_name`, publisher (parsed), and the `seller_id != 1` proportion using pandas
- Schema decision: store `name` raw; do not parse publisher at insert time
