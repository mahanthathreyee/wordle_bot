import multiprocessing
from typing import Callable

from util.singleton import Singleton
from constants.app_constants import *
from constants.multiprocess_constant import *

# Meant to be a singleton class
class ProcessPool(metaclass=Singleton):
    def __init__(self) -> None:
        self.n_process = JOB_POOL_PROCESS
        self._pool = multiprocessing.Pool(processes=self.n_process)
    
    def submit(self, func: Callable, params: list, starmap=False):
        if not starmap:
            job_result = self._pool.map_async(func, params)
        else:
            job_result = self._pool.starmap(func, params)

        return job_result
