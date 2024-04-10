# Standard Imports
import time

# Third-Party Imports
import RPi.GPIO as GPIO


class Electromagnet(object):
    
    def __init__(self, relay_pin1=11, relay_pin2=36):
        self.relay_pin1 = relay_pin1
        self.relay_pin2 = relay_pin2
        
    def activate(self):
        print("Activating electromagnet, turning off LED")
        GPIO.output(self.relay_pin1, GPIO.HIGH)
        GPIO.output(self.relay_pin2, GPIO.LOW)

    def deactivate(self):
        print("Deactivating electromagnet, turning on LED")
        GPIO.output(self.relay_pin1, GPIO.LOW)
        GPIO.output(self.relay_pin2, GPIO.LOW)
        