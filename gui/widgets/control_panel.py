"""
control_panel.py
----------------

Panel de control de adquisición para ThermoLab.
"""

from PyQt6.QtCore import pyqtSignal

from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
)


class ControlPanel(QWidget):
    """
    Panel con los controles principales del sistema.
    """

    start_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    export_clicked = pyqtSignal()

    # --------------------------------------------------

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self.build_ui()

    # --------------------------------------------------

    def build_ui(self):

        layout = QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(12)

        # =================================================

        self.start_button = QPushButton("▶ Iniciar")

        self.pause_button = QPushButton("⏸ Pausar")

        self.stop_button = QPushButton("■ Detener")

        self.export_button = QPushButton("📄 Exportar CSV")

        buttons = [

            self.start_button,

            self.pause_button,

            self.stop_button,

            self.export_button

        ]

        for button in buttons:

            button.setMinimumHeight(40)

            button.setMinimumWidth(120)

            button.setSizePolicy(

                QSizePolicy.Policy.Expanding,

                QSizePolicy.Policy.Fixed

            )

        # =================================================

        layout.addWidget(self.start_button)

        layout.addWidget(self.pause_button)

        layout.addWidget(self.stop_button)

        layout.addStretch(1)

        layout.addWidget(self.export_button)

        self.setLayout(layout)

        self.connect_signals()

        self.set_stopped()

    # --------------------------------------------------

    def connect_signals(self):

        self.start_button.clicked.connect(
            self.start_clicked.emit
        )

        self.pause_button.clicked.connect(
            self.pause_clicked.emit
        )

        self.stop_button.clicked.connect(
            self.stop_clicked.emit
        )

        self.export_button.clicked.connect(
            self.export_clicked.emit
        )

    # --------------------------------------------------

    def set_running(self):

        self.start_button.setEnabled(False)

        self.pause_button.setEnabled(True)

        self.stop_button.setEnabled(True)

    # --------------------------------------------------

    def set_stopped(self):

        self.start_button.setEnabled(True)

        self.pause_button.setEnabled(False)

        self.stop_button.setEnabled(False)

    # --------------------------------------------------

    def set_paused(self):

        self.start_button.setEnabled(True)

        self.pause_button.setEnabled(False)

        self.stop_button.setEnabled(True)