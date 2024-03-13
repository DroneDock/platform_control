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

Anticlockwise is retract
Clockwise is extend

Works once in a while but overheating issues as well.
"""
#classify steps
step = 50
lead_screw_pitch = 2.0 #mm

if __name__ == "__main__":


    motor = StepperMotor()
    
    while True: 

        key = input('Press W to increase rotate clockwise , press S to rotate anticlockwise: ')

        if key == 'w':
            motor.step_clockwise(steps=step, sleep_time=0.001)
            current_postion_mm = motor.get_current_position_mm(lead_screw_pitch)
            print(current_postion_mm)

        elif key == 's':
            motor.step_anticlockwise(steps=step, sleep_time=0.001)
            current_postion_mm = motor.get_current_position_mm(lead_screw_pitch)
            print(current_postion_mm)
    
        elif key == 'b':
            break
        
   
      
  
    GPIO.cleanup()
  
