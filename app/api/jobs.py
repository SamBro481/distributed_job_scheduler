from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import create_job, get_jobs

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post(
    "/",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_job(
    job: JobCreate,
    db: Session = Depends(get_db),
):
    return create_job(db, job)


@router.get("/", response_model=list[JobResponse])
def get_all_jobs(db: Session = Depends(get_db)):
    return get_jobs(db)