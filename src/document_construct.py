import random
import string
import numpy as np
import pytest

from jina import Document, __version__
from .utils.benchmark import benchmark_time


def _generate_random_text(text_length):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(text_length)
    )


def _generate_random_buffer(buffer_length):
    return bytes(bytearray(random.getrandbits(8) for _ in range(buffer_length)))


def _generate_random_blob(num_dims):
    # 1 and 3 can cover from audio signals to images. 3 dimensions make the memory too high
    shape_length = random.randint(1, 2)
    shape = [random.randint(100, 200)] * num_dims

    return np.random.rand(*shape)


def _generate_random_document(
    origin, text_length=None, buffer_length=None, num_dims=None
):
    tags = {'tag1': [0, 2, 3], 'tag2': 'value of tag2'}
    if origin == 'text':
        return Document(text=_generate_random_text(text_length), tags=tags)
    if origin == 'blob':
        return Document(blob=_generate_random_blob(num_dims), tags=tags)
    if origin == 'buffer':
        return Document(buffer=_generate_random_buffer(buffer_length), tags=tags)


def _generate_random_document_with_chunks_and_matches(
    origin, text_length=None, buffer_length=None, num_dims=None
):
    root = _generate_random_document(origin, text_length, buffer_length, num_dims)

    num_chunks = random.randint(1, 20)
    num_matches = random.randint(1, 20)
    for _ in range(num_chunks):
        root.chunks.append(
            _generate_random_document(origin, text_length, buffer_length, num_dims)
        )
    for _ in range(num_matches):
        root.matches.append(
            _generate_random_document(origin, text_length, buffer_length, num_dims)
        )
    return root


NUM_DOCS = 1000


@pytest.mark.parametrize('text_length', [10, 100, 1000, 10000])
def test_construct_text(text_length, json_writer):
    def _doc_build(text):
        Document(text=text)

    mean_time, std_time = benchmark_time(
        _doc_build, NUM_DOCS, kwargs=dict(text=_generate_random_text(text_length))
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_text',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(text_length=text_length),
        )
    )


@pytest.mark.parametrize('num_dims', [1, 2])
def test_construct_blob(num_dims, json_writer):
    def _doc_build(blob):
        Document(blob=blob)

    mean_time, std_time = benchmark_time(
        _doc_build, NUM_DOCS, kwargs=dict(blob=_generate_random_blob(num_dims))
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_blob',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_dims=num_dims),
        )
    )


@pytest.mark.parametrize('buffer_length', [10, 100, 1000, 10000])
def test_construct_buffer(buffer_length, json_writer):
    def _doc_build(buffer):
        Document(buffer=buffer)

    mean_time, std_time = benchmark_time(
        _doc_build, NUM_DOCS, kwargs=dict(buffer=_generate_random_buffer(buffer_length))
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_buffer',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(buffer_length=buffer_length),
        )
    )


@pytest.mark.parametrize('text_length', [10, 100, 1000, 10000])
def test_construct_btyes_origin_text(text_length, json_writer):
    def _doc_build(b):
        Document(document=b)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(
            b=_generate_random_document(
                'text', text_length=text_length
            ).proto.SerializeToString()
        ),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_bytes_origin_text',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(text_length=text_length),
        )
    )


@pytest.mark.parametrize('num_dims', [1, 2])
def test_construct_btyes_origin_blob(num_dims, json_writer):
    def _doc_build(b):
        Document(document=b)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(
            b=_generate_random_document(
                'blob', num_dims=num_dims
            ).proto.SerializeToString()
        ),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_bytes_origin_blob',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_dims=num_dims),
        )
    )


@pytest.mark.parametrize('buffer_length', [10, 100, 1000, 10000])
def test_construct_btyes_origin_buffer(buffer_length, json_writer):
    def _doc_build(b):
        Document(document=b)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(
            b=_generate_random_document(
                'buffer', buffer_length=buffer_length
            ).proto.SerializeToString()
        ),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_bytes_origin_buffer',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(buffer_length=buffer_length),
        )
    )


@pytest.mark.parametrize('text_length', [10, 100, 1000, 10000])
def test_construct_str_json_origin_text(text_length, json_writer):
    def _doc_build(b):
        Document(document=b)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(
            b=_generate_random_document('text', text_length=text_length).json()
        ),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_str_json_origin_text',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(text_length=text_length),
        )
    )


@pytest.mark.parametrize('num_dims', [1, 2])
def test_construct_str_json_origin_blob(num_dims, json_writer):
    def _doc_build(b):
        Document(document=b)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(b=_generate_random_document('blob', num_dims=num_dims).json()),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_str_json_origin_blob',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_dims=num_dims),
        )
    )


@pytest.mark.parametrize('buffer_length', [10, 100, 1000, 10000])
def test_construct_str_json_origin_buffer(buffer_length, json_writer):
    def _doc_build(b):
        Document(document=b)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(
            b=_generate_random_document('buffer', buffer_length=buffer_length).json()
        ),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_str_json_origin_buffer',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(buffer_length=buffer_length),
        )
    )


@pytest.mark.parametrize('text_length', [10, 100, 1000, 10000])
def test_construct_dict_origin_text(text_length, json_writer):
    def _doc_build(b):
        Document(document=b)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(
            b=_generate_random_document('text', text_length=text_length).dict()
        ),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_dict_origin_text',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(text_length=text_length),
        )
    )


@pytest.mark.parametrize('num_dims', [1, 2])
def test_construct_dict_origin_blob(num_dims, json_writer):
    def _doc_build(b):
        Document(document=b)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(b=_generate_random_document('blob', num_dims=num_dims).dict()),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_dict_origin_blob',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_dims=num_dims),
        )
    )


@pytest.mark.parametrize('buffer_length', [10, 100, 1000, 10000])
def test_construct_dict_origin_buffer(buffer_length, json_writer):
    def _doc_build(b):
        Document(document=b)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(
            b=_generate_random_document('buffer', buffer_length=buffer_length).dict()
        ),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_dict_origin_buffer',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(buffer_length=buffer_length),
        )
    )


@pytest.mark.parametrize('copy', [True, False])
@pytest.mark.parametrize('text_length', [10, 100, 1000, 10000])
def test_construct_document_origin_text(copy, text_length, json_writer):
    def _doc_build(d):
        Document(document=d, copy=copy)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(d=_generate_random_document('text', text_length)),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_document_origin_text',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(text_length=text_length, copy=copy),
        )
    )


@pytest.mark.parametrize('copy', [True, False])
@pytest.mark.parametrize('num_dims', [1, 2])
def test_construct_document_origin_blob(copy, num_dims, json_writer):
    def _doc_build(d):
        Document(document=d, copy=copy)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(d=_generate_random_document('blob', num_dims=num_dims)),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_document_origin_blob',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_dims=num_dims, copy=copy),
        )
    )


@pytest.mark.parametrize('copy', [True, False])
@pytest.mark.parametrize('buffer_length', [10, 100, 1000, 10000])
def test_construct_document_origin_buffer(copy, buffer_length, json_writer):
    def _doc_build(d):
        Document(document=d, copy=copy)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(d=_generate_random_document('buffer', buffer_length=buffer_length)),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_document_origin_buffer',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(buffer_length=buffer_length, copy=copy),
        )
    )


@pytest.mark.parametrize('copy', [True, False])
@pytest.mark.parametrize('text_length', [10, 100, 1000, 10000])
def test_construct_document_origin_text_proto(copy, text_length, json_writer):
    def _doc_build(d):
        Document(document=d, copy=copy)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(d=_generate_random_document('text', text_length).proto),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_document_origin_text_proto',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(text_length=text_length, copy=copy),
        )
    )


@pytest.mark.parametrize('copy', [True, False])
@pytest.mark.parametrize('num_dims', [1, 2])
def test_construct_document_origin_blob_proto(copy, num_dims, json_writer):
    def _doc_build(d):
        Document(document=d, copy=copy)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(d=_generate_random_document('blob', num_dims=num_dims).proto),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_document_origin_blob_proto',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_dims=num_dims, copy=copy),
        )
    )


@pytest.mark.parametrize('copy', [True, False])
@pytest.mark.parametrize('buffer_length', [10, 100, 1000, 10000])
def test_construct_document_origin_buffer_proto(copy, buffer_length, json_writer):
    def _doc_build(d):
        Document(document=d, copy=copy)

    mean_time, std_time = benchmark_time(
        _doc_build,
        NUM_DOCS,
        kwargs=dict(
            d=_generate_random_document('buffer', buffer_length=buffer_length).proto
        ),
    )

    json_writer.append(
        dict(
            name='document_construct/test_construct_document_origin_buffer_proto',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(buffer_length=buffer_length, copy=copy),
        )
    )
