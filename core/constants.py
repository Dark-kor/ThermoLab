"""
constants.py
------------

Constantes y enumeraciones globales de ThermoLab.
"""

from enum import Enum

# ==========================================================
# Información de la aplicación
# ==========================================================

APP_NAME = "THERMOLAB"

APP_VERSION = "1.0.0"

APP_AUTHOR = "Diego López y Carlos Betancur"

APP_DESCRIPTION = (
    "Software para adquisición y análisis "
    "de temperatura mediante DAQ USB-5203."
)

# ==========================================================
# DAQ
# ==========================================================

MAX_CHANNELS = 8

DEFAULT_SAMPLE_INTERVAL_MS = 200

DEFAULT_UNIT = "°C"

# ==========================================================
# Enumeraciones
# ==========================================================

class SourceType(Enum):

    SIMULATOR = "simulator"

    USB5203 = "usb5203"


class SensorType(Enum):

    TYPE_K = "K"

    PT100 = "PT100"


class ConnectionStatus(Enum):

    DISCONNECTED = 0

    CONNECTING = 1

    CONNECTED = 2

    ERROR = 3

CHANNEL_COLORS = [

    "#E53935",   # rojo

    "#1E88E5",   # azul

    "#43A047",   # verde

    "#FB8C00",   # naranja

    "#8E24AA",   # morado

    "#00ACC1",   # cyan

    "#6D4C41",   # café

    "#3949AB"    # índigo

]