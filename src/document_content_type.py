import pytest
from jina import Document

from .utils.benchmark import benchmark_time
from .pages import Pages


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_get_content_type(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {"docs": [Document(text=f"d{i}") for i in range(num_docs)]},
        )

    def _doc_content_type(docs):
        for doc in docs:
            _ = doc.content_type

    result = benchmark_time(setup=_input_docs, func=_doc_content_type)

    json_writer.append(
        page=Pages.DOCUMENT_META,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
