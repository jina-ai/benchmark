import pytest
import scipy.sparse as sp
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time
from jina.types.ndarray.sparse.scipy import SparseNdArray as SparseScipy

NUM_REPETITIONS = 5


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_get_sparse_embedding_scipy(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            {
                "docs": [
                    Document(blob=sp.csr_matrix([0, 0, 4, 0, 1]))
                    for i in range(num_docs)
                ]
            },
        )

    def _get_sparse_blob(docs):
        for d in docs:
            d.get_sparse_embedding(SparseScipy)

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_get_sparse_blob, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_get_sparse_embedding/test_document_document_get_sparse_embedding_scipy",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )
