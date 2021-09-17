import pytest
from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap

from .utils.benchmark import benchmark_time
from .pages import Pages


@pytest.mark.parametrize('memmap', [False, True])
@pytest.mark.parametrize('n_docs', [1000, 10_000])
def test_da_shuffle(name, memmap, n_docs, ephemeral_tmpdir, json_writer):
    def _setup(memmap, n_docs):
        docs = [Document(text=f'Document{i}') for i in range(n_docs)]
        da = (
            DocumentArrayMemmap(f'{str(ephemeral_tmpdir)}/memmap')
            if memmap
            else DocumentArray()
        )
        da.extend(docs)
        return (), dict(da=da)

    def _shuffle_da(da):
        da.shuffle()

    def _teardown():
        import os
        import shutil

        if os.path.exists(f'{str(ephemeral_tmpdir)}/memmap'):
            shutil.rmtree(f'{str(ephemeral_tmpdir)}/memmap')

    result = benchmark_time(
        setup=_setup,
        func=_shuffle_da,
        teardown=_teardown,
        kwargs=dict(memmap=memmap, n_docs=n_docs),
    )
    if memmap:
        name = name.replace('_da_', '_dam_')
    json_writer.append(
        name=name,
        page=Pages.DA_SHUFFLE,
        result=result,
        metadata=dict(n_nodes=memmap, n_docs=n_docs),
    )
