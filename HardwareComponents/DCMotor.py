# Standard Imports
import time
# Third Party Imports
import RPi.GPIO as GPIO


class  DCMotor(object):
    """
    DC motor class to control the motor.
    
    This class is developed based on the DC motor directly controlling arm
    angle. The methods "forward" and "backward" assumes the following cable
    config:
    
    With heat sink positioned at the left side, place the black wire to the 
    left of the red wire.
    """

    def __init__(self, In1: int = 17, In2: int = 27, EN: int = 18):
        """Initialize a DC Motor class used to control the motor.

        Args:
            In1 (int): First GPIO pin number (BCM) connected to H Bridge of 
            motor driver.

            In2 (int): Second GPIO pin number (BCM) connected to H Bridge of 
            motor driver.

            EN  (int): The ENABLE pin number (BCM) connected to the PWM 
            connection of the motor driver used to control motor speed.
        """

        # Configure Pins
        GPIO.setmode(GPIO.BCM)
        self._in1Pin = In1
        self._in2Pin = In2
        self._PWMPin = EN

        GPIO.setup(In1, GPIO.OUT)
        GPIO.setup(In2, GPIO.OUT)
        GPIO.setup(EN, GPIO.OUT)

        # Configure and start PWM
        self._PWM = GPIO.PWM(self._PWMPin, 2000)  # Set PWM frequency as 2000
        self._PWM.start(0)   # Start the PWM instance at zero duty cycle (i.e. static)

    def forward(self, dutyCycle:int = 100, duration:int = -1) -> None:
        """(Public) Rotate the DC motor clockwise at a given duty cycle for a
        specified duration.

        Args:
            dutyCycle (int, optional): PWM duty cycle supplied to the motor. 
            Defaults to 100.
            duration (int, optional): Duration in seconds for which the motor
            will rotate. Default is -1, which causes continuous rotation.
        """
        GPIO.output(self._in1Pin, GPIO.LOW)
        GPIO.output(self._in2Pin, GPIO.HIGH)
        self._PWM.ChangeDutyCycle(dutyCycle)
        
        if duration >= 0:
            time.sleep(duration)
            self._PWM.ChangeDutyCycle(0)
            self.stop()

    def backward(self, dutyCycle:int = 100, duration: int = -1) -> None:
        """(Public) Rotate the DC Motor anticlockwise at a given duty cycle for
        a specified duration.

        Args:
            DutyCycle (int, optional): PWM duty cycle supplied to the motor.
            Defaults to 100.
            duration (int, otption): Duration in seconds for which the motor
            will rotate. Default is -1, which causes continuous rotation.
        """
        GPIO.output(self._in1Pin, GPIO.HIGH)
        GPIO.output(self._in2Pin, GPIO.LOW)
        self._PWM.ChangeDutyCycle(dutyCycle)
        
        if duration >= 0:
            time.sleep(duration)
            self._PWM.ChangeDutyCycle(0)
            self.stop()

    def stop(self) -> None:
        """
        (Public) Stop the DC motor from rotating.
        
        Implementation: set the duty cycle to zero. (might be unsafe to leave PWM channel open?)
        """
        self._PWM.ChangeDutyCycle(0)

    def __del__(self):
        """Destructor to cleanup GPIO ports"""
        self._PWM.stop()
        GPIO.cleanup()
    