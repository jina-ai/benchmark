import pytest
import numpy as np
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize('num_docs', [1, 100, 10_000])
def test_document_attributes(num_docs, json_writer):
    def _input_docs():
        return (), dict(docs=[Document(text='doc') for _ in range(num_docs)])

    def _attributes(docs):
        for d in docs:
            aux = d.attributes()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_attributes, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name='document_attributes/test_document_attributes',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs),
        )
    )
