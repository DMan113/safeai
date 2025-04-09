import logging
from typing import Any


class BaseModule:
    """
    Base abstract class for system modules.
    """
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(self.name)

    def process(self, x: Any, t: int) -> float:
        """
        Abstract method for data processing. Must be implemented in subclasses.
        """
        raise NotImplementedError("Each module must implement its own process method.")
