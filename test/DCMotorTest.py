"""
Author: Gai Zhe

Description:
- Revamped DC Motor Test which utilizes the DC Motor class
- Cable config for L298N motor driver: With heat sink positioned at the left 
side, place the black wire to the left of the red wire.

How to use:
W to go forward for 1 second
S to go backward for 1 second
"""

# Standard Imports
import time
# Third-Party Imports
import RPi.GPIO as GPIO
# Project-Specific Imports
from HardwareComponents.DCMotor import DCMotor

# Instantiate DC Motor object
GPIO.setmode(GPIO.BCM)
dcMotor = DCMotor(In1=17, In2=27, EN=18)

while True:

    try:
        key = input('Press W to go clockwise, press S to go anticlockwise: ')

        if key == 'w':  # Goes forward
            dcMotor.forward(dutyCycle=100, duration=1)  # dutyCycle can range from 20 to 100 for forward

        elif key == 's': # Goes backwards
            dcMotor.backward(dutyCycle=100, duration=1)  # dutyCycle can range from 80 to 100 for backward

        elif key == 'b':
            dcMotor.stop()
            break

   # p.ChangeDutyCycle(DutyCycle)
   # print(f"The duty cycle is {DutyCycle}")
    except KeyboardInterrupt:
        dcMotor.stop()
        GPIO.cleanup()

GPIO.cleanup()
