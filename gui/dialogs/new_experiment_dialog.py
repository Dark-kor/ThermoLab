"""
new_experiment_dialog.py
------------------------

Diálogo para crear un nuevo experimento.
"""

from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QSpinBox,
    QPushButton,
    QGroupBox,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout
)


class NewExperimentDialog(QDialog):

    # --------------------------------------------------

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Nuevo Experimento")

        self.resize(520, 520)

        self.build_ui()

    # --------------------------------------------------

    def build_ui(self):

        main_layout = QVBoxLayout(self)

        # ==================================================
        # Información general
        # ==================================================

        group_info = QGroupBox("Información del Experimento")

        grid = QGridLayout()

        self.txt_name = QLineEdit()

        self.txt_name.setPlaceholderText(
            "Ej: Ensayo PT100 - Laboratorio"
        )

        self.txt_operator = QLineEdit()

        self.txt_operator.setPlaceholderText(
            "Nombre del operador"
        )

        self.txt_description = QTextEdit()

        self.txt_description.setMaximumHeight(80)

        grid.addWidget(QLabel("Nombre"), 0, 0)
        grid.addWidget(self.txt_name, 0, 1)

        grid.addWidget(QLabel("Operador"), 1, 0)
        grid.addWidget(self.txt_operator, 1, 1)

        grid.addWidget(QLabel("Descripción"), 2, 0)
        grid.addWidget(self.txt_description, 2, 1)

        group_info.setLayout(grid)

        # ==================================================
        # Configuración
        # ==================================================

        group_config = QGroupBox("Configuración de Adquisición")

        grid2 = QGridLayout()

        self.cmb_source = QComboBox()

        self.cmb_source.addItems([
            "Simulator",
            "USB5203"
        ])

        self.spin_interval = QSpinBox()

        self.spin_interval.setRange(50, 10000)

        self.spin_interval.setSingleStep(50)

        self.spin_interval.setValue(200)

        self.spin_interval.setSuffix(" ms")

        grid2.addWidget(QLabel("Fuente"), 0, 0)
        grid2.addWidget(self.cmb_source, 0, 1)

        grid2.addWidget(QLabel("Intervalo"), 1, 0)
        grid2.addWidget(self.spin_interval, 1, 1)

        group_config.setLayout(grid2)

        # ==================================================
        # Notas
        # ==================================================

        group_notes = QGroupBox("Notas")

        notes_layout = QVBoxLayout()

        self.txt_notes = QTextEdit()

        self.txt_notes.setPlaceholderText(
            "Observaciones del experimento..."
        )

        notes_layout.addWidget(self.txt_notes)

        group_notes.setLayout(notes_layout)

        # ==================================================
        # Botones
        # ==================================================

        buttons = QHBoxLayout()

        buttons.addStretch()

        self.btn_cancel = QPushButton("Cancelar")

        self.btn_accept = QPushButton("Aceptar")

        buttons.addWidget(self.btn_cancel)

        buttons.addWidget(self.btn_accept)

        # ==================================================

        main_layout.addWidget(group_info)

        main_layout.addWidget(group_config)

        main_layout.addWidget(group_notes)

        main_layout.addStretch()

        main_layout.addLayout(buttons)

        # ==================================================
        # Señales
        # ==================================================

        self.btn_cancel.clicked.connect(self.reject)

        self.btn_accept.clicked.connect(self.accept)

    # --------------------------------------------------

    def get_data(self):

        """
        Devuelve toda la configuración del experimento.
        """

        return {

            "name":
                self.txt_name.text().strip(),

            "operator":
                self.txt_operator.text().strip(),

            "description":
                self.txt_description.toPlainText().strip(),

            "source":
                self.cmb_source.currentText().lower(),

            "sample_interval_ms":
                self.spin_interval.value(),

            "notes":
                self.txt_notes.toPlainText().strip()

        }