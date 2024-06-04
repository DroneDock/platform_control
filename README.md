# platform_control
Main code for the project.

### Project Structure
The main folders of the project are shown
```
|
|----- 📁 HardwareComponents
|       |----- Camera.py
|       |----- DCMotor.py
|       |----- Relay.py
|       |----- IMU.py
|       |----- StepperMotor.py
|
|----- 📁 test
|       |----- BaseStepperMotorTest.py
|       |----- DCMotorTest.py
|       |----- ...
|
|----- 📁 demo
|       |----- platform_levelling.py
|       |----- aruco_tracking.py
|       |----- turn_all_components.py
|
|----- 📁 utilities
|       |----- decorators.py
|       |----- path_management.py
|
|----- 📁 logs
```

* 📁 **HardwareComponents** - Contain all the classes used to control the electronic components
* 📁 **test** - Contain all the files that can be run standalone to test whether individual electronic components, such as those defined in 📁 HardwareComponents, work as intended. These are short programs useful for testing electrical connections. 
* 📁 **demo** - Similar to test but instead of testing individual components, this folder contains scripts which
combine multiple components working in tandem to achieve higher-level functionalities such as platform levelling.
* 📁 **utilities** - Contain general tools (constants, functions and classes) to aid development, e.g, a file named `path_management.py` contains paths to the project root that can be referenced by other scripts.
* 📁 **logs** - Contain all the logs and any collected data during run time.


## Setup
### Configuring Virtual Environment
To setup the python environment for the Raspberry Pi Model 4 (main board for 
this project), **python 3.9.4** is used due to dependency limitations of the 
ArUco detection code. Since the default python version for the Pi 4 is version
3.11.2, we can change the environment with the **pyenv** program. The tutorial
on how to use this is shown in [this youtube video](https://www.youtube.com/watch?v=QdlopCUuXxw&t=6s).

The required packages are listed in *requirements.txt*.

Run the following code:
```code
pip install -r requirements.txt
```

### Setup repository as a package
When running the program, you might encounter import issue. If that is the case,
it means the repository must be configured as a library. To do this, run the 
following code in the project root.

```code
pip install -e .
```

## Running the program
To run the program, simply run the following command in the project root:
```code
python main.py
```


## Testing
When developing or working on the project, the connections to individual
components can be tested by running their respective scripts under 
`HardwareComponents`. For example, to check if the IMU is working correctly:
```
python test/IMU.py
```
If there are readings shown, the connections are correct. If the output is I2C
error, then there might be faulty connections.
