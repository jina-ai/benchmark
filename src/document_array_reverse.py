import pytest
from jina import Document, DocumentArray

from .pages import Pages
from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 10


@pytest.mark.parametrize('num_docs', [100, 10_000])
def test_da_reverse(num_docs, json_writer):
    def _setup():
        docs = [Document(text=f'doc{i}') for i in range(num_docs)]
        da = DocumentArray(docs)
        return (), dict(da=da)

    def _da_reverse(da):
        da.reverse()

    result = benchmark_time(
        setup=_setup,
        func=_da_reverse,
        n=NUM_REPETITIONS,
    )

    json_writer.append(
        page=Pages.DA_INSERT,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
