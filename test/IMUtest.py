"""
Run this script to verify readings from a single IMU
"""

# Standard Imports
import time

# Project-Specific Imports
from HardwareComponents.IMU import AdafruitBNO055

## ========================================================================= ##

if __name__ == '__main__':
    
    IMU = AdafruitBNO055()

    while True:
        print(f"Euler Angles (Yaw, roll, pitch) derived from quaternions: {IMU.eulerAngles}")
        print(f"Euler Angles (Yaw, roll, pitch) read from IMU : {IMU.euler()}")
        print()

        time.sleep(1)
