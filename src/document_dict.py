import pytest
import numpy as np
from jina import Document

from .utils.benchmark import benchmark_time


@pytest.mark.parametrize('num_docs', [1, 100, 10_000])
def test_document_dict_with_text(num_docs, json_writer):
    def _input_docs():
        return (), dict(docs=[Document(text='doc') for _ in range(num_docs)])

    def _dict(docs):
        for d in docs:
            aux = d.dict()

    result = benchmark_time(setup=_input_docs, func=_dict)

    json_writer.append(
        name='document_dict/test_document_dict_with_text',
        result=result,
        metadata=dict(num_docs=num_docs),
    )


@pytest.mark.parametrize('num_docs', [1, 100, 10_000])
def test_document_dict_with_array(num_docs, json_writer):
    def _input_docs():
        return (), dict(docs=[Document(blob=np.array([1, 2])) for _ in range(num_docs)])

    def _dict(docs):
        for d in docs:
            aux = d.dict()

    result = benchmark_time(setup=_input_docs, func=_dict)

    json_writer.append(
        name='document_dict/test_document_dict_with_array',
        result=result,
        metadata=dict(num_docs=num_docs),
    )
