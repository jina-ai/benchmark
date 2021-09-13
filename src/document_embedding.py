import numpy as np
import pytest
from jina import Document, DocumentArray, Executor, requests

from .utils.benchmark import benchmark_time
from .pages import Pages

NUM_REPETITIONS = 5
NUM_DOCS = 100


class DummyEncoder(Executor):
    @requests
    def encode(self, docs, **kwargs):
        texts = docs.get_attributes('text')
        embeddings = [np.random.rand(1, 1024) for _ in texts]
        for doc, embedding in zip(docs, embeddings):
            doc.embedding = embedding


@pytest.fixture()
def input_docs():
    return DocumentArray([Document(text='hey here') for _ in range(NUM_DOCS)])


@pytest.fixture()
def executor():
    return DummyEncoder()


@pytest.mark.skip()
def test_document_encoder_executor(name, executor, input_docs, json_writer):
    def _function(**kwargs):
        executor.encode(input_docs)

    mean_time, std_time, profiles = benchmark_time(
        profile_cls=[Document, DocumentArray], func=_function, n=NUM_REPETITIONS
    )

    document_profile = profiles[0]
    document_array_profile = profiles[1]

    json_writer.append(
        dict(
            name=name,
            page=Pages.DOCUMENT_EMBEDDING,
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(
                profiles=dict(
                    Document=document_profile, DocumentArray=document_array_profile
                ),
                num_docs=NUM_DOCS,
            ),
        )
    )
