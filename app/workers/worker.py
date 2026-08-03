import time

from app.database.database import SessionLocal
from app.models.job import Job, JobStatus
from app.redis_client import redis_client
from app.workers.executor import execute_job


def run_worker():
    while True:
        print("Waiting for jobs...")

        result = redis_client.brpop("job_queue")

        if result is None:
            continue

        _, job_id = result

        db = SessionLocal()

        try:
            job = db.query(Job).filter(Job.id == int(job_id)).first()

            if not job:
                continue

            job.status = JobStatus.RUNNING
            db.commit()
            
            try:
                execute_job(job)
                
                job.status = JobStatus.COMPLETED
                db.commit()
            except Exception as e:
                print(f"Job {job.id} failed: {e}")
                
                job.retries += 1
                
                if job.retries < job.max_retries:
                    print({f"Retrying Job {job.id} ({job.retries}/{job.max_retries})"})
                    
                    job.status = JobStatus.CREATED
                
                else:
                    print(f"Moving Job {job.id} to DLQ")
                    
                    job.status = JobStatus.DLQ
                
                db.commit()
        finally:
            db.close()


if __name__ == "__main__":
    run_worker()