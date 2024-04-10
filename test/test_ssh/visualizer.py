"""
Running this code setup the visualizer server to read the IMU data. Ensure this
is running before the IMU sends data.
"""

# Standard Imports
import socket

# Third-Party Imports
import numpy as np
from vpython import *

# Ensure numpy cos, sin functions are accessible
from numpy import cos, sin

# Receiving data setup
host = ''
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()

# V-Python Visualization Setup
scene.range=5
scene.forward=vector(-1,-1,-1)
scene.width=600
scene.height=600

xarrow=arrow(shaftwidth=.1, color=color.red, axis=vector(2,0,0))
yarrow=arrow(shaftwidth=.1, color=color.green, axis=vector(0,2,0))
zarrow=arrow(shaftwidth=.1, color=color.blue, axis=vector(0,0,4))

frontArrow = arrow(shaftwidth=.1, color=color.purple, axis=vector(4, 0, 0))  # Preset length 4
upArrow = arrow(shaftwidth=.1, color=color.magenta, axis=vector(0, 1, 0))  # Preset length 1
sideArrow = arrow(shaftwidth=.1, color=color.orange, axis=vector(0, 0, 2))  # Preset length 2

while True:
    
    try:
        data = conn.recv(1024).decode('utf-8').strip()
        
        if data:
            
            # Sometimes multiple sets of data awaiting at the buffer may be
            # sent. Take the first set only.
            data = data.split('\n')[0]  # Take the first set of reading
            
            print(data)
            
            yaw, roll, pitch = map(float, data.strip().split(','))
            print(f'Yaw, Roll, Pitch = {yaw}, {roll}, {pitch}')
                        
            # Convert angles from degrees to radians
            yaw, roll, pitch = [angle * np.pi/180 for angle in [yaw, roll, pitch]]

            rate(50) # Control the update rate to 50 times per second
                        
            # Calculating the direction vectors based on yaw, pitch, and roll
            k = vector(cos(yaw) * cos(pitch), sin(pitch), sin(yaw) * cos(pitch))
            y = vector(0, 1, 0)
            s = cross(k, y)
            v = cross(s, k)
            vrot = v * cos(roll) + cross(k, v) * sin(roll)

            # Updating the arrows to represent the current orientation
            frontArrow.axis = k
            sideArrow.axis = cross(k, vrot)
            upArrow.axis = vrot

            # Adjusting lengths might not be necessary unless you want them to dynamically change
            sideArrow.axis = sideArrow.axis.norm() * 2
            frontArrow.axis = frontArrow.axis.norm() * 4
            upArrow.axis = upArrow.axis.norm() * 1
                        
    except KeyboardInterrupt:
        
        print("Program has terminated.")
