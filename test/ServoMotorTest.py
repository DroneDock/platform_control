"""
Run this code to test if servo motor rotates to designated angle
"""
# Standard Imports
import time

# Third-Party Imports
import RPi.GPIO as GPIO


# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as output
servo_pin = 19
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM instance
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz (20 ms period)

# Start PWM
pwm.start(0)

# Function to set servo angle
def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        # Move servo to 0 degrees
        set_angle(0)
        time.sleep(1)

        # Move servo to 90 degrees
        set_angle(120)
        time.sleep(1)

        # Move servo to 180 degrees
        set_angle(0)
        time.sleep(1)

# Clean up GPIO on Ctrl+C exit
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
