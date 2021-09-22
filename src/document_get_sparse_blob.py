import pytest
import scipy.sparse as sp
from jina import Document

from .utils.benchmark import benchmark_time
from jina.types.ndarray.sparse.scipy import SparseNdArray as SparseScipy


@pytest.mark.parametrize("num_docs", [100, 1000, 10_000])
def test_document_document_get_sparse_blob_scipy(num_docs, json_writer):
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
            d.get_sparse_blob(SparseScipy)

    result = benchmark_time(setup=_input_docs, func=_get_sparse_blob)

    json_writer.append(
        name="document_get_sparse_blob/test_document_document_get_sparse_blob_scipy",
        result=result,
        metadata=dict(num_docs=num_docs),
    )
