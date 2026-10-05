"""
project_writer.py
-----------------

Guarda un experimento completo de ThermoLab
en formato JSON (.thl).
"""

from __future__ import annotations

import json

from pathlib import Path

from datetime import datetime

from models.experiment import Experiment

from storage.base_writer import BaseWriter

from core.constants import (
    APP_NAME,
    APP_VERSION
)


class ProjectWriter(BaseWriter):

    """
    Guarda un proyecto ThermoLab.
    """

    # -------------------------------------------------

    def save(
        self,
        experiment: Experiment,
        filepath: str | Path
    ) -> None:

        filepath = Path(filepath)

        filepath.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        project = {

            "software": APP_NAME,

            "version": APP_VERSION,

            "format_version": 1,

            "export_date":
                datetime.now().isoformat(),

            "experiment": {

                "name":
                    experiment.name,

                "operator":
                    experiment.operator,

                "description":
                    experiment.description,

                "source":
                    experiment.source,

                "sample_interval_ms":
                    experiment.sample_interval_ms,

                "notes":
                    experiment.notes,

                "start_time":
                    experiment.start_time.isoformat(),

                "end_time":
                    experiment.end_time.isoformat()
                    if experiment.end_time
                    else None,

                "sensor_types":
                    experiment.sensor_types
            },

            "frames": [

                {

                    "sequence":
                        frame.sequence,

                    "timestamp":
                        frame.timestamp.isoformat(),

                    "elapsed_time":
                        frame.elapsed_time,

                    "readings": [

                        {

                            "channel":
                                reading.channel,

                            "temperature":
                                reading.temperature,

                            "valid":
                                reading.valid,

                            "unit":
                                reading.unit,

                            "sensor_type":
                                reading.sensor_type,

                            "status":
                                reading.status,

                            "message":
                                reading.message

                        }

                        for reading in frame.readings

                    ]

                }

                for frame in experiment.frames

            ]

        }

        try:

            with open(
                filepath,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    project,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except OSError as error:

            raise RuntimeError(

                f"No fue posible guardar el proyecto:\n{error}"

            ) from error