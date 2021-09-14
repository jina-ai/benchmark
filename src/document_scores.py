import pytest
from jina import Document

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_get_scores(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {
                "docs": [
                    Document(text=f"d{i}", scores={"euclidean": 5, "cosine": 0.5})
                    for i in range(num_docs)
                ]
            },
        )

    def _doc_get_scores(docs):
        for doc in docs:
            _ = doc._doc_scores["euclidean"]

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_doc_get_scores, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_scores/test_document_get_scores",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_set_scores(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {"docs": [Document(text=f"d{i}") for i in range(num_docs)]},
        )

    def _doc_set_scores(docs):
        for doc in docs:
            doc.scores["euclidean"] = 23

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_doc_set_scores, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_scores/test_document_set_scores",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )
