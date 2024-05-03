# Standard Imports
import time
import multiprocessing as mp 
from pathlib import Path
# Third-Party Imports
import numpy as np
import RPi.GPIO as GPIO
# Project-Specific Imports
from utilities.path_management import PROJECT_ROOT_PATH, LOGS_DIR
from HardwareComponents.IMU import AdafruitBNO055
from HardwareComponents.Camera import RPiCamera
from HardwareComponents.DCMotor import DCMotor
from HardwareComponents.StepperMotor import BaseStepperMotor, LeadscrewStepperMotor

# CONFIG CONSTANTS ------------------------------------------------------------
CAMERA_OFFSET_THRESHOLD = 50  # [cm] the threshold within which the offset is deemed acceptable hence stop tracking


# Threads ---------------------------------------------------------------------
def update_IMU_readings(yaw_deg, pitch_deg, arm_deg, stopEvent: mp.Event):
    """
    Designed for multiprocessing, update the input angles in place with most
    recent IMU sensor readings.
    """
    top_IMU = AdafruitBNO055(ADR=True)
    arm_IMU = AdafruitBNO055()

    while not stopEvent.is_set():
        try: #TODO: update values individually so None for one value does not affect others
            yaw_deg.value = top_IMU.eulerAngles[0]
            pitch_deg.value = top_IMU.eulerAngles[1]
            arm_deg.value = arm_IMU.eulerAngles[1]

        except TypeError:
            pass  # Skip update for one loop if sensor returns None
        
        # print(f"Yaw: {yaw_deg.value}, Pitch: {pitch_deg.value}, Arm: {arm_deg.value}")
        time.sleep(0.05)

def update_camera_readings(delta_x: mp.Value, delta_R: mp.Value, stopEvent: mp.Event):
    """
    Update camera readings into the R and theta variables in place.
    """
    
    calibration_path = Path(PROJECT_ROOT_PATH, "arucoRPi/calibration.yaml")
    camera = RPiCamera(str(calibration_path))
    
    while not stopEvent.is_set():
        camera.update_frame()
        x, y, z = camera.estimate_coordinates(log=False, save_dir = LOGS_DIR / "Images" / "aruco_tracking")
        
        # Guard clause: when no marker is detected
        if (x == y == z == -1):
            delta_x.value = 0  # Signal Base Stepper to stop
            delta_R.value = 0  # Signal DC motor to stop
            print("No marker detected.")
            continue
        
        # Setting values
        print("One marker detected!")
        delta_x.value = -x  # 'estimate_coordinates' return +ve x anti-clockwise. Calibrate it to +ve clockwise.
        delta_R.value = -y  # 'estimate_coordinates' return +ve y backward. Calibrate it to +ve forward.
                
        
def forward_tracking(delta_R: mp.Value, stopEvent: mp.Event):
    """
    Actuate DC motors to track the aruco marker based on camera readings 
    provided by thread `update_camera_readings`
    """    
    dcMotor = DCMotor(In1=17, In2=27, EN=18)
    time.sleep(3)  # For motor to warmup
    
    while not stopEvent.is_set():
        
        # The convention is R is positive forward
        if delta_R.value > CAMERA_OFFSET_THRESHOLD:
            print("----- DC Motor ----- : Going forward")
            dcMotor.forward(dutyCycle=100)
        elif delta_R.value < (-1 * CAMERA_OFFSET_THRESHOLD):
            print("----- DC Motor ----- : Going backwards")
            dcMotor.backward(dutyCycle=100)
        else:
            print("----- DC Motor ----- : Stop")
            dcMotor.stop()      
            
    dcMotor.stop()
    
def side_tracking(delta_x: mp.Value, stopEvent: mp.Event):
    """
    Actuate base stepper motor to track the aruco marker based on camera
    readings provided by thread 'update_camera_readings'
    """
    baseMotor = BaseStepperMotor() 
    time.sleep(3)  # For motor to warmup
    
    while not stopEvent.is_set():
        
        # The convention is x is positive clockwise
        if delta_x.value > CAMERA_OFFSET_THRESHOLD:
            print("----- Base Motor ----- : Going clockwise")
            baseMotor.spin(steps=10, sleep_time=0.0002, clockwise=True)
        elif delta_x.value < (-1 * CAMERA_OFFSET_THRESHOLD):
            print("----- Base Motor ----- : Going anticlockwise")
            baseMotor.spin(steps=10, sleep_time=0.0002, clockwise=False)
        else:
            print("----- Base Motor ----- : Stop")
        
    GPIO.cleanup()


def balance_platform(pitch: mp.Value, stopEvent: mp.Event):
    
    Leadscrew = LeadscrewStepperMotor(dir_pin=20, step_pin=21)
    
    time.sleep(5)
    
    time_sleep = 0.0005 # This has been proved to be consistent
    # steps = 1
    
    while not stopEvent.is_set():
        if pitch.value >= 4:  # Retracts
            Leadscrew.single_spin(sleep_time=time_sleep, clockwise=False)
            # Leadscrew.spin(steps=steps, sleep_time=time_sleep, clockwise=False)  # Retracts to reduce pitch
        elif pitch.value <= -4:  # Extends
            Leadscrew.single_spin(sleep_time=time_sleep, clockwise=True)
            # Leadscrew.spin(steps=steps, sleep_time=time_sleep, clockwise=True)  # Extends to increase pitch
        # time.sleep(time_sleep)

    GPIO.cleanup()


if __name__ == '__main__':
    
    # ===== Parameter setup =====
    yaw = mp.Value('f', 0.0)      # Current yaw angle of the arm [deg]
    pitch = mp.Value('f', 0.0)    # Current pitch value of the platform [deg]
    alpha = mp.Value('f', 0.0)    # Current arm angle [deg]
    delta_x = mp.Value('f', 0.0)  # Horizontal distance between camera and marker [cm]
    delta_R = mp.Value('f', 0.0)  # Vertical distance between camera and marker [cm]
    
    # ===== Component setup =====
    video_save_path = Path(LOGS_DIR, "videos/")

    # Global stop event
    stopEvent = mp.Event()
    
    # ===== Initiate processses =====
    processes = [
        mp.Process(target=update_IMU_readings, args=(yaw, pitch, alpha, stopEvent,)),
        mp.Process(target=update_camera_readings, args=(delta_x, delta_R, stopEvent,)),
        mp.Process(target=forward_tracking, args=(delta_R, stopEvent,)),
        mp.Process(target=side_tracking, args=(delta_x, stopEvent,)),
        mp.Process(target=balance_platform, args=(pitch, stopEvent,))
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
                   