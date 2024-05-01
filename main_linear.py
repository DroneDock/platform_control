import time
from pathlib import Path

# Third-Party Imports
import RPi.GPIO as GPIO

# Project Specific Imports
from HardwareComponents.Camera import RPiCamera
from HardwareComponents.IMU import AdafruitBNO055
from HardwareComponents.DCMotor import DCMotor
from HardwareComponents.StepperMotor import BaseStepperMotor, LeadscrewStepperMotor


if __name__ == '__main__':
    
    camera = RPiCamera(calibration_path=Path(__file__).parent / "arucoRPi/calibration.yaml")
    IMU_top = AdafruitBNO055(ADR=True)
    IMU_arm = AdafruitBNO055(ADR=False)
    dcMotor = DCMotor()
    
    
    while True:
        try:
            start_time = time.time()
            
            yaw = IMU_top.eulerAngles[0]
            pitch = IMU_top.eulerAngles[1]
            alpha = IMU_arm.eulerAngles[1]
            
            camera.update_frame()
            x, y, z = camera.estimate_coordinates(log=False)
            
            if z < 0:
                delta_R = 0
                print("No marker detected.")
            
            if delta_R > 0:
                dcMotor.forward(duration=0.1)
            elif delta_R < 0:
                dcMotor.backward(duration=0.1)
            else:
                dcMotor.stop()
                
            end_time = time.time()
            
            duration = end_time - start_time
            print(f'The program takes {duration} seconds')
            
        except KeyboardInterrupt:
            GPIO.cleanup()
            
        finally:
            GPIO.cleanup()