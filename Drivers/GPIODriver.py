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
        if pin in self.pins:
            raise ValueError(f"Pin:{pin} is already in use. To reset pin, call resetPin function first then this function.")
        elif pin in UNAVILABLE_PINS:
            raise ValueError(f"Pin:{pin} is not an available GPIO pin. Choose a pin number 1-40 not in {UNAVAILABLE_PINS}")
        try:
            GPIO.setup(pin, pin_configuration, pull_up_down=resistor_configuration)
        except:
            raise ValueError("Error setting up pin.")
        finally:
            self.pins[pin] = (pin_configuration, resistor_configuration)
    
    def resetPin(self, pin:int):
        if pin not in self.pin:
            raise ValueError(f"Pin:{pin} not a pin in use.")
        else:
            del self.pins[pin]
    
    def read(self, pin:int):
        if pin not in self.pins:
            raise ValueError(f"Pin:{pin} not a pin in use.")
        elif self.pins[pin][0] != GPIO.IN:
            rasie ValueError(f"Pin:{pin} is configured as an output pin. To change configuration, reset pin and setup new pin.")
        else:
            return GPIO.input(pin)
    
    def write(self, pin:int, pin_state:int):
        if pin not in self.pins:
            raise ValueError(f"Pin:{pin} not a pin in use.")
        else if pin_state not in (GPIO.HIGH, GPIO.LOW,):
            raise ValueError(f"State:{pin_state} is not a valid state")
        else:
            GPIO.output(pin, pin_state)

        
        

# Set up the GPIO pin
led_pin = 11
GPIO.setup(led_pin, GPIO.OUT)

# Turn the LED on and off
while True:
    GPIO.output(led_pin, GPIO.HIGH)  # Turn on
    time.sleep(2)
    GPIO.output(led_pin, GPIO.LOW)   # Turn off

# Clean up
GPIO.cleanup()