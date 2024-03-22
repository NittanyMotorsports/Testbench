import slash
import RPi.GPIO as GPIO
import CANDriver
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
    "APPSLeft": Pin(17, GPIO.OUT),
    "APPSRight": Pin(19, GPIO.OUT)
}

def test_apps_plus_brake():
    '''
    APPS + Brake:
    Checks that if APPS is GPIO_HIGH and Brakes are GPIO_HIGH then the STM sends a zero throttle 
    CAN message. Also checks that after Brakes are set to GPIO_LOW and APPS is set to GPIO_LOW 
    for a small amount of time and then set back to GPIO_HIGH that throttle CAN message 
    is back to non-zero
    '''
    # Step 1: Setting up environment (neither pedals are pressed)
    # Device is in idle state at this point
    GPIO.output(RPi_GPIOs["BrakesLeft"].pin_num, GPIO.LOW)
    GPIO.output(RPi_GPIOs["BrakesRight"].pin_num, GPIO.LOW)
    GPIO.output(RPi_GPIOs["APPSLeft"].pin_num, GPIO.LOW)
    GPIO.output(RPi_GPIOs["APPSRight"].pin_num, GPIO.LOW)

    # Step 2: Check for STM CAN message (should send a zero throttle message)
    message = CANDriver.wait_until_id(0X0C0)
    if message == None:
        slash.add_failure('Did not receive CAN message within time expected')
    else:
        data = message.data
        if data[0] > 0:
            slash.add_failure('Expected a zero throttle CAN message, recieved a non zero message') 

    # Step 3: Setting APPS to high while brakes remain at low (throttle is being pressed)
    GPIO.output(RPi_GPIOs["APPSLeft"].pin_num, GPIO.HIGH)
    GPIO.output(RPi_GPIOs["APPSRight"].pin_num, GPIO.HIGH)

    # Step 4: Check for STM CAN message (should send a non-zero throttle message)
    message = CANDriver.wait_until_id(0X0C0)
    if message == None:
        slash.add_failure('Did not receive CAN message within time expected')
    else:
        data = message.data
        if data[0] == 0:
            slash.add_failure('Expected a non zero throttle CAN message, recieved a zero message') 

    # Step 5: Setting Brakes to high while APPS remains at high (both pedals are being pressed):
    GPIO.output(RPi_GPIOs["BrakesLeft"].pin_num, GPIO.HIGH)
    GPIO.output(RPi_GPIOs["BrakesRight"].pin_num, GPIO.HIGH)

    # Step 6: Check for STM CAN message (should send a zero throttle message)
    message = CANDriver.wait_until_id(0X0C0)
    if message == None:
        slash.add_failure('Did not receive CAN message within time expected')
    else:
        data = message.data
        if data[0] > 0:
            slash.add_failure('Expected a zero throttle CAN message, recieved a non zero message') 

    time.sleep(2) # Add time delay to emulate real procedure

    # Step 7: Setting Brakes to low and keeping APPS at high:
    GPIO.output(RPi_GPIOs["BrakesLeft"].pin_num, GPIO.LOW)
    GPIO.output(RPi_GPIOs["BrakesRight"].pin_num, GPIO.LOW)

    # Step 8: Check for STM CAN message (should send a non-zero throttle message as we are out of the fault state)
    message = CANDriver.wait_until_id(0X0C0)
    if message == None:
        slash.add_failure('Did not receive CAN message within time expected')
    else:
        data = message.data
        if data[0] == 0:
            slash.add_failure('Expected a non zero throttle CAN message, recieved a zero message') 

    # Step 9: Setting Brakes to low and APPS to low
    GPIO.output(RPi_GPIOs["BrakesLeft"].pin_num, GPIO.LOW)
    GPIO.output(RPi_GPIOs["BrakesRight"].pin_num, GPIO.LOW)
    GPIO.output(RPi_GPIOs["APPSLeft"].pin_num, GPIO.LOW)
    GPIO.output(RPi_GPIOs["APPSRight"].pin_num, GPIO.LOW)

    # Step 10: Check for STM CAN message (should send a zero throttle message)
    message = CANDriver.wait_until_id(0X0C0)
    if message == None:
        slash.add_failure('Did not receive CAN message within time expected')
    else:
        data = message.data
        if data[0] > 0:
            slash.add_failure('Expected a zero throttle CAN message, recieved a non zero message') 

    time.sleep(2) # Add time delay to emulate real procedure


    # Step 11: Setting APPS back to high
    GPIO.output(RPi_GPIOs["APPSLeft"].pin_num, GPIO.HIGH)
    GPIO.output(RPi_GPIOs["APPSRight"].pin_num, GPIO.HIGH)

    # Step 12: Check for STM CAN message (should be back to a non-zero throttle message)
    message = CANDriver.wait_until_id(0X0C0)
    if message == None:
        slash.add_failure('Did not receive CAN message within time expected')
    else:
        data = message.data
        if data[0] == 0:
            slash.add_failure('Expected a non zero throttle CAN message, recieved a zero message') 

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

def configure_RPi():
    """ Sets up the RPi for all tests. Connects to CAN bus and configures GPIOs. """
    GPIO.setmode(GPIO.BOARD)
    for pin in RPi_GPIOs:
        GPIO.setup(RPi_GPIOs[pin].pin_num, RPi_GPIOs[pin].config)


configure_RPi()