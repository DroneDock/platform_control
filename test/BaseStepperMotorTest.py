"""
Author: Ken

Description: Useful for checking connections of base stepper motor
"""
import time

import RPi.GPIO as GPIO

from HardwareComponents.StepperMotor import BaseStepperMotor
"""

For ref: https://www.instructables.com/Raspberry-Pi-Python-and-a-TB6600-Stepper-Motor-Dri/
Motor driver position T6880
B-: red
B+: blue
A-: green
A+: black

+ve dir, ena and pul need to connect to 3.3V of RPI
-ve dir: 24
-ve ena: 23
-ve pul: 25

Progress: Works fine.
Microstepping: 8

Next step is making it react to ArUco
"""
#classify steps
time_sleep = 0.0005 #don't change this
step = 1000

if __name__ == "__main__":

    #GPIO.setmode(GPIO.BCM)
    motor = BaseStepperMotor(ena_pin=23, dir_pin=24, pul_pin=25)
    
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
