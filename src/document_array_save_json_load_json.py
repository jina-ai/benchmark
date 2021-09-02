import pytest
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 10


@pytest.mark.parametrize('num_docs', [100, 1000, 10_000])
def test_da_save_json(num_docs, json_writer, ephemeral_tmpdir):
    def _setup():
        docs = [Document(text=f"doc{i}") for i in range(num_docs)]
        da = DocumentArray(docs)
        return (), dict(da=da)

    def _da_save_json(da):
        da.save_json(f'{str(ephemeral_tmpdir)}/docarray.json')

    def _teardown():
        import os

        os.remove(f'{str(ephemeral_tmpdir)}/docarray.json')

    mean_time, std_time = benchmark_time(
        setup=_setup,
        func=_da_save_json,
        teardown=_teardown,
        n=NUM_REPETITIONS,
    )

    json_writer.append(
        dict(
            name='document_array_insert/test_da_save_json',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize('num_docs', [100, 1000, 10_000])
def test_da_load_json(num_docs, json_writer, ephemeral_tmpdir):
    def _setup():
        docs = [Document(text=f"doc{i}") for i in range(num_docs)]
        da = DocumentArray(docs)
        da.save_json(f'{str(ephemeral_tmpdir)}/docarray.json')
        return (), dict(da=da)

    def _da_load_json(da):
        da.load_json(f'{str(ephemeral_tmpdir)}/docarray.json')

    def _teardown():
        import os

        os.remove(f'{str(ephemeral_tmpdir)}/docarray.json')

    mean_time, std_time = benchmark_time(
        setup=_setup,
        func=_da_load_json,
        teardown=_teardown,
        n=NUM_REPETITIONS,
    )

    json_writer.append(
        dict(
            name='document_array_insert/test_da_load_json',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs),
        )
    )
