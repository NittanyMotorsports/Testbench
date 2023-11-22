from firmware_devices import CANableSniffer

import can
import os
import time
import slash

os.system('sudo ifconfig can0 down')
os.system('sudo ip link set can0 type can bitrate 500000')
os.system('sudo ifconfig can0 up')

bus = can.interface.Bus(channel="can0", bustype='socketcan')

def test_MC_clear_faults(CANableSniffer):
    """
    This test is designed to exercise the clear faults functionality. The test conducts the
    following steps:

        1. The testing machine will send a CAN message indicating that a fault occured. 

        2. The testing machine will wait until the STM turns on an LED specifying that it received the fault
           message.

           I. First error case is that the STM doesn't turn on the LED in under 10 seconds.

        3. After the LED is turned on, the testing machine will then "press" the button to indicate that
           the driver wants to clear the fault.
        
        4. The testing machine will then wait until the STM sends the clear fault message.

           II. Second error case is that the STM doesn't send the clear fault message in under 10 seconds.
    """

    # Step 1: Initialize testing equipment

    # Step 2: Verify the STM and testing machine are communicating on the same bus by checking for the STM throttle message

    # Step 3: Send CAN message indicating fault has occured

    # Step 4: Check that LED has turned on

    # Step 5: Indicate button press with GPIO

    # Step 6: Wait for clear faults CAN message

def read():
    message = bus.recv(10.0)
    print(message)

try:
    while True:
        read()
except:
    pass

finally:
    os.system('sudo ifconfig can0 down')