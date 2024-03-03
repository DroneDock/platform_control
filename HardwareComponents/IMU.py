# Standard Imports
from typing import Tuple

# Third Party Imports
import board
import busio
import adafruit_bno055

class CustomIMU:
    """
    Establish an IMU class that can return acceleration, angular velocity,
    temperature, quarternions, etc.

    This is just a wrapper for the adafruit I2C library.
    """
    # Use V_in instead of 3V3

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)  # Initialize I2C connection
        self._sensor = adafruit_bno055.BNO055_I2C(i2c)  # Initialize sensor

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

    def eulerAngle(self, wrap=False) -> Tuple[float, float, float]:
        """
        Get the Euler angle from the IMU as a tuple (yaw, roll, pitch)

        If wrap = True, Wrap the angle to +-180 degree.
        """
        yaw, roll, pitch = self._sensor.euler

        # Wrap the angle from (0, 360) to (-180, 180)
        if wrap:
            if (yaw > 180): yaw -= 360

        return (yaw, roll, pitch)

    
