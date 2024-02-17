# Standard Imports
import time
import multiprocessing as mp
from multiprocessing import Queue

# Project Specific Imports
from HardwareComponents.LinearActuator import LinearActuator
from HardwareComponents.IMU import CustomIMU


def fetchEulerAngle(queue: Queue):

    IMU = CustomIMU()

    while True:
        # To prevent overfilling the queue
        if queue.qsize() < 10:
            queue.put(IMU.get_euler()[2])
        else:
            print("Queue is full. Waiting...")

        time.sleep(0.05)

def printEulerAngle(queue: Queue):

    LinAct = LinearActuator(In1=29, In2=31, EN=32)

    while True:
        if not queue.empty():
            angle = queue.get()
            print(f"The pitch angle is {angle}")

            # Sometimes angle is None, so put in try block to resolve
            try:
                if (angle <= 0):
                    print("EXTEND")
                    LinAct.extend(100)
                elif (angle >= 0):
                    print("RETRACT")
                    LinAct.retract(100)
            except TypeError:
                pass
        
        else:
            print("Waiting for data")
            LinAct.extend(0)

        time.sleep(0.05)


if __name__ == "__main__":

    # Initial Setup
    dataQueue = Queue()

    fetchProcess = mp.Process(target=fetchEulerAngle, args=(dataQueue,))
    printProcess = mp.Process(target=printEulerAngle, args=(dataQueue,))

    # Set processes as daemon which are automatically killed when the main
    # process ends, simplifying cleanup
    # fetchProcess.daemon = True
    # printProcess.daemon = True

    # Start the processes
    fetchProcess.start()
    printProcess.start()

    # Wait indefinitely until program is terminated
    time.sleep(10)

    fetchProcess.join()
    printProcess.join()

    print("All processes has been terminated")