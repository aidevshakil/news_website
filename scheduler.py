import time
import datetime
from src.crew.main_crew import run_news_bot

SIX_HOURS_IN_SECONDS = 6 * 60 * 60

def start_scheduler():
    print("==========================================================")
    print("⏰ Starting 6-Hour Automated Local Cron Scheduler")
    print("Press Ctrl+C to stop the scheduler.")
    print("==========================================================")

    while True:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[Scheduler {now_str}] Triggering 6-hour news sync pipeline...")
        try:
            results = run_news_bot(topics=["AI", "Tech", "Crypto", "Finance"])
            print(f"[Scheduler {now_str}] Sync complete!")
        except Exception as e:
            print(f"[Scheduler {now_str}] Error during scheduled sync: {e}")

        print(f"\nSleeping for 6 hours... Next run at: {(datetime.datetime.now() + datetime.timedelta(seconds=SIX_HOURS_IN_SECONDS)).strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(SIX_HOURS_IN_SECONDS)

if __name__ == "__main__":
    start_scheduler()
