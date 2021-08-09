from typing import Generator, Union

import numpy as np
import pytest
from jina import Document, DocumentArray, __version__
from jina.types.arrays.memmap import DocumentArrayMemmap

from utils.timecontext import TimeContext
from utils.benchmark import average_benchmark, get_output_file_name

NUM_REPETITIONS = 25


def _generate_docs_with_embs(
    n_docs: int, emb_size: int
) -> Generator[Document, None, None]:
    embedings = np.random.random((n_docs, emb_size))
    for emb in embedings:
        yield Document(embedding=emb)


def _match_arrays(
    array1: Union[DocumentArray, DocumentArrayMemmap],
    array2: Union[DocumentArray, DocumentArrayMemmap],
    top_k: int,
    metric: str,
    use_scipy: bool,
) -> float:

    for arr in (array1, array2):
        for doc in arr:
            doc.pop('matches')

    with TimeContext() as t:
        array1.match(array2, limit=top_k, metric=metric, use_scipy=use_scipy)

    return t.duration


def _standard_benchmark(
    size1: int = 10,
    size2: int = 10_000,
    emb_size: int = 128,
    topk: int = 10,
    metric: str = 'cosine',
    use_scipy: bool = False,
) -> str:

    result_template = (
        f"DocumentArray match of array of size {size1} with another of size {size2},"
        f" embedding size {emb_size} for top{topk} matches using {metric} metric"
        f"{' (scipy)' if use_scipy else ''} takes {{avg_time}} seconds\n"
    )

    result_str = average_benchmark(
        _match_arrays,
        result_template,
        NUM_REPETITIONS,
        DocumentArray(_generate_docs_with_embs(size1, emb_size)),
        DocumentArray(_generate_docs_with_embs(size2, emb_size)),
        topk,
        metric,
        use_scipy,
    )
    return result_str


def _match_against_self(size: int, topk: int, emb_size: int = 128) -> float:

    docs = DocumentArray(_generate_docs_with_embs(size, emb_size))
    result_template = (
        f"DocumentArray match of array of size {size} with against itself,"
        f" embedding size {emb_size} for top{topk} matches takes {{avg_time}} seconds\n"
    )

    result_str = average_benchmark(
        _match_arrays,
        result_template,
        NUM_REPETITIONS,
        docs,
        docs,
        topk,
        'cosine',
        False,
    )
    return result_str


@pytest.fixture(scope='module')
def results_file():
    with open(get_output_file_name(__file__), 'w+') as fp:
        yield fp


@pytest.mark.parametrize('size1', [10, 100])
@pytest.mark.parametrize('size2', [10_000, 100_000])
def test_array_sizes(size1: int, size2: int, results_file):
    results_str = _standard_benchmark(size1=size1, size2=size2)
    results_file.write(results_str)

@pytest.mark.parametrize('emb_size', [512, 1024])
def test_emb_sizes(emb_size: int):
    results_str = _standard_benchmark(emb_size=emb_size)
    results_file.write(results_str)


@pytest.mark.parametrize('use_scipy', [True, False])
@pytest.mark.parametrize('metric', ['cosine', 'euclidean', 'sqeuclidean'])
def test_metrics(use_scipy: bool, metric: str, results_file):
    if not use_scipy and metric == 'cosine':
        pytest.skip('Skipping repeated default configuration')
 
    results_str = _standard_benchmark(metric=metric, use_scipy=use_scipy)
    results_file.write(results_str)


@pytest.mark.parametrize('size', [100, 1000])
@pytest.mark.parametrize('topk', [10, 100])
def test_match_against_self(size: int, topk: int, results_file):
    results_str = _match_against_self(size=size, topk=topk)
    results_file.write(results_str)

