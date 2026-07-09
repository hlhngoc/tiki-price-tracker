import sqlite3
from datetime import datetime


def init_db(db_name="tiki.db"):
    """
    Create the products and price_snapshots tables if they don't exist yet.

    Schema design:
    - products: fixed/slow-changing info per product (name, url).
      product_id is the primary key, sourced from Tiki's own id.
    - price_snapshots: one row per scrape, per product. This is what
      makes trend analysis possible — a flat table with only the
      current price would lose all history.
    """
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                name TEXT,
                url TEXT, 
                author_name TEXT,
                seller_id INTEGER,
                category_path TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                timestamp TEXT,
                price INTEGER,
                original_price INTEGER,
                discount_rate INTEGER,
                rating REAL,
                sold_count INTEGER,
                -- id is the surrogate primary key (easier to delete/update
                -- a single row by). This UNIQUE constraint still guarantees
                -- no duplicate snapshot for the same product at the same time.
                UNIQUE(product_id, timestamp),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)

        conn.commit()


def insert_snapshot(conn, product_data):
    """
    Insert one product's current data as a new price snapshot.

    Takes an existing connection (instead of opening its own) so a
    single scraper run can insert many products under one connection
    and commit once, rather than opening/closing per product.

    Does NOT commit — the caller decides when to commit (e.g. once per
    page), so it controls the transaction boundary.
    """
    cursor = conn.cursor()

    # Product info (name, url) can change over time on Tiki's side,
    # so this is treated as "latest known value", not immutable —
    # INSERT OR REPLACE overwrites the row if product_id already exists.
    cursor.execute("""
        INSERT OR REPLACE INTO products (product_id, name, url, author_name, seller_id, category_path) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        product_data.get("product_id"),
        product_data.get("name"),
        product_data.get("url"),
        product_data.get('author_name'),
        product_data.get('seller_id'),
        product_data.get('category_path')
    ))

    timestamp = datetime.now().isoformat(timespec="seconds")

    # Every call adds a brand new row here — this is the time-series
    # part of the schema, one row per (product, point in time).
    cursor.execute("""
        INSERT INTO price_snapshots (
            product_id, timestamp, price, original_price,
            discount_rate, rating, sold_count
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        product_data.get("product_id"),
        timestamp,
        product_data.get("price"),
        product_data.get("original_price"),
        product_data.get("discount_rate"),
        product_data.get("rating"),
        product_data.get("sold_count"),
    ))