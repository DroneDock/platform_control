import time

import RPi.GPIO as GPIO

from HardwareComponents.StepperMotor import StepperMotor


if __name__ == '__main__':


    motor = StepperMotor()

    motor.step_anticlockwise(steps=1000, sleep_time=0.001)

    GPIO.cleanup()
