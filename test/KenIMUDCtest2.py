"""
This code attempts to make the DC motor reacts to the IMU reading.
Doesn't work as inteded yet

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


def fetchEulerAngle(queue: Queue):

    IMU = AdafruitBNO055()

    while True:
        # To prevent overfilling the queue
        if queue.qsize() < 50:
            queue.put(IMU.eulerAngles[2])
        else:
            print("Queue is full. Waiting...")
        
        
        # Manual delay (to be removed later)
        time.sleep(1)


# Initialize GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(Motor1In1, GPIO.OUT)
GPIO.setup(Motor1In2, GPIO.OUT)
GPIO.setup(Motor1EN, GPIO.OUT)
p = GPIO.PWM(Motor1EN, 2000)  # Set PWM frequency (in Hz)

# Constants for PWM control
DutyCycle = 50  # Initial duty cycle

# Initialize IMU
IMU = AdafruitBNO055()

# Initialize lists to store angle values
yaw_values = []
roll_values = []
pitch_values = []
new_D_values = []
timestamps = []

# Start time
start_time = time.time()
p.stop()

# Plotting function
def plot_graph(timestamps, yaw_values, roll_values, pitch_values, new_D_values):
    plt.clf()
    plt.plot(timestamps, yaw_values, label='Yaw', color='r')
    plt.plot(timestamps, roll_values, label='Roll', color='g')
    plt.plot(timestamps, pitch_values, label='Pitch', color='b')
    plt.plot(timestamps, new_D_values, label='new_D', color='y')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Angle (degrees)')
    plt.title('IMU Euler Angles')
    plt.pause(0.001)
    plt.savefig('IMUDCmotor2.png')

def printEulerAngle(queue: Queue):

    while True:
        if not queue.empty():
            current_time = time.time() - start_time
            angle = queue.get()
            #print(f"The pitch angle is {angle}")
            yaw, roll, pitch = IMU.eulerAngles
            wrap_pitch = pitch + 180
            new_D = abs(roll) - 43

            # Append values to lists
            yaw_values.append(yaw)
            roll_values.append(roll)
            pitch_values.append(pitch)
            new_D_values.append(new_D)
            timestamps.append(current_time)
            # Plot the graph
            plot_graph(timestamps, yaw_values, roll_values, pitch_values, new_D_values)


            # Sometimes angle is None, so put in try block to resolve
            try:
                if (wrap_pitch > 290):
                    print(wrap_pitch)
                    p.start(DutyCycle)
                    GPIO.output(Motor1In1, GPIO.HIGH) #High
                    GPIO.output(Motor1In2, GPIO.LOW)
                    time.sleep(0.5)

                    
                    
                elif (wrap_pitch < 290):
                    print(wrap_pitch)
                    p.start(DutyCycle)
                    GPIO.output(Motor1In1, GPIO.LOW)
                    GPIO.output(Motor1In2, GPIO.HIGH) #HIGH
                    time.sleep(0.5)
                    
            except TypeError:
                pass
           
        else:
            print("Waiting for data")
            p.stop()

if __name__ == "__main__":
    time.sleep(3)
    p.stop()
    # Initial Setup
    dataQueue = Queue()
    
    
    print (dataQueue)
    
    # Initiate processes
    fetchProcess = mp.Process(target=fetchEulerAngle, args=(dataQueue,))
    printProcess = mp.Process(target=printEulerAngle, args=(dataQueue,))

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
        p.stop()

GPIO.cleanup()
p.stop()

    
    
    