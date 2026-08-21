from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, ForeignKey
from app.database.database import Base
from datetime import datetime, timezone


class JobStatus(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    ENQUEUED = "ENQUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    DLQ = "DLQ"
    

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, nullable=False)

    type = Column(String, nullable=False)

    payload = Column(JSONB, nullable=False)

    status = Column(
        SQLEnum(JobStatus),
        nullable=False,
        default=JobStatus.CREATED
    )

    priority = Column(
        Integer,
        nullable=False,
        default=0
    )

    retries = Column(
        Integer,
        nullable=False,
        default=0
    )

    max_retries = Column(
        Integer,
        nullable=False,
        default=3
    )


    run_at = Column(

        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)

    )

    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=True)

    error_message = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    started_at = Column(DateTime(timezone=True))

    finished_at = Column(DateTime(timezone=True))
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
