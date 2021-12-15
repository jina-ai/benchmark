from typing import Dict, Generator, Union

import numpy as np
import pytest
from jina import Document, DocumentArray, DocumentArrayMemmap

from .pages import Pages
from .utils.benchmark import benchmark_time


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


def _prepare_inputs_standard(
    size1: int = 10,
    size2: int = 10_000,
    emb_size: int = 128,
    topk: int = 10,
    metric: str = 'cosine',
    use_scipy: bool = False,
    dam_x: bool = False,
    dam_y: bool = False,
    dam_path: str = './',
) -> Dict:
    if not dam_x:
        x = DocumentArray(_generate_docs_with_embs(size1, emb_size))
    else:
        x = DocumentArrayMemmap(f'{dam_path}/x')
        x.extend(_generate_docs_with_embs(size1, emb_size))
    if not dam_y:
        y = DocumentArray(_generate_docs_with_embs(size2, emb_size))
    else:
        y = DocumentArrayMemmap(f'{dam_path}/y')
        y.extend(_generate_docs_with_embs(size2, emb_size))
    return dict(
        array1=x,
        array2=y,
        topk=topk,
        metric=metric,
        use_scipy=use_scipy,
    )


@pytest.mark.parametrize('size_X', [10])
@pytest.mark.parametrize('size_Y', [100000])
@pytest.mark.parametrize('dam_x', [False])
@pytest.mark.parametrize('dam_y', [False])
@pytest.mark.parametrize('emb_size', [256])
@pytest.mark.parametrize('use_scipy', [False])
@pytest.mark.parametrize('metric', ['euclidean'])
@pytest.mark.parametrize('top_k', [3])
def test_match(
    size_X: int,
    size_Y: int,
    dam_x: bool,
    dam_y: bool,
    emb_size: int,
    use_scipy: bool,
    metric: str,
    top_k: int,
    ephemeral_tmpdir,
    json_writer,
):
    result = benchmark_time(
        match_arrays,
        kwargs=_prepare_inputs_standard(
            size1=size_X,
            size2=size_Y,
            dam_x=dam_x,
            dam_y=dam_y,
            emb_size=emb_size,
            use_scipy=use_scipy,
            metric=metric,
            dam_path=str(ephemeral_tmpdir),
            topk=top_k,
        ),
    )

    json_writer.append(
        page=Pages.DA_MATCH,
        result=result,
        metadata=dict(
            size_X=size_X,
            size_Y=size_Y,
            dam_x=dam_x,
            dam_y=dam_y,
            emb_size=emb_size,
            use_scipy=use_scipy,
            metric=metric,
            top_k=top_k,
        ),
    )
