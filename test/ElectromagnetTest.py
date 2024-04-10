import RPi.GPIO as GPIO
import time


"""
Configuration:

+ve electromagnet to NO
+ve power supply (5V) to COM
-ve electromagnet to -ve power supply
relay pin to 36
VCC to 5V
GND to GND

Works with battery, output is 0.6A

LED needs a 470 capacitor. Can be powered by 3.3V of Raspberry Pi
Red LED +ve connect to NC
RED LED +ve to GND
Green LED +ve to NO
Green LED -ve to GND
"""

# Define GPIO pins
relay_pin1 = 11  # Change this to the GPIO pin connected to the relay
relay_pin2 = 36 #LED

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay_pin1, GPIO.OUT)
GPIO.setup(relay_pin2, GPIO.OUT)

def turn_on_electromagnet():
    GPIO.output(relay_pin1, GPIO.HIGH)
    print("Electromagnet turned ON")
    GPIO.output(relay_pin2, GPIO.HIGH)
    

def turn_off_electromagnet():
    GPIO.output(relay_pin1, GPIO.LOW)
    print("Electromagnet turned OFF")
    GPIO.output(relay_pin2, GPIO.LOW)
    print("LED turned OFF")

try:
    while True:
        command = input("Enter command (on/off/exit): ").strip().lower()

        if command == 'on':
            turn_on_electromagnet()
        elif command == 'off':
            turn_off_electromagnet()
        elif command == 'exit':
            break
        else:
            print("Invalid command")

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
