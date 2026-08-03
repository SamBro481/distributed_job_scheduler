import time

def execute_job(job):
    print(f"Executing Job {job.id} ({job.type})")

    time.sleep(5)

    print(f"Finished Job {job.id}")