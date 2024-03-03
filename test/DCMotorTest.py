"""
Limiting the motion of the arm to  +- 30 degrees
"""
# Standard Imports
import time

# Third Party Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import RPi.GPIO as GPIO

# Project-Specific Imports
from HardwareComponents.DCMotor import DCMotor
from HardwareComponents.IMU import AdafruitBNO055

# Initialize Objects ----------------------------------------------------------
dcMotor = DCMotor(In1=17, In2=27, EN=18)
IMU = AdafruitBNO055()

# Plotting --------------------------------------------------------------------
t_data = []
angle_data = []

fig, ax = plt.subplots()
line, = plt.plot([], [], 'r-')
ax.set_xlim(0, 20)
ax.set_ylim(-360, 360)
ax.hold(True)

try:

    # Make sure the angle is initially +-10
    angle = IMU.eulerAngle(wrap=True)[0]
    
    while (angle > 10) and (angle < -10):
        if (angle > 10):
            dcMotor.clockwise(100)
        elif (angle < -10):
            dcMotor.anticlockwise(100)
        else:
            dcMotor.clockwise(100)

    # Main control algorithm
    start_time = time.time()

    while True:
        try:
            # Data Plotting
            current_time = time.time() - start_time
            yaw = IMU.eulerAngle(wrap=True)[0]  # Change subscript to match either roll pitch or yaw

            t_data.append(current_time)
            angle_data.append(yaw)


    
            # Control Algorithm
            if (yaw < -30):
                print("Rotating anticlockwise")
                dcMotor.clockwise(100)
            elif (yaw > 30):
                print("Rotating clockwise")
                dcMotor.anticlockwise(100)

            print(yaw)

            animation = FuncAnimation(fig, update, interval=100)

        except KeyboardInterrupt:
            break

        except:
            print("No angle at this time")

except KeyboardInterrupt:
    dcMotor.stop()
    print("Program terminated. Shutting down...")
