from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.redis_client import redis_client

from app.models.job import Job
from app.models.job import JobStatus


def enqueue_due_jobs(db: Session):
    jobs = (
        db.query(Job)
        .filter(
            Job.status == JobStatus.CREATED,
            Job.run_at <= datetime.now(timezone.utc)
        )
        .all()
    )
    
    print("Checking for Jobs")

    for job in jobs:
        redis_client.lpush("job_queue", job.id)
        print(f"Pushed Job {job.id} to Redis")

        job.status = JobStatus.QUEUED

    db.commit()

    return jobs