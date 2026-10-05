"""
Prueba del exportador CSV.
"""
import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
import time

from controllers.acquisition_controller import AcquisitionController
from storage.csv_writer import CSVWriter
from core.config import EXPORT_DIR


def main():

    controller = AcquisitionController()

    controller.connect()

    controller.new_experiment(
        "Prueba CSV"
    )

    controller.start()

    for _ in range(50):

        controller.acquire_once()

        time.sleep(0.2)

    controller.stop()

    writer = CSVWriter()

    writer.save(

        controller.current_session,

        EXPORT_DIR / "prueba_csv.csv"
    )

    controller.disconnect()

    print("\nCSV generado correctamente.\n")


if __name__ == "__main__":

    main()