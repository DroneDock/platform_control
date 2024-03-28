"""
Shern Kai working code, 

Result
Now only using shared variable. Works.
"""
#Standard imports
import time
import multiprocessing as mp
from multiprocessing import Queue

# Project Specific Imports
from back.Leadscrew import StepperMotor
from back.ShernIMU import AdafruitBNO055
from back.DCMotor import DCMotor

time_sleep = 0.0005 #don't change this, for lead screw

#to put IMU readings into a value
def fetchEulerAngle(angle):
    IMU = AdafruitBNO055()
    print ("IMU angle is",IMU.eulerAngles[1])

    while True:
        try:
            angle.value = IMU.eulerAngles[1]
        except TypeError:
            pass  # Skip updating angle if None

def printEulerAngle(angle):

    motor = StepperMotor()
    while True:
        try:
            while (angle.value >= 2):
                print("EXTEND")
                motor.spin(sleep_time= time_sleep, clockwise=True)
            while (angle.value < -2):
                print("RETRACT")
                motor.spin(sleep_time= time_sleep, clockwise=False)
            else:
                #print("Flat")
                pass
        except TypeError:
            pass

#Currently not completed, angle just used to move DC motor
def reach(angle):
    DC_motor = DCMotor(In1=17, In2=27, EN=18, Duty=100)
    print ("The angle for DC is",angle.value)
    while True:
        try:
            if -1 < angle.value <= 0:
                DC_motor.clockwise(0.5)   # Bring down
                print ("Moving Down")
            elif 0 < angle.value <=1:
                DC_motor.anticlockwise(0.8) #Bring up
                print ("Moving Up")
            else:
                DC_motor.stop()
                print("notmoving")
                pass
        
        except KeyboardInterrupt:
            print("Cleaning up GPIO pins")
            DC_motor.stop()
            DC_motor.cleanup()

if __name__ == "__main__":
    # Initial Setup
    angle = mp.Value('f', 0.0)  # Use 'f' for float type

    # Initiate processes
    fetchProcess = mp.Process(target=fetchEulerAngle, args=(angle,))
    printProcess = mp.Process(target=printEulerAngle, args=(angle,))
    DCProcess = mp.Process(target=reach, args=(angle,))
    # Set processes as daemon which are automatically killed when the main
    # process ends, simplifying cleanup
    fetchProcess.daemon = True
    printProcess.daemon = True
    DCProcess.daemon = True


    # Start the processes
    fetchProcess.start()
    printProcess.start()
    DCProcess.start()

    # Wait indefinitely until program is terminated
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Program has terminated")

