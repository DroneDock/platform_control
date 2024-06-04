import RPi.GPIO as GPIO
import time

class UltrasonicSensor(object):
    
    def __init__(self, trig_pin: int = 10, echo_pin: int = 9):
        
        self.TRIG_PIN = trig_pin
        self.ECHO_PIN = echo_pin
        
        GPIO.setup(self.TRIG_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)        
        GPIO.output(self.TRIG_PIN, GPIO.LOW)
        
        time.sleep(2)
        
    def get_distance(self):
        # Send 10us pulse to TRIG_PIN
        GPIO.output(self.TRIG_PIN, GPIO.HIGH)
        time.sleep(0.00001)  # Wait for 10 microseconds
        GPIO.output(self.TRIG_PIN, GPIO.LOW)

        
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        # Wait for the echo to be received
        while GPIO.input(self.ECHO_PIN) == GPIO.LOW:
            pulse_start_time = time.time()
            if (time.time() - pulse_start_time) > 3:
                break

        while GPIO.input(self.ECHO_PIN) == GPIO.HIGH:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)  # Calculate distance in cm

        return distance
    
    def __del__(self):
        GPIO.cleanup()
                
                
                       