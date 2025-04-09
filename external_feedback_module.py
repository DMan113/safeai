import random
from typing import Any, List, Tuple
from base_module import BaseModule


class ExternalFeedbackModule(BaseModule):
    """
    Module for external feedback, taking into account various indicators.
    """
    def __init__(self, feedback_range: Tuple[float, float] = (0.9, 1.1)):
        super().__init__("ExternalFeedback")
        self.feedback_range = feedback_range
        self.feedback_history: List[float] = []

    def process(self, x: Any, t: int) -> float:
        """
        Evaluates external feedback and accumulates data.
        """
        feedback_value = random.uniform(*self.feedback_range)
        self.feedback_history.append(feedback_value)
        if len(self.feedback_history) > 10:
            self.feedback_history.pop(0)
        return feedback_value
