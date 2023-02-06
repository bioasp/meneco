import os

PARALLEL_NTHREADS: int = os.cpu_count() # Number of threads to use in search
PARALLEL_MODE: str = 'compete' # Run competition or splitting based search

def get_config_options() -> str:
    """Get command line options from configuration
    Note: this function is designed to be enhanced with future options

    Returns:
        str: Options string to pass to clyngor
    """
    return ' '.join([
        f'--parallel-mode {PARALLEL_NTHREADS},{PARALLEL_MODE}',
    ])

__all__ = [
    PARALLEL_NTHREADS,
    PARALLEL_MODE,
    get_config_options
]
