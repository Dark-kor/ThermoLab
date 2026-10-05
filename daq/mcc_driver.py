"""
mcc_driver.py
--------------

Driver de bajo nivel para dispositivos MCC utilizando ULDAQ.
"""

from __future__ import annotations

from uldaq import (
    InterfaceType,
    TInFlag,
    TempScale,
    get_daq_device_inventory,
    DaqDevice
)


class MCCDriver:
    """
    Driver de comunicación con dispositivos MCC.
    """

    # -----------------------------------------------------

    def __init__(self):

        self.device = None

        self.ai_device = None

    # -----------------------------------------------------

    def connect(self):

        """
        Busca y conecta automáticamente el primer dispositivo MCC.
        """

        devices = get_daq_device_inventory(
            InterfaceType.ANY
        )

        if not devices:

            raise RuntimeError(
                "No se encontró ningún dispositivo MCC."
            )

        descriptor = devices[0]

        self.device = DaqDevice(descriptor)

        self.device.connect()

        self.ai_device = self.device.get_ai_device()

    # -----------------------------------------------------

    def disconnect(self):

        if self.device:

            self.device.disconnect()

            self.device.release()

            self.device = None

            self.ai_device = None

    # -----------------------------------------------------

    @property
    def connected(self):

        return self.device is not None

    # -----------------------------------------------------

    def read_temperature(
        self,
        channel: int
    ) -> float:
        """
        Lee un canal de temperatura.

        Retorna grados Celsius.
        """

        if not self.connected:

            raise RuntimeError(
                "Dispositivo no conectado."
            )

        value = self.ai_device.t_in(
            channel,
            TempScale.CELSIUS,
            TInFlag.DEFAULT
        )

        return float(value)