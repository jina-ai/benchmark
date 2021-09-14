import pytest
from jina import Document

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_get_granularity(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {"docs": [Document(text=f"d{i}", granularity=2) for i in range(num_docs)]},
        )

    def _doc_get_granularity(docs):
        for doc in docs:
            _ = doc.granularity

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_doc_get_granularity, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_granularity/test_document_get_granularity",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_set_granularity(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {"docs": [Document(text=f"d{i}", granularity=2) for i in range(num_docs)]},
        )

    def _doc_set_granularity(docs):
        x = np.array([2, 3, 4])
        for doc in docs:
            doc.granularity = 3

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_doc_set_granularity, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_granularity/test_document_set_granularity",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )
