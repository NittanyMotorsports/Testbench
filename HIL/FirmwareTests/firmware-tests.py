import slash
import RPi.GPIO as GPIO
from ..Drivers.CANDriver import CANDriver
import time

class Pin:
    def __init__(self, pin_num, config):
        self.pin_num = pin_num
        self.config = config

RPi_GPIOs = {
    "TSA": Pin(3, GPIO.OUT),
    "RTD_button": Pin(5, GPIO.OUT),
    "BrakesLeft": Pin(11, GPIO.OUT),
    "BrakesRight": Pin(13, GPIO.OUT),
    "Buzzer": Pin(15, GPIO.IN),
}

CAN_BUS = None

def test_ready_to_drive():
    """
    This tests the functionality of the Ready To Drive (RTD) button on the vehicle. Once the
    tractive system gives an active signal and the brakes are pressed to mechanical engage
    the driver can then press the RTD button. The STM32F4 should activate the buzzer and the
    throttle CAN message should contain the inverter enable bit flipped from 0 to 1.
    """

    # Step 1: Turn on GPIO on RPi for TSA
    GPIO.output(RPi_GPIOs["TSA"].pin_num, GPIO.HIGH)

    # Step 2: Turn on GPIO on RPi for both brake inputs
    GPIO.output(RPi_GPIOs["BrakesLeft"].pin_num, GPIO.HIGH)
    GPIO.output(RPi_GPIOs["BrakesRight"].pin_num, GPIO.HIGH)

    # Step 4: Delay to allow signal to reach STM32F4 before activating RTD
    time.sleep(0.5)

    # Step 5: Turn on GPIO on RPi for RTD button
    GPIO.output(RPi_GPIOs["RTD_button"].pin_num, GPIO.HIGH)

    # Step 4: Check that buzzer output from STM32F4 is on (timeout if no voltage after 5 seconds)
    start = time.time()
    success = False
    while time.time() - start < 5:
        if GPIO.input(RPi_GPIOs["Buzzer"].pin_num) == GPIO.HIGH:
            success = True
    if success == False:
        slash.add_failure("Buzzer did not output voltage when Ready To Drive was activated with both brakes signal and Tractive System Active signal present.")

    # Step 5: Check that throttle CAN message contains correct inverter enable bit value (timeout after 5 seconds if no message was received)
    message = CAN_BUS.wait_until_id(id=0x0C0, timeout_s=5)
    if message == None:
        slash.add_failure("Throttle message with id: 0x0C0 was not received within 5 seconds")
    elif message.data[5] != 1:
        slash.add_failure(f"Inverter enable bit was not changed to 1, value is: {message.data[5]}")

def configure_RPi():
    """ Sets up the RPi for all tests. Connects to CAN bus and configures GPIOs. """
    GPIO.setmode(GPIO.BOARD)
    for pin in RPi_GPIOs:
        GPIO.setup(RPi_GPIOs[pin].pin_num, RPi_GPIOs[pin].config)
    
    CAN_BUS = CANDriver()
    CAN_BUS.connect()


configure_RPi()