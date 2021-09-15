import pytest
import numpy as np
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize('num_docs', [1, 100, 10_000])
def test_document_dict_with_text(num_docs, json_writer):
    def _input_docs():
        return (), dict(
            docs=[Document(text='doc' ) for _ in range(num_docs)]
        )

    def _dict(docs):
        for d in docs:
            aux = d.dict()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_dict, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name='document_dict/test_document_dict_with_text',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs),
        )
    )

@pytest.mark.parametrize('num_docs', [1, 100, 10_000])
def test_document_dict_with_array(num_docs, json_writer):
    def _input_docs():
        return (), dict(
            docs=[Document(blob=np.array([1,2])) for _ in range(num_docs)]
        )

    def _dict(docs):
        for d in docs:
            aux = d.dict()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_dict, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name='document_dict/test_document_dict_with_array',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs),
        )
    )
