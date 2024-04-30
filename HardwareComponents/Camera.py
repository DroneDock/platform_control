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
        
    def update_frame(self):
        # Clear the buffer to frame
        self.frame.truncate(0)
        self.frame.seek(0)
        # Capture an image and update it to "frame" attribute
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
        
        for frame in self.cam.capture_continuous(self.frame, format="bgr", use_video_port=True):
            image = frame.array
            gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray_frame,
                                                dictionary=self.arucoDict,
                                                parameters=self.arucoParams)
            
            # If none or more than one arUco marker is detected, return -1
            if not corners or ids.size > 1:
                print("None/More than 1 marker(s) detected!")
                x, y, z = -1
                        
            # Perform pose estimation
            rVec, tVec, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners=corners, 
                markerLength=self.MARKER_SIZE,
                cameraMatrix=self.camMatrix,
                distCoeffs=self.distCof
            )
            
            x, y, z = tVec.flatten()
            
            # Save as a series of images
            if log:
                print(rVec)
                print(tVec)
                topLeft, topRight, btmRight, btmLeft = corners.reshape((4, 2))
                
                # Draw lines on marker for visualisation
                cv2.polylines(image, [corners.astype(np.int32)], isClosed=True,
                              color=(0, 255, 255), thickness=3, 
                              lineType=cv2.LINE_AA)
                # Annotate Pose
                cv2.drawFrameAxes(image, self.camMatrix, self.disCof, 
                                  rVec, tVec, length=50, thickness=3)
                # Annotate with coordinates
                text = f"x = {np.round(x, 2)}, y = {np.round(y, 2)}, z = {np.round(z, 2)}"
                cv2.putText(image, text, (10, image.shape[0] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2, cv2.LINE_AA)
                # Save image as timestamp
                timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")
                cv2.imwrite(f"frames/frame_{timestamp}.png", image)
                
            return x, y, z
            
    def estimate_coordinates(self, log: bool = True):
        """
        Return the coordinates of ArUco marker (if any) relative to the centre
        of the frame. Return (-1, -1, -1) if no markers are detected.
        """
        image = self.frame.array
        gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray_frame,
                                            dictionary=self.arucoDict,
                                            parameters=self.arucoParams)

        # If none or more than one arUco marker is detected, return -1
        if not corners or (ids is not None and ids.size > 1):
            print("None/More than 1 marker(s) detected!")
            self.frame.truncate(0)
            self.frame.seek(0)
            return (-1, -1, -1)
                    
        # Perform pose estimation
        rVec, tVec, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners=corners, 
            markerLength=self.MARKER_SIZE,
            cameraMatrix=self.camMatrix,
            distCoeffs=self.distCof
        )
        
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
            # Save image as timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")
            cv2.imwrite(str(Path(__file__).parent / f"captured_image_t{timestamp}.png"), image)
        
        return x, y, z

        
    def __del__(self):
        self.cam.close()
                        

    
if __name__ == '__main__':
    
    project_root = Path(__file__).parent.parent
    
    calibration_path = Path(project_root, "arucoRPi/calibration.yaml").resolve()
    save_path = Path(project_root, "logs/captured_images/captured_image.png").resolve()
    
    camera = RPiCamera(calibration_path)
    
    camera.capture_and_save(str(save_path))
    
    while True:
        try:
            camera.update_frame()
            x, y, z = camera.estimate_coordinates()
        except KeyboardInterrupt:
            print("Terminated")
            
