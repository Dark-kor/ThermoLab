"""
plots.py
---------

Widget de gráficas en tiempo real para ThermoLab.
"""

from __future__ import annotations

from typing import Dict

import numpy as np
import pyqtgraph as pg

from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QSizePolicy

from core.constants import CHANNEL_COLORS
from models.acquisition import AcquisitionFrame


class TemperaturePlot(QWidget):
    """
    Widget encargado de mostrar las temperaturas de todos
    los canales en tiempo real.
    """

    # --------------------------------------------------

    def __init__(self, parent=None):

        super().__init__(parent)

        self.plot_widget = pg.PlotWidget()

        self.plot_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.setMinimumSize(500,300)

        self.curves: Dict[int, pg.PlotDataItem] = {}

        self.history: dict[int, dict[str, list[float]]] = {}

        self.max_points = 1000

        self.window_seconds = 30

        self.build_ui()

        self.configure_plot()

        self.create_curves()

    # --------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(0)

        layout.addWidget(
            self.plot_widget,
            stretch=1
        )

        self.setLayout(layout)

    # --------------------------------------------------

    def configure_plot(self):

        plot = self.plot_widget

        plot.setClipToView(True)

        plot.setDownsampling(mode="peak")

        plot.setMouseEnabled(
            x=True,
            y=True
        )
        plot.setMenuEnabled(False)

        plot.setBackground("w")

        plot.showGrid(
            x=True,
            y=True,
            alpha=0.18
        )

        plot.setTitle(
            "Temperaturas en Tiempo Real"
        )

        plot.setLabel(
            "left",
            "Temperatura (°C)"
        )

        plot.setLabel(
            "bottom",
            "Tiempo (s)"
        )

        plot.addLegend()

        plot.enableAutoRange(
            x=True,
            y=True
        )

    # --------------------------------------------------

    def create_curves(self):

        for channel in range(1, 9):

            color = CHANNEL_COLORS[channel - 1]

            curve = self.plot_widget.plot(

                [],

                [],

                pen=pg.mkPen(
                    color=color,
                    width=2
                ),

                name=f"CH{channel}"
            )

            self.curves[channel] = curve

            self.history[channel] = {

                "x": [],

                "y": []
            }

    # --------------------------------------------------

    def update_frame(
        self,
        frame: AcquisitionFrame
    ) -> None:
        """
        Actualiza la gráfica utilizando un AcquisitionFrame.
        """

        tiempo = float(frame.elapsed_time)

        for reading in frame.readings:

            canal = int(reading.channel)

            # Validar canal
            if canal not in self.history:
                continue
            #Ignorar lecturas invalidads
            if not reading.valid:
                continue
            if reading.temperature is None:
                continue
            #Convertir explicitamente a float
            temperatura = float(reading.temperature)
            #Guardar Historial
            self.history[canal]["x"].append(tiempo)
            self.history[canal]["y"].append(temperatura)
            #Limitar cantidad de puntos
            if len(self.history[canal]["x"]) > self.max_points:
                self.history[canal]["x"].pop(0)
                self.history[canal]["y"].pop(0)
            #Convertir a arrays Numpy float64
            x_data = np.asarray(
                self.history[canal]["x"],
                dtype=np.float64
            )
            y_data = np.asarray(
                self.history[canal]["y"],
                dtype = np.float64
            )
            #Actualizar curva
            self.curves[canal].setData(
                x=x_data,
                y=y_data
            )
        if tiempo > self.window_seconds:
            self.plot_widget.setXRange(
                tiempo - self.window_seconds,
                tiempo,
                padding=0.02
            )

    # --------------------------------------------------
    

    def show_channel(
        self,
        channel: int
    ) -> None:
        """
        Muestra un canal.
        """

        if channel in self.curves:

            self.curves[channel].show()


    # --------------------------------------------------

    def hide_channel(
        self,
        channel: int
    ) -> None:
        """
        Oculta un canal.
        """

        if channel in self.curves:

            self.curves[channel].hide()


    # --------------------------------------------------

    def show_all(self):

        for curve in self.curves.values():

            curve.show()


    # --------------------------------------------------

    def hide_all(self):
        
        for curve in self.curves.values():

            curve.hide()

    # --------------------------------------------------

    def clear(self) -> None:
        """
        Borra todas las curvas.
        """

        for channel in self.history:

            self.history[channel]["x"].clear()

            self.history[channel]["y"].clear()

            self.curves[channel].setData([], [])

    # --------------------------------------------------

    def reset(self) -> None:
        """
        Reinicia completamente la gráfica.
        """

        self.clear()

        self.plot_widget.enableAutoRange(
            x=True,
            y=True
        )

    # --------------------------------------------------

    def set_title(
        self,
        title: str
    ) -> None:

        self.plot_widget.setTitle(title)

    # --------------------------------------------------

    def set_max_points(
        self,
        points: int
    ) -> None:

        self.max_points = max(10, points)

    # --------------------------------------------------

    def set_window_seconds(
        self,
        seconds: int
    ) -> None:

        self.window_seconds = max(5, seconds)