import inspect
from utils.timecontext import TimeContext


def profile(profile, function, *args, **kwargs):
    def wrapper(*args, **kwargs):
        with TimeContext() as timer:
            func = function(*args, **kwargs)

        profile[function.__name__]['time'] += timer.duration
        profile[function.__name__]['calls'] += 1
        return func

    return wrapper


class Profiler:

    def __init__(self, cls):
        self._cls = cls
        self.profile = {}
        self._old_funcs = {}

    def __enter__(self):
        for _, f in inspect.getmembers(self._cls, predicate=inspect.isfunction):
            self.profile[f.__name__] = {'time': 0.0, 'calls': 0}
            self._old_funcs[f.__name__] = f
            setattr(self._cls, f.__name__, profile(self.profile, f))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for func_name, func_val in self._old_funcs.items():
            setattr(self._cls, func_name, func_val)
