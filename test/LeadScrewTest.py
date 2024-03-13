import time

import RPi.GPIO as GPIO

from HardwareComponents.StepperMotor import StepperMotor
"""
This is for lead screw
Cable config: black to black
green to yellow
red to red
blue to blue

Motor driver position, heat sink on your left
Bottom. Left to right: Yellow blue
Top. Left to right: Red black
"""
#steps_per_revolution = 200
step = 100
lead_screw_pitch = 2.0

if __name__ == '__main__':


    motor = StepperMotor()
    
    #applies to current git config. Don't change sleep_time.
    

    #runs it 10 times
    for i in range (10):
        #retracts platform
        motor.step_anticlockwise(steps=step, sleep_time=0.001)
        current_postion_mm = motor.get_current_position_mm(step,lead_screw_pitch)
        print(current_postion_mm)

        """
        The issue is the code doesn't keep running, it ends there
        """
    
        #extends platform
        motor.step_clockwise(steps=step, sleep_time=0.001)

    GPIO.cleanup()
