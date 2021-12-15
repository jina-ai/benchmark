import pytest
from jina import Document, DocumentArray

from .pages import Pages
from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 10


@pytest.mark.parametrize('num_docs', [100, 10_000])
def test_da_insert(num_docs, json_writer):
    def _setup():
        docs = [Document(text=f'doc{i}') for i in range(num_docs)]
        da = DocumentArray()
        return (), dict(da=da, docs=docs)

    def _insert_in_da(da, docs):
        for doc in docs:
            da.insert(index=0, doc=doc)

    result = benchmark_time(
        setup=_setup,
        func=_insert_in_da,
        n=NUM_REPETITIONS,
    )

    json_writer.append(
        page=Pages.DA_INSERT,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
