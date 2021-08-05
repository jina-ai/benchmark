import os
from pathlib import Path
import random
import string
import numpy as np

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


NUM_DOCS = 10000


def benchmark_get_content_text(fp):
    docs = [Document(text=_generate_random_text()) for _ in range(NUM_DOCS)]
    with TimeContext() as timer:
        for doc in docs:
            _ = doc.text

    fp.write(f'Getting Document text took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_get_content_blob(fp):
    docs = [Document(blob=_generate_random_blob()) for _ in range(NUM_DOCS)]
    with TimeContext() as timer:
        for doc in docs:
            _ = doc.blob

    fp.write(f'Getting Document blob took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_get_content_buffer(fp):
    docs = [Document(buffer=_generate_random_buffer()) for _ in range(NUM_DOCS)]
    with TimeContext() as timer:
        for doc in docs:
            _ = doc.buffer

    fp.write(f'Getting Document buffer took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


def benchmark_get_embedding(fp):
    docs = [Document(embedding=_generate_random_blob()) for _ in range(NUM_DOCS)]
    with TimeContext() as timer:
        for doc in docs:
            _ = doc.embedding

    fp.write(f'Getting Document embedding took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n')


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
        benchmark_get_content_text(fp)
        benchmark_get_content_blob(fp)
        benchmark_get_content_buffer(fp)
        benchmark_get_embedding(fp)


if __name__ == '__main__':
    benchmark()
