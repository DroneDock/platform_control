"""
Author: Gai Zhe
Date: April 11 2024
Description: This script plots a figure corresponding to a log file stored 
in `logs`, and save the figure in the `plot` directory under the same name.
"""
# Standard Imports
from pathlib import Path
# Third-Party Imports
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Path to your log file
log_file_path = Path(__file__).parent.parent / 'logs/IMU_readings.log'

# Initialize lists to hold the parsed data
timestamps_pitch = []
readings_pitch = []
timestamps_yaw = []
readings_yaw = []
timestamps_alpha = []
readings_alpha = []


def parse_time(time_str):
    t = datetime.strptime(time_str, '%d-%b-%y %H:%M:%S.%f')
    t = t.timestamp()   
    return t


# Read and parse the log file
with open(log_file_path, 'r') as file:
    
    # Read the first line to get the starting time
    first_line = file.readline()
    parts = first_line.strip().split(' - ')
    if len(parts) >= 3:
        timestamp_str = parts[0]
        start_time = parse_time(timestamp_str)
    
    # Obtain the remaining data
    for line in file:
        parts = line.strip().split(' - ')
                
        timestamp_str, IMU_no, reading = parts
        ts = parse_time(timestamp_str)
        
        # Handle None case
        if reading == 'None':
            continue
        
        if IMU_no == 'Yaw Angle':
            timestamps_yaw.append(ts - start_time)
            readings_yaw.append(float(reading))
            
        elif IMU_no == 'Pitch Angle':
            timestamps_pitch.append(ts - start_time)
            readings_pitch.append(float(reading))
        
        elif IMU_no == 'Arm Angle':
            timestamps_alpha.append(ts - start_time)
            readings_alpha.append(float(reading))
        
        else:
            continue

# Plotting
fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

# Plot Yaw readings
axes[0].plot(timestamps_yaw, readings_yaw, label='Yaw')
axes[0].set_title('Top IMU')
axes[0].set_ylabel('Yaw Angle [deg]')

# Plot Pitch readings
axes[1].plot(timestamps_pitch, readings_pitch, label='Pitch')
axes[1].set_ylabel('Platform Pitch Angle [deg]')

# Plot Arm readings
axes[2].plot(timestamps_pitch, readings_pitch, label='IMU_2', color='orange')
axes[2].set_title('Arm IMU')
axes[2].set_ylabel('Arm Angle [deg]')

axes[2].set_xlabel('Timestamp')

# Improve layout and show plot
plt.tight_layout()
plt.savefig(Path(__file__).parent / "IMU_readings.png")
plt.show()
