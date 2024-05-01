"""
Author: Ken

Description: Useful for checking connections of base stepper motor
"""
import time

import RPi.GPIO as GPIO

from HardwareComponents.StepperMotor import BaseStepperMotor, LeadscrewStepperMotor
"""
"""
#classify steps
# Base stepper
time_sleep = 0.0005 #don't change this
step = 500

# Leadscrew


if __name__ == "__main__":

    #GPIO.setmode(GPIO.BCM)
    base_motor = BaseStepperMotor(ena_pin=23, dir_pin=24, pul_pin=25)
    leadscrew = LeadscrewStepperMotor(dir_pin=20, step_pin=21)
    
    while True: 

        key = input('Press W to increase rotate clockwise , press S to rotate anticlockwise: ')

        if key == 'w':
            motor.spin(steps=step, sleep_time=time_sleep, clockwise=True)
            #current_postion_mm = motor.add_position_mm(input_step, lead_screw_pitch)
            #print("'My current position in mm is :", format(current_postion_mm,".2f"))
            
        elif key == 's':
            motor.spin(steps=step, sleep_time=time_sleep, clockwise=False)
            #current_postion_mm = motor.subtract_position_mm(input_step, lead_screw_pitch)
            #print("'My current position in mm is :", format(current_postion_mm,".2f"))
    
        elif key == 'b':
            break
  
    GPIO.cleanup()
