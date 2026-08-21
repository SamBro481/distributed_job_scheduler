import time

from app.database.database import SessionLocal
from app.scheduler.enqueue_service import enqueue_due_jobs
from datetime import datetime, timezone, timedelta
from app.database.database import SessionLocal
from app.models.worker import Worker, WorkerStatus
from app.models.job import Job, JobStatus

HEARTBEAT_TIMEOUT = 10

def check_dead_workers():

    db = SessionLocal()

    try:
        workers = (
            db.query(Worker)
            .filter(Worker.status == WorkerStatus.ACTIVE)
            .all()
        )

        now = datetime.now(timezone.utc)

        for worker in workers:
            if now - worker.last_heartbeat > timedelta(
                seconds=HEARTBEAT_TIMEOUT
            ):

                print(f"Worker {worker.worker_name} is dead")
                worker.status = WorkerStatus.DEAD
                jobs = (
                    db.query(Job)
                    .filter(
                        Job.worker_id == worker.id,
                        Job.status == JobStatus.RUNNING
                    )
                    .all()
                )

                for job in jobs:

                    print(f"Recovering Job {job.id}")
                    job.status = JobStatus.CREATED
                    job.worker_id = None

        db.commit()

    finally:
        db.close()



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


        check_dead_workers()
        time.sleep(1)


if __name__ == "__main__":
    run_scheduler()

