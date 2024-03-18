import slash
from slash import test, tag
import RPi.GPIO as GPIO
from .Drivers.CANDriver import CANDriver
import time

class Pin:
    def __init__(self, pin_num, config):
        self.pin_num = pin_num
        self.config = config

RPi_GPIOs = {
    "TSA": Pin(3, GPIO.OUT),
    "RTD_button": Pin(5, GPIO.OUT),
    "BrakesFront": Pin(11, GPIO.OUT),
    "BrakesRear": Pin(13, GPIO.OUT),
    "Buzzer": Pin(15, GPIO.IN),
    "APPSLeft": Pin(19, GPIO.OUT),
    "APPSRight": Pin(21, GPIO.OUT)
}
CAN_BUS = CANDriver()
    
def ready_to_drive_test():
    """
    This tests the functionality of the Ready To Drive (RTD) button on the vehicle. Once the
    tractive system gives an active signal and the brakes are pressed to mechanical engage
    the driver can then press the RTD button. The STM32F4 should activate the buzzer and the
    throttle CAN message should contain the inverter enable bit flipped from 0 to 1.
    """

    # Step 1: Put RTD button state to LOW
    GPIO.output(RPi_GPIOs["RTD_button"].pin_num, GPIO.LOW)
    GPIO.output(RPi_GPIOs["APPSLeft"].pin_num, GPIO.LOW)
    GPIO.output(RPi_GPIOs["APPSRight"].pin_num, GPIO.LOW)

    # Step 2: Turn on GPIO on RPi for TSA
    GPIO.output(RPi_GPIOs["TSA"].pin_num, GPIO.HIGH)

    # Step 3: Turn on GPIO on RPi for both brake inputs
    GPIO.output(RPi_GPIOs["BrakesFront"].pin_num, GPIO.HIGH)
    GPIO.output(RPi_GPIOs["BrakesRear"].pin_num, GPIO.HIGH)

    # Step 4: Delay to allow signal to reach STM32F4 before activating RTD
    time.sleep(1)

    # Step 5: Turn on GPIO on RPi for RTD button
    GPIO.output(RPi_GPIOs["RTD_button"].pin_num, GPIO.HIGH)

    # Step 6: Check that buzzer output from STM32F4 is on (timeout if no voltage after 5 seconds)
    start = time.time()
    success = False
    while time.time() - start < 20:
        if GPIO.input(RPi_GPIOs["Buzzer"].pin_num) == GPIO.HIGH:
            success = True
            break
    if success == False:
        slash.add_failure(f"Buzzer did not output voltage when Ready To Drive ({GPIO.input(RPi_GPIOs['Buzzer'].pin_num)}) was activated with both brakes signal and Tractive System Active signal present.")

    # Step 7: Check that throttle CAN message contains correct inverter enable bit value (timeout after 5 seconds if no message was received)
    message = CAN_BUS.wait_until_id(id=0x0C0, timeout_s=5)
    if message == None:
        slash.add_failure("Throttle message with id: 0x0C0 was not received within 5 seconds")
    elif message.data[5] != 1:
        slash.add_failure(f"Inverter enable bit was not changed to 1, value is: {message.data}")

def configure_env():
    CAN_BUS.connect()

    GPIO.setmode(GPIO.BOARD)
    for pin in RPi_GPIOs:
        GPIO.setup(RPi_GPIOs[pin].pin_num, RPi_GPIOs[pin].config)

    slash.add_critical_cleanup(CAN_BUS.disconnect)
    slash.add_critical_cleanup(GPIO.cleanup)

def test_runner():
    configure_env()
    ready_to_drive_test()