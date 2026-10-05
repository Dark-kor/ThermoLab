"""
channel_card.py
---------------

Widget reutilizable para mostrar un canal de temperatura.
"""

from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy
)

from PyQt6.QtCore import Qt

from PyQt6.QtGui import QFont


class ChannelCard(QFrame):

    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    WARNING = "warning"
    ERROR = "error"

    # -------------------------------------------------

    def __init__(self, channel: int, parent=None):

        super().__init__(parent)

        self.channel = channel

        self.build_ui()

        self.set_state(self.DISCONNECTED)

    # -------------------------------------------------

    def build_ui(self):

        self.setFrameShape(QFrame.Shape.StyledPanel)

        self.setFrameShadow(QFrame.Shadow.Raised)

        self.setMinimumSize(160, 120)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)


        # --------------------------------------------

        self.title = QLabel(f"Canal {self.channel}")

        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_font = QFont()

        title_font.setBold(True)

        title_font.setPointSize(10)

        self.title.setFont(title_font)

        # --------------------------------------------

        self.temperature = QLabel("--.-- °C")

        temp_font = QFont()

        temp_font.setPointSize(18)

        temp_font.setBold(True)

        self.temperature.setFont(temp_font)

        self.temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.temperature.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # --------------------------------------------

        self.sensor = QLabel("Sensor : ---")

        self.sensor.setWordWrap(True)

        self.sensor.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Minimum
        )

        self.sensor.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # --------------------------------------------

        self.status = QLabel("Desconectado")
        
        self.status.setWordWrap(True)
        
        self.status.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Minimum
        )
        

        self.status.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # --------------------------------------------

        layout.addWidget(self.title)

        layout.addWidget(
            self.temperature,
            stretch=1
        )

        layout.addWidget(self.sensor)

        layout.addWidget(self.status)

    # -------------------------------------------------

    def update_reading(self, reading):

        if reading.valid and reading.temperature is not None:
            self.temperature.setText(
                f"{reading.temperature:.2f}°C"
            )
            self.sensor.setText(
                f"Sensor: {reading.sensor_type}"
            )
            self.status.setText(
                "Adquiriendo"
            )
            self.set_state(self.CONNECTED)
        else:
            self.temperature.setText(
                "--.-- °C"
            )
            self.sensor.setText(
                f"Sensor : {reading.sensor_type}"
            )
            self.status.setText(
                reading.status
            )
            if reading.status == "Desconectado":
                self.set_state(self.DISCONNECTED)
            else:
                self.set_state(self.WARNING)




    # -------------------------------------------------

    def set_state(self, state: str):

        if state == self.CONNECTED:

            color = "#2ecc71"

            background = "#1d3b29"

            text = "Adquiriendo"

        elif state == self.WARNING:

            color = "#f1c40f"

            background = "#4a3d12"

            text = "Advertencia"

        elif state == self.ERROR:

            color = "#e74c3c"

            background = "#4a1f1f"

            text = "Error"

        else:

            color = "#95a5a6"

            background = "#2b2b2b"

            text = "Desconectado"

        self.status.setText(text)

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {background};
                border: 2px solid {color};
                border-radius: 8px;
            }}

            QLabel {{
                color: white;
                border: none;
                background: transparent;
            }}
        """)

    # -------------------------------------------------

    def reset(self):

        self.temperature.setText("--.-- °C")

        self.sensor.setText("Sensor : ---")

        self.set_state(self.DISCONNECTED)

    # -------------------------------------------------

    def clear(self):

        self.reset()