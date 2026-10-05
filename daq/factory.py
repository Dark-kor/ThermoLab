"""
factory.py
----------

Fábrica de fuentes de adquisición para ThermoLab.
"""

from .simulator import SimulatorTemperatureSource
from .usb5203 import USB5203TemperatureSource


AVAILABLE_SOURCES = {
    "simulator": SimulatorTemperatureSource,
    "usb5203": USB5203TemperatureSource,
}


def create_source(source_type: str = "simulator", **kwargs):
    """
    Crea una fuente de adquisición.

    Parameters
    ----------
    source_type : str
        Tipo de fuente de datos.

    kwargs :
        Parámetros adicionales para el constructor.

    Returns
    -------
    TemperatureSource
    """

    source_type = source_type.lower()

    if source_type not in AVAILABLE_SOURCES:

        raise ValueError(
            f"Fuente '{source_type}' no soportada."
        )

    return AVAILABLE_SOURCES[source_type](**kwargs)