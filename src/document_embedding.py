import numpy as np

from profiler import Profiler
from jina import Document, Executor, requests, DocumentArray


class DummyEncoder(Executor):

    @requests
    def encode(self, docs, **kwargs):
        texts = docs.get_attributes('text')
        embeddings = [np.random.rand(1, 1024) for _ in texts]
        for doc, embedding in zip(docs, embeddings):
            doc.embedding = embedding


def benchmark():
    with Profiler(Document) as document_profiler, Profiler(DocumentArray) as document_array_profiler:
        docs = DocumentArray([Document(text='hey here') for _ in range(100)])
        executor = DummyEncoder()
        executor.encode(docs)

    print(f' Document profile {document_profiler.profile} \n')
    print(f' DocumentArray profile {document_array_profiler.profile} \n')


if __name__ == '__main__':
    benchmark()
