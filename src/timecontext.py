import time


class TimeContext:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, typ, value, traceback):
        self.duration = time.perf_counter() - self.start
