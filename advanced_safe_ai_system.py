import random
import logging
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Any, Dict
from safe_ai_system import SafeAISystem


class AdvancedSafeAISystem(SafeAISystem):
    """
    Advanced AI safety system with flexible correction strategies and
    analysis of F rate of change for more adaptive adjustments.
    """

    def __init__(self, *args, correction_strategies: Dict = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_F = self.F  # Save the initial value of F
        self.correction_strategies = correction_strategies or {
            'aggressive': {'threshold': 1.5, 'correction_factor': 0.3, 'log_level': logging.WARNING},
            'moderate': {'threshold': 1.2, 'correction_factor': 0.2, 'log_level': logging.INFO},
            'gentle': {'threshold': 1.1, 'correction_factor': 0.1, 'log_level': logging.DEBUG}
        }
        self.risk_metrics = {'total_volatility': 0, 'max_deviation': 0, 'correction_count': 0}
        self.volatility_history: List[float] = []
        self.rate_history: List[float] = []

    def calculate_rate_of_change(self, window: int = 5) -> float:
        """
        Calculates the average rate of change of F for the last "window" iterations.
        If the history is insufficient, returns 0.
        """
        if len(self.history) < window + 1:
            return 0.0
        recent_changes = [self.history[i + 1] - self.history[i] for i in range(-window - 1, -1)]
        rate = np.mean(recent_changes)
        self.rate_history.append(rate)
        return rate

    def _select_correction_strategy(self, multiplier: float) -> Dict:
        """
        Selects a correction strategy based on the multiplier magnitude.
        """
        for name, strategy in sorted(self.correction_strategies.items(), key=lambda x: x[1]['threshold'], reverse=True):
            if multiplier > strategy['threshold']:
                return strategy
        return self.correction_strategies['gentle']

    def _advanced_correction(self, new_F: float, multiplier: float) -> float:
        """
        Advanced correction mechanism considering deviation strength and F rate of change.

        Args:
            new_F: Computed new value of F.
            multiplier: State change multiplier.

        Returns:
            Corrected value of F.
        """
        strategy = self._select_correction_strategy(multiplier)
        delta = new_F - self.F
        L = 0.3  # Base threshold for soft corrections
        rate = abs(self.calculate_rate_of_change(window=3))  # average rate of change for last 3 iterations
        effective_cf = strategy['correction_factor'] * (L / (L + abs(delta))) * (1 / (1 + rate))
        corrected_F = self.F + (delta * effective_cf)

        self.logger.log(
            strategy['log_level'],
            f"Correction ({strategy['threshold']}): {self.F:.3f} -> {corrected_F:.3f} "
            f"(multiplier={multiplier:.3f}, delta={delta:.3f}, rate={rate:.3f}, effective_cf={effective_cf:.3f})"
        )
        self.risk_metrics['correction_count'] += 1
        self.risk_metrics['max_deviation'] = max(self.risk_metrics['max_deviation'], abs(delta))
        return corrected_F

    def iterate(self, x: Any) -> Tuple[float, float]:
        """
        Performs one iteration of the system's operation.

        Args:
            x: Input data.

        Returns:
            Tuple containing the new value of F and the multiplier.
        """
        internal_factor = random.uniform(0.8, 1.2)
        external_factor = random.uniform(0.9, 1.1)
        randomness_factor = random.uniform(0.95, 1.05)
        multiplier = internal_factor * external_factor * randomness_factor
        new_F = self.F * multiplier

        if new_F > self.safety_thresholds[1] or new_F < self.safety_thresholds[0]:
            new_F = self._advanced_correction(new_F, multiplier)

        self.F = new_F
        self.history.append(self.F)
        self.volatility_history.append(abs(self.F - self.initial_F))
        self.risk_metrics['total_volatility'] = np.std(self.volatility_history)
        self.t += 1
        return self.F, multiplier

    def simulate(self, x: Any, iterations: int = 50) -> None:
        """
        Simulates the system's operation for the specified number of iterations.
        """
        self.logger.info(f"Initial state F: {self.F:.3f}")
        for _ in range(iterations):
            F_new, multiplier = self.iterate(x)
            self.logger.info(
                f"Iteration {self.t}: F = {F_new:.3f} (multiplier = {multiplier:.3f})"
            )
        self.logger.info("Final risk metrics:")
        for metric, value in self.risk_metrics.items():
            self.logger.info(f"{metric}: {value:.4f}")

    def plot_history(self) -> None:
        """
        Builds plots for F history and its volatility.
        """
        iterations_F = list(range(len(self.history)))
        iterations_vol = list(range(1, len(self.history)))
        plt.figure(figsize=(12, 6))

        plt.subplot(2, 1, 1)
        plt.plot(iterations_F, self.history, marker='o', label='F')
        plt.title('F Value History')
        plt.xlabel('Iteration')
        plt.ylabel('F')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(iterations_vol, self.volatility_history, marker='x', color='red', label='Volatility')
        plt.title('Volatility (|F - Initial F|)')
        plt.xlabel('Iteration')
        plt.ylabel('Volatility')
        plt.legend()

        plt.tight_layout()
        plt.show()
