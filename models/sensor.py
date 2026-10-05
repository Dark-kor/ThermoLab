"""
sensor.py
---------
Modelos relacionados con sensores de temperatura.   

"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

# ==========================================================
# Configuración del sensor
# ==========================================================

@dataclass(slots=True)
class Sensor:
    """
    Representa un sensor de temperatura.
    """

    channel: int

    name: str

    sensor_type: str = "K"

    unit: str = "°C"

    enabled: bool = True

# ==========================================================
# Lectura de un sensor
# ==========================================================

@dataclass(slots=True)
class ChannelReading:
    """
    Representa una lectura de un canal de temperatura.
    """

    channel: int

    temperature: Optional[float]

    valid: bool = True

    unit: str = "°C"

    sensor_type: str = "K"

    status: str = "OK"

    message: str = ""

    def __str__(self):
        
        if self.valid:

            return (f"Channel {self.channel}: {self.temperature} {self.unit}")
        
        return (f"Channel {self.channel}: "f"ERROR({self.message})") 