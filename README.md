# platform_control
Code for Platform Control

## Setup
### Configuring Virtual Environment
To setup the virtual environment neccessary for this project, namely the
following modules:

* **Raspberry Pi GPIO** - Library to control GPIO pins for the raspberry pi
* **Adafruit BNO055** - Library to control the specific IMU model

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

## Running the Program
To run the program, simply run the following command in the project root:
```code
python main.py
```

## Additional Documentation

