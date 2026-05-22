import time
import functools

from utils.utils import tcolors


def timer(func):
    """
    Decorator to measure the execution time of a function.
    """

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Function {func.__name__!r} took: {tcolors.RED}{execution_time:f}{tcolors.RESET} seconds")
        return result

    return wrapper_timer
