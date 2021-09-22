import pytest
from jina import Document

from .utils.benchmark import benchmark_time
from .pages import Pages


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_parent_id(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {
                "chunks": [
                    Document(
                        chunks=[Document(text="d1 original text", id=str(i))], id="123"
                    ).chunks[0]
                    for i in range(num_docs)
                ]
            },
        )

    def _parent_id(chunks):
        for c in chunks:
            c.parent_id

    result = benchmark_time(setup=_input_docs, func=_parent_id)

    json_writer.append(
        page=Pages.DOCUMENT_META,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
