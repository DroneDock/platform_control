"""
This code attempts to make the DC motor reacts to the IMU reading.
Plots angles specifically as the DC motor moves
Current working file progress. 25/03/24.
Ken
"""


import time
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Queue
import multiprocessing as mp
import RPi.GPIO as GPIO
from HardwareComponents.IMU import AdafruitBNO055

# Pin Definition using BCM numbering system -----------------------------------
Motor1In1 = 17
Motor1In2 = 27
Motor1EN  = 18   # PWM Pin on Raspberry PI

# Initialize GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(Motor1In1, GPIO.OUT)
GPIO.setup(Motor1In2, GPIO.OUT)
GPIO.setup(Motor1EN, GPIO.OUT)
p = GPIO.PWM(Motor1EN, 2000)  # Set PWM frequency (in Hz)

# Constants for PWM control
DutyCycledown = 55  # Initial duty cycle
DutyCycleup = 70
p.stop()

# Initialize IMU
IMU = AdafruitBNO055()

# Initialize lists to store angle values
yaw_values = []
roll_values = []
pitch_values = []
new_D_values = []
timestamps = []
wrap_pitch_values = []
wrap_roll_values = []


# Start time
start_time = time.time()


def transform_angle(angle):
    if angle >= 0:
        return angle
    else:
        return 360 + angle


# Plotting function
def plot_graph(timestamps, yaw_values, roll_values, pitch_values, new_D_values,wrap_pitch_values):
    plt.clf()
    #plt.plot(timestamps, yaw_values, label='Yaw', color='r')
    #plt.plot(timestamps, roll_values, label='Roll', color='g')
    plt.plot(timestamps[2:], wrap_roll_values[2:], label='wrap_roll', color='g')
    #plt.plot(timestamps, pitch_values, label='Pitch', color='b')
    #plt.plot(timestamps, new_D_values, label='new_D', color='y')
    #plt.plot(timestamps[2:], wrap_pitch_values[2:], label='wrap_pitch', color='m')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Angle (degrees)')
    plt.title('IMU Euler Angles')
    plt.pause(0.001)
    plt.savefig('ZhengBottomManualRotation.png')

def fetchEulerAngle(queue: Queue):

    IMU = AdafruitBNO055()
    #print ("point1")
    while True:
        # To prevent overfilling the queue
        if queue.qsize() < 50:
            queue.put(IMU.eulerAngles[2])
        else:
            print("Queue is full. Waiting...")
        
        current_time = time.time() - start_time
        #print ("point2")
        # Get angle from queue
        angle = queue.get()
        #print(f"The pitch angle is {angle}")

        yaw, roll, pitch = IMU.eulerAngles
        wrap_pitch = (transform_angle(pitch) - 118) *-1
        #print(wrap_pitch)

        wrap_roll = (transform_angle(roll) -85 ) *-1
        print(wrap_roll)

        print()
        new_D = abs(roll) - 43

        # Append values to lists
        yaw_values.append(yaw)
        roll_values.append(roll)
        pitch_values.append(pitch)
        new_D_values.append(new_D)
        timestamps.append(current_time)
        wrap_pitch_values.append(wrap_pitch)
        wrap_roll_values.append(wrap_roll)
        #print(wrap_pitch_values)

        # Plot the graph
        plot_graph(timestamps, yaw_values, roll_values, pitch_values, new_D_values,wrap_pitch_values)
            
        # Manual delay (to be removed later)
        time.sleep(1)

def printEulerAngle(queue: Queue):
    while True:
        #print("point3")
        for _ in range(15):  # Assuming you want to run the motor 5 times            
            try:
                p.start(DutyCycleup)
                GPIO.output(Motor1In1, GPIO.HIGH) # High
                GPIO.output(Motor1In2, GPIO.LOW)
                time.sleep(0.05)
                p.stop()
                time.sleep(1)
            except TypeError:
                pass


        for _ in range(15):  # Assuming you want to run the motor 5 times
            # One direction movement, clockwise (up)
            try:
                p.start(DutyCycledown)
                GPIO.output(Motor1In1, GPIO.LOW)
                GPIO.output(Motor1In2, GPIO.HIGH) # High
                time.sleep(0.05)
                p.stop()
                time.sleep(1)
            except TypeError:
                pass

if __name__ == "__main__":
    #print("point9")
    time.sleep(3)
    p.stop()
    # Initial Setup
   # print("point6")
    dataQueue = Queue()
        
    # Initiate processes
    fetchProcess = mp.Process(target=fetchEulerAngle, args=(dataQueue,))
    #print("point7")
    printProcess = mp.Process(target=printEulerAngle, args=(dataQueue,))
    #print("point8")

    # Set processes as daemon which are automatically killed when the main
    # process ends, simplifying cleanup
    fetchProcess.daemon = True
    printProcess.daemon = True

    # Start the processes
    fetchProcess.start()
    printProcess.start()

    # Wait indefinitely until program is terminated
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Program has terminated")
        GPIO.cleanup()
        p.stop()

GPIO.cleanup()
p.stop()