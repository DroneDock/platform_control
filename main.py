"""
The main program to be executed. So far, this is a program where the linear
actuator extends or retracts to level the platform using readings from the IMU.
"""


# Standard Imports
import time
import multiprocessing as mp
import logging
from multiprocessing import Queue
from pathlib import Path

# Third-Party Imports
import numpy as np
import RPi.GPIO as GPIO

# Project Specific Imports
from HardwareComponents.Camera import RPiCamera
from HardwareComponents.IMU import AdafruitBNO055
from HardwareComponents.DCMotor import DCMotor
from HardwareComponents.StepperMotor import BaseStepperMotor, LeadscrewStepperMotor
from HardwareComponents.UltrasonicSensor import UltrasonicSensor
from HardwareComponents.ServoMotor import ServoMotor
from utilities.path_management import PROJECT_ROOT_PATH, LOGS_DIR
from utilities.logger import LoggerManager

# CONFIG CONSTANTS ------------------------------------------------------------
CAMERA_OFFSET_THRESHOLD = 50  # [cm] the threshold within which the offset is deemed acceptable hence stop tracking

# FUNCTION WRAPPERS FOR DIFFERENT PROCESSES -----------------------------------
def update_IMU_readings(yaw_deg, pitch_deg, arm_deg, stopEvent: mp.Event):
    """
    Designed for multiprocessing, update the input angles in place with most
    recent IMU sensor readings.
    """
    top_IMU = AdafruitBNO055(ADR=True)
    arm_IMU = AdafruitBNO055()

    while not stopEvent.is_set():
        try:
            yaw_deg.value = top_IMU.eulerAngles[0]
            pitch_deg.value = top_IMU.eulerAngles[1]
            arm_deg.value = arm_IMU.eulerAngles[1]

            # Logging data
            logger_manager.log_yaw(yaw_deg.value)
            logger_manager.log_pitch(pitch_deg.value)
            logger_manager.log_arm(arm_deg.value)
        
        # If sensor return invalid (None) value, skip updating for one loop
        except TypeError:
            pass
        
        time.sleep(0.05)
    
    
def update_camera_readings(delta_x: mp.Value, delta_R: mp.Value, stopEvent: mp.Event):
    """
    Update camera readings into the delta_x and delta_R variables in place.
    """
    
    calibration_path = Path(PROJECT_ROOT_PATH, "arucoRPi/calibration.yaml")
    camera = RPiCamera(str(calibration_path))
    
    while not stopEvent.is_set():
        camera.update_frame()
        x, y, z = camera.estimate_coordinates(log=False, save_dir = LOGS_DIR / "Images" / "aruco_tracking")
        
        logger_manager.log_camera_position(x, y, z)
        
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
               

def update_ultrasonic_height(height: mp.Value, stopEvent: mp.Event):
    """
    Update ultrasonic distance readings into the height variables in place
    """
    ultrasonicSensor = UltrasonicSensor()
    
    while not stopEvent.is_set():
        distance = ultrasonicSensor.get_distance()
        height.value = distance
        logger_manager.log_ultrasonic_distance(height.value)
        time.sleep(1)


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
            dcMotor.forward(dutyCycle=100)
        elif delta_R.value < (-1 * CAMERA_OFFSET_THRESHOLD):
            dcMotor.backward(dutyCycle=100)
        else:
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
            baseMotor.spin(steps=10, sleep_time=0.0002, clockwise=True)
        elif delta_x.value < (-1 * CAMERA_OFFSET_THRESHOLD):
            baseMotor.spin(steps=10, sleep_time=0.0002, clockwise=False)
        
    GPIO.cleanup()

  
def balance_platform(pitch: mp.Value, stopEvent: mp.Event):
    
    Leadscrew = LeadscrewStepperMotor(dir_pin=20, step_pin=21)
    
    time_sleep = 0.0005
    
    while not stopEvent.is_set():
        if pitch.value >= 4:  # Retracts
            Leadscrew.single_spin(sleep_time=time_sleep, clockwise=False)
            # Leadscrew.spin(steps=steps, sleep_time=time_sleep, clockwise=False)  # Retracts to reduce pitch
        elif pitch.value <= -4:  # Extends
            Leadscrew.single_spin(sleep_time=time_sleep, clockwise=True)
            # Leadscrew.spin(steps=steps, sleep_time=time_sleep, clockwise=True)  # Extends to increase pitch
        # time.sleep(time_sleep)

    GPIO.cleanup()


def turn_servo(height: mp.Value, stopEvent: mp.Event):
    
    servoMotor = ServoMotor()
    servoMotor.set_angle(0)
    
    while not stopEvent.is_set():
        if height.value < 3:
            servoMotor.set_angle(90)
            time.sleep(1)
            servoMotor.set_angle(0)


# MAIN CODE -------------------------------------------------------------------
if __name__ == "__main__":

    # ===== Parameter setup =====
    yaw = mp.Value('f', 0.0)      # Current yaw angle of the arm [deg]
    pitch = mp.Value('f', 0.0)    # Current pitch value of the platform [deg]
    alpha = mp.Value('f', 0.0)    # Current arm angle [deg]
    delta_x = mp.Value('f', 0.0)  # Horizontal distance between camera and marker [cm]
    delta_R = mp.Value('f', 0.0)  # Vertical distance between camera and marker [cm]
    height = mp.Value('f', 0.0)   # Distance measured by ultrasonic sensor

    # File name to log data
    log_file_path = Path(__file__).parent / 'logs/main.log'
    logger_manager = LoggerManager(log_file_path)

    # Global Stop Event
    stopEvent = mp.Event()

    # ===== Initiate processes =====
    processes = [
        mp.Process(target=update_IMU_readings, args=(yaw, pitch, alpha, stopEvent,)),
        mp.Process(target=update_camera_readings, args=(delta_x, delta_R, stopEvent,)),
        mp.Process(target=update_ultrasonic_height, args=(height, stopEvent,)),
        mp.Process(target=forward_tracking, args=(delta_R, stopEvent,)),
        mp.Process(target=side_tracking, args=(delta_x, stopEvent,)),
        mp.Process(target=balance_platform, args=(pitch, stopEvent,)),
        mp.Process(target=turn_servo, args=(height, stopEvent,))
    ]

    # Start the processes
    for p in processes:
        p.start()

    # Wait indefinitely until program is terminated
    try:
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:       
        print("Initializing stop event")
        logger_manager.cleanup()

    # Ensure process resources are cleaned up
    finally:
        stopEvent.set() 
        for p in processes:
            p.join()
        print("Program has ended gracefully.")
        logging.error("Program terminated.")
