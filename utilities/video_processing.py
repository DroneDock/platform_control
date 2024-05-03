# Standard Imports
import os
from pathlib import Path
# Third-Party Imports
import cv2
# Project-Specific Imports
from utilities.path_management import LOGS_DIR

def images_to_video(input_dir: Path, output_path: Path, frame_rate: int = 5):
    """
    Convert a series of images saved under input_dir to a video saved in
    output_path
    """
    # Set up the correct codec and create a VideoWriter obejct
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')

    if isinstance(output_path, Path):  # Ensure this is a string before supplied to cv2
        output_path = str(output_path)
    out = cv2.VideoWriter(output_path, fourcc, frame_rate, (640, 480))
    
    images = [img for img in os.listdir(input_dir) if img.endswith(".png")]
    images.sort()  # Sort by name
    
    for image_name in images:
        img_path = os.path.join(input_dir, image_name)
        img = cv2.imread(img_path)
        
        # Check if the image is successfully loaded
        if img is not None:
            out.write(img)
            

    print("Successfully saved as video")
    
if __name__ == '__main__':
    
    images_to_video(input_dir = LOGS_DIR / "Images", output_path= LOGS_DIR / "Videos" / "output_video.avi")
    