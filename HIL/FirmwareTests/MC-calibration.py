""" File for calibrating the motor controller """
# from .Drivers.CANDriver import CANDriver
import time
# import RPi.GPIO as GPIO

class Pin:
    def __init__(self, pin_num, config):
        self.pin_num = pin_num
        self.config = config

# RPi_GPIOs = {
#     "I_sense": Pin(23, GPIO.IN)
# }

# CAN_BUS = CANDriver()

def calibration():

    for _ in range(10):
        time.sleep(0.01)
        # CAN_BUS.write(id=0x0C0, data=[0,0,0,0,0,0,0,0])
    
    time.sleep(0.1)
    
    for _ in range(10):
        time.sleep(0.01)
        # CAN_BUS.write(id=0x0C0, data=[0,0,0,0,0,1,0,0])

    throttle_value = input("input starting value for throttle: ")
    check = input(f"inputted: {throttle_value}, correct? (y/n) ")
    if check.lower() != "y":
        throttle_value = input("input starting value for throttle: ")
    print(f"inputted: {throttle_value}")

    throttle_l8 = throttle_value & 0xFF
    throttle_h8 = throttle_value & 0xFF00
    # CAN_BUS.write(id=0x0C0, data=[throttle_l8,throttle_h8,0,0,0,1,0,0])


    return

calibration()