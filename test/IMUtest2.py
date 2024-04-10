"""
Run this script to verify readings from two IMUs. Note that one of the IMUs
should have its ADR (address) pin set to HIGH.
"""

# Standard Imports
import time

# Project-Specific Imports
from HardwareComponents.IMU import AdafruitBNO055

## ========================================================================= ##

if __name__ == '__main__':
    
    IMU_1 = AdafruitBNO055()
    IMU_2 = AdafruitBNO055(ADR=True)

    while True:
        print(f"1st IMU Angles (Yaw, Roll, Pitch): {IMU_1.eulerAngles}")
        print(f"2nd IMU Angles (Yaw, Roll, Pitch): {IMU_2.eulerAngles}")
        print()

        time.sleep(1)
