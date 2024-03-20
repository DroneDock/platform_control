"""
This script is to maunally calibrate the position of the keyhole. 

Config: DC motor not on your side 
Stepper motor wire facing you
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
#GPIO.output(Motor1In1, GPIO.HIGH)
#GPIO.output(Motor1In2, GPIO.LOW)

# Setup PWM
p = GPIO.PWM(Motor1EN, 2000)  # Set PWM frequency (in Hz)

# Start PWM signals, specifying the duty cycle (in %)
# Specify the DutyCycle (speed), max rate at 100
DutyCycle = 100
p.start(DutyCycle)

"""
Press W to go clockwise (down)
Press S to go anticlockwise (up)
Press b to stop
"""

while True:

    key = input('Press W to go clockwise, press S to go anticlockwise: ')

    if key == 'w':
        GPIO.output(Motor1In1, GPIO.HIGH)
        GPIO.output(Motor1In2, GPIO.LOW)
        print("Going clockwise")
    elif key == 's':
        GPIO.output(Motor1In1, GPIO.LOW)
        GPIO.output(Motor1In2, GPIO.HIGH)
        print("Going anticlockwise")
    elif key == 'b':
         break

   # p.ChangeDutyCycle(DutyCycle)
   # print(f"The duty cycle is {DutyCycle}")

# Stop PWM
p.stop()

GPIO.cleanup()
