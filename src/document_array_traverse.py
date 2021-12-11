import pytest
import shutil

from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap

from .utils.benchmark import benchmark_time
from .pages import Pages


def _get_docs(num_docs):
    return [Document(text=f'This is the document number: {i}') for i in range(num_docs)]


def _build_da(num_docs, num_matches, num_chunks):
    da = DocumentArray(_get_docs(num_docs))
    for doc in da:
        if num_matches > 0:
            doc.matches.extend(_get_docs(num_matches))
        if num_chunks > 0:
            doc.chunks.extend(_get_docs(num_chunks))

    return da


@pytest.mark.parametrize(
    'num_docs,num_matches,num_chunks,traversal_paths',
    [
        (10, 10, 10, 'r, c, m'),
        (100, 100, 100, 'r, c, m'),
        (1000, 100, 100, 'r, c, m'),
        (1000, 10, 10, 'r'),
        (1000, 10, 100, 'c'),
        (1000, 100, 10, 'm'),
    ],
)
@pytest.mark.parametrize('memmap', [False, True])
def test_da_traverse_flat(
    name,
    num_docs,
    num_matches,
    num_chunks,
    traversal_paths,
    memmap,
    json_writer,
    ephemeral_tmpdir,
):
    if num_docs == 1000 and num_chunks == 1000 and num_matches == 1000:
        pytest.skip('problems with memory')

    def _traverse_flat(da):
        for d in da.traverse_flat(traversal_paths):
            pass

    def _build_da():
        docs = _get_docs(num_docs)
        for doc in docs:
            if num_matches > 0:
                doc.matches.extend(_get_docs(num_matches))
            if num_chunks > 0:
                doc.chunks.extend(_get_docs(num_chunks))

        da = (
            DocumentArray()
            if not memmap
            else DocumentArrayMemmap(f'{str(ephemeral_tmpdir)}/memmap')
        )
        da.extend(docs)

        return (), dict(da=da)

    def _teardown():
        try:
            shutil.rmtree(f'{str(ephemeral_tmpdir)}/memmap')
        except FileNotFoundError:
            pass

    result = benchmark_time(setup=_build_da, func=_traverse_flat, teardown=_teardown)
    if memmap:
        name = name.replace('_da_', '_dam_')
    json_writer.append(
        name=name,
        page=Pages.DA_TRAVERSE,
        result=result,
        metadata=dict(
            num_docs=num_docs,
            num_matches=num_matches,
            num_chunks=num_chunks,
            traversal_paths=traversal_paths,
            memmap=memmap,
        ),
    )
