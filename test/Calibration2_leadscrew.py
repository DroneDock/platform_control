import time

import RPi.GPIO as GPIO

from HardwareComponents.Steppermotor2 import StepperMotor
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


Anticlockwise is retract
Clockwise is extend

Haven't tested with battery




Still need to reconfirm values. Not accurate


"""
#classify steps

#this values currently works
lead_screw_pitch = 8 #mm
time_sleep = 0.0005 #don't change this

#changet this
step = 100

if __name__ == "__main__":


    motor = StepperMotor()
    
    while True: 

        key = input('Press W to increase rotate clockwise , press S to rotate anticlockwise: ')

        if key == 'w':
            motor.spin(steps= step, sleep_time= time_sleep, clockwise=True)
            #current_postion_mm = motor.add_position_mm(input_step, lead_screw_pitch)
            #print("'My current position in mm is :", format(current_postion_mm,".2f"))
            
        elif key == 's':
            motor.spin(steps=step, sleep_time= time_sleep, clockwise=False)
            #current_postion_mm = motor.subtract_position_mm(input_step, lead_screw_pitch)
            #print("'My current position in mm is :", format(current_postion_mm,".2f"))

    
        elif key == 'b':
            break
        
   
      
  
    GPIO.cleanup()
  
