from datetime import datetime, timezone
from app.models.worker import Worker, WorkerStatus


def send_heartbeat(db, worker_name):
    worker = (
        db.query(Worker)
        .filter(Worker.worker_name == worker_name)
        .first()
    )

    if not worker:
        worker = Worker(worker_name=worker_name)
        db.add(worker)

    worker.status = WorkerStatus.ACTIVE
    worker.last_heartbeat = datetime.now(timezone.utc)

    db.commit()