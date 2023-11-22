import RPi.GPIO as GPIO
import time

UNAVAILABLE_PINS = (1, 2, 4, 6, 9, 14, 17, 20, 25, 30, 34, 39)

"""
Make a wrapper for the functions that repeat value errors
"""

class GPIODriver():
    """ Driver class for GPIOs on RPi """

    def __init__(self, mode:int=GPIO.BOARD):
        GPIO.setmode(mode)
        self.pins = {}
    
    def setupPin(self, pin:int, pin_configuration:int, resistor_configuration:int=GPIO.PUD_DOWN):
        """Function to set up a new GPIO pin
        
           args:
                - pin:
                    int, board number of GPIO pin
                - pin_configuration:
                    int, either GPIO.IN for input or GPIO.OUT for output
                - resistor_configuration:
                    int, either GPIO.PUD_DOWN for pulldown or GPIO.PUD_UP for pullup
        """
        if pin in self.pins:
            raise ValueError(f"Pin:{pin} is already in use. To reset pin, call resetPin function first then this function.")
        elif pin in UNAVAILABLE_PINS:
            raise ValueError(f"Pin:{pin} is not an available GPIO pin. Choose a pin number 1-40 not in {UNAVAILABLE_PINS}")
        try:
            GPIO.setup(pin, pin_configuration, pull_up_down=resistor_configuration)
        except:
            raise ValueError("Error setting up pin.")
        finally:
            self.pins[pin] = (pin_configuration, resistor_configuration)
    
    def resetPin(self, pin:int):
        """ Function to reset the pin, removes mark of pin being in use """
        if pin not in self.pin:
            raise ValueError(f"Pin:{pin} not a pin in use.")
        else:
            del self.pins[pin]
    
    def read(self, pin:int):
        """ Function to read the state of the pin """
        if pin not in self.pins:
            raise ValueError(f"Pin:{pin} not a pin in use.")
        elif self.pins[pin][0] != GPIO.IN:
            raise ValueError(f"Pin:{pin} is configured as an output pin. To change configuration, reset pin and setup new pin.")
        else:
            return GPIO.input(pin)
    
    def write(self, pin:int, pin_state:int):
        """ Function to write state to pin """
        if pin not in self.pins:
            raise ValueError(f"Pin:{pin} not a pin in use.")
        elif pin_state not in (GPIO.HIGH, GPIO.LOW,):
            raise ValueError(f"State:{pin_state} is not a valid state")
        else:
            GPIO.output(pin, pin_state)
    
    def disconnect(self):
        """ Function to cleanup the states of the GPIO pins """
        GPIO.cleanup()