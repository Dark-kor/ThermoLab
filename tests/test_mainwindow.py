import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))

from PyQt6.QtWidgets import QApplication

from gui.main_window import MainWindow


app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec())