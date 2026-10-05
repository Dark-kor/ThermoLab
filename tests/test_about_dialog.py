import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from PyQt6.QtWidgets import QApplication

from gui.dialogs.about_dialog import AboutDialog

app = QApplication(sys.argv)

dialog = AboutDialog()

dialog.show()

app.exec()