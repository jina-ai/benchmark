from typing import Dict, Generator, Union

import numpy as np
import pytest
from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap


def _generate_docs_with_embs(
    n_docs: int, emb_size: int
) -> Generator[Document, None, None]:
    embedings = np.random.random((n_docs, emb_size))
    for emb in embedings:
        yield Document(embedding=emb)


def _match_arrays(
    array1: Union[DocumentArray, DocumentArrayMemmap],
    array2: Union[DocumentArray, DocumentArrayMemmap],
    topk: int,
    metric: str,
    use_scipy: bool,
) -> float:

    for arr in (array1, array2):
        for doc in arr:
            doc.pop('matches')

    array1.match(array2, limit=topk, metric=metric, use_scipy=use_scipy)


def prepare_inputs_standard(
    size1: int = 10,
    size2: int = 10_000,
    emb_size: int = 128,
    topk: int = 10,
    metric: str = 'cosine',
    use_scipy: bool = False,
) -> Dict:

    return dict(
        array1=DocumentArray(_generate_docs_with_embs(size1, emb_size)),
        array2=DocumentArray(_generate_docs_with_embs(size2, emb_size)),
        topk=topk,
        metric=metric,
        use_scipy=use_scipy,
    )


def prepare_inputs_self(size: int = 10, emb_size: int = 128, topk: int = 10) -> float:

    docs = DocumentArray(_generate_docs_with_embs(size, emb_size))
    return dict(
        array1=docs,
        array2=docs,
        topk=topk,
        metric='cosine',
        use_scipy=False,
    )


@pytest.mark.parametrize('size1', [10, 100])
@pytest.mark.parametrize('size2', [1000, 10_00])
def test_array_sizes(size1: int, size2: int, benchmark):
    inputs = prepare_inputs_standard(size1=size1, size2=size2)
    benchmark(_match_arrays, **inputs)


@pytest.mark.parametrize('emb_size', [512, 1024])
def test_emb_sizes(emb_size: int, benchmark):
    inputs = prepare_inputs_standard(emb_size=emb_size)
    benchmark(_match_arrays, **inputs)


@pytest.mark.parametrize('use_scipy', [True, False])
@pytest.mark.parametrize('metric', ['cosine', 'euclidean', 'sqeuclidean'])
def test_metrics(use_scipy: bool, metric: str, benchmark):
    if not use_scipy and metric == 'cosine':
        pytest.skip('Skipping repeated default configuration')

    inputs = prepare_inputs_standard(metric=metric, use_scipy=use_scipy)
    benchmark(_match_arrays, **inputs)


@pytest.mark.parametrize('size', [100, 1000])
@pytest.mark.parametrize('topk', [10, 100])
def test_match_against_self(size: int, topk: int, benchmark):
    inputs = prepare_inputs_self(size=size, topk=topk)
    benchmark(_match_arrays, **inputs)
