import pytest
from jina import Document

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_get_content(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {"docs": [Document(text=f"d{i}") for i in range(num_docs)]},
        )

    def _doc_get_content(docs):
        for doc in docs:
            _ = doc.content

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_doc_get_content, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_content/test_document_get_content",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_set_content(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {"docs": [Document(blob=np.array([1, 2])) for i in range(num_docs)]},
        )

    def _doc_get_content(docs):
        x = np.array([2, 3, 4])
        for doc in docs:
            doc.content = x

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_doc_get_content, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_content/test_document_get_content",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )
