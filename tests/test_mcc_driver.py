"""
Prueba del driver MCC.
"""
import os   
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import time

from daq.mcc_driver import MCCDriver


driver = MCCDriver()

driver.connect()

print("Conectado correctamente\n")

try:

    while True:

        value = driver.read_temperature(0)

        print(f"CH0 : {value:.2f} °C")

        time.sleep(1)

except KeyboardInterrupt:

    print("\nFinalizando...")

finally:

    driver.disconnect()

    print("Desconectado.")