import pytest
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time
from .pages import Pages

NUM_REPETITIONS = 10


@pytest.mark.parametrize('num_docs', [100, 10_000])
def test_da_save_binary(name, num_docs, json_writer, ephemeral_tmpdir):
    def _setup():
        docs = [Document(text=f"doc{i}") for i in range(num_docs)]
        da = DocumentArray(docs)
        return (), dict(da=da)

    def _da_save_binary(da):
        da.save_binary(f'{str(ephemeral_tmpdir)}/docarray.bin')

    def _teardown():
        import os

        os.remove(f'{str(ephemeral_tmpdir)}/docarray.bin')

    mean_time, std_time = benchmark_time(
        setup=_setup,
        func=_da_save_binary,
        teardown=_teardown,
        n=NUM_REPETITIONS,
    )

    json_writer.append(
        dict(
            name=name,
            page=Pages.DA_INSERT,
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize('num_docs', [100, 10_000])
def test_da_load_binary(name, num_docs, json_writer, ephemeral_tmpdir):
    def _setup():
        docs = [Document(text=f"doc{i}") for i in range(num_docs)]
        da = DocumentArray(docs)
        da.save_binary(f'{str(ephemeral_tmpdir)}/docarray.bin')
        return (), dict(da=da)

    def _da_load_binary(da):
        da.load_binary(f'{str(ephemeral_tmpdir)}/docarray.bin')

    def _teardown():
        import os

        os.remove(f'{str(ephemeral_tmpdir)}/docarray.bin')

    mean_time, std_time = benchmark_time(
        setup=_setup,
        func=_da_load_binary,
        teardown=_teardown,
        n=NUM_REPETITIONS,
    )

    json_writer.append(
        dict(
            name=name,
            page=Pages.DA_INSERT,
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs),
        )
    )
