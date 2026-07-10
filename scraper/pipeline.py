import logging
import sqlite3
import time
from .fetcher import fetch_listings
from .storage import init_db, insert_snapshot

# Configure logging to save to a file and capture info-level logs or higher
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("scraper.log"),
    ]
)

def run_scraper():
    logging.info("Starting scraper run...")
    init_db()

    with sqlite3.connect("tiki.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        page = 1

        while True:
            result = None
            for attempt in range(2):
                result = fetch_listings(8322, page)
                if result is not None:
                    break
                logging.error(f"Failed to fetch page {page}. Retrying...")
                time.sleep(1)

            if result is None:
                logging.error(f"Failed to load page {page} after retries. Stopping.")
                break

            products = result["products"]
            current_page = result["current_page"]
            last_page = result["last_page"]

            for product in products:
                try:
                    insert_snapshot(conn, product)
                except sqlite3.IntegrityError:
                    logging.warning(f"Skipping duplicate snapshot for product {product.get('product_id')}")

            conn.commit()
            logging.info(f"Page {current_page}/{last_page} done, {len(products)} products saved.")

            if current_page >= last_page:
                logging.info("Reached last page.")
                break

            page += 1
            time.sleep(1)

