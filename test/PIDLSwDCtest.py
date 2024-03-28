"""
Main code for running self balancing platform.
This implements DC motor rotation as well
Gain is tuned.

In my opinion, not fast enough for real life testing.
Ken
"""


import time
import multiprocessing as mp
from multiprocessing import Queue
import numpy as np
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
from multiprocessing import Lock

# Project Specific Imports
from HardwareComponents.Steppermotor2 import StepperMotor
from HardwareComponents.IMU import AdafruitBNO055
from PID_Tuner import PIDController

# Pin Definition using BCM numbering system -----------------------------------
#For DC motor
Motor1In1: int = 17
Motor1In2: int = 27
Motor1EN: int  = 18   # PWM Pin on Raspberry PI

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(Motor1In1, GPIO.OUT)
GPIO.setup(Motor1In2, GPIO.OUT)
GPIO.setup(Motor1EN, GPIO.OUT)


p = GPIO.PWM(Motor1EN, 2000)  # Set PWM frequency (in Hz)

# Constants for PID controller (to be tuned)
kp = 10
ki = kp *(0.001)
kd = kp *(0.000000001)
#PID limits
upper_bound = 500
lower_bound = 0
# Setpoint for the PID controller (desired angle)
setpoint = 0.0

# Constants for PWM control
DutyCycleUp = 50 # Initial duty cycle for going up
DutyCycledown = 30  # Initial duty cycle for going up
Dutycyclestop = 0

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
        time.sleep

def printDC(queue: Queue):
    
    
    while True:
        #print("point3")
        #for _ in range(10):  # Assuming you want to run the motor 5 times            
        #try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(Motor1In1, GPIO.OUT)
            GPIO.setup(Motor1In2, GPIO.OUT)
            GPIO.setup(Motor1EN, GPIO.OUT)

            p.start(DutyCycleUp)
            GPIO.output(Motor1In1, GPIO.HIGH) # High
            GPIO.output(Motor1In2, GPIO.LOW)
            time.sleep(1)
            p.stop()
            print("DCspinclockwise")
            
            p.start(DutyCycledown)
            GPIO.output(Motor1In1, GPIO.LOW)
            GPIO.output(Motor1In2, GPIO.HIGH) # High
            time.sleep(1)
            p.stop()
            print("DCspinanticlockwise")
            
                  
            GPIO.cleanup()

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
            plt.savefig('PIDLSDCtuning.png')     
            
            

        else:
            print("Waiting for data")
            motor.spin(steps= step_stop, sleep_time= time_sleep, clockwise=True)
            time.sleep(1)

        end_time = time.time()  # Record end time
        execution_time = end_time - start_time  # Calculate execution time
        #print(f"Execution time: {execution_time} seconds")        
# Manual delay (to be removed later)
            
if __name__ == "__main__":
    #time.sleep(3)

    # Initial Setup
    dataQueue = Queue()
   #print (dataQueue) #doesn't actually print Queue, why?

    # Initiate processes
    fetchProcess = mp.Process(target=fetchEulerAngle, args=(dataQueue,))
    printProcess = mp.Process(target=printEulerAngle, args=(dataQueue,))
    DCrotationProcess = mp.Process(target=printDC, args=(dataQueue,))

    # Set processes as daemon which are automatically killed when the main
    # process ends, simplifying cleanup
    fetchProcess.daemon = True
    printProcess.daemon = True
    DCrotationProcess.daemon = True

    # Start the processes
    DCrotationProcess.start()
    print("DC started")
    fetchProcess.start()
    printProcess.start()
    


    # Wait indefinitely until program is terminated
    try:
        while True:
            pass
            #time.sleep(0.5)

    except KeyboardInterrupt:
        p.start(Dutycyclestop)
        print("Program has terminated")
        p.stop()

