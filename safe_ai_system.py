import logging
from typing import List, Tuple, Any
from internal_state_module import InternalStateModule
from external_feedback_module import ExternalFeedbackModule
from randomness_module import RandomnessModule


class SafeAISystem:
    """Базова система безпеки ШІ"""

    def __init__(
            self,
            A: float = 1.0,
            B: float = 1.0,
            C: float = 1.0,
            initial_F: float = 1.0,
            safety_thresholds: Tuple[float, float] = (0.5, 1.5)
    ):
        # Налаштування ваг та параметрів
        self.A = A
        self.B = B
        self.C = C

        # Параметри безпеки
        self.safety_thresholds = safety_thresholds

        # Стан системи
        self.F = initial_F
        self.t = 0
        self.history: List[float] = [initial_F]

        # Ініціалізація модулів
        self.internal = InternalStateModule()
        self.external = ExternalFeedbackModule()
        self.randomness = RandomnessModule()

        # Налаштування логування
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.__class__.__name__)

    def iterate(self, x: Any) -> Tuple[float, float, float, float, float]:
        """Виконання однієї ітерації системи безпеки"""

        # Отримання значень від модулів
        f_value = self.internal.process(x, self.t)
        o_value = self.external.process(x, self.t)
        r_value = self.randomness.process(x, self.t)

        # Розрахунок множника
        multiplier = (f_value * self.A) * (o_value * self.B) * (r_value * self.C)

        # Оновлення стану системи
        new_F = multiplier * self.F

        # Контроль меж системи
        min_threshold, max_threshold = self.safety_thresholds
        if new_F > max_threshold or new_F < min_threshold:
            # М'яке обмеження стрибків стану
            correction_factor = 0.5
            new_F = self.F + (new_F - self.F) * correction_factor

        self.F = new_F
        self.t += 1
        self.history.append(self.F)

        return self.F, multiplier, f_value, o_value, r_value

    def simulate(self, x: Any, iterations: int = 10) -> None:
        """Симуляція роботи системи"""
        self.logger.info(f"Початковий стан F: {self.F}")

        for _ in range(iterations):
            F_new, multiplier, f_val, o_val, r_val = self.iterate(x)
            self.logger.info(
                f"Ітерація {self.t}: "
                f"F = {F_new:.3f} "
                f"(multiplier = {multiplier:.3f}; "
                f"f={f_val:.3f}, o={o_val:.3f}, r={r_val:.3f})"
            )
