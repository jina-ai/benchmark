import pytest
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


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

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_merge_from, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_mergefrom/test_document_merge_from",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )
