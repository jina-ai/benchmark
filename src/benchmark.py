from jina import Document
from functools import partialmethod
from timecontext import TimeContext

_meth_profiler = {}


def benchmark(function, *args, **kwargs):
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


class BenchmarkMixin:
    def func(self, func_name, *args, **kwargs):
        """convert async method `func_name` to a normal method
        :param func_name: name of method in super
        :param args: positional args
        :param kwargs: keyword args
        :return: run func_name from super
        """
        f = getattr(super(), func_name, None)
        if f:
            return benchmark(f)(*args, **kwargs)

    __init__ = partialmethod(func, '__init__')
    embedding = partialmethod(func, 'embedding')
    set_attributes = partialmethod(func, 'set_attributes')


class BenchmarkedDocument(BenchmarkMixin, Document):
    pass
