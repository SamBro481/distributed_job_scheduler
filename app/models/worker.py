from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from enum import Enum

from app.database.database import Base
import threading

class WorkerStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DEAD = "DEAD"
       

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True)
    worker_name = Column(String, unique=True, nullable=False)
    last_heartbeat = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    status = Column(
        String, 
        default = WorkerStatus.ACTIVE,
        nullable=False
    )

