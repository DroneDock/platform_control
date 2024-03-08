"""
Run this script to test DC Motor is working

Common Issues:

Issue 1: Running the code the first time does not return an error, but DC motor
does not operate as expected. Running the code again shows a warning about
"channel being in use".
Solution: Check that the motor driver is grounded to the Raspberry Pi.
"""

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
DutyCycle = 0
p.start(DutyCycle)

while True:

    key = input('Press W to increase duty cycle, press S to decrease: ')

    if key == 'w':
        if (DutyCycle < 100):
            DutyCycle += 10
    elif key == 's':
        if (DutyCycle > 0):
            DutyCycle -= 10
    elif key == 'b':
         break

    p.ChangeDutyCycle(DutyCycle)
    print(f"The duty cycle is {DutyCycle}")

# Stop PWM
p.stop()

GPIO.cleanup()
