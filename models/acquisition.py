"""
acquisition.py
--------------

Representa una adquisición completa del sistema DAQ.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from .sensor import ChannelReading


@dataclass(slots=True)
class AcquisitionFrame:
    """
    Una adquisición realizada por el DAQ.

    Todas las lecturas pertenecen al mismo instante.
    """

    timestamp: datetime = field(default_factory=datetime.now)

    readings: List[ChannelReading] = field(default_factory=list)

    sequence: int = 0

    elapsed_time: float = 0.0

    def __len__(self):

        return len(self.readings)

    def __iter__(self):

        return iter(self.readings)

    def __getitem__(self, index):

        return self.readings[index]