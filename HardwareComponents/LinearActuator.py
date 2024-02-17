# Third Party Imports
import RPi.GPIO as GPIO


class LinearActuator(object):

    def __init__(self, In1: int, In2: int, EN:int , mode=GPIO.BOARD):
        """Initialize a Linear Actuator class used to control the motor.

        Args:
            In1 (int): First GPIO pin number connected to H Bridge of motor driver.

            In2 (int): Second GPIO pin number connected to H Bridge of motor driver.

            EN  (int): The pin number connected to the PWM connection of the
            motor driver used to control motor speed.

            mode (, optional): Defines the pin numbering system, either 
            GPIO.BOARD or GPIO.BCM. Defaults to GPIO.BOARD.
        """

        self.In1Pin = In1
        self.In2Pin = In2
        self.PWMPin = EN

        # Configure Pins
        GPIO.setmode(mode)
        GPIO.setup(self.In1Pin, GPIO.OUT)
        GPIO.setup(self.In2Pin, GPIO.OUT)
        GPIO.setup(self.PWMPin, GPIO.OUT)

        # Configure and start PWM
        self.PWM = GPIO.PWM(self.PWMPin, 2000)  # Set PWM frequency as 2000
        self.PWM.start(50)   # Start the PWM instance at zero duty cycle (i.e. static)

    def extend(self, DutyCycle:int = 100):
        
        GPIO.output(self.In1Pin, GPIO.LOW)
        GPIO.output(self.In2Pin, GPIO.HIGH)
        self.PWM.ChangeDutyCycle(DutyCycle)

    def retract(self, DutyCycle:int = 100):

        GPIO.output(self.In1Pin, GPIO.HIGH)
        GPIO.output(self.In2Pin, GPIO.LOW)
        self.PWM.ChangeDutyCycle(DutyCycle)


    def __del__(self):
        """Destructor to cleanup GPIO ports
        """
        GPIO.cleanup()
    