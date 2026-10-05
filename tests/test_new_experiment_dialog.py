import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt6.QtWidgets import QApplication

from gui.dialogs.new_experiment_dialog import NewExperimentDialog

app = QApplication(sys.argv)

dialog = NewExperimentDialog()

dialog.show()

app.exec()