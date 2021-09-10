import numpy as np
import pytest
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


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

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_tags_set, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_embedding/test_document_document_tags_setter",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
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

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_get_tags_tag1, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_embedding/test_document_document_tags_getter",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )
