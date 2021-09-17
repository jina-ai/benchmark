import pytest
from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap

from .utils.benchmark import benchmark_time
from .pages import Pages

NUM_REPETITIONS = 10

# IMPORTANT: This benchmark currently is covered by
# - document_array_save_binary_load_binary.py
# - document_array_save_json_load_json.py
# Only relevant if for future releases `.save` expands to other methods


@pytest.mark.parametrize('num_docs', [100, 10_000])
def test_da_save(num_docs, json_writer, ephemeral_tmpdir):
    def _setup():
        da = DocumentArray([Document(text=f'doc{i}') for i in range(num_docs)])
        return (), dict(da=da)

    def _da_save(da):
        da.save(f'{str(ephemeral_tmpdir)}/docarray')

    def _teardown():
        import os

        os.remove(f'{str(ephemeral_tmpdir)}/docarray')

    result = benchmark_time(
        setup=_setup, func=_da_save, teardown=_teardown, n=NUM_REPETITIONS
    )

    def _teardown():
        import shutil

        shutil.rmtree(f'{str(ephemeral_tmpdir)}/save')

    json_writer.append(
        page=Pages.DA_CLEAR,
        result=result,
        metadata=dict(num_docs=num_docs),
    )


@pytest.mark.parametrize('num_docs', [100, 10_000])
def test_dam_save(num_docs, json_writer, ephemeral_tmpdir):
    def _setup():
        dam = DocumentArrayMemmap((f'{str(ephemeral_tmpdir)}/memmap'))
        dam.extend([Document(text=f'doc{i}') for i in range(num_docs)])
        return (), dict(dam=dam)

    def _dam_clear(dam):
        dam.clear()

    def _teardown():
        import shutil

        shutil.rmtree(f'{str(ephemeral_tmpdir)}/memmap')

    result = benchmark_time(
        setup=_setup, func=_dam_clear, teardown=_teardown, n=NUM_REPETITIONS
    )

    json_writer.append(
        page=Pages.DA_CLEAR,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
