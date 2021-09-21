import pytest
import numpy as np
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize('num_docs', [1, 100, 10_000])
def test_document_non_empty_fields(num_docs, json_writer):
    def _input_docs():
        return (), dict(docs=[Document(text='doc') for _ in range(num_docs)])

    def _non_empty_fields(docs):
        for d in docs:
            aux = d.dict()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_non_empty_fields, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name='document_dict/test_document_non_empty_fields',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs),
        )
    )
