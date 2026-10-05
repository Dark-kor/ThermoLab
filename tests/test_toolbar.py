import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt6.QtWidgets import QApplication

from gui.toolbar import MainToolBar


app = QApplication(sys.argv)

toolbar = MainToolBar()

toolbar.show()

toolbar.new_clicked.connect(
    lambda: print("Nuevo")
)

toolbar.open_clicked.connect(
    lambda: print("Abrir")
)

toolbar.save_clicked.connect(
    lambda: print("Guardar")
)

toolbar.export_clicked.connect(
    lambda: print("Exportar")
)

sys.exit(app.exec())