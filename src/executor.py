from jina import Executor, requests

from .pages import Pages
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

    result = benchmark_time(func=_build)

    json_writer.append(
        page=Pages.EXECUTOR,
        result=result,
        metadata={},
    )
