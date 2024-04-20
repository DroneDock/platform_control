"""
Run this code to check if electromagnet is working, by entering three possible
inputs "on/off/exit" to control the magnet.
"""

import RPi.GPIO as GPIO
import time
from HardwareComponents.Electromagnet import Electromagnet

magnet = Electromagnet()

try:
    while True:
        command = input("Enter command (on/off/exit): ").strip().lower()

        if command == 'on':
            magnet.activate()
        elif command == 'off':
            magnet.deactivate()
        elif command == 'exit':
            break
        else:
            print("Invalid command")

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
