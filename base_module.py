import logging
from typing import Any

class BaseModule:
    """
    Базовий абстрактний клас для модулів системи.
    """
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(self.name)

    def process(self, x: Any, t: int) -> float:
        """
        Абстрактний метод обробки даних. Повинен бути реалізований у підкласах.
        """
        raise NotImplementedError("Кожен модуль має реалізувати власний метод process")
