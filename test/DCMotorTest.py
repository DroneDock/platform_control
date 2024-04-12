"""
Author: Ken

Description:
- Cable config for L298N motor driver: With heat sink positioned at the left 
side, place the black wire to the left of the red wire.

How to use:
W (clockwise is make platform tilt up/ goes back)
s (anticlockwise makes platform tilt down/ goes forward)

Progress:
This is working with the new soldering (April 12)
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

    try:
        key = input('Press W to go clockwise, press S to go anticlockwise: ')

        if key == 'w':  # Goes backwards
            GPIO.output(Motor1In1, GPIO.HIGH)
            GPIO.output(Motor1In2, GPIO.LOW)
            print("Going clockwise")
        elif key == 's': # Goes forward
            GPIO.output(Motor1In1, GPIO.LOW)
            GPIO.output(Motor1In2, GPIO.HIGH)
            print("Going anticlockwise")
        elif key == 'b':
            p.stop()
            break

   # p.ChangeDutyCycle(DutyCycle)
   # print(f"The duty cycle is {DutyCycle}")
    except KeyboardInterrupt:

        # Stop PWM
        p.stop()
        GPIO.cleanup()

GPIO.cleanup()
