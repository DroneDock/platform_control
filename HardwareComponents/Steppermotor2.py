import RPi.GPIO as GPIO
import time

# Pin Definitions





class StepperMotor(object):
    def __init__(self, steps_per_revolution = 200, dir_pin: int = 38, step_pin: int = 40):
        
        GPIO.cleanup()
        
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.steps_per_revolution = steps_per_revolution
        

        GPIO.setmode(GPIO.BOARD)


        # Configure Pins
        GPIO.setup(dir_pin, GPIO.OUT)
        GPIO.setup(step_pin, GPIO.OUT)
        

        #Current position of lead screw (in steps)
        self.current_postion = 0


    



    def spin(self, steps ,sleep_time,clockwise=True ):

        """
        dirPin = High for clockwise
        """
        GPIO.output(self.dir_pin, GPIO.HIGH if clockwise else GPIO.LOW)
        # Set motor direction
        #GPIO.output(self.dir_pin, GPIO.HIGH)

        # Spin motor
        for _ in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(sleep_time)  # Delay in seconds
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(sleep_time)  # Delay in seconds
                
            
           