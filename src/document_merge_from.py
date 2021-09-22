import pytest
from jina import Document

from .utils.benchmark import benchmark_time


@pytest.mark.parametrize("num_docs", [1, 100, 10_000])
def test_document_merge_from(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {
                "docs": [Document(text=f"{i}") for i in range(num_docs)],
                "doc": Document(text="newdoc"),
            },
        )

    def _merge_from(docs, doc):
        for d in docs:
            d.MergeFrom(doc)

    result = benchmark_time(setup=_input_docs, func=_merge_from)

    json_writer.append(
        name="document_mergefrom/test_document_merge_from",
        result=result,
        metadata=dict(num_docs=num_docs),
    )
