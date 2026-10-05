"""
experiment_panel.py
-------------------

Panel de información del experimento.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QGroupBox,
    QVBoxLayout,
    QSizePolicy,
)

from PyQt6.QtCore import Qt


class ExperimentPanel(QWidget):
    """
    Panel que muestra el estado del experimento actual.
    """

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

        group = QGroupBox("Información del Experimento")

        group.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        layout = QGridLayout()

        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(6)

        # ==================================================
        # Primera fila
        # ==================================================

        self.lbl_name = QLabel("-")
        self.lbl_operator = QLabel("-")
        self.lbl_state = QLabel("Detenido")

        # ==================================================
        # Segunda fila
        # ==================================================

        self.lbl_source = QLabel("-")
        self.lbl_sensor = QLabel("-")
        self.lbl_interval = QLabel("-")

        # ==================================================
        # Tercera fila
        # ==================================================

        self.lbl_duration = QLabel("0.0 s")
        self.lbl_samples = QLabel("0")
        self.lbl_export = QLabel("-")

        # ==================================================
        # Cuarta fila
        # ==================================================

        self.lbl_file = QLabel("-")

        # ==================================================
        # Ajustes de comportamiento
        # ==================================================

        self.lbl_sensor.setWordWrap(True)
        self.lbl_export.setWordWrap(True)
        self.lbl_file.setWordWrap(True)

        self.lbl_sensor.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        self.lbl_export.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        self.lbl_file.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        self.lbl_file.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        # ==================================================
        # Alineación uniforme
        # ==================================================

        for label in [

            self.lbl_name,
            self.lbl_operator,
            self.lbl_state,

            self.lbl_source,
            self.lbl_sensor,
            self.lbl_interval,

            self.lbl_duration,
            self.lbl_samples,
            self.lbl_export,

            self.lbl_file

        ]:

            label.setAlignment(
                Qt.AlignmentFlag.AlignLeft |
                Qt.AlignmentFlag.AlignVCenter
            )

        # ==================================================
        # Construcción del Grid
        # ==================================================

        layout.addWidget(QLabel("Nombre"), 0, 0)
        layout.addWidget(self.lbl_name, 0, 1)

        layout.addWidget(QLabel("Operador"), 0, 2)
        layout.addWidget(self.lbl_operator, 0, 3)

        layout.addWidget(QLabel("Estado"), 0, 4)
        layout.addWidget(self.lbl_state, 0, 5)

        # -----------------------------------------------

        layout.addWidget(QLabel("Fuente"), 1, 0)
        layout.addWidget(self.lbl_source, 1, 1)

        layout.addWidget(QLabel("Sensor"), 1, 2)
        layout.addWidget(self.lbl_sensor, 1, 3)

        layout.addWidget(QLabel("Intervalo"), 1, 4)
        layout.addWidget(self.lbl_interval, 1, 5)

        # -----------------------------------------------

        layout.addWidget(QLabel("Duración"), 2, 0)
        layout.addWidget(self.lbl_duration, 2, 1)

        layout.addWidget(QLabel("Muestras"), 2, 2)
        layout.addWidget(self.lbl_samples, 2, 3)

        layout.addWidget(QLabel("Exportación"), 2, 4)
        layout.addWidget(self.lbl_export, 2, 5)

        # -----------------------------------------------

        layout.addWidget(QLabel("Archivo"), 3, 0)
        layout.addWidget(self.lbl_file, 3, 1, 1, 5)

        # ==================================================
        # Las columnas de datos ocupan el espacio sobrante
        # ==================================================

        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(5, 1)

        group.setLayout(layout)

        # ==================================================
        # Layout principal
        # ==================================================

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(group)

        self.setLayout(main_layout)

    # --------------------------------------------------

    def set_experiment(self, experiment):

        self.lbl_name.setText(experiment.name)

        self.lbl_operator.setText(experiment.operator)

        self.lbl_source.setText(experiment.source.title())

        self.lbl_interval.setText(
            f"{experiment.sample_interval_ms} ms"
        )

        if experiment.sensor_types:

            self.lbl_sensor.setText(
                ", ".join(experiment.sensor_types)
            )

        else:

            self.lbl_sensor.setText("-")

    # --------------------------------------------------

    def set_duration(self, seconds: float):

        self.lbl_duration.setText(
            f"{seconds:.1f} s"
        )

    # --------------------------------------------------

    def set_state(self, state: str):

        self.lbl_state.setText(state)

    # --------------------------------------------------

    def set_sample_count(self, samples: int):

        self.lbl_samples.setText(str(samples))

    # --------------------------------------------------

    def set_export_directory(self, directory: str):

        self.lbl_export.setText(directory)

    # --------------------------------------------------

    def set_filename(self, filename: str):

        self.lbl_file.setText(filename)

    # --------------------------------------------------

    def clear(self):

        self.lbl_name.setText("-")
        self.lbl_operator.setText("-")
        self.lbl_source.setText("-")
        self.lbl_sensor.setText("-")
        self.lbl_interval.setText("-")
        self.lbl_duration.setText("0.0 s")
        self.lbl_samples.setText("0")
        self.lbl_export.setText("-")
        self.lbl_file.setText("-")
        self.lbl_state.setText("Detenido")