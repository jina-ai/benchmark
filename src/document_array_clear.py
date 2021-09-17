import pytest
from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap

from .utils.benchmark import benchmark_time
from .pages import Pages


@pytest.mark.parametrize('num_docs', [100, 10_000])
def test_da_clear(num_docs, json_writer):
    def _setup():
        da = DocumentArray([Document(text=f'doc{i}') for i in range(num_docs)])
        return (), dict(da=da)

    def _da_clear(da):
        da.clear()

    result = benchmark_time(setup=_setup, func=_da_clear)

    json_writer.append(
        page=Pages.DA_CLEAR,
        result=result,
        metadata=dict(num_docs=num_docs),
    )


@pytest.mark.parametrize('num_docs', [100, 10_000])
def test_dam_clear(num_docs, json_writer, ephemeral_tmpdir):
    def _setup():
        dam = DocumentArrayMemmap((f'{str(ephemeral_tmpdir)}/memmap'))
        dam.extend([Document(text=f'doc{i}') for i in range(num_docs)])
        return (), dict(dam=dam)

    def _dam_clear(dam):
        dam.clear()

    def _teardown():
        import shutil

        shutil.rmtree(f'{str(ephemeral_tmpdir)}/memmap')

    result = benchmark_time(setup=_setup, func=_dam_clear, teardown=_teardown)

    json_writer.append(
        page=Pages.DA_CLEAR,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
