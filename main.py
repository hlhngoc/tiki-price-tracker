from scraper.pipeline import run_scraper
from scheduler import start_schedule

if __name__ == "__main__":
    run_scraper()

    start_schedule()
