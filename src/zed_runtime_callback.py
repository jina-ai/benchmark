import numpy as np
import pytest


from jina import Executor, requests
from jina.parsers import set_pea_parser
from jina.types.document import Document
from jina.types.arrays.document import DocumentArray
from jina.types.message import Message
from jina.types.request import Request
from jina.clients.request import request_generator
from jina.peapods.runtimes.zmq.zed import ZEDRuntime

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
def process_message():
    req = list(
        request_generator(
            '/', DocumentArray([Document(text='input document') for _ in range(10)])
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

    with Profiler(Document) as document_profiler, Profiler(
        DocumentArray
    ) as document_array_profiler, Profiler(Message) as message_profiler, Profiler(
        Request
    ) as request_profiler:
        time, _ = benchmark_time(_function, 1)

    json_writer.append(
        dict(
            name='zed_runtime_callback/test_zed_runtime_callback',
            time=time,
            metadata=dict(
                Document=document_profiler.profile,
                DocumentArray=document_array_profiler.profile,
                Message=message_profiler.profile,
                Request=request_profiler.profile,
            ),
        )
    )
