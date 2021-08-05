import numpy as np

from profiler import Profiler

from jina import Executor, requests
from jina.parsers import set_pea_parser
from jina.types.document import Document
from jina.types.arrays.document import DocumentArray
from jina.types.message import Message
from jina.types.request import Request
from jina.clients.request import request_generator
from jina.peapods.runtimes.zmq.zed import ZEDRuntime


class DummyEncoder(Executor):

    @requests
    def encode(self, docs, **kwargs):
        texts = docs.get_attributes('text')
        embeddings = [np.random.rand(1, 1024) for _ in texts]
        for doc, embedding in zip(docs, embeddings):
            doc.embedding = embedding


def benchmark():
    req = list(
        request_generator(
            '/', DocumentArray([Document(text='input document') for _ in range(10)])
        )
    )[0]
    msg = Message(None, req, 'test', '123')
    args = set_pea_parser().parse_args(['--uses', 'DummyEncoder'])
    runtime = ZEDRuntime(args)
    with Profiler(Document) as document_profiler, \
            Profiler(DocumentArray) as document_array_profiler, \
            Profiler(Message) as message_profiler, \
            Profiler(Request) as request_profiler:
        runtime._callback(msg)

    print(f' Document profile {document_profiler.profile} \n')
    print(f' DocumentArray profile {document_array_profiler.profile} \n')
    print(f' Message profile {message_profiler.profile} \n')
    print(f' Request profile {request_profiler.profile} \n')


if __name__ == '__main__':
    benchmark()
