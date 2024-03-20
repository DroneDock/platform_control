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

Works once in a while but overheating issues as well (for battery)

Results: step @100, results in 1cm extension / retraction

Method: 
1.Make platform tilt upwards until motor hits arm.
2. Then change input step to 500 from 100, and press s. IMPORTANT!
3. Then change input step back to 100

Still need to reconfirm values. Not accurate


"""
#classify steps
input_step = 200
lead_screw_pitch = 8 #mm

if __name__ == "__main__":


    motor = StepperMotor()
    
    while True: 

        key = input('Press W to increase rotate clockwise , press S to rotate anticlockwise: ')

        if key == 'w':
            motor.step_clockwise(steps=input_step, sleep_time=0.001)
            current_postion_mm = motor.add_position_mm(input_step, lead_screw_pitch)
            print("'My current position in mm is :", format(current_postion_mm,".2f"))
            
        elif key == 's':
            motor.step_anticlockwise(steps=input_step, sleep_time=0.001)
            current_postion_mm = motor.subtract_position_mm(input_step, lead_screw_pitch)
            print("'My current position in mm is :", format(current_postion_mm,".2f"))

    
        elif key == 'b':
            break
        
   
      
  
    GPIO.cleanup()
  
