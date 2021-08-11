import numpy as np

import pytest

from jina import Document, Executor, requests, DocumentArray

from .utils.benchmark import benchmark_time
from .utils.profiler import Profiler


class DummyEncoder(Executor):

    @requests
    def encode(self, docs, **kwargs):
        texts = docs.get_attributes('text')
        embeddings = [np.random.rand(1, 1024) for _ in texts]
        for doc, embedding in zip(docs, embeddings):
            doc.embedding = embedding


@pytest.fixture()
def input_docs():
    return DocumentArray([Document(text='hey here') for _ in range(100)])


@pytest.fixture()
def executor():
    return DummyEncoder()


@pytest.skip
def test_document_encoder_executor(executor, input_docs, json_writer):
    def _function(**kwargs):
        executor.encode(input_docs)

    with Profiler(Document) as document_profiler, Profiler(DocumentArray) as document_array_profiler:
        time, _ = benchmark_time(
            _function,
            1)

    json_writer.append(
        dict(
            name='document_embedding/test_document_encoder_executor',
            time=time,
            metadata=dict(Document=document_profiler.profile, DocumentArray=document_array_profiler.profile)
        )
    )
