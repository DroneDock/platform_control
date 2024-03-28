"""
This is a simple code where the lead screw REACTS   to IMU readings.
Ken

"""


import time
import multiprocessing as mp
from multiprocessing import Queue

# Project Specific Imports
from HardwareComponents.Steppermotor2 import StepperMotor
from HardwareComponents.IMU import AdafruitBNO055


lead_screw_pitch = 8 #mm
time_sleep = 0.0005 #don't change this

#changet this
step = 100
step_stop = 0

def fetchEulerAngle(queue: Queue):

    IMU = AdafruitBNO055()

    while True:
        # To prevent overfilling the queue
        if queue.qsize() < 50:
            queue.put(IMU.eulerAngles[1])
        else:
            print("Queue is full. Waiting...")
        
        # Manual delay (to be removed later)
        time.sleep(0.5)


def printEulerAngle(queue: Queue):

    motor = StepperMotor()

    
    while True:
        if not queue.empty():
            angle = queue.get()
            print(f"The pitch angle is {angle}")

            

            # Sometimes angle is None, so put in try block to resolve
            try:
                if (angle > 0):
                    print("EXTEND")
                    motor.spin(steps= step, sleep_time= time_sleep, clockwise=True)
                    time.sleep(0.5)
                elif (angle < 0):
                    print("RETRACT")
                    motor.spin(steps= step, sleep_time= time_sleep, clockwise=False)
                    time.sleep(0.5)
            except TypeError:
                pass
        
        else:
            print("Waiting for data")
            motor.spin(steps= step_stop, sleep_time= time_sleep, clockwise=True)

        # Manual delay (to be removed later)
       


if __name__ == "__main__":
    time.sleep(3)
    # Initial Setup
    dataQueue = Queue()
    

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
