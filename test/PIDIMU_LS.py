"""
Main code for running self balancing platform.
Gain is tuned.

In my opinion, not fast enough for real life testing.

"""


import time
import multiprocessing as mp
from multiprocessing import Queue
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Lock

# Project Specific Imports
from HardwareComponents.Steppermotor2 import StepperMotor
from HardwareComponents.IMU import AdafruitBNO055
from PID_Tuner import PIDController

# Constants for PID controller (to be tuned)
kp = 10
ki = kp *(0.001)
kd = kp *(0.000000001)
#PID limits
upper_bound = 500
lower_bound = 0
# Setpoint for the PID controller (desired angle)
setpoint = 0.0

# Initialize PID controller
pid_controller = PIDController(kp, ki, kd, setpoint,upper_bound,lower_bound)

lead_screw_pitch = 8 #mm
time_sleep = 0.0005 #don't change this

step_stop = 0 #to stop the motor

#to plot graph of PID tuning
angle_values = []
time_values = []
setpoint_values = []
lock = Lock()

#to put IMU readings into a queue
def fetchEulerAngle(queue: Queue):

    IMU = AdafruitBNO055()

    while True:
        # To prevent overfilling the queue
        if queue.qsize() < 50:
            queue.put(IMU.eulerAngles[1])
        else:
            print("Queue is full. Waiting...")
        
        print(queue.qsize())
        # Manual delay (to be removed later)
        time.sleep(0.9)


def printEulerAngle(queue: Queue):

    motor = StepperMotor()
    start_time = time.time()  # Record start time


    while True:
        if not queue.empty():

            angle = queue.get()
            step = pid_controller.calculate(angle)#output step size
            print(f"The angle is {angle}")
            with lock: #to keep the values clean
                angle_values.append(angle)
                time_values.append(time.time())  # current time
                setpoint_values.append(pid_controller.setpoint)  # setpoint value

            # Sometimes angle is None, so put in try block to resolve
            try:
                if (angle > 0):
                    print("EXTEND")
                    motor.spin(steps= step, sleep_time= time_sleep, clockwise=True)
                    print(f"The step is {step}")
                    #time.sleep(0.5)
                    
                elif (angle < 0):
                    print("RETRACT")
                    motor.spin(steps= step, sleep_time= time_sleep, clockwise=False)
                    print(f"The step is {step}")
                    #time.sleep(0.5)
                    
            except TypeError:
                pass
            # # Update plot periodically
            plt.clf()
            # First few points are ommited
            plt.plot(time_values[2:], angle_values[2:], '-o', color='red', label='Angle')
            plt.plot(time_values[2:], setpoint_values[2:], '--', color='blue', label='Setpoint')
            plt.xlabel('Time')
            plt.ylabel('Angle')
            plt.legend()
            plt.title('Real-Time Angle Response')
            plt.pause(0.001)  # Pause to allow the plot to update
            plt.savefig('tuning.png')
        else:
            print("Waiting for data")
            motor.spin(steps= step_stop, sleep_time= time_sleep, clockwise=True)

        end_time = time.time()  # Record end time
        execution_time = end_time - start_time  # Calculate execution time
        print(f"Execution time: {execution_time} seconds")        
# Manual delay (to be removed later)
            
if __name__ == "__main__":
    #time.sleep(3)

    # Initial Setup
    dataQueue = Queue()
    print (dataQueue) #doesn't actually print Queue, why?

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
            pass
            #time.sleep(0.5)

    except KeyboardInterrupt:
        print("Program has terminated")
