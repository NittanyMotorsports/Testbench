import slash
import RPi.GPIO as GPIO
#import CANDriver

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
    "APPSLeft": Pin(17, GPIO.OUT),
    "APPSRight": Pin(19, GPIO.OUT)
}

def test_ready_to_drive():
    """
    This tests the functionality of the Ready To Drive (RTD) button on the vehicle. Once the
    tractive system gives an active signal and the brakes are pressed to mechanical engage
    the driver can then press the RTD button. The STM32F4 should activate the buzzer and the
    throttle CAN message should contain the inverter enable bit flipped from 0 to 1.
    """

    # Step 1: Turn on GPIO on RPi for TSA

    # Step 2: Turn on GPIO on RPi for both brake inputs

    # Step 3: Turn on GPIO on RPi for RTD button

    # Step 4: Check that buzzer output from STM32F4 is on (timeout if no voltage after 5 seconds)

    # Step 5: Check that throttle CAN message contains correct inverter enable bit value

    # Step 6: Reset all pins to put STM32F4 back in idle state
    pass

def test_APPS():

    #Output GPIO_HIGH on RPi to both APPS inputs on STM

    GPIO.output(RPi_GPIOs["APPSLeft"].pin_num, GPIO.HIGH)
    GPIO.output(RPi_GPIOs["APPSRight"].pin_num, GPIO.HIGH)

    #Check that throttle CAN message is greater than 2^15

    #if CAN.read > 32768:
        #pass
    #else:
        #pass

    #Switch one APPS input to GPIO_LOW while other is GPIO_HIGH

    GPIO.output(RPi_GPIOs["APPSRight"].pin_num, GPIO.LOW)

    #Check that throttle CAN message is zero

    #if CAN.read == 0:
        #pass
    #else:
        #pass


def configure_RPi():
    """ Sets up the RPi for all tests. Connects to CAN bus and configures GPIOs. """
    GPIO.setmode(GPIO.BOARD)
    for pin in RPi_GPIOs:
        GPIO.setup(RPi_GPIOs[pin].pin_num, RPi_GPIOs[pin].config)


configure_RPi()