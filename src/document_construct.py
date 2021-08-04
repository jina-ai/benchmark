import random
import string
import numpy as np
import os
import uuid
from pathlib import Path

from jina import Document, __version__
from timecontext import TimeContext


def _generate_random_text():
    length = random.randint(30, 3000)
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def _generate_random_buffer():
    length = random.randint(30, 3000)
    return bytes(bytearray(random.getrandbits(8) for _ in range(length)))


def _generate_random_blob():
    # 1 and 3 can cover from audio signals to images. 3 dimensions make the memory too high
    shape_length = random.randint(1, 2)
    shape = [random.randint(100, 200)] * shape_length

    return np.random.rand(*shape)


def _generate_random_document():
    tags = {'tag1': [0, 2, 3], 'tag2': 'value of tag2'}
    option = random.choice(['text', 'blob', 'buffer'])
    if option == 'text':
        return Document(text=_generate_random_text(), tags=tags)
    if option == 'blob':
        return Document(blob=_generate_random_blob(), tags=tags)
    if option == 'buffer':
        return Document(buffer=_generate_random_buffer(), tags=tags)


def _generate_random_document_with_chunks_and_matches():
    root = _generate_random_document()

    num_chunks = random.randint(1, 20)
    num_matches = random.randint(1, 20)
    for _ in range(num_chunks):
        root.chunks.append(_generate_random_document())
    for _ in range(num_matches):
        root.matches.append(_generate_random_document())
    return root


NUM_DOCS = 1000


# 1000 documents
def benchmark_construct_text(fp):
    texts = []
    for _ in range(NUM_DOCS):
        texts.append(_generate_random_text())
    with TimeContext() as timer:
        for text in texts:
            Document(text=text)

    fp.write(f'Constructing Document from text took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_construct_blob(fp):
    blobs = []
    for _ in range(NUM_DOCS):
        blobs.append(_generate_random_blob())
    with TimeContext() as timer:
        for blob in blobs:
            Document(blob=blob)

    fp.write(f'Constructing Document from blob took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_construct_buffer(fp):
    buffers = []
    for _ in range(NUM_DOCS):
        buffers.append(_generate_random_buffer())
    with TimeContext() as timer:
        for buffer in buffers:
            Document(buffer=buffer)

    fp.write(f'Constructing Document from buffer took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_construct_bytes(fp):
    bytes_list = []
    for _ in range(NUM_DOCS):
        bytes_list.append(_generate_random_document().proto.SerializeToString())
    with TimeContext() as timer:
        for b in bytes_list:
            Document(document=b)

    fp.write(f'Constructing Document from bytes took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_construct_str_json(fp):
    json_list = []
    for _ in range(NUM_DOCS):
        json_list.append(_generate_random_document().json())
    with TimeContext() as timer:
        for s in json_list:
            Document(document=s)

    fp.write(f'Constructing Document from str took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_construct_str_json_with_chunks_and_matches(fp):
    json_list = []
    for _ in range(NUM_DOCS):
        json_list.append(_generate_random_document_with_chunks_and_matches().json())
    with TimeContext() as timer:
        for s in json_list:
            Document(document=s)

    fp.write(f'Constructing Document from str with chunks and matches took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_construct_dict(fp):
    dict_list = []
    for _ in range(NUM_DOCS):
        dict_list.append(_generate_random_document().dict())
    with TimeContext() as timer:
        for d in dict_list:
            Document(document=d)

    fp.write(f'Constructing Document from Dict took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_construct_dict_with_chunks_and_matches(fp):
    json_list = []
    for _ in range(NUM_DOCS):
        json_list.append(_generate_random_document_with_chunks_and_matches().dict())
    with TimeContext() as timer:
        for s in json_list:
            Document(document=s)

    fp.write(f'Constructing Document from str with chunks and matches took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_construct_document_no_copy(fp):
    docs_list = []
    for _ in range(NUM_DOCS):
        docs_list.append(_generate_random_document())
    with TimeContext() as timer:
        for d in docs_list:
            Document(document=d)

    fp.write(f'Constructing Document from Document without copy took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_construct_proto_no_copy(fp):
    proto_list = []
    for _ in range(NUM_DOCS):
        proto_list.append(_generate_random_document())
    with TimeContext() as timer:
        for p in proto_list:
            Document(document=p)

    fp.write(f'Constructing Document from proto without copy took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_construct_document_copy(fp):
    docs_list = []
    for _ in range(NUM_DOCS):
        docs_list.append(_generate_random_document())
    with TimeContext() as timer:
        for d in docs_list:
            Document(document=d, copy=True)

    fp.write(f'Constructing Document from Document with copy took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_construct_proto_copy(fp):
    proto_list = []
    for _ in range(NUM_DOCS):
        proto_list.append(_generate_random_document())
    with TimeContext() as timer:
        for p in proto_list:
            Document(document=p, copy=True)

    fp.write(f'Constructing Document from proto with copy took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark():
    output_dir = os.path.join(
        os.getcwd().replace('/src', ''), 'docs/static/artifacts/{}'.format(__version__)
    )
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    fp = open(
        os.path.join(
            output_dir,
            '{}.txt'.format(os.path.basename(__file__)).replace('.py', ''),
        ),
        'w+',
    )
    with fp:
        benchmark_construct_text(fp)
        benchmark_construct_blob(fp)
        benchmark_construct_buffer(fp)
        benchmark_construct_bytes(fp)
        benchmark_construct_str_json(fp)
        benchmark_construct_str_json_with_chunks_and_matches(fp)
        benchmark_construct_dict(fp)
        benchmark_construct_dict_with_chunks_and_matches(fp)
        benchmark_construct_document_no_copy(fp)
        benchmark_construct_proto_no_copy(fp)
        benchmark_construct_document_copy(fp)
        benchmark_construct_proto_copy(fp)


if __name__ == '__main__':
    benchmark()
