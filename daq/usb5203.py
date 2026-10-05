"""
usb5203.py
----------

Fuente real de adquisición de temperatura para ThermoLab
utilizando un Measurement Computing USB-5203.

La conversión del termopar Type K a °C es realizada por
la Universal Library de Measurement Computing mediante
cbTIn(). La configuración del tipo de termopar se toma
de la configuración realizada en InstaCal.
"""

from __future__ import annotations

import ctypes
from ctypes import (
    c_int,
    c_float,
    POINTER,
    byref,
)
from datetime import datetime
from pathlib import Path
from typing import List, Optional


from .base import TemperatureSource

from models.acquisition import AcquisitionFrame
from models.sensor import ChannelReading


class USB5203TemperatureSource(TemperatureSource):
    """
    Fuente de temperatura basada en un Measurement Computing
    USB-5203.

    El USB-5203 dispone de 8 canales de temperatura.

    La API utilizada es cbTIn() de cbw64.dll.
    """

    # ======================================================
    # Constantes
    # ======================================================

    DEFAULT_DLL_PATH = (
        r"C:\Program Files (x86)\Measurement Computing"
        r"\DAQ\cbw64.dll"
    )

    CHANNEL_COUNT = 8

    # Escala Celsius utilizada por cbTIn()
    CELSIUS = 0

    # Opciones por defecto
    OPTIONS = 0

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(
        self,
        board: int = 0,
        channels: int = 8,
        dll_path: Optional[str] = None,
    ):

        super().__init__(
            min(channels, self.CHANNEL_COUNT)
        )

        self.board = board

        self.dll_path = (
            dll_path
            if dll_path is not None
            else self.DEFAULT_DLL_PATH
        )

        self.dll = None

        self.sequence = 0

        self.start_time = None

        self._load_library()

        self._configure_functions()

    # ======================================================
    # Carga de DLL
    # ======================================================

    def _load_library(self):
        """
        Carga cbw64.dll.
        """

        dll = Path(self.dll_path)

        if not dll.exists():

            raise FileNotFoundError(
                "No se encontró cbw64.dll.\n\n"
                f"Ruta esperada:\n{self.dll_path}"
            )

        try:

            self.dll = ctypes.WinDLL(
                str(dll)
            )

        except OSError as error:

            raise RuntimeError(
                "No fue posible cargar cbw64.dll.\n\n"
                f"Ruta:\n{self.dll_path}\n\n"
                f"Error:\n{error}"
            ) from error

    # ======================================================
    # Configuración de funciones
    # ======================================================

    def _configure_functions(self):
        """
        Configura la firma ctypes de cbTIn().
        """

        self.dll.cbTIn.argtypes = [

            c_int,              # BoardNum

            c_int,              # Chan

            c_int,              # Scale

            POINTER(c_float),   # TempVal

            c_int               # Options
        ]

        self.dll.cbTIn.restype = c_int

    # ======================================================
    # Conexión
    # ======================================================

    def connect(self) -> bool:
        """
        Conecta lógicamente con el USB-5203.

        La conexión física ya es administrada por
        Measurement Computing / InstaCal.

        Returns
        -------
        bool
            True si la fuente está disponible.
        """

        try:

            # Verificamos que la DLL esté cargada.

            if self.dll is None:

                self._load_library()

                self._configure_functions()

            # Verificamos el primer canal configurado.
            #
            # No necesitamos que todos los canales tengan
            # un sensor conectado.

            temperature = c_float()

            status = self.dll.cbTIn(

                self.board,

                0,

                self.CELSIUS,

                byref(temperature),

                self.OPTIONS
            )

            # status == 0 significa que la llamada fue correcta.

            if status != 0:

                self.connected = False

                return False

            self.connected = True

            self.sequence = 0

            self.start_time = datetime.now()

            return True

        except Exception:

            self.connected = False

            return False

    # ======================================================
    # Desconexión
    # ======================================================

    def disconnect(self):
        """
        Desconecta lógicamente la fuente.
        """

        self.connected = False

        self.sequence = 0

        self.start_time = None

    # ======================================================
    # Lectura de un canal
    # ======================================================

    def _read_channel(
        self,
        channel: int
    ) -> ChannelReading:
        """
        Lee un canal individual del USB-5203.

        Parameters
        ----------
        channel:
            Canal físico del USB-5203, 0-7.

        Returns
        -------
        ChannelReading
        """

        temperature = c_float()

        status_code = self.dll.cbTIn(

            self.board,

            channel,

            self.CELSIUS,

            byref(temperature),

            self.OPTIONS
        )

        # --------------------------------------------------
        # Lectura correcta
        # --------------------------------------------------

        if status_code == 0:

            return ChannelReading(

                # ThermoLab utiliza canales 1-8
                channel=channel + 1,

                temperature=round(
                    temperature.value,
                    2
                ),

                valid=True,

                sensor_type="K",

                status="OK",

                message=""
            )

        # --------------------------------------------------
        # Canal sin sensor / lectura inválida
        # --------------------------------------------------

        return ChannelReading(

            channel=channel + 1,

            temperature=None,

            valid=False,

            sensor_type="K",

            status="Desconectado",

            message=(
                f"Error de lectura USB-5203 "
                f"(código {status_code})"
            )
        )

    # ======================================================
    # Adquisición
    # ======================================================

    def acquire(self) -> AcquisitionFrame:
        """
        Realiza una adquisición completa de los canales
        configurados.

        Returns
        -------
        AcquisitionFrame
        """

        if not self.connected:

            raise RuntimeError(
                "USB-5203 no conectado."
            )

        self.sequence += 1

        acquisition_time = datetime.now()

        if self.start_time is None:

            self.start_time = acquisition_time

        elapsed = (
            acquisition_time - self.start_time
        ).total_seconds()

        readings: List[ChannelReading] = []

        # --------------------------------------------------
        # Leer todos los canales
        # --------------------------------------------------

        for channel in range(self.channels):

            reading = self._read_channel(
                channel
            )

            readings.append(reading)

        # --------------------------------------------------
        # Crear frame
        # --------------------------------------------------

        return AcquisitionFrame(

            timestamp=acquisition_time,

            readings=readings,

            sequence=self.sequence,

            elapsed_time=elapsed
        )

    # ======================================================
    # Información
    # ======================================================

    def get_board_number(self) -> int:

        return self.board

    # --------------------------------------------------

    def get_dll_path(self) -> str:

        return self.dll_path