from firmware_devices import CANableSniffer, GPIOController

import time
import slash

def test_MC_clear_faults(CANableSniffer, GPIOController):
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
    CANableSniffer.connect()

    # Step 2: Verify the STM and testing machine are communicating on the same bus by checking for the STM throttle message
    if CANableSniffer.wait_until_id(id=0x0C0, timeout_s=1.0) == False:
        slash.add_failure("Could not establish CAN connection with STM.")
        return

    # Step 3: Send CAN message indicating fault has occured
    id = 0x0AB
    data = [0,0,0,0,b'00000111',0,0,0]
    CANableSniffer.write(id=id, data=data)

    # Step 4: Check that LED has turned on

    # Step 5: Indicate button press with GPIO

    # Step 6: Wait for clear faults CAN message

    # Step 7: Reset testing equipment
    CANableSniffer.disconnect()
