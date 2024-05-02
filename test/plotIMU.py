import logging
from pathlib import Path

class LoggerManager:
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

    def log_yaw(self, yaw):
        self.logger_yaw.info(yaw)

    def log_pitch(self, pitch):
        self.logger_pitch.info(pitch)

    def log_arm(self, alpha):
        self.logger_arm.info(alpha)

    def log_camera_position(self, position):
        self.logger_camera.info(position)

    def cleanup(self):
        logging.info("Successful Cleanup")

#Test to log a simple file
if __name__ == '__main__':
    # Standard Imports
    import time

    # File Management
    log_file_path = Path(__file__).parent.parent / 'logs/test1.log'

    logger_manager = LoggerManager(log_file_path)

    try:
        while True:
            # Sample data
            yaw = 45
            pitch = 30
            alpha = 60
            position = (10, 20)

            # Logging
            logger_manager.log_yaw(yaw)
            logger_manager.log_pitch(pitch)
            logger_manager.log_arm(alpha)
            logger_manager.log_camera_position(position)

            time.sleep(1)  # For demonstration, wait for 1 second between readings
    except KeyboardInterrupt:
        logging.error("Program terminated via keyboard.")
    finally:
        logger_manager.cleanup()
