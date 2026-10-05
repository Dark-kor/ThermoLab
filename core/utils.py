"""
utils.py
---------

Funciones auxiliares.
"""

from datetime import timedelta


def format_temperature(value):

    if value is None:

        return "--.-- °C"

    return f"{value:.2f} °C"


def format_elapsed(seconds):

    return str(
        timedelta(
            seconds=round(seconds)
        )
    )