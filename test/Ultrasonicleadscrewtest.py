import RPi.GPIO as GPIO
import time
from HardwareComponents.Steppermotor2 import StepperMotor

# Define GPIO pins
TRIG_PIN = 23  # GPIO pin for the ultrasonic sensor's trigger
ECHO_PIN = 32  # GPIO pin for the ultrasonic sensor's echo

lead_screw_pitch = 8 #mm
time_sleep = 0.0005 #don't change this
step = 10


def setup():
    # Set GPIO mode
    GPIO.setmode(GPIO.BOARD)

    # Setup GPIO pins
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
    # Send a pulse to the ultrasonic sensor
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Wait for the echo response
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Calculate distance based on the time difference between the pulses
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound (343 m/s) / 2
    distance = round(distance, 2)  # Round to 2 decimal places

    return distance



def cleanup():
    # Cleanup GPIO
    GPIO.cleanup()

if __name__ == '__main__':

    motor = StepperMotor()

    try:
        setup()

        # Main loop
        while True:
            distance = get_distance()
            print("Distance:", distance, "cm")
            #time.sleep(0.05)  # Wait for 1 second before taking the next measurement
            
            

            if (30<= distance <= 60):
                step_distance = int (step*(distance-30))
                motor.spin(steps= step_distance, sleep_time= time_sleep, clockwise=True)
                time.sleep(1)
            elif (distance < 30):
                step_distance = int (step*(30-distance))
                motor.spin(steps=step_distance, sleep_time= time_sleep, clockwise=False)
                time.sleep(1)
            

    except KeyboardInterrupt:
        print("Program terminated by user")
    
    finally:
        cleanup()
