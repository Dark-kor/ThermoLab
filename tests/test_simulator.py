"""
test_simulator.py
-----------------

Prueba del simulador de ThermoLab.

Autor: Diego López
"""
import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
import time

from daq.simulator import SimulatorTemperatureSource


def print_frame(frame):
    """
    Imprime una adquisición completa.
    """

    print("-" * 60)
    print(f"Adquisición : {frame.sequence}")
    print(f"Tiempo      : {frame.elapsed_time:.3f} s")
    print(f"Timestamp   : {frame.timestamp}")
    print("-" * 60)

    for reading in frame:
        print(reading)

    print()


def main():

    daq = SimulatorTemperatureSource()

    print("=" * 60)
    print("THERMOLAB")
    print("TEST DEL SIMULADOR")
    print("=" * 60)

    # ---------------------------------------------------
    # Conexión
    # ---------------------------------------------------

    if not daq.connect():

        print("No fue posible conectar el simulador.")
        return

    print("✓ Simulador conectado correctamente\n")

    # ---------------------------------------------------
    # Estado inicial
    # ---------------------------------------------------

    print("LECTURA INICIAL\n")

    frame = daq.acquire()

    print_frame(frame)

    # ---------------------------------------------------
    # Espera
    # ---------------------------------------------------

    print("Esperando 2 segundos...\n")

    time.sleep(2)

    # ---------------------------------------------------
    # Calentar canal 1
    # ---------------------------------------------------

    print("Calentando Canal 1 hasta 80 °C\n")

    daq.set_channel_target(1, 80)

    for _ in range(40):

        frame = daq.acquire()

        print_frame(frame)

        time.sleep(0.2)

    # ---------------------------------------------------
    # Calentar todos
    # ---------------------------------------------------

    print("\nTodos los canales → 40 °C\n")

    daq.set_all_targets(40)

    for _ in range(20):

        frame = daq.acquire()

        print_frame(frame)

        time.sleep(0.2)

    # ---------------------------------------------------
    # Enfriar todos
    # ---------------------------------------------------

    print("\nTodos los canales → 20 °C\n")

    daq.set_all_targets(20)

    for _ in range(20):

        frame = daq.acquire()

        print_frame(frame)

        time.sleep(0.2)

    # ---------------------------------------------------
    # Desconexión
    # ---------------------------------------------------

    daq.disconnect()

    print("\n✓ Simulador desconectado correctamente")


if __name__ == "__main__":
    main()