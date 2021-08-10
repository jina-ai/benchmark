from typing import Dict, Generator, Tuple, Union

import numpy as np
import pytest
from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap

from utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


def _generate_docs_with_embs(
    n_docs: int, emb_size: int
) -> Generator[Document, None, None]:
    embedings = np.random.random((n_docs, emb_size))
    for emb in embedings:
        yield Document(embedding=emb)


def match_arrays(
    array1: Union[DocumentArray, DocumentArrayMemmap],
    array2: Union[DocumentArray, DocumentArrayMemmap],
    topk: int,
    metric: str,
    use_scipy: bool,
):
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


def prepare_inputs_self(size: int = 10, emb_size: int = 128, topk: int = 10) -> Dict:
    docs = DocumentArray(_generate_docs_with_embs(size, emb_size))
    return dict(
        array1=docs,
        array2=docs,
        topk=topk,
        metric='cosine',
        use_scipy=False,
    )


def setup_match(**kwargs) -> Tuple[Tuple, Dict]:
    array1 = kwargs["array1"]
    array2 = kwargs["array2"]

    for arr in (array1, array2):
        for doc in arr:
            doc.pop('matches')

    return (), kwargs


@pytest.mark.parametrize('size1', [10, 100])
@pytest.mark.parametrize('size2', [10_000, 100_000])
def test_array_sizes(size1: int, size2: int, json_metadata):

    mean_time, std_time = benchmark_time(
        match_arrays,
        NUM_REPETITIONS,
        setup=setup_match,
        kwargs=prepare_inputs_standard(size1=size1, size2=size2),
    )

    json_metadata["mean_time"] = mean_time
    json_metadata["std_time"] = std_time


@pytest.mark.parametrize('emb_size', [512, 1024])
def test_emb_sizes(emb_size: int, json_metadata):

    mean_time, std_time = benchmark_time(
        match_arrays,
        NUM_REPETITIONS,
        setup=setup_match,
        kwargs=prepare_inputs_standard(emb_size=emb_size),
    )

    json_metadata["mean_time"] = mean_time
    json_metadata["std_time"] = std_time


@pytest.mark.parametrize('use_scipy', [True, False])
@pytest.mark.parametrize('metric', ['cosine', 'euclidean', 'sqeuclidean'])
def test_metrics(use_scipy: bool, metric: str, json_metadata):
    if not use_scipy and metric == 'cosine':
        pytest.skip('Skipping repeated default configuration')

    mean_time, std_time = benchmark_time(
        match_arrays,
        NUM_REPETITIONS,
        setup=setup_match,
        kwargs=prepare_inputs_standard(metric=metric, use_scipy=use_scipy),
    )

    json_metadata["mean_time"] = mean_time
    json_metadata["std_time"] = std_time


@pytest.mark.parametrize('size', [100, 1000])
@pytest.mark.parametrize('topk', [10, 100])
def test_match_against_self(size: int, topk: int, json_metadata):

    mean_time, std_time = benchmark_time(
        match_arrays,
        NUM_REPETITIONS,
        setup=setup_match,
        kwargs=prepare_inputs_self(size=size, topk=topk),
    )

    json_metadata["mean_time"] = mean_time
    json_metadata["std_time"] = std_time
