import pytest
from jina import Document

from .utils.benchmark import benchmark_time
from .pages import Pages


@pytest.mark.parametrize('num_docs', [1, 100, 10_000])
def test_document_non_empty_fields(num_docs, json_writer):
    def _input_docs():
        return (), dict(docs=[Document(text='doc') for _ in range(num_docs)])

    def _non_empty_fields(docs):
        for d in docs:
            aux = d.dict()

    result = benchmark_time(setup=_input_docs, func=_non_empty_fields)

    json_writer.append(
        page=Pages.DOCUMENT_HELPER,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
