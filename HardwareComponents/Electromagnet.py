# Standard Imports
import time

# Third-Party Imports
import RPi.GPIO as GPIO


class Electromagnet(object):
    
    def __init__(self, relay_pin1=14, relay_pin2=15):
        GPIO.setmode(GPIO.BCM)
        self.relay_pin1 = relay_pin1 # Electromagnet
        self.relay_pin2 = relay_pin2 # LED
        GPIO.setup(self.relay_pin1, GPIO.OUT)
        GPIO.setup(self.relay_pin2, GPIO.OUT)
        
    def activate(self):
        print("Activating electromagnet, turning off LED")
        GPIO.output(self.relay_pin1, GPIO.HIGH)
        GPIO.output(self.relay_pin2, GPIO.HIGH)

    def deactivate(self):
        print("Deactivating electromagnet, turning on LED")
        GPIO.output(self.relay_pin1, GPIO.LOW)
        GPIO.output(self.relay_pin2, GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()
    