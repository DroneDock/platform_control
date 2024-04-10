"""Takes IMU reading, independent of DC motor movement.

DC motor moves from point a to point B, IMU keeps taking readings

"""

"""
Used to get angles of IMU. Code not in use anymore.
"""

"""
Cable config:
L298N motor driver
Heat sink to your left.
left to right: black, red

W (clockwise is make platform tilt up)
s (anticlockwise makes platform tilt down)

Can be used for callibration

"""

# Standard Imports
import time
import matplotlib.pyplot as plt
import numpy as np

# Project-Specific Imports
from HardwareComponents.IMU import AdafruitBNO055
import RPi.GPIO as GPIO

# Pin Definition using BCM numbering system -----------------------------------
Motor1In1 = 17
Motor1In2 = 27
Motor1EN  = 18   # PWM Pin on Raspberry PI
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

GPIO.setup(Motor1In1, GPIO.OUT)
GPIO.setup(Motor1In2, GPIO.OUT)
GPIO.setup(Motor1EN, GPIO.OUT)

# Setup PWM
p = GPIO.PWM(Motor1EN, 2000)  # Set PWM frequency (in Hz)

# Initialize lists to store angle values
yaw_values = []
roll_values = []
pitch_values = []
new_D_values = []
timestamps = []

# Start PWM signals, specifying the duty cycle (in %)
# Specify the DutyCycle (speed), max rate at 100
DutyCycle = 80
p.stop()

time.sleep(3)

# Start time
start_time = time.time()

"""
Press W to go clockwise (down)
Press S to go anticlockwise (up)
Press b to stop
"""


## ========================================================================= ##

if __name__ == '__main__':
    
    IMU = AdafruitBNO055()

    while True:
        current_time = time.time() - start_time
        
        # Read Euler angles from IMU
        yaw, roll, pitch = IMU.eulerAngles
        print(f"Yaw : {IMU.eulerAngles[0]}")
        print(f"ROll : {IMU.eulerAngles[1]}")
        print(f"Pitch : {IMU.eulerAngles[2]}")
        new_D = (abs(roll) - 43)
        print(new_D)
        print()
        # Append values to lists
        yaw_values.append(yaw)
        roll_values.append(roll)
        pitch_values.append(pitch)
        new_D_values.append(new_D)
        timestamps.append(current_time)
        
        # Clear the axis and plot the data
        plt.clf()
        
        plt.plot(timestamps, yaw_values, label='Yaw', color='r')
        plt.plot(timestamps, roll_values, label='Roll', color='g')
        plt.plot(timestamps, pitch_values, label='Pitch', color='b')
        plt.plot(timestamps, new_D_values, label='new_D', color='y')
        
        # Add legend
        plt.legend()
        # Set up the plot
        plt.xlabel('Time')
        plt.ylabel('Angle (degrees)')
        plt.title('IMU Euler Angles')
        
        # Show plot
        plt.pause(0.001)
        plt.savefig('IMU2.png')

        # Wait for a short duration
        time.sleep(0.1)


        key = input('Press W to go clockwise, press S to go anticlockwise: ')

        if key == 'w':
            p.start(DutyCycle)
            GPIO.output(Motor1In1, GPIO.HIGH)
            GPIO.output(Motor1In2, GPIO.LOW)

            print("Going clockwise")
        elif key == 's':
            p.start(DutyCycle)
            GPIO.output(Motor1In1, GPIO.LOW)
            GPIO.output(Motor1In2, GPIO.HIGH)
            print("Going anticlockwise")
        elif key == 'b':
            p.stop()


GPIO.cleanup()
