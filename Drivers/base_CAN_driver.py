"""
Base CAN Driver file for all CAN drivers.
"""

from abc import ABC, abstractmethod
from typing import List, Union

class BaseCANDriver(ABC):

    @abstractmethod
    def connect(self, CAN_channel: str, baud_rate: int, bus_type: str):
        pass

    @abstractmethod
    def read(self, delay_ms: Union[float, int]):
        pass

    @abstractmethod
    def write(self, id: int, data: List[int]):
        pass

    @abstractmethod
    def disconnect(self):
        pass