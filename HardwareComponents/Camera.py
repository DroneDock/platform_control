"""
This class is a wrapper around the pose estimation code written by Jalen.

Author: Jalen, Gai Zhe
"""

# Standard Imports
import time
import datetime
from pathlib import Path
# Third party imports
import cv2
import numpy as np
import yaml
from picamera import PiCamera
from picamera.array import PiRGBArray
# Project-Specific Imports
from utilities.path_management import PROJECT_ROOT_PATH, LOGS_DIR
from arucoRPi.arucoDict import ARUCO_DICT

class RPiCamera(object):
    """
    Wrapper class around the PiCamera class.
    """
    
    def __init__(self, calibration_path:str):
        
        # Initialize camera properties
        self.cam = PiCamera()
        self.cam.resolution = (640, 480)
        self.cam.framerate = 32
        self.cam.rotation = 0
        
        # Initialize ArUco marker properties
        self.MARKER_SIZE = 60  # Square size [mm] - allow for pose and distance estimation
        self.arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_6X6_50"])
        self.arucoParams = cv2.aruco.DetectorParameters_create()  # Use default parameters
        
        # Load calibration data
        with open(calibration_path) as f:
            loadeddict = yaml.load(f, Loader=yaml.FullLoader)
        camMatrix = loadeddict.get('camera_matrix')
        distCof = loadeddict.get('dist_coeff')
        self.camMatrix = np.array(camMatrix)
        self.distCof = np.array(distCof)
        print("Loaded calibration data successfully")
        
        self.frame = PiRGBArray(self.cam, size=self.cam.resolution)  # Array to store RGB arrays of a single frame, updated with capture 
        
        time.sleep(2)  # For startup
        
    def _clear_frame_buffer(self):
        """
        Clear the PiRGBArray stored in self.frame. This is required between
        updates of the frame attribute.
        """
        self.frame.truncate(0)
        self.frame.seek(0)
        
    def update_frame(self):
        """
        Capture an image and store it in the frame attribute. This can be used
        consecutively since the buffer is cleared in this function.
        """
        self._clear_frame_buffer()
        self.cam.capture(self.frame, format='bgr')
        
    def capture_and_save(self, save_path):
        """
        Capture the frame and save it within specified path. Good to test
        if the camera is working.
        """
        self.update_frame()
        cv2.imwrite(save_path, self.frame.array)
    
    def capture_continuous(self, log : bool = True):
        """
        Return the x, y coordinates of the marker relative to the camera centre.
        Returns -1 if:
            - No marker is detected
            - More than one markers are detected
        """
        
        self._clear_frame_buffer()
        
        for frame in self.cam.capture_continuous(self.frame, format="bgr", use_video_port=True):
            try: 
                
                image = frame.array
                gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray_frame,
                                                    dictionary=self.arucoDict,
                                                    parameters=self.arucoParams)
                
                # If none or more than one arUco marker is detected, return -1
                if not corners or ids.size > 1:
                    print("None/More than 1 marker(s) detected!")
                    x, y, z = (-1, -1, -1)
                    self.frame.truncate(0)
                    self.frame.seek(0)
                    continue
                            
                # Perform pose estimation
                rVec, tVec, _ = cv2.aruco.estimatePoseSingleMarkers(
                    corners=corners, 
                    markerLength=self.MARKER_SIZE,
                    cameraMatrix=self.camMatrix,
                    distCoeffs=self.distCof
                )
                print(rVec)
                print(tVec)
                
                x, y, z = tVec.flatten()
                
                # Save as a series of images
                if log:
                    
                    # Draw lines on marker for visualisation
                    cv2.polylines(image, [corners[0].astype(np.int32)], isClosed=True,
                                color=(0, 255, 255), thickness=3, 
                                lineType=cv2.LINE_AA)
                    # Annotate Pose
                    cv2.drawFrameAxes(image, self.camMatrix, self.distCof, 
                                    rVec, tVec, length=50, thickness=3)
                    # Annotate with coordinates
                    text = f"x = {np.round(x, 2)}, y = {np.round(y, 2)}, z = {np.round(z, 2)}"
                    cv2.putText(image, text, (10, image.shape[0] - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2, cv2.LINE_AA)
                    # Save image with a timestamp in its name
                    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")
                    cv2.imwrite(f"frames/frame_{timestamp}.png", image)
                    self.output.write(image)
                    
                    self.frame.truncate(0)

            except KeyboardInterrupt:
                self.output.release()
            finally:
                self.output.release()
                
            return x, y, z
            
    def estimate_coordinates(self, log: bool = True, save_dir: Path = LOGS_DIR / "captured_images"):
        """
        Return the coordinates of ArUco marker (if any) relative to the centre
        of the frame. Return (-1, -1, -1) if no markers are detected.
        
        If `log` is set to true, save each frame as an image named after its 
        timestamp under the directory `save_dir`.
        """
        image = self.frame.array
        gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray_frame,
                                            dictionary=self.arucoDict,
                                            parameters=self.arucoParams)

        # If none or more than one arUco marker is detected, return -1
        if not corners or (ids is not None and ids.size > 1):
            if not corners:
                print("No marker detected")
            else:
                print("More than one marker detected")
            self._clear_frame_buffer()
            return (-1, -1, -1)
                    
        # Perform pose estimation
        rVec, tVec, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners=corners, 
            markerLength=self.MARKER_SIZE,
            cameraMatrix=self.camMatrix,
            distCoeffs=self.distCof
        )
        
        x, y, z = tVec.flatten()
        
        # Save as a video
        if log: 
            # Draw lines on marker for visualisation
            cv2.polylines(image, [corners[0].astype(np.int32)], isClosed=True,
                            color=(0, 255, 255), thickness=3, 
                            lineType=cv2.LINE_AA)
            # Annotate Pose
            cv2.drawFrameAxes(image, self.camMatrix, self.distCof, 
                                rVec, tVec, length=50, thickness=3)
            # Annotate with coordinates
            text = f"x = {np.round(x, 2)}, y = {np.round(y, 2)}, z = {np.round(z, 2)}"
            cv2.putText(image, text, (10, image.shape[0] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2, cv2.LINE_AA)
            # Save the video named after its timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")
            cv2.imwrite(str(save_dir / f"captured_image_t{timestamp}.png"), image)
        
        return x, y, z

        
    def __del__(self):
        self.cam.close()
                        

    
if __name__ == '__main__':
        
    calibration_path = Path(PROJECT_ROOT_PATH, "arucoRPi/calibration.yaml").resolve()
    save_path = Path(LOGS_DIR, "captured_images/captured_image.png").resolve()
    
    camera = RPiCamera(calibration_path)
    
    camera.capture_and_save(str(save_path))
    
    while True:
        try:
            camera.update_frame()
            x, y, z = camera.estimate_coordinates()
        except KeyboardInterrupt:
            print("Terminated")

