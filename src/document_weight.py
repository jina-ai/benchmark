import pytest
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_set_weight(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=DocumentArray([Document(text="hey here") for _ in range(num_docs)])
            ),
        )

    def _set_weight(docs):
        for d in docs:
            d.weight = 2.3

    result = benchmark_time(setup=_input_docs, func=_set_weight)

    json_writer.append(
        name="document_embedding/test_document_document_set_weight",
        result=result,
        metadata=dict(num_docs=num_docs),
    )


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_get_weight(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=DocumentArray([Document(text="hey here") for _ in range(num_docs)])
            ),
        )

    def _get_weight(docs):
        for d in docs:
            aux = d.weight

    result = benchmark_time(setup=_input_docs, func=_get_weight)

    json_writer.append(
        name="document_embedding/test_document_document_get_weight",
        result=result,
        metadata=dict(num_docs=num_docs),
    )
