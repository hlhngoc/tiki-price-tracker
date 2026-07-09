import sqlite3
import pandas as pd

from scraper.pipeline import run_scraper
from scheduler import start_schedule
from analysis.trends import most_volatile_products
from analysis.trends import price_history
from analysis.trends import price_drop_alert

if __name__ == "__main__":

    run_scraper()

    conn = sqlite3.connect("tiki.db")
    df = pd.read_sql("SELECT * FROM price_snapshots", conn)

    print(most_volatile_products(df))
    print(price_history(df, df['product_id'].unique()[0]))
    print(price_drop_alert(df, -10))

    start_schedule()
