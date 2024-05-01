"""
The main program to be executed. So far, this is a program where the linear
actuator extends or retracts to level the platform using readings from the IMU.
"""


# Standard Imports
import time
import threading
from pathlib import Path

# Third-Party Imports
import numpy as np
import RPi.GPIO as GPIO

# Project Specific Imports
from HardwareComponents.Camera import RPiCamera
from HardwareComponents.IMU import AdafruitBNO055
from HardwareComponents.DCMotor import DCMotor
from HardwareComponents.StepperMotor import BaseStepperMotor, LeadscrewStepperMotor
from utility.decorators import time_this_func

# FUNCTION WRAPPERS FOR DIFFERENT PROCESSES -----------------------------------
def update_IMU_readings(stopEvent: threading.Event):
    """
    Designed for multiprocessing, update the input angles in place with most
    recent IMU sensor readings.
    """
    top_IMU = AdafruitBNO055(ADR=True)
    arm_IMU = AdafruitBNO055()
    
    while not stopEvent.is_set():
        try: #TODO: update values individually so None for one value does not affect others
            yaw = top_IMU.eulerAngles[0]
            pitch = top_IMU.eulerAngles[1]
            alpha = arm_IMU.eulerAngles[1]
        except TypeError:
            pass  # Skip update for one loop if sensor returns None
        
        # print(f"Yaw: {yaw_deg.value}, Pitch: {pitch_deg.value}, Arm: {arm_deg.value}")
        time.sleep(0.05)
    
    
def update_camera_readings(stopEvent: threading.Event):
    """
    Update camera readings into the R and theta variables in place.
    """
    
    camera = RPiCamera(calibration_path=Path(__file__).parent / "arucoRPi/calibration.yaml")
    
    while not stopEvent.is_set():
        start_time = time.time()
        camera.update_frame()
        x, y, z = camera.estimate_coordinates(log=False)
        
        print("Camera outputs are: ", x, y, z)
        
        # Guard clause: when no marker is detected
        if z < 0:
            delta_R = 0  # Signal DC motor to stop
            print("No marker detected.")
            end_time = time.time()
            duration = end_time - start_time
            print(f'Camera code executed in {duration} seconds')
            continue
        
        y = -y  # 'estimate_coordinates' return y positive downwards, so recalibrate it with htis
        
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        
        # When angle is lower than zero, the marker is located at third or fourth
        # quadrant, so a retraction is required.
        if theta < 0:
            delta_R = -r
        delta_theta = theta
        
        print(delta_R)
        print(delta_theta)
        
        end_time = time.time()
        duration = end_time - start_time
        print(f'Camera code executed in {duration} seconds')


# def move_arm(stopEvent: threading.Event):
    
#     dcMotor = DCMotor(In1=17, In2=27, EN=18)
    
#     time.sleep(5)
    
#     while not stopEvent.is_set():
#         dcMotor.forward(duration=0.5)
#         dcMotor.backward(duration=0.5)  # FOR THE SAME 
        
#     dcMotor.stop()
#     GPIO.cleanup()
    

# Only track radius changes for now
def track_marker(stopEvent: threading.Event):
    
    dcMotor = DCMotor(In1=17, In2=27, EN=18)
    time.sleep(5)
    
    while not stopEvent.is_set():
        if delta_R > 0:  # Require extension
            dcMotor.forward(duration=0.1)
        elif delta_R < 0:  # Require retraction
            dcMotor.backward(duration=0.1)
        else:  # Stop the motor (happens when no marker detected)
            dcMotor.stop()

    dcMotor.stop()
    GPIO.cleanup()
        
def balance_platform(stopEvent: threading.Event):
    
    Leadscrew = LeadscrewStepperMotor(dir_pin=20, step_pin=21)
    
    time.sleep(5)
    
    time_sleep = 0.0005 #don't change this
    steps = 30
    
    while not stopEvent.is_set():
        if pitch >=0:
            Leadscrew.spin(steps=steps, sleep_time=time_sleep, clockwise=False)  # Extends to increase pitch
        else:
            Leadscrew.spin(steps=steps, sleep_time=time_sleep, clockwise=True)  # Retracts to reduce pitch
        time.sleep(0.1)

    GPIO.cleanup()
    

# MAIN CODE -------------------------------------------------------------------
if __name__ == "__main__":

    # ===== Initial Setup =====
    yaw = 0.0    # Store yaw angle of platform
    pitch = 0.0  # Store the pitch angle of platform (for balancing purposes)
    alpha = 0.0  # Store the arm angle
    delta_R = 0.0  # Radial difference between centre of camera and marker
    delta_theta = 0.0  # Yaw difference between centre of camera and marker
    
    # Global Stop Event
    stopEvent = threading.Event()

    # ===== Initiate processes =====
    threads = [
        threading.Thread(target=update_IMU_readings, args=(stopEvent,)),
        threading.Thread(target=update_camera_readings, args=(stopEvent,)),
        # threading.Process(target=move_arm, args=(stopEvent,)),
        threading.Thread(target=track_marker, args=(stopEvent,)),
        threading.Thread(target=balance_platform, args=(stopEvent,))
    ]

    # Start the processes
    for t in threads:
        t.start()

    # Wait indefinitely until program is terminated
    try:
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:       
        print("Initializing stop event")

    # Ensure process resources are cleaned up
    finally:
        stopEvent.set() 
        for t in threads:
            t.join()
        print("Program has ended gracefully.")
