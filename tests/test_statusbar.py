import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow
)

from gui.statusbar import MainStatusBar


app = QApplication(sys.argv)

window = QMainWindow()

status = MainStatusBar()

window.setStatusBar(status)

status.set_status("Adquiriendo")

status.set_source("Simulator")

status.set_frames(120)

window.resize(700,150)

window.show()

sys.exit(app.exec())