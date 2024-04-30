import RPi.GPIO as GPIO
import time

# Define GPIO pins in BCM mode
TRIG_PIN1 = 10  # Broadcom SOC channel for the ultrasonic sensor's trigger
ECHO_PIN1 = 9  # Broadcom SOC channel for the ultrasonic sensor's echo


# Define GPIO pins in BCM mode
TRIG_PIN2 = 10  # Broadcom SOC channel for the ultrasonic sensor's trigger
ECHO_PIN2 = 9  # Broadcom SOC channel for the ultrasonic sensor's echo


# Setup GPIO
def setup():
    GPIO.setmode(GPIO.BCM)  # Set Broadcom SOC channel numbering
    GPIO.setup(TRIG_PIN1, GPIO.OUT)  # Trigger Pin as output
    GPIO.setup(ECHO_PIN1, GPIO.IN)  # Echo Pin as input
    GPIO.output(TRIG_PIN1, GPIO.LOW)

    # GPIO.setup(TRIG_PIN2, GPIO.OUT)  # Trigger Pin as output
    # GPIO.setup(ECHO_PIN2, GPIO.IN)  # Echo Pin as input
    # GPIO.output(TRIG_PIN2, GPIO.LOW)

    time.sleep(2)  # Settle time for sensor

# Get distance measurement
def get_distance1():
    # Send 10us pulse to TRIG_PIN
    GPIO.output(TRIG_PIN1, GPIO.HIGH)
    time.sleep(0.00001)  # Wait for 10 microseconds
    GPIO.output(TRIG_PIN1, GPIO.LOW)

    
    pulse_start_time = time.time()
    pulse_end_time = time.time()

    # Wait for the echo to be received
    while GPIO.input(ECHO_PIN1) == GPIO.LOW:
        pulse_start_time = time.time()
        #print(f'{pulse_start_time=}')

    while GPIO.input(ECHO_PIN1) == GPIO.HIGH:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)  # Calculate distance in cm

    return distance

# def get_distance2():
#     # Send 10us pulse to TRIG_PIN
#     GPIO.output(TRIG_PIN2, GPIO.HIGH)
#     time.sleep(0.00001)  # Wait for 10 microseconds
#     GPIO.output(TRIG_PIN2, GPIO.LOW)


    
#     pulse_start_time = time.time()
#     pulse_end_time = time.time()

#     # Wait for the echo to be received
#     while GPIO.input(ECHO_PIN2) == GPIO.LOW:
#         pulse_start_time = time.time()
#         #print(f'{pulse_start_time=}')

#     while GPIO.input(ECHO_PIN2) == GPIO.HIGH:
#         pulse_end_time = time.time()

#     pulse_duration = pulse_end_time - pulse_start_time
#     distance = round(pulse_duration * 17150, 2)  # Calculate distance in cm

#     return distance

def cleanup():
    GPIO.cleanup()  # Clean up GPIO to reset ports used in this session

if __name__ == '__main__':
    try:
        setup()
        while True:
            distance1 = get_distance1()
            print(f"Distance1: {distance1} cm")
            print()
            print()
            time.sleep(1)  # Delay to not spam the sensor, allows for settling

            # distance2 = get_distance2()
            # print(f"Distance2: {distance2} cm")
            # time.sleep(1)  # Delay to not spam the sensor, allows for settling
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    finally:
        cleanup()
