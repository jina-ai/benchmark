import inspect
from statistics import mean, stdev
from typing import Dict, List

from .timecontext import TimeContext


def profile(profile, function, *args, **kwargs):
    def wrapper(*args, **kwargs):
        with TimeContext() as timer:
            func = function(*args, **kwargs)

        if function.__name__ in profile.keys():
            profile[function.__name__]['time'] += timer.duration
            profile[function.__name__]['calls'] += 1
        else:
            profile[function.__name__] = {}
            profile[function.__name__]['time'] = timer.duration
            profile[function.__name__]['calls'] = 1
        return func

    return wrapper


def merge_profiles(profiles: List[Dict]) -> Dict:
    avg_profile = {}
    for profile in profiles:
        for function in profile.keys():
            if function in avg_profile:
                avg_profile[function]['time'].append(profile[function]['time'])
                avg_profile[function]['calls'].append(profile[function]['calls'])
            else:
                avg_profile[function] = {}
                avg_profile[function]['time'] = []
                avg_profile[function]['calls'] = []
                avg_profile[function]['time'].append(profile[function]['time'])
                avg_profile[function]['calls'].append(profile[function]['calls'])

    for function in avg_profile.keys():
        avg_time = mean(avg_profile[function]['time'])
        stdev_time = (
            stdev(avg_profile[function]['time'])
            if len(avg_profile[function]['time']) > 0
            else None
        )
        avg_calls = mean(avg_profile[function]['calls'])
        stdev_calls = (
            stdev(avg_profile[function]['calls'])
            if len(avg_profile[function]['calls']) > 0
            else None
        )
        del avg_profile[function]['time']
        del avg_profile[function]['calls']
        avg_profile[function]['mean_time'] = avg_time
        avg_profile[function]['std_time'] = stdev_time
        avg_profile[function]['mean_calls'] = avg_calls
        avg_profile[function]['std_calls'] = stdev_calls

    return avg_profile


class Profiler:
    def __init__(self, cls):
        self._cls = cls
        self.profile = {}
        self._old_funcs = {}

    def __enter__(self):
        for _, f in inspect.getmembers(self._cls, predicate=inspect.isfunction):
            self._old_funcs[f.__name__] = f
            setattr(self._cls, f.__name__, profile(self.profile, f))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for func_name, func_val in self._old_funcs.items():
            setattr(self._cls, func_name, func_val)
