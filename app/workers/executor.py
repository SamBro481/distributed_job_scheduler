import time

def execute_job(job):
    print(f"Executing Job {job.id} ({job.type})")

    time.sleep(5)
    
    # raise Exception("Intentional Failure")

    print(f"Finished Job {job.id}")