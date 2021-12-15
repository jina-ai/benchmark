import numpy as np
import pytest
from jina import Document, DocumentArray, Executor, requests
from jina.clients.request import request_generator
from jina.parsers import set_pea_parser
from jina.peapods.runtimes.zmq.zed import ZEDRuntime
from jina.types.message import Message
from jina.types.request import Request

from .utils.benchmark import benchmark_time

NUM_DOCS = 100


class DummyEncoder(Executor):
    @requests
    def encode(self, docs, **kwargs):
        texts = docs.get_attributes('text')
        embeddings = [np.random.rand(1, 1024) for _ in texts]
        for doc, embedding in zip(docs, embeddings):
            doc.embedding = embedding


@pytest.fixture()
def process_message():
    req = list(
        request_generator(
            '/',
            DocumentArray([Document(text='input document') for _ in range(NUM_DOCS)]),
        )
    )[0]
    msg = Message(None, req, 'test', '123')
    return msg


@pytest.fixture()
def runtime():
    args = set_pea_parser().parse_args(['--uses', 'DummyEncoder'])
    return ZEDRuntime(args)


@pytest.mark.skip()
def test_zed_runtime_callback(runtime, process_message, json_writer):
    def _function(**kwargs):
        runtime._callback(process_message)

    result = benchmark_time(
        profile_cls=[Document, DocumentArray, Message, Request],
        func=_function,
    )
    profiles = result.profiles
    document_profile = profiles[0]
    document_array_profile = profiles[1]
    message_profile = profiles[2]
    request_profile = profiles[3]

    json_writer.append(
        name='zed_runtime_callback/test_zed_runtime_callback',
        result=result,
        metadata=dict(
            profiles=dict(
                Document=document_profile,
                DocumentArray=document_array_profile,
                Message=message_profile,
                Request=request_profile,
            ),
            num_docs=NUM_DOCS,
        ),
    )
