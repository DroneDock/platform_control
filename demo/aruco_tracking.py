# Standard Imports
import time
import threading  # This file uses threading instead of multiprocessing for ease of code
import multiprocessing as mp 
from pathlib import Path
# Third-Party Imports
import numpy as np
# Project-Specific Imports
from utilities.path_management import PROJECT_ROOT_PATH, LOGS_DIR
from HardwareComponents.Camera import RPiCamera
from HardwareComponents.DCMotor import DCMotor
from HardwareComponents.StepperMotor import BaseStepperMotor

# CONFIG CONSTANTS ------------------------------------------------------------
CAMERA_OFFSET_THRESHOLD = 5  # [cm] the threshold within which the offset is deemed acceptable hence stop tracking


# Threads ---------------------------------------------------------------------
def update_camera_readings(stopEvent: threading.Event):
    """
    Update camera readings into the R and theta variables in place.
    """
    global delta_x, delta_y
    
    calibration_path = Path(PROJECT_ROOT_PATH, "arucoRPi/calibration.yaml")
    camera = RPiCamera(str(calibration_path))
    
    while not stopEvent.is_set():
        start_time = time.time()
        camera.update_frame()
        x, y, z = camera.estimate_coordinates(log=False)
        
        print("Camera outputs are: ", x, y, z)
        
        # Guard clause: when no marker is detected
        if (x == y == z == -1):
            delta_x = 0  # Signal Base Stepper to stop
            delta_y = 0  # Signal DC motor to stop
            print("No marker detected.")
            end_time = time.time()
            duration = end_time - start_time
            print(f'Camera code executed in {duration} seconds')
            continue
        
        # Recalibration
        delta_x = -x  # 'estimate_coordinates' return +ve X to the left. Recalibrate to +ve X to the right
        delta_y = -y  # 'estimate_coordinates' return +ve y behind, so recalibrate it with htis
        
        end_time = time.time()
        duration = end_time - start_time
        print(f'Camera code executed in {duration} seconds')
        
        
def marker_tracking(stopEvent: threading.Event):
    """
    Actuate DC motors and base stepper motor to track the aruco marker based on
    the camera readings provided b thread `update_camera_readings`
    """
    global delta_x, delta_y, CAMERA_OFFSET_THRESHOLD
    
    dcMotor = DCMotor()
    baseMotor = BaseStepperMotor()
    
    # Adjust base stepper to correct x (If delta_x is +ve, turn clockwise)
    if delta_x > CAMERA_OFFSET_THRESHOLD:
        baseMotor.spin(10, sleep_time=0.0005, clockwise=True)
    elif delta_x < (-1 * CAMERA_OFFSET_THRESHOLD):
        baseMotor.spin(10, sleep_time=0.0005, clockwise=False)
        
    
        
        
    
    while not stopEvent.is_set():
        
        #

if __name__ == '__main__':
    
    # ===== Parameter setup =====
    yaw = 0.0      # Current yaw angle of the arm [deg]
    pitch = 0.0    # Current pitch value of the platform [deg]
    alpha = 0.0    # Current arm angle [deg]
    delta_x = 0.0  # Horizontal distance between camera and marker [cm]
    delta_y = 0.0  # Vertical distance between camera and marker [cm]
    
    # ===== Component setup =====
    video_save_path = Path(LOGS_DIR, "videos/")
    
    
    # Global stop event
    stopEvent = threading.Event()
    
    
    
    while True:
        try:
            
            camera.update_frame()
            
            # Based on the captured frame, perform pose estimation.
            # x is +ve when marker is to the left 
            # y is +ve when marker is behind
            x, y, z = camera.estimate_coordinates(log=False)
            
            # If x, y, z are all -1, indicates that no marker or more than one
            # marker detected. Continue to the next loop
            if x == y == z == -1:
                continue
            
            print(f'x = {x:.2f}, y = {y:.2f}, z = {z:.2f}')
            print("----------")
            
            
                   
            
        except KeyboardInterrupt:
            pass
        finally:
            pass
    