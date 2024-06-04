# Standard Imports
import time
# Third-Party Imports
import RPi.GPIO as GPIO

class ServoMotor(object):
    
    def __init__(self, servo_pin: int = 5):
        
        self.SERVO_PIN = servo_pin
        GPIO.setup(self.SERVO_PIN, GPIO.OUT)
        time.sleep(5)  # This should be sufficiently long if it takes reading from the ultrasonic sensor
        
        # Create PWM instance
        self._PWM = GPIO.PWM(servo_pin, 50)  # 50Hz (20ms period)
        # Start PWM
        self._PWM.start(0)
        
    def set_angle(self, angle: int):
        
        duty = angle / 18 + 2
        GPIO.output(self.SERVO_PIN, True)
        self._PWM.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(self.SERVO_PIN, False)
        self._PWM.ChangeDutyCycle(0)
        
    def __del__(self):
        self.set_angle(0)
