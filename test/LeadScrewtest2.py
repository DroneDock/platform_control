import time

import RPi.GPIO as GPIO

from HardwareComponents.StepperMotor import LeadscrewStepperMotor
"""
This is for lead screw
Cable config: black to black
green to yellow
red to red
blue to blue

For reference: https://how2electronics.com/control-stepper-motor-with-a4988-driver-arduino/
Motor driver position A4988
2B: yellow
2A: black
1B: blue
1A: red
dir pin = GPIO 20 (int 38)
step pin = GPIO 21 (int 40)

ISSUE: Once the program finished running, it will go into idle buzzing.

"""
lead_screw_pitch = 8 #mm
time_sleep = 0.0005 #don't change this
step = 400



if __name__ == '__main__':


    motor = LeadscrewStepperMotor()
    
    #applies to current git config. Don't change sleep_time.
    

    #runs it 10 times
    for i in range (10):
        #retracts platform
        motor.spin(steps= step, sleep_time= time_sleep, clockwise=True)

        #current_postion_mm = motor.add_position_mm(step,lead_screw_pitch)
        #print("Extension is ",current_postion_mm)
        time.sleep(0.7)
        """
        The issue is the code doesn't keep running, it ends there
        """
    
        #extends platform
        motor.spin(steps=step, sleep_time= time_sleep, clockwise=False)

        time.sleep(0.7)

    GPIO.cleanup()
