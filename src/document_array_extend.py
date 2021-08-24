import os
import string

import numpy as np
import pytest
from jina import Document, DocumentArray, __version__
from jina.types.arrays.memmap import DocumentArrayMemmap

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 25
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


def text_docs():
    return [Document(text=_generate_random_text()) for _ in range(NUM_DOCS)]


def blob_docs():
    return [Document(blob=_generate_random_blob()) for _ in range(NUM_DOCS)]


def buffer_docs():
    return [Document(buffer=_generate_random_buffer()) for _ in range(NUM_DOCS)]


@pytest.mark.parametrize('memmap', [False, True])
@pytest.mark.parametrize(
    'docs, label',
    [
        (empty_docs(), 'empty'),
        (blob_docs(), 'blob'),
        (text_docs(), 'text'),
        (buffer_docs(), 'buffer'),
    ],
)
def test_da_extend(docs, label, memmap, json_writer, ephemeral_tmpdir):
    def _extend(da):
        da.extend(docs)

    def _build_da(**kwargs):
        memmap = kwargs.get('memmap', False)
        da = (
            DocumentArray()
            if not memmap
            else DocumentArrayMemmap(f'{str(ephemeral_tmpdir)}/memmap')
        )
        return (), dict(da=da)

    def _teardown():
        import os
        import shutil

        if os.path.exists(f'{str(ephemeral_tmpdir)}/memmap'):
            shutil.rmtree(f'{str(ephemeral_tmpdir)}/memmap')

    mean_time, std_time = benchmark_time(
        setup=_build_da,
        func=_extend,
        teardown=_teardown,
        n=NUM_REPETITIONS,
        kwargs=dict(memmap=memmap),
    )

    json_writer.append(
        dict(
            name='document_array_extend/test_da_extend',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=len(docs), label=label, memmap=memmap),
        )
    )
