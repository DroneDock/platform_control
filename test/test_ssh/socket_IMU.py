"""
Run this code to send IMU data to the visualizer server. 
"""

import socket
import time

# Project-Specific Imports
from HardwareComponents.test.IMU import AdafruitBNO055

# Read sensor
IMU = AdafruitBNO055()

# Setup network connection
host = '192.168.1.56'
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting...")
    s.connect((host, port))
    print("Connected!")

    while True:
        yaw, roll, pitch = IMU.eulerAngles
        if yaw and roll and pitch:
            print(f'Yaw, Pitch, Roll = {yaw}, {roll}, {pitch}')

            s.sendall(f"{yaw}, {roll}, {pitch}\n".encode('utf-8'))
            time.sleep(0.1)
        continue
