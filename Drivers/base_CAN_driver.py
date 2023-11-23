"""
Base CAN Driver file for all CAN drivers.
"""

from abc import ABC, abstractmethod
from typing import List, Union

class BaseCANDriver(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def read(self, delay_ms: Union[float, int]):
        pass

    @abstractmethod
    def write(self, id: int, data: List[int]):
        pass

    @abstractmethod
    def wait_until_id(self,  id: int, timeout_s: Union[float, int]=20):
        pass

    @abstractmethod
    def disconnect(self):
        pass