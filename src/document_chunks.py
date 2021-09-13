import pytest
from jina import Document

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_chunks(num_docs, json_writer):
    def _input_docs():
        doc = Document()
        doc.chunks = [Document(text=f"d{i}") for i in range(num_docs)]
        return ((), {"doc": doc})

    def _get_chunks(doc):
        return doc.chunks

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_get_chunks, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_chunks/test_document_document_chunks",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )
