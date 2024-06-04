import RPi.GPIO as GPIO
import time

# Define GPIO pins in BCM mode
TRIG_PIN = 10  # Broadcom SOC channel for the ultrasonic sensor's trigger
ECHO_PIN = 9  # Broadcom SOC channel for the ultrasonic sensor's echo

# Setup GPIO
def setup():
    GPIO.setmode(GPIO.BCM)  # Set Broadcom SOC channel numbering
    GPIO.setup(TRIG_PIN, GPIO.OUT)  # Trigger Pin as output
    GPIO.setup(ECHO_PIN, GPIO.IN)  # Echo Pin as input
    GPIO.output(TRIG_PIN, GPIO.LOW)

    time.sleep(2)  # Settle time for sensor

# Get distance measurement
def get_distance():
    # Send 10us pulse to TRIG_PIN
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)  # Wait for 10 microseconds
    GPIO.output(TRIG_PIN, GPIO.LOW)

    
    pulse_start_time = time.time()
    pulse_end_time = time.time()

    # Wait for the echo to be received
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start_time = time.time()

    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)  # Calculate distance in cm

    return distance

def cleanup():
    GPIO.cleanup()  # Clean up GPIO to reset ports used in this session

if __name__ == '__main__':
    try:
        setup()
        while True:
            distance1 = get_distance()
            print(f"Distance1: {distance1} cm")
            print()
            print()
            time.sleep(1)  # Delay to not spam the sensor, allows for settling
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    finally:
        cleanup()
