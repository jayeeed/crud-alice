from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import httpx

scheduler = BackgroundScheduler()


def ping_health_check():
    urls = [
        "https://crud-alice.onrender.com/",
        "https://n8n-vl1r.onrender.com/",
        "https://landcraft-be.onrender.com/",
        "https://expense-tracker-llm-zm78.onrender.com/",
    ]

    for url in urls:
        try:
            response = httpx.get(url)
            print(f"Health check for {url}: {response.status_code}")
        except Exception as e:
            print(f"Health check failed for {url}: {e}")


# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    ping_health_check,
    trigger=IntervalTrigger(minutes=10),
    id="health_check_job",
    replace_existing=True,
)


def health_start():
    """Start the health check scheduler."""
    scheduler.start()
    print("Health check scheduler started.")


def health_stop():
    """Stop the health check scheduler."""
    scheduler.shutdown()
    print("Health check scheduler stopped.")
