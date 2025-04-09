import logging
from typing import List, Tuple, Any
from internal_state_module import InternalStateModule
from external_feedback_module import ExternalFeedbackModule
from randomness_module import RandomnessModule


class SafeAISystem:
    """Basic AI safety system"""

    def __init__(
            self,
            A: float = 1.0,
            B: float = 1.0,
            C: float = 1.0,
            initial_F: float = 1.0,
            safety_thresholds: Tuple[float, float] = (0.5, 1.5)
    ):
        # Weight and parameter settings
        self.A = A
        self.B = B
        self.C = C

        # Safety parameters
        self.safety_thresholds = safety_thresholds

        # System state
        self.F = initial_F
        self.t = 0
        self.history: List[float] = [initial_F]

        # Module initialization
        self.internal = InternalStateModule()
        self.external = ExternalFeedbackModule()
        self.randomness = RandomnessModule()

        # Logging setup
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.__class__.__name__)

    def iterate(self, x: Any) -> Tuple[float, float, float, float, float]:
        """Performs one iteration of the safety system"""

        # Retrieve values from modules
        f_value = self.internal.process(x, self.t)
        o_value = self.external.process(x, self.t)
        r_value = self.randomness.process(x, self.t)

        # Calculate multiplier
        multiplier = (f_value * self.A) * (o_value * self.B) * (r_value * self.C)

        # Update system state
        new_F = multiplier * self.F

        # Control system bounds
        min_threshold, max_threshold = self.safety_thresholds
        if new_F > max_threshold or new_F < min_threshold:
            correction_factor = 0.5
            new_F = self.F + (new_F - self.F) * correction_factor

        self.F = new_F
        self.t += 1
        self.history.append(self.F)

        return self.F, multiplier, f_value, o_value, r_value

    def simulate(self, x: Any, iterations: int = 10) -> None:
        """Simulates the system"""
        self.logger.info(f"Initial state F: {self.F}")

        for _ in range(iterations):
            F_new, multiplier, f_val, o_val, r_val = self.iterate(x)
            self.logger.info(
                f"Iteration {self.t}: "
                f"F = {F_new:.3f} "
                f"(multiplier = {multiplier:.3f}; "
                f"f={f_val:.3f}, o={o_val:.3f}, r={r_val:.3f})"
            )
