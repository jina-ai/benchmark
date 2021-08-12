from typing import Union


def get_readable_size(num_bytes: Union[int, float]) -> str:
    """
    Transform the bytes into readable value with different units (e.g. 1 KB, 20 MB, 30.1 GB).

    :param num_bytes: Number of bytes.
    :return: Human readable string representation.
    """
    num_bytes = int(num_bytes)
    if num_bytes < 1024:
        return f'{num_bytes} Bytes'
    elif num_bytes < 1024 ** 2:
        return f'{num_bytes / 1024:.1f} KB'
    elif num_bytes < 1024 ** 3:
        return f'{num_bytes / (1024 ** 2):.1f} MB'
    else:
        return f'{num_bytes / (1024 ** 3):.1f} GB'


def used_memory(unit: int = 1024 * 1024 * 1024) -> float:
    """
    Get the memory usage of the current process.

    :param unit: Unit of the memory, default in Gigabytes.
    :return: Memory usage of the current process.
    """
    import resource

    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / unit


class MemoryContext:
    """Profiling memory consumption of a code snippet"""

    def __enter__(self):
        self.start_mem = used_memory(unit=1)
        return self

    def __exit__(self, typ, value, traceback):
        self.used_memory = used_memory(1) - self.start_mem
