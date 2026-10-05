"""
statusbar.py
------------

Barra inferior de estado de ThermoLab.
"""

from PyQt6.QtWidgets import (
    QLabel,
    QStatusBar,
)

from PyQt6.QtCore import Qt


class MainStatusBar(QStatusBar):

    # --------------------------------------------------

    def __init__(self, parent=None):

        super().__init__(parent)

        self.build_ui()

    # --------------------------------------------------

    def build_ui(self):

        self.setSizeGripEnabled(True)

        # ================================================

        self.lbl_message = QLabel("Listo")

        self.lbl_message.setAlignment(
            Qt.AlignmentFlag.AlignLeft |
            Qt.AlignmentFlag.AlignVCenter
        )

        # ================================================

        self.lbl_source = QLabel("Fuente: ---")

        self.lbl_source.setMinimumWidth(170)

        self.lbl_source.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # ================================================

        self.lbl_connection = QLabel("Desconectado")

        self.lbl_connection.setMinimumWidth(130)

        self.lbl_connection.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # ================================================

        self.lbl_time = QLabel("Tiempo: 0.0 s")

        self.lbl_time.setMinimumWidth(120)

        self.lbl_time.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # ================================================

        self.lbl_frames = QLabel("Frames: 0")

        self.lbl_frames.setMinimumWidth(100)

        self.lbl_frames.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # ================================================

        self.addWidget(
            self.lbl_message,
            stretch=1
        )

        self.addPermanentWidget(self.lbl_source)

        self.addPermanentWidget(self.lbl_connection)

        self.addPermanentWidget(self.lbl_time)

        self.addPermanentWidget(self.lbl_frames)

    # ==================================================
    # Métodos públicos
    # ==================================================

    def set_message(self, text: str):

        self.lbl_message.setText(text)

        self.showMessage(text)

    # --------------------------------------------------

    def set_source(self, source: str):

        self.lbl_source.setText(f"Fuente: {source}")

    # --------------------------------------------------

    def set_connection(self, connected: bool):

        if connected:

            self.lbl_connection.setText("Conectado")

            self.lbl_connection.setStyleSheet(
                "color: green; font-weight: bold;"
            )

        else:

            self.lbl_connection.setText("Desconectado")

            self.lbl_connection.setStyleSheet(
                "color: red; font-weight: bold;"
            )

    # --------------------------------------------------

    def set_time(self, seconds: float):

        self.lbl_time.setText(
            f"Tiempo: {seconds:.1f} s"
        )

    # --------------------------------------------------

    def set_frames(self, frames: int):

        self.lbl_frames.setText(
            f"Frames: {frames}"
        )

    # --------------------------------------------------

    def reset(self):

        self.set_message("Listo")

        self.set_source("---")

        self.set_connection(False)

        self.set_time(0.0)

        self.set_frames(0)