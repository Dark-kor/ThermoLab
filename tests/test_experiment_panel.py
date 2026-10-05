import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt6.QtWidgets import QApplication

from gui.widgets.experiment_panel import ExperimentPanel

from models.experiment import Experiment


app = QApplication(sys.argv)

panel = ExperimentPanel()

panel.resize(800, 120)

exp = Experiment(
    name="Prueba Simulador",
    operator="Diego López",
    source="simulator",
    sample_interval_ms=200
)

panel.set_experiment(exp)

panel.set_duration(12.6)

panel.set_state("Adquiriendo")

panel.show()

sys.exit(app.exec())