# platform_control
Code for Platform Control

## Setup
### Configuring Virtual Environment
To setup the python environment for the Raspberry Pi Model 4 (main board for 
this project), **python 3.9.2** is needed due to dependency limitations of the 
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

## Running the Program
To run the program, simply run the following command in the project root:
```code
python main.py
```

## Additional Documentation
