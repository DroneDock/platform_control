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
2B: green
2A: black
1B: blue
1A: red
dir pin = GPIO 20 (int 38)
step pin = GPIO 21 (int 40)

Description: The leadscrew will extend and retract for a designated amount of times.
ISSUE: Once the program finished running, it will go into idle buzzing.
"""
lead_screw_pitch = 8 # mm
time_sleep = 0.0005 #don't change this (For full stepping, use 0.0004 - 0.0007s)
step = 200

if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)
    motor = LeadscrewStepperMotor(dir_pin=20, step_pin=21)
    
    #applies to current git config. Don't change sleep_time.
    

    # Runs it 3 times
    for i in range (2):
        # Extend platform
        motor.spin(steps= step, sleep_time= time_sleep, clockwise=True)

        #current_postion_mm = motor.add_position_mm(step,lead_screw_pitch)
        #print("Extension is ",current_postion_mm)
        time.sleep(0.7)
    
        # Retract platform
        # motor.spin(steps=step, sleep_time= time_sleep, clockwise=False)

        # time.sleep(0.7)

    GPIO.cleanup()