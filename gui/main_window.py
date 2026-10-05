"""
main_window.py
--------------

Ventana principal de ThermoLab.
"""
from __future__ import annotations
import traceback
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QFileDialog,
)
from PyQt6.QtGui import QGuiApplication


from controllers.acquisition_controller import AcquisitionController
from storage.csv_writer import CSVWriter
from storage.project_writer import ProjectWriter
from storage.project_reader import ProjectReader
from gui.dashboard import Dashboard
from gui.toolbar import MainToolBar
from gui.statusbar import MainStatusBar
from gui.menubar import MainMenuBar
from gui.dialogs.new_experiment_dialog import NewExperimentDialog
from gui.dialogs.about_dialog import AboutDialog
from gui.dialogs.connection_dialog import ConnectionDialog

class MainWindow(QMainWindow):

    # --------------------------------------------------

    def __init__(self):

        super().__init__()

        self.setWindowTitle("ThermoLab")

        self.resize(1600, 900)

        self.setMinimumSize(1280, 720)

        screen = QGuiApplication.primaryScreen()
        geometry = screen.availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(geometry.center())
        self.move(frame.topLeft())

        if geometry.width() < 1500:
            self.showMaximized()

        # ==================================================
        # GUI
        # ==================================================

        self.dashboard = Dashboard()

        self.dashboard.setContentsMargins(8,8,8,8)

        self.setCentralWidget(self.dashboard)

        self.menu = MainMenuBar(self)

        self.setMenuBar(self.menu)

        self.toolbar = MainToolBar(self)

        self.addToolBar(self.toolbar)

        self.status = MainStatusBar(self)

        self.setStatusBar(self.status)

        # ==================================================
        # Backend
        # ==================================================

        self.controller = AcquisitionController()

        # ==================================================
        # Timer
        # ==================================================

        self.timer = QTimer(self)

        self.timer.setInterval(self.controller.sample_interval)

        # ==================================================

        self.create_connections()

        # Estado inicial de la interfaz
        self.dashboard.control_panel.set_stopped()

        self.update_application_state()

        self.status.showMessage("ThermoLab iniciado")

    # --------------------------------------------------

    def create_connections(self):

        self.connect_timer()

        self.connect_control_panel()

        self.connect_toolbar()

        self.connect_menubar()

    # --------------------------------------------------

    def connect_timer(self):

        self.timer.timeout.connect(
            self.update_acquisition
        )

    # --------------------------------------------------

    def update_timer_interval(self):

        self.timer.setInterval(
            self.controller.sample_interval
        )

    # --------------------------------------------------

    def connect_control_panel(self):

        panel = self.dashboard.control_panel

        panel.start_clicked.connect(
            self.on_start_clicked
        )

        panel.pause_clicked.connect(
            self.on_pause_clicked
        )

        panel.stop_clicked.connect(
            self.on_stop_clicked
        )

        panel.export_clicked.connect(
            self.on_export_clicked
        )

    # --------------------------------------------------

    def connect_toolbar(self):

        toolbar = self.toolbar

        toolbar.action_start.triggered.connect(
            self.on_start_clicked
        )

        toolbar.action_pause.triggered.connect(
            self.on_pause_clicked
        )

        toolbar.action_stop.triggered.connect(
            self.on_stop_clicked
        )

        toolbar.action_export.triggered.connect(
            self.on_export_clicked
        )

        toolbar.channel_toggled.connect(
            self.on_channel_toggled
        )

        toolbar.show_all_clicked.connect(
            self.on_show_all_channels
        )

        toolbar.hide_all_clicked.connect(
            self.on_hide_all_channels
        )

        toolbar.new_clicked.connect(
            self.on_new_experiment
        )

        toolbar.open_clicked.connect(
            self.on_open_project
        )

        toolbar.save_clicked.connect(
            self.on_save_project
        )

    # --------------------------------------------------

    def connect_menubar(self):

        menu = self.menu

        menu.export_clicked.connect(
            self.on_export_clicked
        )

        menu.channel_toggled.connect(
            self.on_channel_toggled
        )

        menu.show_all_clicked.connect(
            self.on_show_all_channels
        )

        menu.hide_all_clicked.connect(
            self.on_hide_all_channels
        )

        menu.autorange_clicked.connect(
            self.dashboard.temperature_plot.reset
        )

        menu.reset_plot_clicked.connect(
            self.dashboard.temperature_plot.clear
        )

        menu.new_clicked.connect(
            self.on_new_experiment
        )

        menu.about_clicked.connect(
            self.on_about
        )

        menu.open_clicked.connect(
            self.on_open_project
        )

        menu.save_clicked.connect(
            self.on_save_project
        )

        menu.connection_clicked.connect(
            self.on_connection_dialog
        )

    # ==================================================
    # Estado de la aplicación
    # ==================================================

    def update_application_state(self):

        # ------------Dashboard------------

        self.dashboard.set_state(
            self.controller.state
        )

        # ------------StatusBar------------

        self.status.set_message(
            self.controller.state
        )

        self.status.set_source(
            self.controller.source_type
        )

        self.status.set_connection(
            self.controller.connected
        )

        self.status.set_frames(
            len(self.controller.history)
        )
        if self.controller.current_session is not None:

            self.status.set_time(
                self.controller.current_session.duration)

        else:

            self.status.set_time(0)

            
    # ==================================================
    # ADQUISICIÓN
    # ==================================================

    def on_start_clicked(self):

        self.controller.start()

        if self.controller.current_session is not None:

            self.dashboard.set_experiment(
                self.controller.current_session
            )

        self.update_timer_interval()

        self.dashboard.control_panel.set_running()

        self.update_application_state()

        self.timer.start()

    # --------------------------------------------------

    def update_acquisition(self):

        frame = self.controller.read()

        if frame is None:

            return

        self.dashboard.update_frame(frame)

        self.update_application_state()

    # --------------------------------------------------

    def on_pause_clicked(self):

        if self.controller.is_paused:

            self.controller.resume()

            self.dashboard.control_panel.set_running()

        else:

            self.controller.pause()

            self.dashboard.control_panel.set_paused()

        self.update_application_state()

    # --------------------------------------------------

    def on_stop_clicked(self):

        self.timer.stop()

        self.controller.stop()

        self.dashboard.control_panel.set_stopped()

        self.update_application_state()

    # ==================================================
    # EXPORTACIÓN
    # ==================================================

    def on_export_clicked(self):

        experiment = self.controller.current_session

        if experiment is None:

            QMessageBox.warning(

                self,

                "Exportar",

                "No hay experimento para exportar."

            )

            return

        filename, _ = QFileDialog.getSaveFileName(

            self,

            "Exportar Experimento",

            "",

            "CSV Files (*.csv)"

        )

        if not filename:

            return

        try:

            writer = CSVWriter()

            writer.save(

                experiment,

                filename

            )

            self.status.set_message(

                f"Exportado: {Path(filename).name}"

            )

            QMessageBox.information(

                self,

                "Exportar",

                "Experimento exportado exitosamente."

            )

        except Exception as error:

            QMessageBox.critical(

                self,

                "Exportar",

                str(error)

            )

    # ==================================================
    # CANALES
    # ==================================================

    def on_channel_toggled(

        self,

        channel,

        checked

    ):

        if checked:

            self.dashboard.temperature_plot.show_channel(channel)

        else:

            self.dashboard.temperature_plot.hide_channel(channel)

        self.toolbar.set_channel_checked(

            channel,

            checked

        )

        self.menu.set_channel_checked(

            channel,

            checked

        )

    # --------------------------------------------------

    def on_show_all_channels(self):

        self.dashboard.temperature_plot.show_all()

        self.toolbar.show_all_channels()

        self.menu.show_all_channels()

        self.status.set_message(

            "Mostrando todos los canales"

        )

    # --------------------------------------------------

    def on_hide_all_channels(self):

        self.dashboard.temperature_plot.hide_all()

        self.toolbar.hide_all_channels()

        self.menu.hide_all_channels()

        self.status.set_message(

            "Ocultando todos los canales"

        )

    # ==================================================
    # ACERCA DE
    # ==================================================

    def on_about(self):
        """
        Muestra la informacion del software
        """

        dialog = AboutDialog(self)

        dialog.exec()

    # ---------------------------------------------------

    def closeEvent(self, event):

        if self.timer.isActive():

            self.timer.stop()

        self.controller.stop()

        self.status.set_message(

            "Cerrando ThermoLab..."

        )
        self.status.showMessage(
            "Cerrando ThermoLab..."
        )

        event.accept()

    # ==================================================
    # NUEVO EXPERIMENTO
    # ==================================================

    def on_new_experiment(self):

        # Si estaba adquiriendo detener primero

        if self.controller.is_running:

            reply = QMessageBox.question(

                self,

                "Nuevo experimento",

                "Hay una adquisición en curso.\n\n¿Desea detenerla y crear un nuevo experimento?"

            )

            if reply != QMessageBox.StandardButton.Yes:

                return

            self.on_stop_clicked()

        # --------------------------------------------

        dialog = NewExperimentDialog(self)

        if dialog.exec():

            data = dialog.get_data()

            # =====================================
            # Validacion
            # =====================================

            if not data["name"]:

                QMessageBox.warning(
                    self,
                    "Nuevo experimento",
                    "Debe ingresar un nombre para el experimento"
                )

                return

            self.controller.new_experiment(**data)

            exp = self.controller.current_session

            exp.operator = data["operator"]

            exp.description = data["description"]

            exp.notes = data["notes"]

            exp.sample_interval_ms = data["sample_interval_ms"]

            # Reiniciar interfaz

            self.dashboard.clear()

            self.dashboard.set_experiment(exp)

            self.dashboard.set_state("Listo")

            self.dashboard.control_panel.set_stopped()

            self.update_application_state()
    # ==================================================
    # PROYECTOS
    # ==================================================

    def on_save_project(self):

        experiment = self.controller.current_session

        if experiment is None:

            QMessageBox.warning(
                self,
                "Guardar proyecto",
                "No existe ningún experimento."
            )

            return

        filename, _ = QFileDialog.getSaveFileName(

            self,

            "Guardar proyecto",

            f"{experiment.name}.thl",

            "ThermoLab Project (*.thl)"

        )

        if not filename:

            return

        try:

            writer = ProjectWriter()

            writer.save(

                experiment,

                filename

            )

            self.status.set_message(

                f"Proyecto guardado: {Path(filename).name}"

            )

            QMessageBox.information(

                self,

                "Proyecto",

                "Proyecto guardado correctamente."

            )

        except Exception as error:

            QMessageBox.critical(

                self,

                "Proyecto",

                str(error)

            )    


    # --------------------------------------------------

    def on_open_project(self):

        filename, _= QFileDialog.getOpenFileName(

            self,
            "Abrir Proyecto",
            "",
            "Thermolab Project (*.thl)"
        ) 
        if not filename:
            return
        try:
            reader = ProjectReader()
            experiment = reader.load(filename)


            # --------------------------------------------
            
            self.controller.current_session = experiment
            self.controller.history = experiment.frames.copy()

            # --------------------------------------------

            self.dashboard.clear()
            self.dashboard.set_experiment(experiment)
            for frame in experiment.frames:
                self.dashboard.update_frame(frame)
            self.update_application_state()
            self.status.set_message(
                f"Proyecto cargado: {Path(filename).name}"
            )
        except Exception as error:

            traceback.print_exc()

            QMessageBox.critical(

                self,
                "Abrir Proyecto",
                traceback.format_exc()
            )
    def on_connection_dialog(self):

        dialog = ConnectionDialog(self)

        if dialog.exec():

            config = dialog.get_data()

            self.controller.set_source(
                config["source"]
            )

            self.controller.set_interval(
                config["interval"]
            )
            self.update_timer_interval()

            self.controller.set_channels(
                config["channels"]
            )

            self.status.set_source(
                config["source"]
            )

            self.status.set_message(
                "Configuración actualizada"
            )

    