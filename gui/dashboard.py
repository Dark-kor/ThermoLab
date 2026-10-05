"""
dashboard.py
------------

Ventana principal del Dashboard de ThermoLab.
Organiza todos los widgets de la aplicación.
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QScrollArea,
    QSizePolicy
)
from PyQt6.QtCore import Qt

from gui.plots import TemperaturePlot
from gui.widgets.channel_card import ChannelCard
from gui.widgets.control_panel import ControlPanel
from gui.widgets.experiment_panel import ExperimentPanel


class Dashboard(QWidget):

    # --------------------------------------------------

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("ThermoLab")

        self.resize(1400, 900)

        self.experiment_panel = ExperimentPanel()

        self.control_panel = ControlPanel()

        self.temperature_plot = TemperaturePlot()

        # Altura mínima de la gráfica
        self.temperature_plot.setMinimumHeight(420)

        self.temperature_plot.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.channel_cards = []

        self.build_ui()

    # --------------------------------------------------

    def build_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(12,12,12,12)

        main_layout.setSpacing(12)

        # =====================================================
        # Información del experimento
        # =====================================================

        main_layout.addWidget(
            self.experiment_panel,
            stretch=0
        )

        # =====================================================
        # Panel de control
        # =====================================================

        main_layout.addWidget(
            self.control_panel,
            stretch=0
        )

        # =====================================================
        # Gráfica
        # =====================================================

        main_layout.addWidget(
            self.temperature_plot,
            stretch=5
        )

        # =====================================================
        # Tarjetas de canales
        # =====================================================

        grid = QGridLayout()

        grid.setSpacing(12)

        for channel in range(8):

            card = ChannelCard(channel + 1)

            self.channel_cards.append(card)

            row = channel // 4

            col = channel % 4

            grid.addWidget(card, row, col)

        cards_widget = QWidget()

        cards_widget.setLayout(grid)

        cards_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        scroll.setWidget(cards_widget)
        scroll.setMinimumHeight(220)
        main_layout.addWidget(
            scroll,
            stretch=2
        )
        main_layout.setStretch(0,0)
        main_layout.setStretch(1,0)
        main_layout.setStretch(2,6)
        main_layout.setStretch(3,2)
        self.setLayout(main_layout)

    # --------------------------------------------------

    def reset(self):

        self.temperature_plot.reset()

        for card in self.channel_cards:

            card.reset()

    # --------------------------------------------------

    def clear(self):

        self.temperature_plot.clear()

        for card in self.channel_cards:

            card.reset()

    # --------------------------------------------------

    def update_frame(self, frame):

        """
        Actualiza todos los widgets utilizando un AcquisitionFrame.
        """

        # Actualizar tarjetas

        for reading in frame.readings:

            index = reading.channel - 1

            if 0 <= index < len(self.channel_cards):

                self.channel_cards[index].update_reading(reading)
        # Actualizar grafica
        try:
            self.temperature_plot.update_frame(frame)
        except Exception as e:
            print(
                f"[ERROR GRAFICA] {type(e).__name__}: {e}"
            )

        # Actualizar duración

        self.experiment_panel.set_duration(
            frame.elapsed_time
        )

    # --------------------------------------------------

    def set_state(self, state: str):

        self.experiment_panel.set_state(state)

    # --------------------------------------------------

    def set_experiment(self, experiment):

        self.experiment_panel.set_experiment(experiment)