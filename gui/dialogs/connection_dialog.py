"""
connection_dialog.py
--------------------

Diálogo de configuración de conexión para ThermoLab.
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QRadioButton,
    QComboBox,
    QSpinBox,
    QCheckBox
)


class ConnectionDialog(QDialog):

    # -----------------------------------------------------

    def __init__(
        self,
        parent=None,
        configuration: dict | None = None
    ):

        super().__init__(parent)

        self.setWindowTitle("Configuración de conexión")

        self.setMinimumWidth(520)

        self.build_ui()

        if configuration is not None:

            self.load_configuration(configuration)

    # =====================================================
    # Construcción
    # =====================================================

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.addWidget(self.create_source_group())

        layout.addWidget(self.create_configuration_group())

        layout.addWidget(self.create_channels_group())

        layout.addWidget(self.create_status_group())

        layout.addLayout(self.create_buttons())

        self.update_controls()

    # =====================================================
    # Fuente
    # =====================================================

    def create_source_group(self):

        group = QGroupBox("Fuente de adquisición")

        layout = QVBoxLayout()

        self.rb_simulator = QRadioButton("Simulator")

        self.rb_usb = QRadioButton("MCC USB-5203")

        self.rb_simulator.setChecked(True)

        self.rb_simulator.toggled.connect(
            self.update_controls
        )

        self.rb_usb.toggled.connect(
            self.update_controls
        )

        layout.addWidget(self.rb_simulator)

        layout.addWidget(self.rb_usb)

        group.setLayout(layout)

        return group

    # =====================================================
    # Configuración
    # =====================================================

    def create_configuration_group(self):

        group = QGroupBox("Configuración")

        layout = QGridLayout()

        layout.addWidget(QLabel("Puerto"), 0, 0)

        self.cmb_port = QComboBox()

        self.cmb_port.addItems([
            "Automático",
            "USB-5203"
        ])

        layout.addWidget(self.cmb_port, 0, 1)

        layout.addWidget(QLabel("Intervalo (ms)"), 1, 0)

        self.spin_interval = QSpinBox()

        self.spin_interval.setRange(50, 5000)

        self.spin_interval.setSingleStep(50)

        self.spin_interval.setValue(200)

        layout.addWidget(self.spin_interval, 1, 1)

        group.setLayout(layout)

        return group

    # =====================================================
    # Canales
    # =====================================================

    def create_channels_group(self):

        group = QGroupBox("Canales habilitados")

        layout = QGridLayout()

        self.channel_checks = []

        for channel in range(8):

            checkbox = QCheckBox(f"Canal {channel+1}")

            checkbox.setChecked(True)

            self.channel_checks.append(checkbox)

            row = channel % 4

            column = channel // 4

            layout.addWidget(
                checkbox,
                row,
                column
            )

        group.setLayout(layout)

        return group

    # =====================================================
    # Estado
    # =====================================================

    def create_status_group(self):

        group = QGroupBox("Estado")

        layout = QGridLayout()

        layout.addWidget(QLabel("Fuente actual"), 0, 0)

        self.lbl_source = QLabel("---")

        layout.addWidget(self.lbl_source, 0, 1)

        layout.addWidget(QLabel("Estado"), 1, 0)

        self.lbl_status = QLabel("Desconectado")

        layout.addWidget(self.lbl_status, 1, 1)

        group.setLayout(layout)

        return group

    # =====================================================
    # Botones
    # =====================================================

    def create_buttons(self):

        layout = QHBoxLayout()

        layout.addStretch()

        btn_cancel = QPushButton("Cancelar")

        btn_connect = QPushButton("Aceptar")

        btn_cancel.clicked.connect(self.reject)

        btn_connect.clicked.connect(self.accept)

        layout.addWidget(btn_cancel)

        layout.addWidget(btn_connect)

        return layout

    # =====================================================
    # Configuración
    # =====================================================

    def load_configuration(self, config: dict):

        source = config.get("source", "simulator")

        if source == "simulator":

            self.rb_simulator.setChecked(True)

        else:

            self.rb_usb.setChecked(True)

        interval = config.get("interval", 200)

        self.spin_interval.setValue(interval)

        port = config.get("port", "Automático")

        index = self.cmb_port.findText(port)

        if index >= 0:

            self.cmb_port.setCurrentIndex(index)

        enabled = config.get(
            "channels",
            list(range(1, 9))
        )

        for i, checkbox in enumerate(self.channel_checks):

            checkbox.setChecked((i + 1) in enabled)

        self.update_controls()

    # =====================================================

    def update_controls(self):

        simulator = self.rb_simulator.isChecked()

        self.cmb_port.setEnabled(not simulator)

        self.lbl_source.setText(
            "Simulator"
            if simulator
            else "USB-5203"
        )

    # =====================================================

    def set_connection_status(
        self,
        connected: bool
    ):

        if connected:

            self.lbl_status.setText("Conectado")

        else:

            self.lbl_status.setText("Desconectado")

    # =====================================================

    def get_data(self):

        return {

            "source":
                "simulator"
                if self.rb_simulator.isChecked()
                else "usb5203",

            "port":
                self.cmb_port.currentText(),

            "interval":
                self.spin_interval.value(),

            "channels": [

                i + 1

                for i, checkbox

                in enumerate(self.channel_checks)

                if checkbox.isChecked()

            ]

        }