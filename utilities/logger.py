import logging
from pathlib import Path

class LoggerManager:
    """
    The project-wide class for logging purposes, designed to log sensor data
    pertaining to the project.
    
    Currently supported data are:
    1. Yaw Angle (float)
    2. Pitch angle (float)
    3. Arm Angle
    4. Camera Position
    5. Ultrasonic Distance
    """

    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(filename=self.log_file_path,
                            filemode='w',
                            datefmt='%d-%b-%y %H:%M:%S',
                            format='%(asctime)s.%(msecs)03d - %(name)s - %(message)s',
                            level=logging.INFO)

        self.logger_yaw = logging.getLogger('Yaw Angle')
        self.logger_pitch = logging.getLogger('Pitch Angle')
        self.logger_arm = logging.getLogger('Arm Angle')
        self.logger_camera = logging.getLogger('Camera Position')
        self.logger_ultrasonic = logging.getLogger('Ultrasonic Distance')

    def log_yaw(self, yaw):
        self.logger_yaw.info(yaw)

    def log_pitch(self, pitch):
        self.logger_pitch.info(pitch)

    def log_arm(self, alpha):
        self.logger_arm.info(alpha)

    def log_camera_position(self, x, y, z):
        self.logger_camera.info(f"X: {x}, Y: {y}, Z: {z}")

    def log_ultrasonic_distance(self, height):
        self.logger_ultrasonic.info(height)

    def cleanup(self):
        logging.info("Successful Cleanup")
        logging.shutdown()
