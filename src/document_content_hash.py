import pytest
from jina import Document

from .utils.benchmark import benchmark_time


@pytest.mark.parametrize('num_docs', [100, 1000, 10_000])
def test_document_document_content_hash(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {'docs': [Document(text=f'text doc {i}') for i in range(num_docs)]},
        )

    def _content_hash(docs):
        for d in docs:
            d.content_hash

    result = benchmark_time(setup=_input_docs, func=_content_hash)
    json_writer.append(
        name='document_content_hash/test_document_document_content_hash',
        result=result,
        metadata=dict(num_docs=num_docs),
    )
