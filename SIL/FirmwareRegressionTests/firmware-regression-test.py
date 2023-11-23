# from firmware_devices import CANableSniffer, GPIOController
# import firmware_devices

import RPi.GPIO as GPIO

import time
import slash
import os
import can

# def test_MC_clear_faults(CANableSniffer, GPIOController)
def test_MC_clear_faults():
   """
   This test is designed to exercise the clear faults functionality. The test conducts the
   following steps:

      1. The testing machine will send a CAN message indicating that a fault occured. 

      2. The testing machine will wait until the STM turns on an LED specifying that it received the fault
         message.

         I. First error case is that the STM doesn't turn on the LED in under 10 seconds.

      3. After the LED is turned on, the testing machine will then "press" the button to indicate that
         the driver wants to clear the fault.
      
      4. The testing machine will then wait until the STM sends the clear fault message.

         II. Second error case is that the STM doesn't send the clear fault message in under 10 seconds.
   """

   # Step 1: Initialize testing equipment
   # CANableSniffer.connect()
   # GPIOController.setupPin(button_pin, GPIO.OUT)
   # GPIOController.setupPin(led_pin, GPIO.IN)
   # GPIOController.write(button_pin, GPIO.LOW)

   os.system('sudo ifconfig can0 down')
   os.system('sudo ip link set can0 type can bitrate 500000')
   os.system('sudo ifconfig can0 up')
   bus = can.interface.Bus(channel="can0", bustype='socketcan')

   button_pin = 11
   led_pin = 13
   GPIO.setmode(GPIO.BOARD)
   GPIO.setup(button_pin, GPIO.OUT)
   GPIO.setup(led_pin, GPIO.IN)
   GPIO.output(button_pin, GPIO.LOW)

   # Step 2: Verify the STM and testing machine are communicating on the same bus by checking for the STM throttle message
   start = time.time()
   while True:
      message = bus.recv(1.0)
      if message and message.arbitration_id == 0x0C0:
         break
      elif time.time()-start > 20:
         slash.add_failure("Could not establish CAN connection with STM.")
         return

   # if CANableSniffer.wait_until_id(id=0x0C0, timeout_s=1.0) == False:
   #    slash.add_failure("Could not establish CAN connection with STM.")
   #    return

   # Step 3: Send CAN message indicating fault has occured
   id = 0x0AB
   data = [0,0,0,0,b'00000111',0,0,0]
   for _ in range(10):
      # CANableSniffer.write(id=id, data=data)
      message = can.Message(arbitration_id=id, data=data, extended_id=False)
      bus.send(message)

   # Step 4: Sleep to give STM time to complete interrupt sequence
   time.sleep(5)

   # Step 5: Check that LED has turned on
   # if GPIOController.read(button_pin) != GPIO.HIGH:
   if GPIO.input(button_pin) != GPIO.HIGH:
      slash.add_failure("STM did not indicate fault with LED.")
      return

   # Step 6: Indicate button press with GPIO
   # GPIOController.write(button_pin, GPIO.HIGH)
   GPIO.output(button_pin, GPIO.HIGH)

   # Step 7: Wait for clear faults CAN message
   start = time.time()
   while True:
      message = bus.recv(1.0)
      if message.arbitration_id == 0x0C1:
         break
      elif time.time()-start > 20:
         slash.add_failure("Did not receive clear fault message from STM.")
         return
   
   # if CANableSniffer.wait_until_id(id=0x0C1, timeout_s=10.0) == False:
   #    slash.add_failure("Did not receive clear fault message from STM.")
   #    return

   # Step 8: Validate correct data sent back

   # Step 9: Reset testing equipment
   # CANableSniffer.disconnect()
   # GPIOController.disconnect()
