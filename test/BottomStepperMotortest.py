import time

import RPi.GPIO as GPIO

from HardwareComponents.StepperMotor import StepperMotor
"""
This is for Bottok Stepper Motor


Motor driver position, heat sink on your left
Bottom. Left to right: orange green
Top. Left to right: yellow blue

Correct orientation for clockwise and anticlockwise
Need to power at 12V otherwise insufficient power to make the first rotation.

110 steps rotate platform 360 completely.
"""

if __name__ == '__main__':


    motor = StepperMotor()
    
    #applies to current git config. Don't change sleep_time. Applies for all stepper motor.

    #retracts platform
    motor.step_anticlockwise(steps=200, sleep_time=0.001)



    #adds a delay
    #time.sleep(2)
    
    #extends platform
    #motor.step_clockwise(steps=1000, sleep_time=0.001)

   

    GPIO.cleanup()
