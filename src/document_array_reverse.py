import pytest
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time
from .pages import Pages

NUM_REPETITIONS = 10


@pytest.mark.parametrize('num_docs', [100, 10_000])
def test_da_reverse(name, num_docs, json_writer):
    def _setup():
        docs = [Document(text=f"doc{i}") for i in range(num_docs)]
        da = DocumentArray(docs)
        return (), dict(da=da)

    def _da_reverse(da):
        da.reverse()

    mean_time, std_time = benchmark_time(
        setup=_setup,
        func=_da_reverse,
        n=NUM_REPETITIONS,
    )

    json_writer.append(
        dict(
            name=name,
            page=Pages.DA_INSERT,
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs),
        )
    )
