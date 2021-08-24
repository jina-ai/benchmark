import pytest
from faker import Faker
from jina import Document, DocumentArray, __version__
from jina.types.arrays.memmap import DocumentArrayMemmap

from .utils.benchmark import benchmark_time

fake = Faker()
NUM_DOCS = 10000
NUM_REPETITIONS = 5


@pytest.fixture
def docs():
    return [Document(text=fake.text()) for _ in range(NUM_DOCS)]


def test_docarray_append(docs, json_writer):
    def _append(da):
        for doc in docs:
            da.append(doc)

    def _setup(**kwargs):
        return (), dict(da=DocumentArray())

    mean_time, std_time = benchmark_time(setup=_setup, func=_append, n=NUM_REPETITIONS)

    json_writer.append(
        dict(
            name='document_array_append/test_docarray_append',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs_append=NUM_DOCS),
        )
    )


@pytest.mark.parametrize('flush', [True, False])
def test_document_array_memmap_append(docs, flush, json_writer, ephemeral_tmpdir):
    def _append(da):
        for doc in docs:
            da.append(doc, flush=flush)

    def _setup(**kwargs):
        return (), dict(da=DocumentArrayMemmap(f'{str(ephemeral_tmpdir)}/memmap'))

    def _teardown():
        import shutil

        shutil.rmtree(f'{str(ephemeral_tmpdir)}/memmap')

    mean_time, std_time = benchmark_time(
        setup=_setup, func=_append, teardown=_teardown, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name='document_array_append/test_document_array_memmap_append',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs_append=NUM_DOCS, flush=flush),
        )
    )
