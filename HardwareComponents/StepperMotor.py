# Standard Imports
import time

# Third Party Imports
import RPi.GPIO as GPIO


class StepperMotor(object):

    def __init__(self, steps_per_revolution = 200, coilA1Pin: int = 11, coilA2Pin: int = 12, coilB1Pin: int = 13, coilB2Pin: int = 15):
        """Initialize a Stepper Motor class used to control the motor.
        int 11 = GPIO17
        int 12 = GPIO18
        int 13 = GPIO27
        int 15 = GPIO22
        
        Pin numbering is currently denoted by the physical system.

        Args:
        """
        GPIO.cleanup()
        
        self.coilA1Pin = coilA1Pin
        self.coilA2Pin = coilA2Pin
        self.coilB1Pin = coilB1Pin
        self.coilB2Pin = coilB2Pin
        self.steps_per_revolution = steps_per_revolution

        GPIO.setmode(GPIO.BOARD)


        # Configure Pins
        GPIO.setup(coilA1Pin, GPIO.OUT)
        GPIO.setup(coilA2Pin, GPIO.OUT)
        GPIO.setup(coilB1Pin, GPIO.OUT)
        GPIO.setup(coilB2Pin, GPIO.OUT)

        #Current position of lead screw (in steps)
        self.current_postion = 0 

    def set_step(self, A1, A2, B1, B2):
        GPIO.output(self.coilA1Pin, A1)
        GPIO.output(self.coilA2Pin, A2)
        GPIO.output(self.coilB1Pin, B1)
        GPIO.output(self.coilB2Pin, B2)

    def step_clockwise(self, steps, sleep_time):

        # Clockwise sequence
        seq_cw = [(GPIO.HIGH, GPIO.LOW , GPIO.LOW , GPIO.LOW ),
                  (GPIO.LOW , GPIO.HIGH, GPIO.LOW , GPIO.LOW ),
                  (GPIO.LOW , GPIO.LOW , GPIO.HIGH, GPIO.LOW ),
                  (GPIO.LOW , GPIO.LOW , GPIO.LOW , GPIO.HIGH)]

        for _ in range(steps):
            for seq in seq_cw:
                self.set_step(*seq)
                time.sleep(sleep_time)

    def step_anticlockwise(self, steps, sleep_time):

        # Anticlockwise sequence
        seq_ccw = [(GPIO.LOW , GPIO.LOW , GPIO.LOW , GPIO.HIGH),
                   (GPIO.LOW , GPIO.LOW , GPIO.HIGH, GPIO.LOW ),
                   (GPIO.LOW , GPIO.HIGH, GPIO.LOW , GPIO.LOW ),
                   (GPIO.HIGH, GPIO.LOW , GPIO.LOW , GPIO.LOW )]

        for _ in range(steps):
            for seq in seq_ccw:
                self.set_step(*seq)
                time.sleep(sleep_time)


    def add_position_mm(self, steps, lead_screw_pitch):
        """
        Lead screw pitch is 2.0mm
        Steps per revolution is set to 200steps (Nema 17)
        
        Code already multiplies by the number of step you input.
        """        
        for _ in range(steps):
           self.current_postion = self.current_postion + (lead_screw_pitch / self.steps_per_revolution) #this is for one step
            
        return self.current_postion
    

    def subtract_position_mm(self, steps, lead_screw_pitch):
        for _ in range(steps):
            self.current_postion = self.current_postion - (lead_screw_pitch / self.steps_per_revolution)
        return self.current_postion
    
    def step(self, step_count):

        i = 0

        try:

            for i in range(step_count):

                if i%4==0:
                    GPIO.output(self.coilA1Pin, GPIO.LOW)
                    GPIO.output(self.coilA2Pin, GPIO.LOW)
                    GPIO.output(self.coilB1Pin, GPIO.LOW)
                    GPIO.output(self.coilB2Pin, GPIO.HIGH)

                elif i%4==1:
                    GPIO.output(self.coilA1Pin, GPIO.LOW)
                    GPIO.output(self.coilA2Pin, GPIO.HIGH)
                    GPIO.output(self.coilB1Pin, GPIO.LOW)
                    GPIO.output(self.coilB2Pin, GPIO.HIGH)

                elif i%4==2:
                    GPIO.output(self.coilA1Pin, GPIO.LOW)
                    GPIO.output(self.coilA2Pin, GPIO.LOW)
                    GPIO.output(self.coilB1Pin, GPIO.HIGH)
                    GPIO.output(self.coilB2Pin, GPIO.LOW)

                elif i%4==3:
                    GPIO.output(self.coilA1Pin, GPIO.HIGH)
                    GPIO.output(self.coilA2Pin, GPIO.LOW)
                    GPIO.output(self.coilB1Pin, GPIO.LOW)
                    GPIO.output(self.coilB2Pin, GPIO.LOW)

                time.sleep(0.002)  # Sleep for 2ms between loops (probably to prevent overheat?)

        except KeyboardInterrupt:
            GPIO.output(self.coilA1Pin, GPIO.LOW)
            GPIO.output(self.coilA2Pin, GPIO.LOW)
            GPIO.output(self.coilB1Pin, GPIO.LOW)
            GPIO.output(self.coilB2Pin, GPIO.LOW)

            print("Program has terminated")

            GPIO.cleanup()

        print("Exiting STEP function")


    def stop(self):

        GPIO.output(self.coilA1Pin, GPIO.LOW)
        GPIO.output(self.coilA2Pin, GPIO.LOW)
        GPIO.output(self.coilB1Pin, GPIO.LOW)
        GPIO.output(self.coilB2Pin, GPIO.LOW)


    # def __del__(self):
    #     """Destructor to perform cleanup operations"""

    #     GPIO.output(self.coilA1Pin, GPIO.LOW)
    #     GPIO.output(self.coilA2Pin, GPIO.LOW)
    #     GPIO.output(self.coilB1Pin, GPIO.LOW)
    #     GPIO.output(self.coilB2Pin, GPIO.LOW)
    #     GPIO.cleanup()


class BaseStepperMotor(object):
    def __init__(self, ena_pin: int = 23, dir_pin: int = 20, pul_pin: int = 25):
        """
        Initialize a BaseStepperMotor class used to control the stepper motor
        located at the base that controls yaw of the entire platform. The
        implementation of this class assumes the stepper motor is connected to
        the TB6600 motor driver.
        """
        
        GPIO.cleanup()  # For a clean slate
        
        self.ena_pin = ena_pin  # Enable Pin
        self.dir_pin = dir_pin  # Direction Pin
        self.pul_pin = pul_pin  # Pulse Pin

        GPIO.setmode(GPIO.BCM)

        # Configure Pins
        GPIO.setup(ena_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)
        GPIO.setup(pul_pin, GPIO.OUT)

    
    def spin(self, steps, sleep_time, clockwise=True):
        """
        Rotate the stepper motor by designated number of steps in the clockwise
        or anticlockwise direction. The rotation speed is set by `sleep_time`.
        """
        # Enable motor driver
        GPIO.output(self.ena_pin, GPIO.HIGH)
        
        # Set motor direction: HIGH for clockwise, LOW for anticlockwise
        GPIO.output(self.dir_pin, GPIO.HIGH if clockwise else GPIO.LOW)

        # Spin motor
        for _ in range(steps):
            GPIO.output(self.pul_pin, GPIO.HIGH)
            time.sleep(sleep_time)  # Delay in seconds
            GPIO.output(self.pul_pin, GPIO.LOW)
            time.sleep(sleep_time)  # Delay in seconds
        
        # Disable motor driver after spinning
        GPIO.output(self.ena_pin, GPIO.LOW)      


class LeadscrewStepperMotor(object):
    def __init__(self, dir_pin: int = 20, step_pin: int = 21):
        """Initialize a stepper motor class used to control the leadscrew.
        This assumes the leadscrew is connected to the RED motor driver.
        """
        
        GPIO.cleanup()
        self.dir_pin = dir_pin    # Direction Pin
        self.step_pin = step_pin  # Step Pin
        GPIO.setmode(GPIO.BCM)

        # Configure Pins
        GPIO.setup(dir_pin, GPIO.OUT)
        GPIO.setup(step_pin, GPIO.OUT)


    def spin(self, steps, sleep_time, clockwise=True):

        GPIO.output(self.dir_pin, GPIO.HIGH if clockwise else GPIO.LOW)

        # Spin motor
        for _ in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(sleep_time)  # Delay in seconds
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(sleep_time)  # Delay in seconds