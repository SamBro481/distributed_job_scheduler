import time

from app.database.database import SessionLocal
from app.scheduler.enqueue_service import enqueue_due_jobs


def run_scheduler():
    while True:
        db = SessionLocal()

        try:
            jobs = enqueue_due_jobs(db)
            
            # print("Checking for jobs...")

            for job in jobs:
                print(f"Found Job: {job.id}")
        finally:
            db.close()

        time.sleep(1)


if __name__ == "__main__":
    run_scheduler()