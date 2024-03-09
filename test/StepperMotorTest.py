import time

import RPi.GPIO as GPIO

from HardwareComponents.StepperMotor import StepperMotor
"""
Cable config: black to black
green to yellow
red to red
blue to blue

Motor driver position, heat sink on your left
Bottom. Left to right: Yellow blue
Top. Left to right: Red black
"""

if __name__ == '__main__':


    motor = StepperMotor()
    
    #applies to current config. Don't change sleep_time.

    #retracts platform
    motor.step_anticlockwise(steps=10, sleep_time=0.001)
    
    #extends platform
    #motor.step_clockwise(steps=10, sleep_time=0.001)

    GPIO.cleanup()
