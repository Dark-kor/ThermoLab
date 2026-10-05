"""
simulator.py
------------

Simulador de adquisición de temperatura.

Genera temperaturas realistas para desarrollar ThermoLab
sin necesidad del hardware USB-5203.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import random
from typing import List

from .base import TemperatureSource
from models.acquisition import AcquisitionFrame
from models.sensor import ChannelReading   


# ==========================================================
# Canal simulado
# ==========================================================

@dataclass
class SimulatedChannel:
    """
    Representa un canal de temperatura simulado.
    """

    channel: int

    current_temperature: float

    target_temperature: float

    response_speed: float

    noise_amplitude: float = 0.03

    sensor_type: str = "K"

    valid: bool = True

    status: str = "OK"

    message: str = ""

    # ------------------------------------------------------

    def update(self):

        delta = (
            self.target_temperature
            - self.current_temperature
        )

        self.current_temperature += (
            delta * self.response_speed
        )

        self.current_temperature += random.uniform(
            -self.noise_amplitude,
            self.noise_amplitude
        )

    # ------------------------------------------------------

    def get_reading(self) -> ChannelReading:

        return ChannelReading(

            channel=self.channel,

            temperature=round(
                self.current_temperature,
                2
            ),

            valid=self.valid,

            sensor_type=self.sensor_type,

            status=self.status,

            message=self.message
        )


# ==========================================================
# Fuente simulada
# ==========================================================

class SimulatorTemperatureSource(TemperatureSource):

    def __init__(self, channels: int = 8):

        super().__init__(channels)

        self.channels_state: List[SimulatedChannel] = []

        self.sequence = 0

        self.start_time = None

        for ch in range(channels):

            initial = random.uniform(24.0, 26.0)

            self.channels_state.append(

                SimulatedChannel(

                    channel=ch + 1,

                    current_temperature=initial,

                    target_temperature=initial,

                    response_speed=random.uniform(
                        0.03,
                        0.08
                    )
                )

            )

    # ------------------------------------------------------

    def connect(self) -> bool:

        self.connected = True

        self.sequence = 0

        self.start_time = datetime.now()

        return True

    # ------------------------------------------------------

    def disconnect(self):

        self.connected = False

        self.sequence = 0

        self.start_time = None

    # ------------------------------------------------------

    def acquire(self) -> AcquisitionFrame:

        if not self.connected:

            raise RuntimeError("Simulador no conectado.")
        
        self.sequence += 1

        acquisition_time = datetime.now()

        elapsed = (acquisition_time - self.start_time).total_seconds()
        readings = []

        for channel in self.channels_state:
            
            channel.update()

            readings.append(channel.get_reading())
        
        frame = AcquisitionFrame(timestamp=acquisition_time, readings=readings, sequence=self.sequence, elapsed_time=elapsed)
        return frame

    # ------------------------------------------------------

    def set_channel_target(
        self,
        channel: int,
        temperature: float
    ):

        if channel < 1 or channel > self.channels:

            raise ValueError("Canal inválido.")

        self.channels_state[
            channel - 1
        ].target_temperature = temperature

    # ------------------------------------------------------

    def set_all_targets(
        self,
        temperature: float
    ):

        for channel in self.channels_state:

            channel.target_temperature = temperature