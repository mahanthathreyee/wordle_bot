import math
import multiprocessing
from typing import Callable

from util.singleton import Singleton
from constants.app_constants import *

# Meant to be a singleton class
class JobPool(metaclass=Singleton):
    def __init__(self) -> None:
        self.n_process = JOB_POOL_PROCESS
        self._pool = multiprocessing.Pool(processes=self.n_process)
    
    def submit(self, func: Callable, params: list, starmap=False):
        if not starmap:
            job_result = self._pool.imap_unordered(func, params)
        else:
            job_result = self._pool.starmap(func, params)

        return job_result

def generate_jobs(data: list, items_per_job: int) -> list[list]:
    n_items = len(data)
    n_jobs = math.ceil(n_items / items_per_job)

    job_items = [None] * n_jobs
    for i in range(n_jobs):
        start_idx = i * items_per_job
        end_idx = start_idx + items_per_job
        
        job_items[i] = data[start_idx : end_idx]

    return job_items
