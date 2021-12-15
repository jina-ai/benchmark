import pytest
from jina import Flow

from .pages import Pages
from .utils.benchmark import benchmark_time

NUM_PODS = 10


def _long_flow():
    f = Flow()
    for _ in range(NUM_PODS):
        f = f.add()

    return f


def _wide_flow():
    f = Flow().add(name='pod0')
    for i in range(NUM_PODS):
        f = f.add(needs=['pod0'], name=f'wide_{i}')
    f = f.add(name='join', needs=[f'wide_{i}' for i in range(NUM_PODS)])
    return f


@pytest.mark.parametrize(
    'flow, ftype', [(_long_flow(), 'long'), (_wide_flow(), 'wide')]
)
def test_local_flow_start(flow, ftype, json_writer):
    def _start():
        flow.start()

    def _close():
        flow.close()

    result = benchmark_time(func=_start, teardown=_close)

    json_writer.append(
        page=Pages.FLOW,
        result=result,
        metadata=dict(flow=ftype, num_pods=NUM_PODS),
    )


@pytest.mark.parametrize(
    'flow, ftype', [(_long_flow(), 'long'), (_wide_flow(), 'wide')]
)
def test_local_flow_close(flow, ftype, json_writer):
    def _start():
        flow.start()
        return (), {}

    def _close():
        flow.close()

    result = benchmark_time(setup=_start, func=_close)

    json_writer.append(
        page=Pages.FLOW,
        result=result,
        metadata=dict(flow=ftype, num_pods=NUM_PODS),
    )


yaml_long = '''jtype: Flow
version: '1'
pods:
  - uses:
    name: pod1
  - uses:
    name: pod2
  - uses:
    name: pod3
  - uses:
    name: pod4
  - uses:
    name: pod5
  - uses:
    name: pod6
  - uses:
    name: pod7
  - uses:
    name: pod8
  - uses:
    name: pod9
  - uses:
    name: pod10
    '''

yaml_wide = '''jtype: Flow
version: '1'
pods:
  - uses:
    name: pod0
  - uses:
    name: wide_0
    needs: [pod0]
  - uses:
    name: wide_1
    needs: [pod0]
  - uses:
    name: wide_2
    needs: [pod0]
  - uses:
    name: wide_3
    needs: [pod0]
  - uses:
    name: wide_4
    needs: [pod0]
  - uses:
    name: wide_5
    needs: [pod0]
  - uses:
    name: wide_6
    needs: [pod0]
  - uses:
    name: wide_7
    needs: [pod0]
  - uses:
    name: wide_8
    needs: [pod0]
  - uses:
    name: wide_9
    needs: [pod0]
  - uses:
    name: join
    needs: [wide_0, wide_1, wide_2, wide_3, wide_4, wide_5, wide_6, wide_7, wide_8, wide_9]
    '''


@pytest.mark.parametrize('config, ftype', [(yaml_long, 'long'), (yaml_wide, 'wide')])
def test_flow_load_config(config, ftype, json_writer):
    def _build():
        Flow.load_config(config)

    result = benchmark_time(func=_build)

    json_writer.append(
        page=Pages.FLOW,
        result=result,
        metadata=dict(flow=ftype, num_pods=NUM_PODS),
    )
