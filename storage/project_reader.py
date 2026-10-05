"""
project_reader.py
-----------------

Carga un proyecto ThermoLab (.thl)
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

from models.experiment import Experiment
from models.acquisition import AcquisitionFrame
from models.sensor import ChannelReading


class ProjectReader:

    # -----------------------------------------------------

    def load(self, filepath: str | Path) -> Experiment:

        filepath = Path(filepath)

        with open(filepath, "r", encoding="utf-8") as file:

            data = json.load(file)

        # Compatibilidad entre versiones

        format_version = data.get("format_version",1)

        if format_version ==1:

            data = self._normalize_project(data)

        exp = data["experiment"]
        experiment = Experiment(

            name=exp.get("name"),

            operator=exp.get("operator"),

            description=exp.get("description"),

            source=exp.get("source"),

            sample_interval_ms=exp.get("sample_interval_ms"),

            notes=exp.get("notes")

        )

        experiment.start_time = datetime.fromisoformat(
            exp["start_time"]
        )

        if exp.get("end_time"):

            experiment.end_time = datetime.fromisoformat(
                exp["end_time"]
            )
        experiment.sensor_types = exp.get(
            "sensor_types",
            []
        )
        # ---------------------------------------------
        # Reconstruir Frames
        # ---------------------------------------------

        for frame_data in data["frames"]:

            readings = []

            for r in frame_data["readings"]:

                reading = ChannelReading(

                    channel=r["channel"],

                    temperature=r.get("temperature"),

                    valid=r.get("valid", True),

                    unit=r.get("unit","°C"),

                    sensor_type=r.get("sensor_type"),

                    status=r.get("status"),
                    
                    message =r.get("message", "")

                )

                readings.append(reading)

            frame = AcquisitionFrame(

                sequence=frame_data["sequence"],

                timestamp=datetime.fromisoformat(
                    frame_data["timestamp"]
                ),

                elapsed_time=frame_data["elapsed_time"],

                readings=readings

            )

            experiment.add_frame(frame)

        return experiment
        # -----------------------------------------------------

    def _normalize_project(self, data: dict) -> dict:
        """
        Normaliza proyectos antiguos para mantener
        compatibilidad entre versiones.
        """

        experiment = data.setdefault("experiment", {})

        experiment.setdefault("name", "Nuevo experimento")
        experiment.setdefault("operator", "")
        experiment.setdefault("description", "")
        experiment.setdefault("source", "simulator")
        experiment.setdefault("sample_interval_ms", 200)
        experiment.setdefault("notes", "")
        experiment.setdefault("sensor_types", [])
        experiment.setdefault("start_time", datetime.now().isoformat())
        experiment.setdefault("end_time", None)

        data.setdefault("frames", [])

        return data