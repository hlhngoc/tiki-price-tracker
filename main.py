import sqlite3
import time

from scraper.fetcher import fetch_listings
from scraper.storage import init_db, insert_snapshot


if __name__ == "__main__":
    init_db()

    with sqlite3.connect("tiki.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        page = 1
        max_pages = 20  # hard cap to avoid infinite loop if last_page is ever wrong

        while page <= max_pages:
            result = None
            for attempt in range(2):
                result = fetch_listings(8095, page)
                if result is not None:
                    break
                print(f"Failed to fetch page {page}. Retrying...")
                time.sleep(1)

            if result is None:
                print(f"Skipping page {page} due to repeated request errors.")
                page += 1
                continue

            products = result["products"]
            current_page = result["current_page"]
            last_page = result["last_page"]

            for product in products:
                insert_snapshot(conn, product)

            conn.commit()
            print(f"Page {current_page}/{last_page} done, {len(products)} products saved.")

            if current_page >= last_page:
                print("Reached last page.")
                break

            page += 1
            time.sleep(1)