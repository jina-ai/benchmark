import pytest
from jina import Document

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_get_mime_type(num_docs, json_writer):
    def _input_docs():
        docs = []
        for i in range(num_docs):
            d = Document(text=f"d{i}")
            d.mime_type = "text"
            docs.append(d)

        return (
            (),
            {"docs": docs},
        )

    def _get_mime_type(docs):
        for doc in docs:
            _ = doc.mime_type

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_get_mime_type, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_mime_type/test_document_get_mime_type",
            iterations=num_docs,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_set_mime_type(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {"docs": [Document(text=f"d{i}") for i in range(num_docs)]},
        )

    def _set_mime_type(docs):
        for doc in docs:
            doc.mime_type = "text"

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_set_mime_type, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_mime_type/test_document_set_mime_type",
            iterations=num_docs,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )
