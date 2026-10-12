from sqlalchemy.orm import Session

from app.models.job import Job
from app.schemas.job import JobCreate
from datetime import datetime, timezone


def create_job(db: Session, job: JobCreate) -> Job:    
    new_job = Job(
        type=job.type,
        payload=job.payload,
        priority=job.priority,
        run_at=job.run_at or datetime.now(timezone.utc),
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

def get_jobs(db: Session):
    return db.query(Job).order_by(Job.id.desc()).all()