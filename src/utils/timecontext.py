import time


class TimeContext:
    """Timing a code snippet with a context manager."""

    def __enter__(self):
        self.start = time.time_ns()
        return self

    def __exit__(self, typ, value, traceback):
        self.duration = self.time_since_start()

    def time_since_start(self):
        return time.time_ns() - self.start
