"""
File: plotIMU.py
Author: Gai Zhe
Date: April 11 2024
Description: This script allows the user to control the base stepper and DC 
motors, logging and plotting the IMU readings at the same time. 

Example Usage:
    ```
    python test/plotIMU.py
    ```
"""

# Standard Imports
import time
import logging
import multiprocessing as mp
from pathlib import Path
import keyboard
# Project-Specific Imports
from HardwareComponents.IMU import AdafruitBNO055
from HardwareComponents.DCMotor import DCMotor
from HardwareComponents.StepperMotor import BaseStepperMotor, LeadscrewStepperMotor

# File Management
log_file_path = Path(__file__).parent.parent / 'logs/IMU_readings.log'
logging.basicConfig(filename=log_file_path, 
                    filemode='w', 
                    datefmt='%d-%b-%y %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(message)s',
                    level=logging.INFO)

# Processes -------------------------------------------------------------------
def keyboard_monitor(shared_keys):
    # Mapping of keys to their respective positions in the shared array
    key_map = {'w': 0, 'a': 1, 's': 2, 'd': 3}

    # Registering hotkeys
    for key in key_map:
        keyboard.on_press_key(key, lambda e, k=key: shared_keys.__setitem__(key_map[k], 1))
        keyboard.on_release_key(key, lambda e, k=key: shared_keys.__setitem__(key_map[k], 0))

    # Keep the process running
    keyboard.wait()


if __name__ == '__main__':
    
    # Initialize Components
    IMU_top = AdafruitBNO055(ADR=True)    # Top-IMU measuring pitch_angle
    IMU_arm = AdafruitBNO055(ADR=False)   # Arm IMU measuring arm_angle
    YawMotor = BaseStepperMotor(ena_pin=23, dir_pin=20, pul_pin=25)
    ArmMotor = DCMotor(In1=17, In2=27, EN=18)
    # Leadscrew = LeadscrewStepperMotor(dir_pin=20, step_pin=21)
    
    # Create loggers for each component
    logger_IMU_1 = logging.getLogger('IMU_1')
    logger_IMU_2 = logging.getLogger('IMU_2')
    
    # Global array storing the pressed keyboard values
    shared_keys = mp.Array('i', [0]*4)
    listener_process = mp.Process(target=keyboard_monitor, args=(shared_keys,))
    listener_process.start()
    
    # Initial 2 seconds delay for components to be ready
    print("Waking up"); time.sleep(2); print("Ready!!")
    
    # Main Program
    try:
        while True:
            
            # Get the IMU values
            pitch = IMU_top.eulerAngles[2]
            alpha = IMU_arm.eulerAngles[1]
            
            # Movement logic
            if shared_keys[0]: # W
                ArmMotor.forward()
            if shared_keys[1]: # A
                YawMotor.spin(steps=100, sleep_time=0.0005, clockwise=True)
            if shared_keys[2]: # S
                ArmMotor.backward()
            if shared_keys[3]: # D
                YawMotor.spin(steps=100, sleep_time=0.0005, clockwise=False)
                
            time.sleep(0.1)
            ArmMotor.stop()
            
            # Logging
            logger_IMU_1.info(pitch)
            logger_IMU_2.info(alpha)
            
    except KeyboardInterrupt:
        logging.error("Program terminated via keyboard.")
        
    finally:
        listener_process.terminate()
        listener_process.join()
        logging.info("Successful Cleanup")

