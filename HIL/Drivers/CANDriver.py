# from base_CAN_driver import BaseCANDriver

import can
import os
import time
from typing import List, Union

class CANableDriver:
    def __init__(self, CAN_channel: str="can0", baud_rate: int=500_000, bus_type: str="socketcan") -> None:
        self.CAN_channel = CAN_channel
        self.baud_rate = baud_rate
        self.bus_type = bus_type
        self.bus = None

    def connect(self):
        """ Starts up the CAN bus connection and creates the bus interface. """
        os.system('sudo ifconfig can0 down')
        os.system('sudo ip link set can0 type can bitrate 500000')
        os.system('sudo ifconfig can0 up')
        self.bus = can.interface.Bus(channel=self.CAN_channel, interface=self.bus_type, baud_rate = self.baud_rate)

        

    def read(self, delay_ms: Union[float, int]):
        """ Reads the bus and returns the first message received. """
        assert(self.bus != None, "Connection not instantiated")
        message = self.bus.recv(delay_ms)
        return message
        

    def write(self, id: int, data: List[int]):
        """ Writes specified message to the bus. """
        assert(self.bus != None, "Connection not instantiated")
        can_m = can.Message(arbitration_id = id, data = data)
        self.bus.send(can_m)
        

    def wait_until_id(self,  id: int, timeout_s: Union[float, int]=20) -> Union[List[Union[float, int]], bool]:
        """ Reads the bus and returns the message with given id or times out after specified duration. """
        assert(self.bus != None, "Connection not instantiated")
        start = time.time()
        while time.time() - start < timeout_s:
            message = self.read(1.0)
            if message.arbitration_id == id:
                return message
        return None

    def disconnect(self):
        """ Disconnects from the CAN bus. """
        assert(self.bus != None, "Connection not instantiated")
        os.system('sudo ifconfig can0 down')