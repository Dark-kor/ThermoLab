"""
experiment.py
-------------

Modelo que representa un experimento o sesión de adquisición
de ThermoLab.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Any

from models.acquisition import AcquisitionFrame


@dataclass
class Experiment:
    """
    Representa un experimento completo.
    """

    # ======================================================
    # Información general
    # ======================================================

    name: str = "Nuevo experimento"

    operator: str = ""

    description: str = ""

    sensor_types: List[str] = field(default_factory=list)

    source: str = ""

    sample_interval_ms: int = 200

    # ======================================================
    # Tiempo
    # ======================================================

    start_time: datetime = field(default_factory=datetime.now)

    end_time: Optional[datetime] = None

    # ======================================================
    # Datos
    # ======================================================

    frames: List[AcquisitionFrame] = field(default_factory=list)

    # ======================================================
    # Observaciones
    # ======================================================

    notes: str = ""

    # ------------------------------------------------------

    def add_frame(
        self,
        frame: AcquisitionFrame
    ) -> None:
        """Agrega una adquisición."""

        self.frames.append(frame)
        self.update_sensor_types()

    # ------------------------------------------------------

    def clear(self) -> None:
        """Elimina todas las adquisiciones."""

        self.frames.clear()
        self.sensor_types.clear()
        self.end_time = None
        self.start_time = datetime.now()

    # ------------------------------------------------------

    def finish(self) -> None:
        """Marca el experimento como finalizado."""

        self.end_time = datetime.now()

    # ------------------------------------------------------

    def metadata(self) -> dict[str, Any]:
        """
        Devuelve la información general del experimento.
        """

        return {

            "Nombre": self.name,

            "Operador": self.operator,

            "Descripción": self.description,

            "Fuente": self.source.title() if self.source else "Desconocida",

            "Sensores": ", ".join(self.sensor_types),

            "Intervalo (ms)": self.sample_interval_ms,

            "Fecha inicio": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),

            "Fecha fin": self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else "",

            "Duración (s)": round(self.duration, 3),

            "Total de adquisiciones": self.total_frames,

            "Notas": self.notes
        }

    # ------------------------------------------------------

    def headers(self) -> List[str]:
        """
        Devuelve los encabezados de la tabla de datos.
        """

        headers = [

            "Frame",

            "Timestamp",

            "Tiempo (s)"
        ]

    
        for channel in range(self.channel_count):

            headers.append(
                f"Canal {channel+1} (°C)"
            )


        return headers

    # ------------------------------------------------------

    def rows(self) -> List[List[Any]]:
        """
        Devuelve todas las adquisiciones listas para exportar.
        """

        rows = []

        for frame in self.frames:

            row = [

                frame.sequence,

                frame.timestamp.strftime(
                    "%Y-%m-%d %H:%M:%S.%f"
                )[:-3],

                round(
                    frame.elapsed_time,
                    3
                )
            ]

            for reading in frame.readings:

                row.append(
                    reading.temperature
                )

            rows.append(row)

        return rows

    # ------------------------------------------------------

    def summary(self) -> str:
        """
        Devuelve un resumen del experimento.
        """

        return (
            f"{self.name} | "
            f"{self.channel_count} canales | "
            f"{self.total_frames} adquisiciones | "
            f"{round(self.duration,1)} s"
        )

    # ------------------------------------------------------

    def update_sensor_types(self) -> None:
        """
        Actualiza automáticamente los tipos de sensor
        presentes en el experimento.
        """

        sensors = set()

        if self.first_frame is None:

            self.sensor_types = []

            return

        for reading in self.first_frame.readings:

            sensors.add(reading.sensor_type)

        self.sensor_types = sorted(sensors)

    # ------------------------------------------------------

    def channel_data(
        self,
        channel: int
    ) -> List[float]:
        """
        Devuelve las temperaturas de un canal.
        """

        if channel < 0 or channel >= self.channel_count:

            raise ValueError(
                "Canal inválido."
            )

        return [

            frame.readings[channel].temperature

            for frame in self.frames
        ]

    # ------------------------------------------------------

    @property
    def first_frame(self) -> Optional[AcquisitionFrame]:
        """
        Primera adquisición.
        """

        if not self.frames:
            return None

        return self.frames[0]

    # ------------------------------------------------------

    @property
    def last_frame(self) -> Optional[AcquisitionFrame]:
        """
        Última adquisición.
        """

        if not self.frames:
            return None

        return self.frames[-1]

    # -----------------------------------------------------
    
    @property
    def channel_count(self) -> int:
        """
        Número de canales del experimento.
        """

        if self.first_frame is None:

            return 0

        return len(
            self.first_frame.readings
        )

    # ------------------------------------------------------

    @property
    def total_frames(self) -> int:
        """Número total de adquisiciones."""

        return len(self.frames)

    # ------------------------------------------------------

    @property
    def duration(self) -> float:
        """Duración en segundos."""

        end = self.end_time or datetime.now()

        return (
            end - self.start_time
        ).total_seconds()

    # ------------------------------------------------------

    @property
    def is_finished(self) -> bool:
        """Indica si el experimento terminó."""

        return self.end_time is not None

    # ------------------------------------------------------

    @property
    def timestamps(self) -> List[datetime]:
        """
        Devuelve todos los timestamps.
        """

        return [
            frame.timestamp
            for frame in self.frames
        ]

    # ------------------------------------------------------

    @property
    def elapsed_times(self) -> List[float]:
        """
        Devuelve el tiempo transcurrido de cada adquisición.
        """

        return [
            frame.elapsed_time
            for frame in self.frames
        ]