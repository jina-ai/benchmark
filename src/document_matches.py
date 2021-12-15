import pytest
from jina import Document

from .pages import Pages
from .utils.benchmark import benchmark_time


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_matches(num_docs, json_writer):
    def _input_docs():
        doc = Document(text="d1")
        doc.matches = [Document(text=f"d{i}") for i in range(num_docs)]
        return ((), {"doc": doc})

    def _get_matches(doc):
        return doc.matches

    result = benchmark_time(setup=_input_docs, func=_get_matches)

    json_writer.append(
        page=Pages.DOCUMENT_RECURSIVE,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
