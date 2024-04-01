"""Run this script to verify readings from the IMU"""

# Standard Imports
import time
import matplotlib.pyplot as plt
import numpy as np

# Project-Specific Imports
from IMU import AdafruitBNO055

# Initialize lists to store angle values
yaw_values = []
roll_values = []
pitch_values = []
timestamps = []

start_time = time.time()


def plot_graph(timestamps, yaw_values, roll_values, pitch_values):
    plt.clf()
    plt.plot(timestamps, yaw_values, label='Yaw', color='r')
    plt.plot(timestamps, roll_values, label='Roll', color='g')
    plt.plot(timestamps, pitch_values, label='Pitch', color='b')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Angle (degrees)')
    plt.title('IMU Euler Angles')
    plt.pause(0.001)
    plt.savefig('IMUDCmotor2.png')

if __name__ == '__main__':
    
    IMU = AdafruitBNO055()

    while True:
        print(f"Temperature: {IMU.temperature} degrees C")
        print(f"Euler Angles (Yaw, roll, pitch) derived from quaternions: {IMU.eulerAngles}")
        print(f"Euler Angles (Yaw, roll, pitch) read from IMU : {IMU.euler()}")
        print()

        yaw, roll, pitch = IMU.eulerAngles
        current_time = time.time() - start_time

        # Append values to lists
        yaw_values.append(yaw)
        roll_values.append(roll)
        pitch_values.append(pitch)
        timestamps.append(current_time)

        #plot_graph(timestamps, yaw_values, roll_values, pitch_values)

        time.sleep(1)
