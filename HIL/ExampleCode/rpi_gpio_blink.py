"""
This is an example blink sketch brought to you by ChatGPT

Follow this layout for how to control the GPIOs on the rpi
"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)  # Use board pinout numbering for GPIO pins

# Set up the GPIO pin
led_pin = 11
GPIO.setup(led_pin, GPIO.OUT)

# Turn the LED on and off
GPIO.output(led_pin, GPIO.HIGH)  # Turn on
time.sleep(2)
GPIO.output(led_pin, GPIO.LOW)   # Turn off

# Clean up
GPIO.cleanup()
