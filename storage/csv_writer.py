"""
csv_writer.py
-------------

Exportador CSV para ThermoLab.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from core.config import CSV_SEPARATOR
from core.constants import (
    APP_NAME,
    APP_VERSION,
    APP_AUTHOR,
)

from models.experiment import Experiment
from storage.base_writer import BaseWriter


class CSVWriter(BaseWriter):
    """
    Exporta un experimento al formato CSV.
    """

    # -----------------------------------------------------

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

        try:

            with open(
                filepath,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(
                    file,
                    delimiter=CSV_SEPARATOR
                )

                # ==================================================
                # Información del software
                # ==================================================

                writer.writerow([APP_NAME])

                writer.writerow(
                    ["Versión", APP_VERSION]
                )

                writer.writerow(
                    ["Autor", APP_AUTHOR]
                )

                writer.writerow(
                    [
                        "Fecha de exportación",
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    ]
                )

                writer.writerow([])

                # ==================================================
                # Información del experimento
                # ==================================================

                writer.writerow(
                    ["INFORMACIÓN DEL EXPERIMENTO"]
                )

                for key, value in experiment.metadata().items():

                    writer.writerow([key, value])

                writer.writerow([])

                # ==================================================
                # Resumen de adquisición
                # ==================================================

                writer.writerow(
                    [
                        "Número de canales",
                        experiment.channel_count
                    ]
                )

                writer.writerow(
                    [
                        "Total de adquisiciones",
                        experiment.total_frames
                    ]
                )

                writer.writerow([])

                # ==================================================
                # Datos
                # ==================================================

                writer.writerow(
                    ["DATOS DE ADQUISICIÓN"]
                )

                writer.writerow([])

                writer.writerow(
                    experiment.headers()
                )

                for row in experiment.rows():

                    writer.writerow(row)

                writer.writerow([])

                # ==================================================
                # Pie de archivo
                # ==================================================

                writer.writerow(
                    [f"Archivo generado por {APP_NAME}"]
                )

                writer.writerow(
                    [f"Versión {APP_VERSION}"]
                )

        except OSError as error:

            raise RuntimeError(
                f"No fue posible guardar el archivo:\n{error}"
            ) from error