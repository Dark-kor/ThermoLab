import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from gui.plots import TemperaturePlot

from daq.simulator import SimulatorTemperatureSource


app = QApplication(sys.argv)

plot = TemperaturePlot()

plot.resize(1000, 600)

plot.show()


daq = SimulatorTemperatureSource()

daq.connect()

daq.set_channel_target(1, 80)
daq.set_channel_target(2, 70)
daq.set_channel_target(3, 55)
daq.set_channel_target(4, 45)


def update():

    frame = daq.acquire()

    plot.update_frame(frame)


timer = QTimer()

timer.timeout.connect(update)

timer.start(200)


sys.exit(app.exec())