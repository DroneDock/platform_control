import time

import RPi.GPIO as GPIO

import pygame

from HardwareComponents.StepperMotor import StepperMotor
"""
This is for Bottok Stepper Motor


Motor driver position, heat sink on your left
Bottom. Left to right: orange green
Top. Left to right: yellow blue

Correct orientation for clockwise and anticlockwise
Need to power at 12V otherwise insufficient power to make the first rotation.

110 steps rotate platform 360 completely.

Result of test: Doesn't work after a few tries.

"""

#classify steps
step = 50

if __name__ == "__main__":


    motor = StepperMotor()
    
    while True: 

        key = input('Press W to increase rotate clockwise , press S to rotate anticlockwise: ')

        if key == 'w':
            motor.step_clockwise(steps=step, sleep_time=0.001)
        elif key == 's':
            motor.step_anticlockwise(steps=step, sleep_time=0.001)
    
        elif key == 'b':
            break
   
      
  
    GPIO.cleanup()
  
