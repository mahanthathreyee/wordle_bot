import math

from .job_pool import ProcessPool

def generate_jobs(data: list, items_per_job: int) -> list[list]:
    n_items = len(data)
    n_jobs = math.ceil(n_items / items_per_job)

    job_items = [None] * n_jobs
    for i in range(n_jobs):
        start_idx = i * items_per_job
        end_idx = start_idx + items_per_job
        
        job_items[i] = data[start_idx : end_idx]

    return job_items
