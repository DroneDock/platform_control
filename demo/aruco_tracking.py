# Standard Imports
import time
import multiprocessing as mp 
from pathlib import Path
# Third-Party Imports
import numpy as np
import RPi.GPIO as GPIO
# Project-Specific Imports
from utilities.path_management import PROJECT_ROOT_PATH, LOGS_DIR
from HardwareComponents.Camera import RPiCamera
from HardwareComponents.DCMotor import DCMotor
from HardwareComponents.StepperMotor import BaseStepperMotor

# CONFIG CONSTANTS ------------------------------------------------------------
CAMERA_OFFSET_THRESHOLD = 5  # [cm] the threshold within which the offset is deemed acceptable hence stop tracking


# Threads ---------------------------------------------------------------------
def update_camera_readings(delta_x: mp.Value, delta_y: mp.Value, stopEvent: mp.Event):
    """
    Update camera readings into the R and theta variables in place.
    """
    
    calibration_path = Path(PROJECT_ROOT_PATH, "arucoRPi/calibration.yaml")
    camera = RPiCamera(str(calibration_path))
    
    while not stopEvent.is_set():
        camera.update_frame()
        x, y, z = camera.estimate_coordinates(log=False)
        
        # Guard clause: when no marker is detected
        if (x == y == z == -1):
            delta_x.value = 0  # Signal Base Stepper to stop
            delta_y.value = 0  # Signal DC motor to stop
            print("No marker detected.")
            continue
        
        # Setting values
        print("One marker detected!")
        delta_x.value = -x  # 'estimate_coordinates' return +ve X to the left. Recalibrate to +ve X to the right
        delta_y.value = -y  # 'estimate_coordinates' return +ve y behind. Recalibrate to +ve Y to in front
                
        
def marker_tracking(delta_x: mp.Value, delta_y: mp.Value, stopEvent: mp.Event):
    """
    Actuate DC motors and base stepper motor to track the aruco marker based on
    the camera readings provided b thread `update_camera_readings`
    """    
    GPIO.setmode(GPIO.BCM)
    dcMotor = DCMotor()
    baseMotor = BaseStepperMotor()
    
    while not stopEvent.is_set():
        
        print("Tracking")
        
        # Adjust base stepper to correct x (If delta_x is +ve, turn clockwise)
        if delta_x.value > CAMERA_OFFSET_THRESHOLD:
            print("----- Stepper Motor ----- : Turning clockwise")
            baseMotor.spin(10, sleep_time=0.0005, clockwise=True)
        elif delta_x.value < (-1 * CAMERA_OFFSET_THRESHOLD):
            print("----- Stepper Motor ----- : Turning anticlockwise")
            baseMotor.spin(10, sleep_time=0.0005, clockwise=False)
        else:
            print("----- Stepper Motor ----- : Stop")
            
        # Adjust DC motor to correct y (If delta_y is +ve, extend)
        if delta_y.value > CAMERA_OFFSET_THRESHOLD:
            print("----- DC Motor ----- : Going forward")
            dcMotor.forward()
        elif delta_y.value < (-1 * CAMERA_OFFSET_THRESHOLD):
            print("----- DC Motor ----- : Going backwards")
            dcMotor.backward()
        else:
            print("----- DC Motor ----- : Stop")
            dcMotor.stop()
            
        time.sleep(0.5)
            
    # dcMotor.stop()
    GPIO.cleanup()


if __name__ == '__main__':
    
    # ===== Parameter setup =====
    yaw = mp.Value('f', 0.0)      # Current yaw angle of the arm [deg]
    pitch = mp.Value('f', 0.0)    # Current pitch value of the platform [deg]
    alpha = mp.Value('f', 0.0)    # Current arm angle [deg]
    delta_x = mp.Value('f', 0.0)  # Horizontal distance between camera and marker [cm]
    delta_y = mp.Value('f', 0.0)  # Vertical distance between camera and marker [cm]
    
    # ===== Component setup =====
    video_save_path = Path(LOGS_DIR, "videos/")

    # Global stop event
    stopEvent = mp.Event()
    
    # ===== Initiate processses =====
    processes = [
        mp.Process(target=update_camera_readings, args=(delta_x, delta_y, stopEvent,)),
        mp.Process(target=marker_tracking, args=(delta_x, delta_y, stopEvent,))
    ]
    
    for p in processes:
        p.start()
        
    try:
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Inititalizing stop event")
    
    finally:
        stopEvent.set()
        for p in processes:
            p.join()
        print("Program has been terminated gracefully.")
                   