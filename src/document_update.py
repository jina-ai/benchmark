import numpy as np
import pytest
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5



@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_update_embedding(num_docs,  json_writer):
    def _input_docs():
        return ( (), {'docs': [Document( embedding=np.array([1,2,3])) for _ in range(num_docs)],
                      'new_doc': Document(embedding=np.array([4,5,6]))})

    def _update_embedding(docs, new_doc):
        for d in docs:
            d.update(new_doc)

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_update_embedding, n=NUM_REPETITIONS
    )
    json_writer.append(
        dict(
            name="document_update/test_document_document_update_embedding",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )



@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_update_text(num_docs,  json_writer):
    def _input_docs():
        return ( (), {'docs': [Document( text='original text') for _ in range(num_docs)],
                      'new_doc': Document(text='new text')})


    def _update_text(docs, new_doc):
        for d in docs:
            d.update(new_doc)

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_update_text, n=NUM_REPETITIONS
    )
    json_writer.append(
        dict(
            name="document_update/test_document_document_update_text",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )

