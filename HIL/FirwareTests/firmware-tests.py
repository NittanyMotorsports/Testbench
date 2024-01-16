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

def test_motor_controller_fault():
    """
    This tests the functionality of the clear faults button in the cockpit of the vehicle.
    If a over voltage, over current, or over speed fault occur within the Motor Controller (MC)
    then the MC sends a message over CAN indicating that a fault occured. An LED driven by the
    STM32F4 should turn on if this message is received. Once the clear faults button is pressed
    the STM32F4 should send a message over CAN to the MC indicating to reset itself. The LED that
    is being driven by the STM32F4 should also turn off.
    """

    # Step 1: Check that the throttle message from the STM32F4 is able to be received

    # Step 2: Send the CAN message indicating that the fault has occured (id = 0x0AB, data = [0,0,0,0,3,0,0,0])

    # Step 3: Allow time for STM32F4 to receive CAN message and process the data

    # Step 4: Check that the LED driven by the STM32F4 turned on

    # Step 5: Turn on GPIO on RPi for the clear fault button

    # Step 6: Check that the STM32F4 sends the CAN message to clear faults (id = 0x0C1)

    # Step 7: Check that the LED turns off after the button is pressed

    # Step 8: Reset all pins to put STM32F4 back in idle state
    pass

def configure_RPi():
    """ Sets up the RPi for all tests. Connects to CAN bus and configures GPIOs. """
    GPIO.setmode(GPIO.BOARD)
    for pin in RPi_GPIOs:
        GPIO.setup(RPi_GPIOs[pin].pin_num, RPi_GPIOs[pin].config)


configure_RPi()