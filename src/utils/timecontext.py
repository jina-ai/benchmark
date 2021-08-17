import time


def now_ms():
    return time.time_ns() // 1_000_000


class TimeContext:
    """Timing a code snippet with a context manager."""

    def __enter__(self):
        self.start = now_ms()
        return self

    def __exit__(self, typ, value, traceback):
        self.duration = now_ms() - self.start
