import pytest

from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap


from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


def _get_docs(num_docs):
    return [Document(text=f'This is the document number: {i}') for i in range(num_docs)]


def _build_da(num_docs, num_matches, num_chunks):
    da = DocumentArray(_get_docs(num_docs))
    for doc in da:
        if num_matches > 0:
            doc.matches.extend(_get_docs(num_matches))
        if num_chunks > 0:
            doc.chunks.extend(_get_docs(num_matches))

    return da


@pytest.mark.parametrize('num_docs', [10, 100, 1000])
@pytest.mark.parametrize('num_matches', [10, 100, 1000])
@pytest.mark.parametrize('num_chunks', [10, 100, 1000])
@pytest.mark.parametrize('traversal_paths', [['r', ], ['c', ], ['m', ]])
@pytest.mark.parametrize('memmap', [False, True])
def test_document_array_traverse_flat(num_docs, num_matches, num_chunks, traversal_paths, memmap, json_writer, tmpdir):
    def _traverse_flat(da):
        da.traverse_flat(traversal_paths)

    def _build_da(num_docs, num_matches, num_chunks):
        da = DocumentArray() if not memmap else DocumentArrayMemmap(f'{str(tmpdir)}/memmap')
        da.extend(_get_docs(num_docs))
        for doc in da:
            if num_matches > 0:
                doc.matches.extend(_get_docs(num_matches))
            if num_chunks > 0:
                doc.chunks.extend(_get_docs(num_matches))

        return da

    mean_time, std_time = benchmark_time(
        setup=_build_da,
        func=_traverse_flat,
        n=NUM_REPETITIONS,
        kwargs=dict(num_docs=num_docs, num_matches=num_matches, num_chunks=num_chunks, traversal_paths=traversal_paths),
    )

    json_writer.append(
        dict(
            name='document_array_traverse/test_document_array_traverse_flat',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs, num_matches=num_matches, num_chunks=num_chunks, traversal_paths=traversal_paths, memmap=memmap),
        )
    )
