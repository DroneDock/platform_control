"""
The main program to be executed. So far, this is a program where the linear
actuator extends or retracts to level the platform using readings from the IMU.
"""


# Standard Imports
import time
import multiprocessing as mp
from multiprocessing import Queue

# Project Specific Imports
from HardwareComponents.LinearActuator import LinearActuator
from HardwareComponents.IMU import AdafruitBNO055


def fetchEulerAngle(queue: Queue):

    IMU = AdafruitBNO055()

    while True:
        # To prevent overfilling the queue
        if queue.qsize() < 50:
            queue.put(IMU.eulerAngle()[2])
        else:
            print("Queue is full. Waiting...")
        
        # Manual delay (to be removed later)
        time.sleep(0.05)

def printEulerAngle(queue: Queue):

    # Other modules use GPIO.setmode(BCM), so must go by BCM
    LinAct = LinearActuator(In1=5, In2=6, EN=12)

    while True:
        if not queue.empty():
            angle = queue.get()
            print(f"The pitch angle is {angle}")

            # Sometimes angle is None, so put in try block to resolve
            try:
                if (angle >= 0):
                    print("EXTEND")
                    LinAct.extend(100)
                elif (angle <= 0):
                    print("RETRACT")
                    LinAct.retract(100)
            except TypeError:
                pass
        
        else:
            print("Waiting for data")
            LinAct.extend(0)

        # Manual delay (to be removed later)
        time.sleep(0.05)


if __name__ == "__main__":

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
