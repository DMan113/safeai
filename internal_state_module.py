from typing import Tuple, Any
from base_module import BaseModule


class InternalStateModule(BaseModule):
    """Модуль внутрішнього стану з розширеною логікою"""

    def __init__(
            self,
            name: str = "InternalState",
            stability_range: Tuple[float, float] = (0.8, 1.2)
    ):
        super().__init__(name)
        self.stability_range = stability_range

    def process(self, x: Any, t: int) -> float:
        """
        Обчислення внутрішнього стану з урахуванням часу

        Args:
            x: Вхідні дані
            t: Поточний часовий крок

        Returns:
            float: Значення стану
        """
        base_value = random.uniform(*self.stability_range)
        time_factor = 1 + (t * 0.01)
        return base_value * time_factor
import random
from typing import Tuple, Any
from base_module import BaseModule

class InternalStateModule(BaseModule):
    """
    Модуль внутрішнього стану з налаштуванням стабільності.
    """
    def __init__(self, stability_range: Tuple[float, float] = (0.8, 1.2)):
        super().__init__("InternalState")
        self.stability_range = stability_range

    def process(self, x: Any, t: int) -> float:
        """
        Обробка внутрішнього стану із залежністю від часу.
        """
        base_value = random.uniform(*self.stability_range)
        time_factor = 1 + (t * 0.01)  # Легка залежність від часу.
        return base_value * time_factor
