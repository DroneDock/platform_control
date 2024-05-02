import time
import logging
from pathlib import Path

log_file_path = Path(__file__).parent.parent / 'logs/timings.log'
logging.basicConfig(filename=log_file_path,
                    filemode='w',
                    datefmt='%d-%b-%y %H:%M:%S',
                    format='%(asctime)s.%(msecs)03d - %(name)s - %(message)s',
                    level=logging.INFO)

def time_this_func(func):
    
    def wrapper(*args, **kwargs):
        
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"Function '{func.__name__}' executed in {duration:.4f} seconds")
        return result
    
    return wrapper

