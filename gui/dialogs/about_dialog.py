"""
about_dialog.py
---------------

Ventana "Acerca de ThermoLab".
"""

from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout
)

from PyQt6.QtCore import Qt

from PyQt6.QtGui import QFont

from core.constants import (
    APP_NAME,
    APP_VERSION,
    APP_AUTHOR
)


class AboutDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Acerca de")

        self.setFixedSize(450, 380)

        self.build_ui()

    # ------------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setSpacing(15)

        layout.setContentsMargins(20,20,20,20)

        # ==================================================

        title = QLabel(APP_NAME)

        font = QFont()

        font.setPointSize(18)

        font.setBold(True)

        title.setFont(font)

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ==================================================

        subtitle = QLabel(
            "Sistema de adquisición de temperatura"
        )

        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ==================================================

        version = QLabel(
            f"Versión: {APP_VERSION}"
        )

        version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ==================================================

        author = QLabel(
            f"Autor:\n{APP_AUTHOR}"
        )

        author.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ==================================================

        university = QLabel(
            "Ingeniería Mecatrónica\nITM"
        )

        university.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ==================================================

        description = QLabel(

            "ThermoLab permite adquirir, visualizar\n"
            "y exportar datos de temperatura\n"
            "desde el simulador o un dispositivo\n"
            "MCC USB-5203."

        )

        description.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        description.setWordWrap(True)

        # ==================================================

        close_btn = QPushButton("Cerrar")

        close_btn.clicked.connect(self.accept)

        # ==================================================

        layout.addWidget(title)

        layout.addWidget(subtitle)

        layout.addWidget(version)

        layout.addWidget(author)

        layout.addWidget(university)

        layout.addStretch()

        layout.addWidget(description)

        layout.addStretch()

        layout.addWidget(close_btn)

        self.setLayout(layout)