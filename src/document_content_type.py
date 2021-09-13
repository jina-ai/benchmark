import pytest
from jina import Document

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_get_content_type(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {"docs": [Document(text=f"d{i}") for i in range(num_docs)]},
        )

    def _doc_content_type(docs):
        for doc in docs:
            _ = doc.content_type

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_doc_content_type, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_content_type/test_document_get_content_type",
            iterations=num_docs,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )
