import pytest
from faker import Faker
from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap

from .utils.benchmark import benchmark_time
from .pages import Pages

fake = Faker()
Faker.seed(42)
NUM_DOCS = 10000


@pytest.fixture
def docs():
    return [Document(text=fake.text()) for _ in range(NUM_DOCS)]


def test_da_append(docs, json_writer):
    def _append(da):
        for doc in docs:
            da.append(doc)

    def _setup(**kwargs):
        return (), dict(da=DocumentArray())

    result = benchmark_time(setup=_setup, func=_append)

    json_writer.append(
        page=Pages.DA_APPEND,
        result=result,
        metadata=dict(num_docs_append=NUM_DOCS),
    )


@pytest.mark.parametrize('flush', [True, False])
def test_dam_append(docs, flush, json_writer, ephemeral_tmpdir):
    def _append(da):
        for doc in docs:
            da.append(doc, flush=flush)

    def _setup(**kwargs):
        return (), dict(da=DocumentArrayMemmap(f'{str(ephemeral_tmpdir)}/memmap'))

    def _teardown():
        import shutil

        shutil.rmtree(f'{str(ephemeral_tmpdir)}/memmap')

    result = benchmark_time(setup=_setup, func=_append, teardown=_teardown)

    json_writer.append(
        page=Pages.DA_APPEND,
        result=result,
        metadata=dict(num_docs_append=NUM_DOCS, flush=flush),
    )
