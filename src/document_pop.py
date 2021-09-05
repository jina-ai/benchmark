import pytest
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


@pytest.mark.parametrize('num_docs', [100, 1000, 10_000])
def test_document_document_pop(num_docs, json_writer):
    def _input_docs():
        return (), dict(
            docs=DocumentArray([Document(text='hey here') for _ in range(num_docs)])
        )

    def _pop_text(docs):
        for d in docs:
            d.pop('text')

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_pop_text, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name='document_embedding/test_document_document_pop',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs),
        )
    )
