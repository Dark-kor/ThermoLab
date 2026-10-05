"""
base_writer.py
--------------

Clase base para todos los exportadores.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from models.experiment import Experiment


class BaseWriter(ABC):
    """
    Clase base para todos los exportadores.
    """

    @abstractmethod
    def save(
        self,
        experiment: Experiment,
        filepath: str | Path
    ) -> None:
        """
        Guarda un experimento.
        """
        pass