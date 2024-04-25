""" File for calibrating the motor controller """
from Drivers.CANDriver import CANDriver
import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

class Pin:
    def __init__(self, pin_num, config):
        self.pin_num = pin_num
        self.config = config

RPi_GPIOs = {
    "I_sense": Pin(23, GPIO.IN)
}

# Initializing CAN bus
CAN_BUS = CANDriver()
CAN_BUS.connect()
print('CAN connected successfully')

# Initializing MCP3008
SPI_PORT   = 0
SPI_DEVICE = 0
s=SPI.SpiDev(SPI_PORT, SPI_DEVICE)
s.max_speed_hz = 3600000/4
mcp = Adafruit_MCP3008.MCP3008(spi = s)

# Function to write dataset contained in dictionary to a file
def write_data_to_file(dict):
    with open('output.txt', 'w') as file:
        # Iterate through the dictionary
        for key in dict.keys():
            file.write(f"{key},{dict[key]}\n")

def calibration():
    # Getting throttle input
    # whatever newton meters multiply by 10
    throttle_value = int(input("input starting value for throttle: "))
    check = input(f"inputted: {throttle_value}, correct? (y/n) ")
    if check.lower() != "y":
        throttle_value = input("input starting value for throttle: ")
    print(f"inputted: {throttle_value}")
    throttle_l8 = throttle_value & 0xFF
    throttle_h8 = (throttle_value & 0xFF00) >> 8

    # Sending 0s to MC
    for _ in range(500):
        time.sleep(0.01)
        CAN_BUS.write(id=0x0C0, data=[0,0,0,0,0,0,0,0])
    
    time.sleep(0.1)
    
    # Sending Inverter Enable to MC
    for _ in range(500):
        time.sleep(0.01)
        CAN_BUS.write(id=0x0C0, data=[0,0,0,0,0,1,0,0])

    # Create dictionary buffer to hold data where time is key and voltage is value
    data_set = {}

    start_time = time.time()

    try:
        while True:
            time.sleep(0.0000001)

            # Write CAN message with Throttle Value
            CAN_BUS.write(id=0x0C0, data=[throttle_l8,throttle_h8,0,0,0,1,0,0])

            # Get current time
            current_time = time.time() - start_time

            # Read ADC value
            voltage = mcp.read_adc(0)

            # Adjust raw ADC value to voltage
            data_set[current_time] = voltage * 3.3 / (2 ** 10 - 1)

    except KeyboardInterrupt:
        print("Keyboard Interrupt Occurred.")

        # write data collected in the buffer to a text file
        write_data_to_file(data_set)

        # print first 10 values
        for key in list(data_set.keys())[:10]:
            print(f"{key}, {data_set[key]} V")

    return

calibration()