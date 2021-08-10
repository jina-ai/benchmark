from statistics import mean, stdev
from typing import Any, Callable, Dict, Iterable, Optional, Tuple

from .timecontext import TimeContext


def benchmark_time(
    func: Callable[[Any], Any],
    n: int,
    setup: Optional[Callable[[Any], Tuple[Iterable, Dict[str, Any]]]] = None,
    args: Optional[Tuple] = None,
    kwargs: Optional[Dict] = None,
) -> str:
    """Get average time and std by benchmarking a function multiple times

    :param func: The function to benchmark
    :param setup: A setup function that can perform setup before running
        the ``func``. It should take as inputs the ``args`` and ``kwargs``
        that you provided, and return a tuple of an iterable, which will
        be used to provide ``args`` to ``func``, and a dictionary, which
        will be used to provide ``kwargs`` to ``func``.
    :param n: Number of repetitions
    :param args: Positional arguments to pass to ``func`` (or ``setup``)
    :param kwargs: Keyword arguments to pass to ``func`` (or ``setup``)
    """

    results = []
    args = args if args is not None else ()
    kwargs = kwargs if kwargs is not None else {}

    for i in range(n):
        if setup is not None:
            args, kwargs = setup(*args, **kwargs)

        with TimeContext() as t:
            func(*args, **kwargs)

        results.append(t.duration)

    return mean(results), stdev(results)
