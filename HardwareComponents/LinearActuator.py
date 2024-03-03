# Third Party Imports
import RPi.GPIO as GPIO


class LinearActuator(object):

    def __init__(self, In1: int, In2: int, EN:int, input_mode=GPIO.BCM):
        """Initialize a Linear Actuator class used to control the motor.

        Args:
            In1 (int): First GPIO pin number (BCM) connected to H Bridge of 
            motor driver.

            In2 (int): Second GPIO pin number (BCM) connected to H Bridge of 
            motor driver.

            EN  (int): The ENABLE pin number (BCM) connected to the PWM connection of 
            the motor driver used to control motor speed.
        """

        # Configure Pins
        self._in1Pin = In1
        self._in2Pin = In2
        self._PWMPin = EN

        GPIO.setup(In1, GPIO.OUT)
        GPIO.setup(In2, GPIO.OUT)
        GPIO.setup(EN, GPIO.OUT)

        # Configure and start PWM
        self._PWM = GPIO.PWM(self._PWMPin, 2000)  # Set PWM frequency as 2000
        self._PWM.start(50)   # Start the PWM instance at zero duty cycle (i.e. static)


    def extend(self, dutyCycle:int = 100) -> None:
        """(Public) Extend the Linear Actuator at a given duty cycle.

        Args:
            DutyCycle (int, optional): PWM duty cycle supplied to the linear actuator. Defaults to 100.
        """
        
        GPIO.output(self._in1Pin, GPIO.LOW)
        GPIO.output(self._in2Pin, GPIO.HIGH)
        self._PWM.ChangeDutyCycle(dutyCycle)


    def retract(self, dutyCycle:int = 100) -> None:
        """(Public) Retract the linear actuator at a given duty cycle,

        Args:
            DutyCycle (int, optional): PWM duty cycle supplied to the linear actuator. Defaults to 100.
        """

        GPIO.output(self._in1Pin, GPIO.HIGH)
        GPIO.output(self._in2Pin, GPIO.LOW)
        self._PWM.ChangeDutyCycle(dutyCycle)


    def __del__(self):
        """Destructor to cleanup GPIO ports"""
        GPIO.cleanup()
    