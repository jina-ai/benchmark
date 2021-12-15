import pytest
from jina import Document, DocumentArray

from .pages import Pages
from .utils.benchmark import benchmark_time


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_tags_setter(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=DocumentArray(
                    [Document(tags={"tag1": "val1"}) for _ in range(num_docs)]
                )
            ),
        )

    def _tags_set(docs):
        for d in docs:
            d.tags["tag1"] = "newval1"

    result = benchmark_time(setup=_input_docs, func=_tags_set)

    json_writer.append(
        page=Pages.DOCUMENT_CONTENT,
        result=result,
        metadata=dict(num_docs=num_docs),
    )


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_tags_getter(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=DocumentArray(
                    [Document(tags={"tag1": "val1"}) for _ in range(num_docs)]
                )
            ),
        )

    def _get_tags_tag1(docs):
        for d in docs:
            tag = d.tags.get("tag1")

    result = benchmark_time(setup=_input_docs, func=_get_tags_tag1)

    json_writer.append(
        page=Pages.DOCUMENT_CONTENT,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
