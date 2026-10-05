"""
acquisition_controller.py
-------------------------

Controlador principal de adquisición de ThermoLab.
"""

from __future__ import annotations

from typing import List, Optional

from core.config import (
    DEFAULT_SOURCE,
    MAX_HISTORY_POINTS,
)

from daq.factory import create_source

from models.acquisition import AcquisitionFrame
from models.experiment import Experiment


class AcquisitionController:

    # -----------------------------------------------------

    def __init__(
        self,
        source_type: str = DEFAULT_SOURCE
    ):

        # ============================================
        # Configuración
        # ============================================

        self.source_type = source_type

        self.sample_interval = 200

        self.enabled_channels = list(range(1, 9))

        self.port = "Automático"

        # ============================================
        # Fuente
        # ============================================

        self.source = create_source(source_type)

        self.connected = False

        # ============================================
        # Estado
        # ============================================

        self.running = False

        self.paused = False

        # ============================================
        # Historial
        # ============================================

        self.history: List[AcquisitionFrame] = []

        self.max_history = MAX_HISTORY_POINTS

        # ============================================
        # Experimento actual
        # ============================================

        self.current_session: Optional[Experiment] = None

    # =====================================================
    # CONFIGURACIÓN
    # =====================================================

    def configure(
        self,
        source: str | None = None,
        interval: int | None = None,
        channels: list[int] | None = None,
        port: str | None = None
    ):

        """
        Configura completamente la adquisición.
        """

        if source is not None:

            self.set_source(source)

        if interval is not None:

            self.sample_interval = interval

        if channels is not None:

            self.enabled_channels = channels.copy()

        if port is not None:

            self.port = port

        self.apply_configuration()

    # -----------------------------------------------------

    def configuration(self) -> dict:

        """
        Devuelve la configuración actual.
        """

        return {

            "source": self.source_type,

            "interval": self.sample_interval,

            "channels": self.enabled_channels.copy(),

            "port": self.port

        }

    # =====================================================
    # Fuente
    # =====================================================

    def set_source(self, source_type: str):

        if self.connected:

            self.disconnect()

        self.source_type = source_type

        self.source = create_source(source_type)

    # -----------------------------------------------------

    def set_interval(self, interval: int):

        self.sample_interval = interval

        if self.current_session is not None:
            self.current_session.sample_interval_ms = interval

    # -----------------------------------------------------

    def set_channels(self, channels: list[int]):

        self.enabled_channels = channels.copy()

        self.apply_configuration()

    # -----------------------------------------------------

    def set_port(self, port: str):

        self.port = port

        self.apply_configuration()

    # -----------------------------------------------------

    def apply_configuration(self):

        """
        Envía la configuración a la fuente de adquisición.

        El simulador actualmente ignora estos métodos.
        El USB5203 sí los implementará.
        """

        if hasattr(self.source, "set_interval"):

            self.source.set_interval(
                self.sample_interval
            )

        if hasattr(self.source, "set_channels"):

            self.source.set_channels(
                self.enabled_channels
            )

        if hasattr(self.source, "set_port"):

            self.source.set_port(
                self.port
            )

    # -----------------------------------------------------

    def connect(self) -> bool:

        if self.connected:

            return True

        self.connected = self.source.connect()

        return self.connected

    # -----------------------------------------------------

    def disconnect(self):

        if not self.connected:

            return

        self.source.disconnect()

        self.connected = False

        self.running = False

        self.paused = False

    # =====================================================
    # Experimento
    # =====================================================

    def new_experiment(self, **kwargs):


        """
        Crea un nuevo experimento.
        """

        if self.current_session is not None:

            self.current_session.finish()

        self.clear_history()
        self.running = False
        self.paused = False

        new_source = kwargs.get(
            "source",
            self.source_type
        )

        new_interval = kwargs.get(
            "sample_interval_ms",
            getattr(self, "sample_interval",200)
        )

        if new_source != self.source_type:
            self.set_source(new_source)
        self.source_type = new_source
        self.sample_interval = new_interval

        self.current_session = Experiment(

            name=kwargs.get(
                "name",
                "Nuevo experimento"
            ),

            operator=kwargs.get(
                "operator",
                ""
            ),

            description=kwargs.get(
                "description",
                ""
            ),

            notes=kwargs.get(
                "notes",
                ""
            ),

            source=self.source_type,

            sample_interval_ms=self.sample_interval

        )
        return self.current_session

    # =====================================================
    # Adquisición
    # =====================================================

    def acquire_once(self) -> AcquisitionFrame:

        if not self.connected:

            raise RuntimeError(

                "La fuente no está conectada."

            )

        frame = self.source.acquire()

        self.history.append(frame)

        if self.current_session is not None:

            self.current_session.add_frame(frame)

        if len(self.history) > self.max_history:

            self.history.pop(0)

        return frame

    # -----------------------------------------------------

    def read(self) -> Optional[AcquisitionFrame]:

        if not self.running:

            return None

        if self.paused:

            return None

        return self.acquire_once()

    # =====================================================
    # Estados
    # =====================================================

    def start(self):

        if not self.connected:

            if not self.connect():

                raise RuntimeError(

                    "No fue posible conectar la fuente."

                )

        if self.current_session is None:

            self.new_experiment()

        self.running = True

        self.paused = False

    # -----------------------------------------------------

    def pause(self):

        if not self.running:

            return

        self.paused = True

    # -----------------------------------------------------

    def resume(self):

        if not self.running:

            return

        self.paused = False

    # -----------------------------------------------------

    def stop(self):

        self.running = False

        self.paused = False

        if self.current_session is not None:

            self.current_session.finish()

        self.disconnect()

    # =====================================================
    # Historial
    # =====================================================

    def clear_history(self):

        self.history.clear()

    # -----------------------------------------------------

    def get_history(self) -> List[AcquisitionFrame]:

        return self.history

    # =====================================================
    # Propiedades
    # =====================================================

    @property
    def is_running(self):

        return self.running

    # -----------------------------------------------------

    @property
    def is_paused(self):

        return self.paused

    # -----------------------------------------------------

    @property
    def is_connected(self):

        return self.connected

    # -----------------------------------------------------

    @property
    def state(self):

        if not self.running:

            return "Detenido"

        if self.paused:

            return "Pausado"

        return "Adquiriendo"