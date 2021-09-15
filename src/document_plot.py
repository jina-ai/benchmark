import os
import pytest
from jina import Document, DocumentArray
from jina.helper import random_identity

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


random_identity(use_uuid1=True)


@pytest.mark.parametrize("num_docs", [1, 5])
def test_document_plot(num_docs, json_writer, ephemeral_tmpdir):
    def _input_docs():
        return (
            (),
            dict(docs=[Document(text="doc") for _ in range(num_docs)]),
        )

    def _plot(docs):
        for d in docs:
            d.plot(output=os.path.join(ephemeral_tmpdir, "doc.svg"))

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_plot, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_plot/test_document_plot",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )
