import random
from typing import Any, Tuple
from base_module import BaseModule


class RandomnessModule(BaseModule):
    """
    Module for adding controlled randomness.
    """
    def __init__(self, randomness_range: Tuple[float, float] = (0.95, 1.05)):
        super().__init__("Randomness")
        self.randomness_range = randomness_range

    def process(self, x: Any, t: int) -> float:
        """
        Generates random data within the given range.
        """
        return random.uniform(*self.randomness_range)
