import pytest
from jina import Document

from .utils.benchmark import benchmark_time


@pytest.mark.parametrize("num_docs", [100, 10_000])
def test_document_uri(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {"docs": [Document(text=f"d{i}") for i in range(num_docs)]},
        )

    def _doc_uri(docs):
        for doc in docs:
            _ = doc.uri

    result = benchmark_time(setup=_input_docs, func=_doc_uri)

    json_writer.append(
        name="document_uri/test_document_uri",
        result=result,
        metadata=dict(num_docs=num_docs),
    )
