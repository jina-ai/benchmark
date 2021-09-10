import numpy as np
import pytest
from jina import Document, DocumentArray
from jina.helper import random_identity

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


random_identity(use_uuid1=True)

@pytest.mark.parametrize('num_docs', [100, 1000, 10_000])
@pytest.mark.parametrize('use_uuid1', [True, False])
def test_document_document_generate_id(num_docs, use_uuid1, json_writer):

    def _generate_id():
        for _ in range(num_docs):
            random_identity(use_uuid1)

    mean_time, std_time = benchmark_time(func=_generate_id, n=NUM_REPETITIONS)

    json_writer.append(
        dict(
            name='document_embedding/test_document_document_generate_id',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs),
        )
    )

@pytest.mark.parametrize('num_docs', [100, 1000, 10_000])
def test_document_document_get_id(num_docs, json_writer):
    def _input_docs():
        return (), dict(
            docs=DocumentArray([Document(text='hey here') for _ in range(num_docs)])
        )

    def _get_id(docs):
        for d in docs:
            aux = d.id

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_get_id, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name='document_embedding/test_document_document_get_id',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs),
        )
    )

