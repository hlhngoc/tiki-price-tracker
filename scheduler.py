import time
import schedule

from scraper.pipeline import run_scraper

def start_schedule():
    schedule.every(3).hours.do(run_scraper)

    while True:
        schedule.run_pending()
        time.sleep(60)