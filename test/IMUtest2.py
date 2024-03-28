<<<<<<< HEAD
"""Run this script to verify readings from the IMU"""
=======
"""
Run this script to verify readings from the IMU

This scripts takes in both IMU readings
"""
>>>>>>> d6414c5 (28.03.24 Ken & Zheng Aun)

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

<<<<<<< HEAD
        time.sleep(1)
=======
        time.sleep(1)
>>>>>>> d6414c5 (28.03.24 Ken & Zheng Aun)
