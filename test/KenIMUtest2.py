"""
Used to plot graphs
"""

import time
import matplotlib.pyplot as plt
import numpy as np
from HardwareComponents.IMU import AdafruitBNO055

# Initialize IMU
IMU = AdafruitBNO055()

# Initialize lists to store angle values
yaw_values = []
roll_values = []
pitch_values = []
new_D_values = []
timestamps = []


time.sleep(3)

# Start time
start_time = time.time()

if __name__ == '__main__':

    # Main loop
    while True:
        # Get current time
        
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
