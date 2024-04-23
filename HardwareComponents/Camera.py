"""
This class is a wrapper around the pose estimation code written by Jalen.

Author: Jalen, Gai Zhe
"""

# Standard Imports
import time
from pathlib import Path
# Third party imports
import cv2
import numpy as np
import yaml
from picamera import PiCamera
from picamera.array import PiRGBArray
# Project-Specific Imports
from arucoRPi.arucoDict import ARUCO_DICT

class Camera(object):
    """
    Wrapper class around the PiCamera class.
    """
    
    def __init__(self, calibration_path:str):
        
        # Initialize camera properties
        self.cam = PiCamera()
        self.cam.resolution = (640, 480)
        self.cam.framerate = 32
        self.cam.rotation = 180
        
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
        prev_print_time = time.time()
    
    def marker_coordinates(self, polar: bool = True):
        """
        Return polar coordinates of the centre of an ArUco marker if polar is 
        True, otherwise return in cartersian.
        Returns None if:
            - No marker is detected
            - More than one markers are detected
        """
        
        for frame in self.cam.capture_continuous(self.frame, format="bgr", use_video_port=True):
            image = frame.array
            gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray_frame,
                                                dictionary=self.arucoDict,
                                                parameters=self.arucoParams)
            
            # If ArUco marker is not detected
            if not corners:
                print("No corners detected!")
                return None
            
            # If more than one marker is detected
            if ids.size > 1:
                print("More than one marker detected!")
                return None
            
            # Perform pose estimation
            rVec, tVec, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners=corners, 
                markerLength=self.MARKER_SIZE,
                cameraMatrix=self.camMatrix,
                distCoeffs=self.distCof
            )
            
            # Loggign purposes
            print(rVec)
            print('-----')
            print(tVec)
            
            x, y, z= tVec.flatten()
            
            # Return the coordinates
            if polar:
                r = np.sqrt(x**2 + y**2)  # in metres
                theta = np.arctan2(y, x)  # in radians
                return r, theta
            else:
                return x, y
            
    def capture(self):
        self.cam.capture(self.frame, 'bgr')
        cv2.imwrite(str(Path(__file__).parent / "captured_image.png"), self.frame.array)
        
        
        
    def __del__(self):
        
        self.cam.close()
                        
            
            

    
if __name__ == '__main__':
    
    calibration_path = Path(__file__).parent.parent / "arucoRPi/calibration.yaml"
    
    camera = Camera(calibration_path)
    
    camera.capture()
    
    
        