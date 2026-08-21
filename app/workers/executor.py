import time

def execute_job(job, worker_name):
    print(f"{worker_name}: Executing Job {job.id} ({job.type})")

    time.sleep(5)
    
    # raise Exception("Intentional Failure")
    # time.sleep(15)

    print(f"{worker_name}: Finished Job {job.id}")