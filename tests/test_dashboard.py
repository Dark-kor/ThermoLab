import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from PyQt6.QtWidgets import QApplication

from gui.dashboard import Dashboard


app = QApplication(sys.argv)

window = Dashboard()

window.show()

sys.exit(app.exec())