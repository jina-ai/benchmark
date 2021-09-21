import pytest
from jina import Document

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_get_evaluations(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {
                "docs": [
                    Document(evaluations={'precision': 0.9}) for i in range(num_docs)
                ]
            },
        )

    def _doc_get_evaluations(docs):
        for doc in docs:
            _ = doc.evaluations['precision'].value

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_doc_get_evaluations, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_scores/test_document_get_evaluations",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_set_evaluations(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {
                "docs": [
                    Document(evaluations={'precision': 0.9}) for i in range(num_docs)
                ]
            },
        )

    def _doc_set_evaluations(docs):
        for doc in docs:
            doc.evaluations['precision'] = 0.99

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_doc_set_evaluations, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_scores/test_document_set_evaluations",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )
