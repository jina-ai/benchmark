import pytest
from jina import Document

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_matches(num_docs, json_writer):
    def _input_docs():
        doc = Document(text="d1")
        doc.matches = [Document(text=f"d{i}") for i in range(num_docs)]
        return ((), {"doc": doc})

    def _get_matches(doc):
        return doc.matches

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_get_matches, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_matches/test_document_document_matches",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )
