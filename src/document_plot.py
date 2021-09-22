import os
import pytest
from jina import Document
from jina.helper import random_identity

from .utils.benchmark import benchmark_time
from .pages import Pages


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

    result = benchmark_time(setup=_input_docs, func=_plot)

    json_writer.append(
        page=Pages.DOCUMENT_HELPER,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
