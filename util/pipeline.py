import logging
from typing import Callable, Any

log = logging.getLogger()

class Pipeline:
    def __init__(self, steps: list[Callable[[Any], Any]]) -> None:
        self._steps = steps

    def run(self, input: Any = None) -> Any:
        params = input

        for step in self._steps:
            params = step(params)
        return params
