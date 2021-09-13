import pytest
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_parent_id(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {
                "chunks": [
                    Document(
                        chunks=[Document(text="d1 original text", id=str(i))], id="123"
                    ).chunks[0]
                    for i in range(num_docs)
                ]
            },
        )

    def _content_hash(chunks):
        for c in chunks:
            c.parent_id

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_content_hash, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_parent_id/test_document_document_parent_id",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )
