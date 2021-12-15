import pytest
from jina import Document

from .pages import Pages
from .utils.benchmark import benchmark_time


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_chunks(num_docs, json_writer):
    def _input_docs():
        doc = Document()
        doc.chunks = [Document(text=f"d{i}") for i in range(num_docs)]
        return ((), {"doc": doc})

    def _get_chunks(doc):
        return doc.chunks

    result = benchmark_time(setup=_input_docs, func=_get_chunks)

    json_writer.append(
        page=Pages.DOCUMENT_RECURSIVE,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
