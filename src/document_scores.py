import pytest
from jina import Document

from .pages import Pages
from .utils.benchmark import benchmark_time


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_get_scores(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {
                "docs": [
                    Document(text=f"d{i}", scores={"euclidean": 5, "cosine": 0.5})
                    for i in range(num_docs)
                ]
            },
        )

    def _doc_get_scores(docs):
        for doc in docs:
            _ = doc.scores["euclidean"]

    result = benchmark_time(setup=_input_docs, func=_doc_get_scores)

    json_writer.append(
        page=Pages.DOCUMENT_RELEVANCE,
        result=result,
        metadata=dict(num_docs=num_docs),
    )


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_set_scores(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {"docs": [Document(text=f"d{i}") for i in range(num_docs)]},
        )

    def _doc_set_scores(docs):
        for doc in docs:
            doc.scores["euclidean"] = 23

    result = benchmark_time(setup=_input_docs, func=_doc_set_scores)

    json_writer.append(
        page=Pages.DOCUMENT_RELEVANCE,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
