import time


class TimeContext:
    """Timing a code snippet with a context manager."""

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, typ, value, traceback):
        self.duration = time.perf_counter() - self.start
