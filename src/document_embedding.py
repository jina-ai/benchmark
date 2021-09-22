import numpy as np
import pytest
from jina import Document, DocumentArray, Executor, requests

from .utils.benchmark import benchmark_time
from .pages import Pages

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
def test_document_encoder_executor(executor, input_docs, json_writer):
    def _function(**kwargs):
        executor.encode(input_docs)

    result = benchmark_time(profile_cls=[Document, DocumentArray], func=_function)
    profiles = result.profiles
    document_profile = profiles[0]
    document_array_profile = profiles[1]

    json_writer.append(
        page=Pages.DOCUMENT_CONTENT,
        result=result,
        metadata=dict(
            profiles=dict(
                Document=document_profile, DocumentArray=document_array_profile
            ),
            num_docs=NUM_DOCS,
        ),
    )
