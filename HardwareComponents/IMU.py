# Standard Imports
from typing import Tuple

# Third Party Imports
import board
import busio
import adafruit_bno055

class CustomIMU:

    def __init__(self):
        # Initialize IMU connection
        i2c = busio.I2C(board.SCL, board.SDA)
        # Initialize the sensor
        self._sensor = adafruit_bno055.BNO055_I2C(i2c)

    def temperature(self) -> float:
        """
        Return the temperature measured by the IMU.
        """
        return self._sensor.temperature

    def acceleration(self) -> Tuple[float, float, float]:
        """
        Return the 3-axis acceleration [m/s^2] measured by the IMU as a 
        tuple.
        """
        return self._sensor.acceleration
    
    def angularVelocity(self) -> Tuple[float, float, float]:
        """
        Return the 3-axis angular velocity [m/s] measured by the IMU as a 
        tuple.
        """
        return self._sensor.gyro

    def eulerAngle(self) -> Tuple[float, float, float]:
        """
        Get the Euler angle from the IMU.
        """
        return self._sensor.euler
