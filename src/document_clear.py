import numpy as np
import pytest
from jina import Document, DocumentArray

from .pages import Pages
from .utils.benchmark import benchmark_time


@pytest.mark.parametrize('num_docs', [100, 1000, 10_000])
def test_document_document_clear_doc_with_1_field(num_docs, json_writer):
    def _input_docs():
        return (), dict(
            docs=DocumentArray([Document(text='hey here') for _ in range(num_docs)])
        )

    def _pop_text(docs):
        for d in docs:
            d.clear()

    result = benchmark_time(setup=_input_docs, func=_pop_text)

    json_writer.append(
        page=Pages.DOCUMENT_HELPER,
        result=result,
        metadata=dict(num_docs=num_docs),
    )


@pytest.mark.parametrize('num_docs', [100, 1000, 10_000])
def test_document_document_clear_doc_with_2_fields(num_docs, json_writer):
    def _input_docs():
        return (), dict(
            docs=DocumentArray(
                [
                    Document(text='hey here', embedding=np.array([1, 2, 3]))
                    for _ in range(num_docs)
                ]
            )
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
