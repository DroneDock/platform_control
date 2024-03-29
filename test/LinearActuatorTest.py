# Standard Imports

# Third Party Imports
import RPi.GPIO as GPIO

# Project Specific Imports
from HardwareComponents.LinearActuator import LinearActuator


# Pin Definition ---------------------------------------------------------------
Motor1In1 = 29
Motor1In2 = 31
Motor1EN  = 32   # PWM Pin on Raspberry PI

GPIO.setmode(GPIO.BOARD)
LinearMotor = LinearActuator(In1=Motor1In1, In2=Motor1In2, EN=Motor1EN)

while True:

    key = input('Press W to increase duty cycle, press S to decrease: ')

    if key == 'w':
        LinearMotor.extend(100)
    elif key == 's':
        LinearMotor.retract(100)
    elif key == 'b':
        break

print("Program terminated.")
