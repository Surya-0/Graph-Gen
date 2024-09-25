# performance_utils.py
import time
import psutil
import tracemalloc
from functools import wraps

def measure_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Start time and memory tracking
        start_time = time.time()
        tracemalloc.start()
        start_memory = psutil.Process().memory_info().rss / (1024 * 1024)  # Memory in MB

        # Execute the function
        result = func(*args, **kwargs)

        # End time and memory tracking
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_memory = psutil.Process().memory_info().rss / (1024 * 1024)  # Memory in MB

        # Calculate metrics
        execution_time = end_time - start_time
        memory_used = end_memory - start_memory
        peak_memory = peak / (1024 * 1024)  # Convert to MB

        # Store metrics in the result if it's a tuple, otherwise create a new tuple
        performance_metrics = {
            'execution_time': execution_time,
            'memory_used': memory_used,
            'peak_memory': peak_memory
        }

        if isinstance(result, tuple):
            return result + (performance_metrics,)
        else:
            return (result, performance_metrics)

    return wrapper

def format_performance_metrics(metrics):
    return (
        f"Execution Time: {metrics['execution_time']:.4f} seconds\n"
        f"Memory Used: {metrics['memory_used']:.2f} MB\n"
        f"Peak Memory: {metrics['peak_memory']:.2f} MB"
    )

def get_metrics_explanation():
    return """
    Explanation of metrics:
    - Execution Time: The total time taken to complete the operation, measured in seconds.
    - Memory Used: The additional memory consumed during the operation, measured in megabytes (MB).
    - Peak Memory: The maximum amount of memory used at any point during the operation, measured in megabytes (MB).
    """