import os
import string
import pytest

from faker import Faker
import numpy as np


from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap
from .utils.benchmark import benchmark_time

fake = Faker()
NUM_REPETITIONS = 5
NUM_DOCS = 1000
CHARS = tuple(string.ascii_uppercase + string.digits)


def _generate_random_text():
    return ''.join(np.random.choice(CHARS, 256))


def _generate_random_blob():
    return np.random.random(512)


def _generate_random_buffer():
    return bytes(bytearray(os.urandom(512 * 4)))


def empty_docs():
    return [Document() for _ in range(NUM_DOCS)]


def text_docs(num_docs):
    return [Document(text=_generate_random_text()) for _ in range(num_docs)]


def blob_docs(num_docs):
    return [Document(blob=_generate_random_blob()) for _ in range(num_docs)]


def buffer_docs(num_docs):
    return [Document(buffer=_generate_random_buffer()) for _ in range(num_docs)]


def embedding_docs(num_docs):
    return [Document(embedding=_generate_random_blob()) for _ in range(num_docs)]


@pytest.mark.parametrize('memmap', [False, True])
@pytest.mark.parametrize(
    'field, docs_get_fn',
    [
        ('blob', blob_docs),
        ('text', text_docs),
        ('buffer', buffer_docs),
        ('embedding', embedding_docs),
    ],
)
@pytest.mark.parametrize(
    'num_docs',
    [10, 100, 1000],
)
def test_da_get_attributes(field, docs_get_fn, memmap, num_docs, json_writer, tmpdir):
    def _get_attributes(da):
        da.get_attributes(*[field])

    def _build_da(**kwargs):
        memmap = kwargs.get('memmap', False)
        docs = kwargs.get('docs', False)
        da = (
            DocumentArray()
            if not memmap
            else DocumentArrayMemmap(f'{str(tmpdir)}/memmap')
        )
        da.extend(docs)
        return (), dict(da=da)

    def _teardown():
        import shutil
        import os

        if os.path.exists(f'{str(tmpdir)}/memmap'):
            shutil.rmtree(f'{str(tmpdir)}/memmap')

    mean_time, std_time = benchmark_time(
        setup=_build_da,
        func=_get_attributes,
        teardown=_teardown,
        n=NUM_REPETITIONS,
        kwargs=dict(memmap=memmap, docs=docs_get_fn(num_docs)),
    )

    json_writer.append(
        dict(
            name='document_array_get_attributes/test_da_get_attributes',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs, field=field, memmap=memmap),
        )
    )


@pytest.mark.parametrize('memmap', [False, True])
@pytest.mark.parametrize(
    'num_docs',
    [10, 100, 1000],
)
def test_embeddings_property(memmap, num_docs, json_writer, tmpdir):
    def _get_embeddings(da):
        da.embeddings

    def _build_da(**kwargs):
        memmap = kwargs.get('memmap', False)
        docs = embedding_docs(num_docs)
        da = (
            DocumentArray()
            if not memmap
            else DocumentArrayMemmap(f'{str(tmpdir)}/memmap')
        )
        da.extend(docs)
        return (), dict(da=da)

    def _teardown():
        import shutil
        import os

        if os.path.exists(f'{str(tmpdir)}/memmap'):
            shutil.rmtree(f'{str(tmpdir)}/memmap')

    mean_time, std_time = benchmark_time(
        setup=_build_da,
        func=_get_embeddings,
        teardown=_teardown,
        n=NUM_REPETITIONS,
        kwargs=dict(memmap=memmap),
    )

    json_writer.append(
        dict(
            name='document_array_get_attributes/test_embeddings_property',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs, memmap=memmap),
        )
    )
