import time

import RPi.GPIO as GPIO

from HardwareComponents.Steppermotor2 import StepperMotor
"""
This is for Bottom Stepper Motor


For reference: https://how2electronics.com/control-stepper-motor-with-a4988-driver-arduino/
Motor driver position A4988
2B: orange
2A: blue
1B: green
1A: yellow
dir pin = GPIO 20 (int 38)
step pin = GPIO 21 (int 40)
"""

time_sleep = 0.0009 #don't change this
step = 200

if __name__ == '__main__':


    motor = StepperMotor()
    
    #applies to current git config. Don't change sleep_time. Applies for all stepper motor.

    #retracts platform
    motor.spin(steps= step, sleep_time= time_sleep, clockwise=True)



    #adds a delay
    time.sleep(1)
    
    #extends platform
    motor.spin(steps= step, sleep_time= time_sleep, clockwise=False)


   

    GPIO.cleanup()
