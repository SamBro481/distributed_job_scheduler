import time
import os
from datetime import datetime, timedelta, timezone


from app.database.database import SessionLocal
from app.models.job import Job, JobStatus
from app.redis_client import redis_client
from app.workers.executor import execute_job


def run_worker():
    worker_name = os.getenv("WORKER_NAME", "WORKER")
    while True:
        print(f"{worker_name}: Waiting for jobs...")

        result = redis_client.brpop("job_queue")

        if result is None:
            continue

        _, job_id = result

        db = SessionLocal()

        try:
            job = db.query(Job).filter(Job.id == int(job_id)).first()

            if not job:
                continue
            
            
            print(f"{worker_name}: Picked Job {job.id}")
            job.status = JobStatus.RUNNING
            db.commit()
            
            try:
                execute_job(job, worker_name)
                
                job.status = JobStatus.COMPLETED
                db.commit()
            except Exception as e:
                print(f"{worker_name} Job {job.id} failed: {e}")
                
                job.retries += 1
                
                if job.retries < job.max_retries:
                    backoff = 2**job.retries
                    job.run_at = datetime.now(timezone.utc) + timedelta(seconds=backoff)
                    job.status = JobStatus.CREATED
                    
                    print({f"Retrying Job {job.id} ({job.retries}/{job.max_retries}) in {backoff} seconds"})
                
                else:
                    print(f"Moving Job {job.id} to DLQ")
                    
                    job.status = JobStatus.DLQ
                
                db.commit()
        finally:
            db.close()


if __name__ == "__main__":
    run_worker()