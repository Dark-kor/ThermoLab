import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from PyQt6.QtWidgets import QApplication

from gui.widgets.control_panel import ControlPanel


def start():
    print("START")


def pause():
    print("PAUSE")


def stop():
    print("STOP")


def export():
    print("EXPORT")


app = QApplication(sys.argv)

panel = ControlPanel()

panel.start_clicked.connect(start)

panel.pause_clicked.connect(pause)

panel.stop_clicked.connect(stop)

panel.export_clicked.connect(export)

panel.resize(700, 80)

panel.show()

sys.exit(app.exec())