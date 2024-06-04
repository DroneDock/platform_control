"""
Description -------------------------------------------------------------------
This class is a wrapper around the pose estimation code written by Jalen.
This script can be run to save a video of the camera with pose estimation. 

Example Usage -----------------------------------------------------------------
Run this script in a terminal:
```
python HardwareComponents/Camera.py
```
The camera will start recording, then press Ctrl+C to stop and save the video.

Authors -----------------------------------------------------------------------
Jalen & Gai Zhe
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
        self.MARKER_SIZE = 30  # Square size [mm] - allow for pose and distance estimation
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
        
        time.sleep(2)  # To warm up camera before any operations
        
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
        self.cam.capture(self.frame, 
                         format='bgr', 
                         use_video_port=True)  # NOTE: THIS IS ESSENTIAL FOR RAPID CAPTURES
        
    def capture_and_save(self, save_path):
        """
        Capture the frame and save it within specified path. Good to test
        if the camera is working.
        """
        self.update_frame()
        cv2.imwrite(save_path, self.frame.array)

    def capture_video(self, save_dir: Path = LOGS_DIR / "Videos"):
        """
        Turn on the camera and save camera output as a video named after the
        start time under the specified directory.
        """
        # Initialize VideoWriter and file object to write to
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S")
        save_dir.mkdir(parents=True, exist_ok=True)  # Create video folder if not exists
        video_path = save_dir / f"{timestamp}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        output = cv2.VideoWriter(str(video_path), fourcc, self.cam.framerate, self.cam.resolution)
        
        # Continuously capture images
        self._clear_frame_buffer()  # Ensure buffer is clear for first frame
        for frame in self.cam.capture_continuous(self.frame, format="bgr", use_video_port=True):
            try:
                image = frame.array  # Numpy array representing the image
                gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                # Detect markers
                (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray_frame,
                                                    dictionary=self.arucoDict,
                                                    parameters=self.arucoParams)
                
                # If none or more than one arUco marker is detected, return -1
                if not corners or (ids is not None and ids.size > 1):
                    if not corners:
                        print("No marker detected")
                    else:
                        print("More than one marker detected")
                    self.x = self.y = self.z = -1
                    output.write(image)
                    self._clear_frame_buffer()
                    continue
                
                # Perform pose estimation
                print("One marker detected!")
                rVec, tVec, _ = cv2.aruco.estimatePoseSingleMarkers(
                    corners=corners, 
                    markerLength=self.MARKER_SIZE,
                    cameraMatrix=self.camMatrix,
                    distCoeffs=self.distCof
                )
                self.x, self.y, self.z = tVec.flatten()
                
                # Draw lines on marker for visualisation
                cv2.polylines(image, [corners[0].astype(np.int32)], isClosed=True,
                            color=(0, 255, 255), thickness=3, 
                            lineType=cv2.LINE_AA)
                # Annotate Pose
                cv2.drawFrameAxes(image, self.camMatrix, self.distCof, 
                                rVec, tVec, length=50, thickness=3)
                # Annotate with coordinates
                text = f"x = {np.round(self.x, 2)}, y = {np.round(self.y, 2)}, z = {np.round(self.z, 2)}"
                cv2.putText(image, text, (10, image.shape[0] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 127, 127), 2, cv2.LINE_AA)

                output.write(image)
                self._clear_frame_buffer()
                    
            except KeyboardInterrupt:
                break
            
    def _rotation_matrix_to_euler_angles(self, R):
        """
        Return the Euler roll, pitch and yaw in degrees , which are the 
        rotations around the x, y and z axes respectively.
        
        Note: Assumes the rotation matrix uses the rotation sequence z-y-x
        """
        sy = np.sqrt(R[0,0] * R[0,0] + R[1,0] * R[1,0])
        singular = sy < 1e-6
        if not singular:
            x = np.arctan2(R[2,1], R[2,2])
            y = np.arctan2(-R[2,0], sy)
            z = np.arctan2(R[1,0], R[0,0])
        else:
            x = np.arctan2(-R[1,2], R[1,1])
            y = np.arctan2(-R[2,0], sy)
            z = 0

        return np.degrees(x), np.degrees(y), np.degrees(z)
        
            
    def estimate_coordinates(self, log: bool = False, save_dir: Path = LOGS_DIR / "Images"):
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
            
            if log:
                # Save the frame in a folder named after its timestamp. Create if not yet exist
                save_dir.mkdir(parents=True, exist_ok=True)
                timestamp = datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S-%f")
                cv2.imwrite(str(save_dir / f"{timestamp}.png"), image)

            return (-1, -1, -1)
                    
        # Perform pose estimation
        rVec, tVec, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners=corners, 
            markerLength=self.MARKER_SIZE,
            cameraMatrix=self.camMatrix,
            distCoeffs=self.distCof
        )
        # Save results 
        print("Marker detected")
        rotation_matrix, _ = cv2.Rodrigues(rVec[0][0])  # rVec is naturally a nested matrix, hence the subscript [0][0]
        roll, pitch, yaw = self._rotation_matrix_to_euler_angles(rotation_matrix)
        print(f"The pitch of the marker is {roll}")

        x, y, z = tVec.flatten()
        
        # Save the series of images
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
            text2 = f"Roll = ({np.round(roll, 2)}, Pitch = {np.round(pitch, 2)}, Yaw = {np.round(yaw, 2)},)"
            cv2.putText(image, text2, (10, image.shape[0] - 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
            # Save the frame in a folder named after its timestamp. Create if not yet exist
            save_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S-%f")
            cv2.imwrite(str(save_dir / f"{timestamp}.png"), image)
        
        return x, y, z
                            
    def __del__(self):
        self.cam.close()

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    
    # Path of file containing calibration matrices
    calibration_path = Path(PROJECT_ROOT_PATH, "arucoRPi/calibration.yaml").resolve()
    
    # Path of images saved
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S-%f")
    save_directory = Path(LOGS_DIR / "Images" / "images_{timestamp}")

    camera = RPiCamera(calibration_path)
    
    while True:
        try:
            camera.update_frame()
            x, y, z = camera.estimate_coordinates(log=True, save_dir=save_directory,)
            
        except KeyboardInterrupt:
            break
