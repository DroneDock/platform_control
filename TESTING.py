# Standard Imports
import time
import multiprocessing as mp
import logging
# from multiprocessing import Queue
from pathlib import Path

# # Third-Party Imports
# import numpy as np
# import RPi.GPIO as GPIO

# Project Specific Imports
# from HardwareComponents.Camera import RPiCamera
# from HardwareComponents.IMU import AdafruitBNO055
# from HardwareComponents.DCMotor import DCMotor
#from HardwareComponents.StepperMotor import BaseStepperMotor, LeadscrewStepperMotor
#from utilities.decorators import time_this_func
from utilities.path_management import PROJECT_ROOT_PATH, LOGS_DIR
from test.plotIMU import LoggerManager #Logger 

# # FUNCTION WRAPPERS FOR DIFFERENT PROCESSES -----------------------------------
# def update_IMU_readings(yaw_deg, pitch_deg, arm_deg, stopEvent: mp.Event):
#     """
#     Designed for multiprocessing, update the input angles in place with most
#     recent IMU sensor readings.
#     """
#     top_IMU = AdafruitBNO055(ADR=True)
#     arm_IMU = AdafruitBNO055()
#     #logger = LoggerManager(log_file_path=LOGS_DIR / "logs/test2.log")

#     while not stopEvent.is_set():
#         try: #TODO: update values individually so None for one value does not affect others
#             yaw_deg.value = top_IMU.eulerAngles[0]
#             pitch_deg.value = top_IMU.eulerAngles[1]
#             arm_deg.value = arm_IMU.eulerAngles[1]
            
#         except TypeError:
#             pass  # Skip update for one loop if sensor returns None
        
#         # print(f"Yaw: {yaw_deg.value}, Pitch: {pitch_deg.value}, Arm: {arm_deg.value}")
#         time.sleep(0.05)
    
    
# def update_camera_readings(delta_R, delta_theta, stopEvent: mp.Event):
#     """
#     Update camera readings into the R and theta variables in place.
#     """
    
#     camera = RPiCamera(calibration_path=Path(__file__).parent / "arucoRPi/calibration.yaml")
    
#     while not stopEvent.is_set():
#         start_time = time.time()
#         camera.update_frame()
#         x, y, z = camera.estimate_coordinates(log=False)
        
#         print("Camera outputs are: ", x, y, z)

#         # Guard clause: when no marker is detected
#         if z < 0:
#             delta_R.value = 0  # Signal DC motor to stop
#             print("No marker detected.")
#             end_time = time.time()
#             duration = end_time - start_time
#             print(f'Camera code executed in {duration} seconds')
#             continue
        
#         y = -y  # 'estimate_coordinates' return y positive downwards, so recalibrate it with htis
        
#         r = np.sqrt(x**2 + y**2)
#         theta = np.arctan2(y, x)
        
#         # When angle is lower than zero, the marker is located at third or fourth
#         # quadrant, so a retraction is required.
#         if theta < 0:
#             delta_R.value = -r
#         delta_theta.value = theta
        
#         print(delta_R.value)
#         print(delta_theta.value)
        
#         end_time = time.time()
#         duration = end_time - start_time
#         print(f'Camera code executed in {duration} seconds')

# Function to be executed by each process
def worker_function(logger,stopEvent: mp.Event):
    while not stopEvent.is_set():
        logger_manager.log_yaw(logger)
        print("it should be fucking logging")

    logger_manager.cleanup()


# def move_arm(stopEvent: mp.Event):
    
#     dcMotor = DCMotor(In1=17, In2=27, EN=18)
    
#     time.sleep(5)
    
#     while not stopEvent.is_set():
#         dcMotor.forward(duration=1.5)
#         dcMotor.backward(duration=1.8)  # FOR THE SAME 
        
#     dcMotor.stop()
#     GPIO.cleanup()
    

# # Only track radius changes for now
# def track_marker(delta_R, delta_theta, stopEvent: mp.Event):
    
#     dcMotor = DCMotor(In1=17, In2=27, EN=18)
#     time.sleep(5)
    
#     while not stopEvent.is_set():
#         if delta_R > 0:  # Require extension
#             dcMotor.forward(duration=0.1)
#         elif delta_R < 0:  # Require retraction
#             dcMotor.backward(duration=0.1)
#         else:  # Stop the motor (happens when no marker detected)
#             dcMotor.stop()

#     dcMotor.stop()
#     GPIO.cleanup()
        
# def balance_platform(pitch: mp.Value, stopEvent: mp.Event):
    
#     Leadscrew = LeadscrewStepperMotor(dir_pin=20, step_pin=21)
    
#     time.sleep(5)
    
#     time_sleep = 0.0006 # This has been proved to be consistent
#     # steps = 1
    
#     while not stopEvent.is_set():
#         if pitch.value >= 2:  # Retracts
#             Leadscrew.single_spin(sleep_time=time_sleep, clockwise=False)
#             # Leadscrew.spin(steps=steps, sleep_time=time_sleep, clockwise=False)  # Retracts to reduce pitch
#         elif pitch.value <= -2:  # Extends
#             Leadscrew.single_spin(sleep_time=time_sleep, clockwise=True)
#             # Leadscrew.spin(steps=steps, sleep_time=time_sleep, clockwise=True)  # Extends to increase pitch
#         # time.sleep(time_sleep)

#     GPIO.cleanup()
    

if __name__ == "__main__":
    log_file_path = Path(__file__).parent / 'logs/multiprocessing.log'
    logger_manager = LoggerManager(log_file_path)
    # Global Stop Event
    stopEvent = mp.Event()

    # ===== Initiate processes =====
    logger= 5
    processes = [
     mp.Process(target=worker_function, args=(logger,stopEvent))
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

    # Ensure process resources are cleaned up
    finally:
        stopEvent.set() 
        for p in processes:
            p.join()
        print("Program has ended gracefully.")

        logging.error("Program terminated.")