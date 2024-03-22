"""
Running this code setup the visualizer server to read the IMU data. Ensure this
is running before the IMU sends data.
"""

import socket
import matplotlib.pyplot as plt

# Receiving data
host = ''
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()

while True:

    # print("Trying to receive data...")
    data = conn.recv(1024).decode('utf-8')

    if data:
        yaw, roll, pitch = map(float, data.strip().split(','))

        print(f'Yaw, Pitch, Roll = {yaw}, {roll}, {pitch}')
