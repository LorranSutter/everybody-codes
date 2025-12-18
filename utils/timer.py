import time
import functools


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
        print(f"Function {func.__name__!r} took: {execution_time:f} seconds")
        return result

    return wrapper_timer
