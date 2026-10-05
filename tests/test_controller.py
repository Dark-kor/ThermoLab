import time
import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from controllers.acquisition_controller import AcquisitionController


def main():

    controller = AcquisitionController()

    print("=" * 60)
    print("PRUEBA DEL ACQUISITION CONTROLLER")
    print("=" * 60)

    controller.connect()

    controller.new_experiment("Prueba de adquisición")
    controller.start()
    for i in range(10):

        frame = controller.acquire_once()

        print(
            f"Frame {frame.sequence} | "
            f"Tiempo: {frame.elapsed_time:.3f} s"
        )

        for reading in frame:
            print(reading)

        print("-" * 60)

        time.sleep(0.2)
    controller.stop()
    controller.disconnect()

    print(f"\nFrames almacenados: {len(controller.get_history())}")


if __name__ == "__main__":
    main()