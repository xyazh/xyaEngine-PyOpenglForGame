import time
import base64
import re
import threading
from PIL import Image
from io import BytesIO

import threading
import time

def xyaTimerFunc(t: int, fuc):
    if not hasattr(xyaTimerFunc, 'frist') or xyaTimerFunc.frist:
        t /= 1000
        xyaTimerFunc.frist = False
        nano_time_start = time.process_time_ns()
        nano_time_end = nano_time_start

        def wrapper():
            while True:
                nonlocal nano_time_start, nano_time_end
                nano_time_end = time.process_time_ns()
                dt = nano_time_end - nano_time_start
                dt /= 1000000000
                fuc()
                nano_time_start = time.process_time_ns()
                sleep_time = t - dt
                if sleep_time > 0:
                    time.sleep(sleep_time)
        threading.Thread(target=wrapper, daemon=True).start()


def run_time(fuc):
    def r_fuc(*args, **kw):
        t = time.time()
        r = fuc(*args, **kw)
        print(time.time()-t)
        return r
    return r_fuc

def get_run_time(fuc):
    def r_fuc(*args, **kw):
        t = time.time()
        r = fuc(*args, **kw)
        return time.time()-t,r
    return r_fuc

def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds to execute.")
        return result
    return wrapper
    
def base64_to_image(base64_data)->Image:
    base64_data = re.sub('^data:image/.+;base64,', '', base64_data)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    return Image.open(image_data)