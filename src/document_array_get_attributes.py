import os
import string

import numpy as np
import pytest
from faker import Faker
from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap

from .utils.benchmark import benchmark_time
from .pages import Pages

fake = Faker()
Faker.seed(42)
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
    [100, 10000],
)
def test_da_get_attributes(
    name, field, docs_get_fn, memmap, num_docs, json_writer, ephemeral_tmpdir
):
    def _get_attributes(da):
        da.get_attributes(*[field])

    def _build_da(**kwargs):
        memmap = kwargs.get('memmap', False)
        docs = kwargs.get('docs', False)
        da = (
            DocumentArray()
            if not memmap
            else DocumentArrayMemmap(f'{str(ephemeral_tmpdir)}/memmap')
        )
        da.extend(docs)
        return (), dict(da=da)

    def _teardown():
        import os
        import shutil

        if os.path.exists(f'{str(ephemeral_tmpdir)}/memmap'):
            shutil.rmtree(f'{str(ephemeral_tmpdir)}/memmap')

    mean_time, std_time = benchmark_time(
        setup=_build_da,
        func=_get_attributes,
        teardown=_teardown,
        n=NUM_REPETITIONS,
        kwargs=dict(memmap=memmap, docs=docs_get_fn(num_docs)),
    )
    if memmap:
        name = name.replace('_da_', '_dam_')
    json_writer.append(
        dict(
            name=name,
            page=Pages.DA_GET_ATTRIBUTE,
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs, field=field, memmap=memmap),
        )
    )


@pytest.mark.parametrize('memmap', [False, True])
@pytest.mark.parametrize(
    'num_docs',
    [100, 10000],
)
def test_da_embeddings_property(name, memmap, num_docs, json_writer, ephemeral_tmpdir):
    def _get_embeddings(da):
        da.embeddings

    def _build_da(**kwargs):
        memmap = kwargs.get('memmap', False)
        docs = embedding_docs(num_docs)
        da = (
            DocumentArray()
            if not memmap
            else DocumentArrayMemmap(f'{str(ephemeral_tmpdir)}/memmap')
        )
        da.extend(docs)
        return (), dict(da=da)

    def _teardown():
        import os
        import shutil

        if os.path.exists(f'{str(ephemeral_tmpdir)}/memmap'):
            shutil.rmtree(f'{str(ephemeral_tmpdir)}/memmap')

    mean_time, std_time = benchmark_time(
        setup=_build_da,
        func=_get_embeddings,
        teardown=_teardown,
        n=NUM_REPETITIONS,
        kwargs=dict(memmap=memmap),
    )
    if memmap:
        name = name.replace('_da_', '_dam_')
    json_writer.append(
        dict(
            name=name,
            page=Pages.DA_GET_ATTRIBUTE,
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs, memmap=memmap),
        )
    )
