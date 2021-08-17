from contextlib import ExitStack
from statistics import mean, stdev
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from .profiler import Profiler, merge_profiles
from .timecontext import TimeContext


def benchmark_time(
    func: Callable[[Any], Any],
    n: int,
    setup: Optional[Callable[[Any], Tuple[Iterable, Dict[str, Any]]]] = None,
    teardown: Optional[Callable[[None], None]] = None,
    profile_cls: Optional[List[type]] = [],
    args: Optional[Tuple] = None,
    kwargs: Optional[Dict] = None,
):
    """Get average time and std by benchmarking a function multiple times

    :param func: The function to benchmark
    :param setup: A setup function that can perform setup before running
        the ``func``. It should take as inputs the ``args`` and ``kwargs``
        that you provided, and return a tuple of an iterable, which will
        be used to provide ``args`` to ``func``, and a dictionary, which
        will be used to provide ``kwargs`` to ``func``.
    :param teardown: A teardown function that can perform teardown/cleanup after running
        the ``func``.
    :param profile_cls: A list of the classes that want to be profiled
    :param n: Number of repetitions
    :param args: Positional arguments to pass to ``func`` (or ``setup``)
    :param kwargs: Keyword arguments to pass to ``func`` (or ``setup``)
    """

    results = []
    args = args if args is not None else ()
    kwargs = kwargs if kwargs is not None else {}

    profiles_by_cls = {_cls: [] for _cls in profile_cls}

    for i in range(n):
        if setup is not None:
            new_args, new_kwargs = setup(*args, **kwargs)

        ctx_manager = ExitStack()

        profiles = [ctx_manager.enter_context(Profiler(cls)) for cls in profile_cls]
        with ctx_manager:
            with TimeContext() as t:
                func(*new_args, **new_kwargs)

        for p in profiles:
            profiles_by_cls[p._cls].append(p.profile)

        if teardown is not None:
            teardown()

        results.append(t.duration)

    mean_profiles = []
    for profile_cls, profile_list in profiles_by_cls.items():
        mean_profiles.append(merge_profiles(profile_list))

    m = mean(results)
    s = stdev(results) if len(results) > 1 else None

    if len(mean_profiles) > 0:
        return m, s, mean_profiles
    else:
        return m, s
