import string
import pytest
import random

from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 25
NUM_DOCS = 1000
CHARS = tuple(string.ascii_uppercase + string.digits)


def _get_docs(num_docs):
    return [Document(scores={'cosine': random.random()}) for _ in range(num_docs)]


@pytest.mark.parametrize('num_docs', [100, 1000, 10000, 100000])
def test_da_sort(num_docs, json_writer):
    def _sort(da):
        da.sort(key=lambda x: x.scores['cosine'].value)

    def _build_da(**kwargs):
        docs = kwargs.get('docs')
        da = DocumentArray(docs)
        return (), dict(da=da)

    mean_time, std_time = benchmark_time(
        setup=_build_da,
        func=_sort,
        n=NUM_REPETITIONS,
        kwargs=dict(docs=_get_docs(num_docs)),
    )

    json_writer.append(
        dict(
            name='document_array_sort/test_da_sort',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )
