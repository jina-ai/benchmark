import pytest
from jina import Document

from .utils.benchmark import benchmark_time
from .pages import Pages


@pytest.mark.parametrize('num_docs', [1, 100, 10_000])
def test_document_attributes(num_docs, json_writer):
    def _input_docs():
        return (), dict(docs=[Document(text='doc') for _ in range(num_docs)])

    def _attributes(docs):
        for d in docs:
            aux = d.attributes()

    result = benchmark_time(setup=_input_docs, func=_attributes)

    json_writer.append(
        page=Pages.DOCUMENT_ATTRIBUTES,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
