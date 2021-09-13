import pytest
from jina import Document

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_uri(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {"docs": [Document(text=f"d{i}") for i in range(num_docs)]},
        )

    def _doc_uri(docs):
        for doc in docs:
            _ = doc.uri

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_doc_uri, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_uri/test_document_uri",
            iterations=num_docs,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )
