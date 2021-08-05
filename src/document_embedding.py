import numpy as np
from benchmark import BenchmarkedDocument, BenchmarkedDocumentArray
from jina import Document, Executor, requests, DocumentArray


class DummyEncoder(Executor):

    @requests
    def encode(self, docs, **kwargs):
        texts = docs.get_attributes('text')
        embeddings = [np.random.rand(1, 1024) for text in texts]
        for doc, embedding in zip(docs, embeddings):
            doc.embedding = embedding


def benchmark():
    docs = BenchmarkedDocumentArray([BenchmarkedDocument(text='hey here') for _ in range(100)])
    executor = DummyEncoder()
    executor.encode(docs)
    print(f' Document profile {BenchmarkedDocument.profile}')
    print(f' DocumentArray profile {BenchmarkedDocumentArray.profile}')


if __name__ == '__main__':
    benchmark()
