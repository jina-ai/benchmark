from jina import Executor, requests

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 100


class DummyLoadExecutor(Executor):
    def __init__(self, a, b, c, d, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @requests
    def foo(self, **kwargs):
        pass


executor_yaml = '''
jtype: DummyLoadExecutor
with:
  a: 0
  b: 1
  c: 2
  d: 3
metas:
  name: dummy-executor
'''


def test_executor_load_config(json_writer):
    def _build():
        _ = Executor.load_config(executor_yaml)

    mean_time, std_time = benchmark_time(func=_build, n=NUM_REPETITIONS)

    json_writer.append(
        dict(
            name='executor/test_executor_load_config',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
        )
    )
