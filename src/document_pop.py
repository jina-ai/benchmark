import pytest
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time
from .pages import Pages


@pytest.mark.parametrize('num_docs', [100, 1000, 10_000])
def test_document_document_pop(num_docs, json_writer):
    def _input_docs():
        return (), dict(
            docs=DocumentArray([Document(text='hey here') for _ in range(num_docs)])
        )

    def _pop_text(docs):
        for d in docs:
            d.pop('text')

    result = benchmark_time(setup=_input_docs, func=_pop_text)

    json_writer.append(
        page=Pages.DOCUMENT_HELPER,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
