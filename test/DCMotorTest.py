"""Run this script to test DC Motor is working"""

# Standard Imports
import time

# Third Party Imports
import RPi.GPIO as GPIO


# Pin Definition using BCM numbering system -----------------------------------
Motor1In1 = 17
Motor1In2 = 27
Motor1EN  = 18   # PWM Pin on Raspberry PI
GPIO.setmode(GPIO.BCM)

GPIO.setup(Motor1In1, GPIO.OUT)
GPIO.setup(Motor1In2, GPIO.OUT)
GPIO.setup(Motor1EN, GPIO.OUT)

# Specify direction
GPIO.output(Motor1In1, GPIO.HIGH)
GPIO.output(Motor1In2, GPIO.LOW)

# Setup PWM
p = GPIO.PWM(Motor1EN, 2000)  # Set PWM frequency (in Hz)

# Start PWM signals, specifying the duty cycle (in %)
DutyCycle = 50
p.start(DutyCycle)

while True:

    key = input('Press W to increase duty cycle, press S to decrease: ')

    match key:
            case 'w':
                if (DutyCycle < 100):
                    DutyCycle += 10
            case 's':
                if (DutyCycle > 0):
                    DutyCycle -= 10
            case 'b':
                break

    p.ChangeDutyCycle(DutyCycle)
    print(f"The duty cycle is {DutyCycle}")

# Stop PWM
p.stop()

GPIO.cleanup()