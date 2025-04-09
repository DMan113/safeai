import logging
from advanced_safe_ai_system import AdvancedSafeAISystem


def main():
    """
    Main function to run the simulation of the advanced AI safety system
    with optimized corrections and visualization.
    """
    safe_ai = AdvancedSafeAISystem(
        initial_F=1.0,
        safety_thresholds=(0.5, 2.0),
        correction_strategies={
            'super_aggressive': {
                'threshold': 2.0,
                'correction_factor': 0.5,
                'log_level': logging.CRITICAL
            },
            'aggressive': {
                'threshold': 1.5,
                'correction_factor': 0.3,
                'log_level': logging.WARNING
            },
            'moderate': {
                'threshold': 1.2,
                'correction_factor': 0.2,
                'log_level': logging.INFO
            },
            'gentle': {
                'threshold': 1.1,
                'correction_factor': 0.1,
                'log_level': logging.DEBUG
            }
        }
    )

    safe_ai.simulate(x="default", iterations=30)
    safe_ai.plot_history()

if __name__ == "__main__":
    main()
