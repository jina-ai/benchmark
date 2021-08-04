from .timecontext import TimeContext

_meth_profiler = {}

def benchmark(function):

    def wrapper(*args, **kwargs):
        with TimeContext() as timer:
            func = function(*args, **kwargs)

        if function.__name__ not in _meth_profiler.keys():
            _meth_profiler[function.__name__] = {'time': timer.duration, 'calls': 1}
        else:
            _meth_profiler[function.__name__]['time'] += timer.duration
            _meth_profiler[function.__name__]['calls'] += 1

        print(f' {function.__name__} duration {timer.duration}')
        return func

    return wrapper
