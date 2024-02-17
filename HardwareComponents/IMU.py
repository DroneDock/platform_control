import board
import busio
import adafruit_bno055

class CustomIMU:

    def __init__(self):
        # Initialize IMU connection
        i2c = busio.I2C(board.SCL, board.SDA)
        # Initialize the sensor
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)

    def get_euler(self):
        """Get the Euler angle from the IMU."""
        return self.sensor.euler
