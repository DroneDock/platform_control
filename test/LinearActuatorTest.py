# Standard Imports

# Third Party Imports

# Project Specific Imports
from ..HardwareComponents.LinearActuator import LinearActuator


# Pin Definition ---------------------------------------------------------------
Motor1In1 = 29
Motor1In2 = 31
Motor1EN  = 32   # PWM Pin on Raspberry PI

LinearMotor = LinearActuator(In1=Motor1In1, In2=Motor1In2, EN=Motor1EN)


while True:

    key = input('Press W to increase duty cycle, press S to decrease: ')

    match key:
        case 'w':
            LinearMotor.extend(100)
        case 's':
            LinearMotor.retract(100)
        case 'b':
            break
