"""
toolbar.py
----------

Barra de herramientas principal de ThermoLab.
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QToolBar,
    QToolButton,
)
from PyQt6.QtGui import QAction


class MainToolBar(QToolBar):

    # ==================================================
    # Señales
    # ==================================================

    new_clicked = pyqtSignal()
    open_clicked = pyqtSignal()
    save_clicked = pyqtSignal()

    start_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()

    export_clicked = pyqtSignal()

    show_all_clicked = pyqtSignal()
    hide_all_clicked = pyqtSignal()

    channel_toggled = pyqtSignal(int, bool)

    # ==================================================

    def __init__(self, parent=None):

        super().__init__("Toolbar", parent)

        self.setMovable(False)

        self.channel_buttons = {}

        self.build_toolbar()

    # ==================================================

    def build_toolbar(self):

        # ------------------------------------------------
        # Archivo
        # ------------------------------------------------

        self.action_new = QAction("Nuevo", self)
        self.action_open = QAction("Abrir", self)
        self.action_save = QAction("Guardar", self)

        self.addAction(self.action_new)
        self.addAction(self.action_open)
        self.addAction(self.action_save)

        self.addSeparator()

        # ------------------------------------------------
        # Adquisición
        # ------------------------------------------------

        self.action_start = QAction("▶ Iniciar", self)
        self.action_pause = QAction("⏸ Pausar", self)
        self.action_stop = QAction("■ Detener", self)

        self.addAction(self.action_start)
        self.addAction(self.action_pause)
        self.addAction(self.action_stop)

        self.addSeparator()

        # ------------------------------------------------
        # Exportación
        # ------------------------------------------------

        self.action_export = QAction("CSV", self)

        self.addAction(self.action_export)

        self.addSeparator()

        # ------------------------------------------------
        # Mostrar / Ocultar
        # ------------------------------------------------

        self.action_show_all = QAction("Mostrar", self)
        self.action_hide_all = QAction("Ocultar", self)

        self.addAction(self.action_show_all)
        self.addAction(self.action_hide_all)

        self.addSeparator()

        # ------------------------------------------------
        # Canales
        # ------------------------------------------------

        for channel in range(1, 9):

            button = QToolButton()

            button.setText(f"CH{channel}")

            button.setCheckable(True)

            button.setChecked(True)

            button.setAutoRaise(True)

            button.setToolTip(
                f"Mostrar Canal {channel}"
            )

            button.toggled.connect(
                lambda checked, ch=channel:
                self.channel_toggled.emit(ch, checked)
            )

            self.channel_buttons[channel] = button

            self.addWidget(button)

        # ------------------------------------------------
        # Conexión señales
        # ------------------------------------------------

        self.action_new.triggered.connect(
            self.new_clicked.emit
        )

        self.action_open.triggered.connect(
            self.open_clicked.emit
        )

        self.action_save.triggered.connect(
            self.save_clicked.emit
        )

        self.action_start.triggered.connect(
            self.start_clicked.emit
        )

        self.action_pause.triggered.connect(
            self.pause_clicked.emit
        )

        self.action_stop.triggered.connect(
            self.stop_clicked.emit
        )

        self.action_export.triggered.connect(
            self.export_clicked.emit
        )

        self.action_show_all.triggered.connect(
            self.show_all_clicked.emit
        )

        self.action_hide_all.triggered.connect(
            self.hide_all_clicked.emit
        )

    # ==================================================
    # Utilidades
    # ==================================================

    def set_channel_checked(
        self,
        channel: int,
        checked: bool
    ):

        if channel not in self.channel_buttons:
            return

        button = self.channel_buttons[channel]

        button.blockSignals(True)

        button.setChecked(checked)

        button.blockSignals(False)

    # --------------------------------------------------

    def show_all_channels(self):

        for channel in self.channel_buttons:

            self.set_channel_checked(channel, True)

    # --------------------------------------------------

    def hide_all_channels(self):

        for channel in self.channel_buttons:

            self.set_channel_checked(channel, False)