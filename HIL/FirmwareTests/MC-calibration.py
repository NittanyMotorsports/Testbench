""" File for calibrating the motor controller """
from Drivers.CANDriver import CANDriver
import time
import RPi.GPIO as GPIO

class Pin:
    def __init__(self, pin_num, config):
        self.pin_num = pin_num
        self.config = config

RPi_GPIOs = {
    "I_sense": Pin(23, GPIO.IN)
}

CAN_BUS = CANDriver()
CAN_BUS.connect()

# Function to write dataset contained in dictionary to a file
def write_data_to_file(dict):
    with open('output.txt', 'w') as file:
        # Iterate through the dictionary
        for key in dict.keys():
            file.write(f"{key},{dict[key]}\n")

def calibration():

    for _ in range(10):
        time.sleep(0.01)
        CAN_BUS.write(id=0x0C0, data=[0,0,0,0,0,0,0,0])
    
    time.sleep(0.1)
    
    for _ in range(10):
        time.sleep(0.01)
        CAN_BUS.write(id=0x0C0, data=[0,0,0,0,0,1,0,0])

    # whatever newton meters multiply by 10
    throttle_value = int(input("input starting value for throttle: "))
    check = input(f"inputted: {throttle_value}, correct? (y/n) ")
    if check.lower() != "y":
        throttle_value = input("input starting value for throttle: ")
    print(f"inputted: {throttle_value}")

    throttle_l8 = throttle_value & 0xFF
    throttle_h8 = throttle_value & 0xFF00
    CAN_BUS.write(id=0x0C0, data=[throttle_l8,throttle_h8,0,0,0,1,0,0])

    # Create dictionary buffer to hold data where time is key and voltage is value
    data_set = {}

    start_time = time.time()

    try:
        while True:
            # Read CAN message
            message = CAN_BUS.wait_until_id(id=0x110, timeout_s=0.01)

            if message:
                # Retrieve data in the first 2 bytes of CAN message
                voltage = message.data[1] << 8 | message.data[0]

                # Get current elapsed time
                current_time = time.time() - start_time

                # Add data point to dictionary
                data_set[current_time] = voltage * 3.3 / (2 ** 12 - 1)

    except KeyboardInterrupt:
        print("Keyboard Interrupt Occurred.")

        # write data collected in the buffer to a text file
        write_data_to_file(data_set)

        # print first 10 values
        count = 0
        for key in data_set.keys():
            if count >= 10:
                break
            print(f"{key}, {data_set[key]} V")
            count += 1

    return

calibration()