from base_CAN_driver import BaseCANDriver

import can
import os
import time
from typing import List, Union

class CANableDriver(BaseCANDriver):
    
    def __init__(self, CAN_channel: str="can0", baud_rate: int=500_000, bus_type: str="socketcan") -> None:
        pass

    def connect(self):
        pass

    def read(self, delay_ms: Union[float, int]):
        pass

    def write(self, id: int, data: List[int]):
        pass

    def wait_until_id(self,  id: int, timeout_s: Union[float, int]=20) -> Union[List[Union[float, int]], bool]:
        pass

    def disconnect(self):
        pass