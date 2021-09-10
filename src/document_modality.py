import numpy as np
import pytest
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_modality_setter(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=DocumentArray([Document(text="hey here") for _ in range(num_docs)])
            ),
        )

    def _set_modality(docs):
        for d in docs:
            d.modality = "modality"

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_set_modality, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_embedding/test_document_document_modality_setter",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_modality_getter(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=DocumentArray(
                    [
                        Document(text="hey here", embedding=np.array([1, 2, 3]))
                        for _ in range(num_docs)
                    ]
                )
            ),
        )

    def _get_modality(docs):
        for d in docs:
            aux = d.modality

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_get_modality, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_embedding/test_document_document_modality_getter",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )
