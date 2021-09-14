import random
import string

import numpy as np
import pytest
from jina import Document

from .utils.benchmark import benchmark_time
from .pages import Pages


def _generate_random_text(text_length):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(text_length)
    )


def _generate_random_buffer(buffer_length):
    return bytes(bytearray(random.getrandbits(8) for _ in range(buffer_length)))


def _generate_random_blob(num_dims):
    # 1 and 3 can cover from audio signals to images. 3 dimensions make the memory too high
    shape = [random.randint(100, 200)] * num_dims

    return np.random.rand(*shape)


NUM_DOCS = 10000


@pytest.mark.parametrize('text_length', [10, 100, 1000, 10000])
def test_set_attribute_text(name, text_length, json_writer):
    def _set_doc(doc):
        doc.set_attributes(text=_generate_random_text(text_length))

    mean_time, std_time = benchmark_time(
        _set_doc,
        NUM_DOCS,
        kwargs=dict(doc=Document()),
    )

    json_writer.append(
        dict(
            name=name,
            page=Pages.DOCUMENT_SET_ATTRIBUTES,
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(text_length=text_length),
        )
    )


@pytest.mark.parametrize('num_dims', [1, 2])
def test_set_attribute_blob(name, num_dims, json_writer):
    def _set_doc(doc):
        doc.set_attributes(blob=_generate_random_blob(num_dims))

    mean_time, std_time = benchmark_time(
        _set_doc,
        NUM_DOCS,
        kwargs=dict(doc=Document()),
    )

    json_writer.append(
        dict(
            name=name,
            page=Pages.DOCUMENT_SET_ATTRIBUTES,
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_dims=num_dims),
        )
    )


@pytest.mark.parametrize('buffer_length', [10, 1000, 100000])
def test_set_attribute_buffer(name, buffer_length, json_writer):
    def _set_doc(doc):
        doc.set_attributes(buffer=_generate_random_buffer(buffer_length))

    mean_time, std_time = benchmark_time(
        _set_doc,
        NUM_DOCS,
        kwargs=dict(doc=Document()),
    )

    json_writer.append(
        dict(
            name=name,
            page=Pages.DOCUMENT_SET_ATTRIBUTES,
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(buffer_length=buffer_length),
        )
    )
