"""
menubar.py
----------

Barra de menús principal de ThermoLab.
"""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal

from PyQt6.QtGui import QAction

from PyQt6.QtWidgets import QMenuBar


class MainMenuBar(QMenuBar):

    # =====================================================
    # Señales Archivo
    # =====================================================

    new_clicked = pyqtSignal()

    open_clicked = pyqtSignal()

    save_clicked = pyqtSignal()

    export_clicked = pyqtSignal()

    connection_clicked = pyqtSignal()

    # =====================================================
    # Señales Ayuda
    # =====================================================

    about_clicked = pyqtSignal()

    # =====================================================
    # Señales Vista
    # =====================================================

    show_all_clicked = pyqtSignal()

    hide_all_clicked = pyqtSignal()

    reset_plot_clicked = pyqtSignal()

    autorange_clicked = pyqtSignal()

    channel_toggled = pyqtSignal(int, bool)

    # =====================================================

    def __init__(self, parent=None):

        super().__init__(parent)

        self.channel_actions = {}

        self.build_menus()

    # =====================================================

    def build_menus(self):

        self.build_file_menu()

        self.build_view_menu()

        self.build_help_menu()

    # =====================================================
    # Archivo
    # =====================================================

    def build_file_menu(self):

        file_menu = self.addMenu("Archivo")

        self.action_new = QAction("Nuevo", self)

        self.action_open = QAction("Abrir", self)

        self.action_save = QAction("Guardar", self)

        self.action_connection = QAction(
            "Conexión...",
            self
        )

        self.action_export = QAction(
            "Exportar CSV",
            self
        )

        file_menu.addAction(self.action_new)

        file_menu.addAction(self.action_open)

        file_menu.addAction(self.action_save)

        file_menu.addSeparator()

        file_menu.addAction(self.action_connection)

        file_menu.addAction(self.action_export)

        self.action_new.triggered.connect(
            self.new_clicked.emit
        )

        self.action_open.triggered.connect(
            self.open_clicked.emit
        )

        self.action_save.triggered.connect(
            self.save_clicked.emit
        )

        self.action_connection.triggered.connect(
            self.connection_clicked.emit
        )

        self.action_export.triggered.connect(
            self.export_clicked.emit
        )

    # =====================================================
    # Ver
    # =====================================================

    def build_view_menu(self):

        view_menu = self.addMenu("Ver")

        # -----------------------------------------

        self.action_show_all = QAction(
            "Mostrar todos",
            self
        )

        self.action_hide_all = QAction(
            "Ocultar todos",
            self
        )

        self.action_reset_plot = QAction(
            "Restaurar gráfica",
            self
        )

        self.action_autorange = QAction(
            "Autoescala",
            self
        )

        view_menu.addAction(
            self.action_show_all
        )

        view_menu.addAction(
            self.action_hide_all
        )

        view_menu.addSeparator()

        # -----------------------------------------
        # Canales
        # -----------------------------------------

        for channel in range(1, 9):

            action = QAction(
                f"Canal {channel}",
                self
            )

            action.setCheckable(True)

            action.setChecked(True)

            action.toggled.connect(

                lambda checked,
                ch=channel:

                self.channel_toggled.emit(
                    ch,
                    checked
                )

            )

            self.channel_actions[channel] = action

            view_menu.addAction(action)

        view_menu.addSeparator()

        view_menu.addAction(
            self.action_autorange
        )

        view_menu.addAction(
            self.action_reset_plot
        )

        # -----------------------------------------

        self.action_show_all.triggered.connect(
            self.show_all_clicked.emit
        )

        self.action_hide_all.triggered.connect(
            self.hide_all_clicked.emit
        )

        self.action_reset_plot.triggered.connect(
            self.reset_plot_clicked.emit
        )

        self.action_autorange.triggered.connect(
            self.autorange_clicked.emit
        )

    # =====================================================
    # Ayuda
    # =====================================================

    def build_help_menu(self):

        help_menu = self.addMenu("Ayuda")

        self.action_about = QAction(
            "Acerca de ThermoLab",
            self
        )

        help_menu.addAction(
            self.action_about
        )

        self.action_about.triggered.connect(
            self.about_clicked.emit
        )

    # =====================================================
    # Utilidades
    # =====================================================

    def set_channel_checked(
        self,
        channel: int,
        checked: bool
    ):

        if channel not in self.channel_actions:

            return

        action = self.channel_actions[channel]

        action.blockSignals(True)

        action.setChecked(checked)

        action.blockSignals(False)

    # =====================================================

    def show_all_channels(self):

        for channel in self.channel_actions:

            self.set_channel_checked(
                channel,
                True
            )

    # =====================================================

    def hide_all_channels(self):

        for channel in self.channel_actions:

            self.set_channel_checked(
                channel,
                False
            )