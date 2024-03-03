# Standard Imports
import time

# Third Party Imports
import RPi.GPIO as GPIO
import board
import busio
import adafruit_bno055

from HardwareComponents.IMU import CustomIMU

## ========================================================================== ##
IMU = CustomIMU()

# def temperature():
#     last_val = 0xFFFF
#     result = sensor.temperature
#     if abs(result - last_val) == 128:
#         result = sensor.temperature
#         if abs(result - last_val) == 128:
#             return 0b00111111 & result
#     last_val = result
#     return result


while True:
    print("Temperature: {} degrees C".format(IMU.temperature()))
    """
    print(
        "Temperature: {} degrees C".format(temperature())
    )  # Uncomment if using a Raspberry Pi
    """
    
    # These returns a tuple of in the (x, y, z) direction
    # print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    # print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    # print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    print("Euler angle: {}".format(IMU.eulerAngle()))
    print("Wrapped angle: {}".format(IMU.eulerAngle(wrap=True)))
    # print("Quaternion: {}".format(sensor.quaternion))
    # print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    # print("Gravity (m/s^2): {}".format(sensor.gravity))
    print()

    time.sleep(1)
