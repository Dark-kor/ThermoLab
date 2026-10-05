from abc import ABC, abstractmethod

from models.acquisition import AcquisitionFrame


class TemperatureSource(ABC):

    def __init__(self, channels=8):

        self.channels = channels

        self.connected = False

    @abstractmethod
    def connect(self) -> bool:
        ...

    @abstractmethod
    def disconnect(self):
        ...

    @abstractmethod
    def acquire(self) -> AcquisitionFrame:
        ...

    def is_connected(self):

        return self.connected

    def get_channel_count(self):

        return self.channels