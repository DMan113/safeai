import random
import logging
import numpy as np
from typing import List, Tuple, Any, Dict
from safe_ai_system import SafeAISystem


class AdvancedSafeAISystem(SafeAISystem):
    """
    Розширена система безпеки ШІ із гнучкими стратегіями корекції.
    """

    def __init__(self, *args, correction_strategies: Dict = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_F = self.F  # Ініціалізація початкового стану
        self.correction_strategies = correction_strategies or {
            'aggressive': {'threshold': 1.5, 'correction_factor': 0.3, 'log_level': logging.WARNING},
            'moderate': {'threshold': 1.2, 'correction_factor': 0.2, 'log_level': logging.INFO},
            'gentle': {'threshold': 1.1, 'correction_factor': 0.1, 'log_level': logging.DEBUG}
        }
        self.risk_metrics = {'total_volatility': 0, 'max_deviation': 0, 'correction_count': 0}
        self.volatility_history: List[float] = []

    def _select_correction_strategy(self, multiplier: float) -> Dict:
        """
        Вибір стратегії корекції на основі множника.
        """
        for name, strategy in sorted(self.correction_strategies.items(), key=lambda x: x[1]['threshold'], reverse=True):
            if multiplier > strategy['threshold']:
                return strategy
        return self.correction_strategies['gentle']

    def _advanced_correction(self, new_F: float, multiplier: float):
        """
        Розширений механізм корекції із використанням адаптивного коефіцієнта.
        """
        strategy = self._select_correction_strategy(multiplier)
        delta = new_F - self.F
        L = 0.3  # Порогова величина для м'яких корекцій
        effective_cf = strategy['correction_factor'] * (L / (L + abs(delta)))
        corrected_F = self.F + (delta * effective_cf)

        # Логування інформації про корекцію
        self.logger.log(
            strategy['log_level'],
            f"Корекція ({strategy['threshold']}): {self.F:.3f} -> {corrected_F:.3f} "
            f"(multiplier={multiplier:.3f}, effective_cf={effective_cf:.3f})"
        )

        # Оновлення метрик ризику
        self.risk_metrics['correction_count'] += 1
        self.risk_metrics['max_deviation'] = max(self.risk_metrics['max_deviation'], abs(delta))
        return corrected_F

    def iterate(self, x: Any):
        """
        Виконує одну ітерацію системи, розраховує множник та корекцію.
        """
        internal_factor = random.uniform(0.8, 1.2)
        external_factor = random.uniform(0.9, 1.1)
        randomness_factor = random.uniform(0.95, 1.05)
        multiplier = internal_factor * external_factor * randomness_factor
        new_F = self.F * multiplier

        # Перевірка та застосування корекцій
        if new_F > self.safety_thresholds[1] or new_F < self.safety_thresholds[0]:
            new_F = self._advanced_correction(new_F, multiplier)

        self.F = new_F
        self.history.append(self.F)
        self.volatility_history.append(abs(self.F - self.initial_F))
        self.risk_metrics['total_volatility'] = np.std(self.volatility_history)
        return self.F, multiplier

    def simulate(self, x: Any, iterations: int = 50):
        """
        Симуляція роботи системи із адаптивною корекцією.
        """
        self.logger.info(f"Початковий стан F: {self.F}")
        for _ in range(iterations):
            F_new, multiplier = self.iterate(x)
            self.logger.info(
                f"Ітерація {self.t}: F = {F_new:.3f} (multiplier = {multiplier:.3f})"
            )

        # Вивід фінальних метрик ризику
        self.logger.info("Підсумкові метрики ризику:")
        for metric, value in self.risk_metrics.items():
            self.logger.info(f"{metric}: {value:.4f}")
