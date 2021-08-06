import os
import string
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable

import numpy as np
from jina import Document, DocumentArray, __version__
from jina.types.arrays.memmap import DocumentArrayMemmap

from utils.timecontext import TimeContext

NUM_REPETITIONS = 25
NUM_DOCS = [100, 1000, 10000]
CHARS = tuple(string.ascii_uppercase + string.digits)


def _generate_random_text():
    return ''.join(np.random.choice(CHARS, 256))


def _generate_random_blob():
    return np.random.random(512)


def _generate_random_buffer():
    return bytes(bytearray(os.urandom(512 * 4)))


def _average_benchmark(
    func: Callable[[Any], float], description: str, n: int, *args, **kwargs
) -> str:
    """Get average benchmark result over multiple repetitions

    :param func: The function to benchmark
    :param description: the description of the result, should contain
        ``{avg_time}`` in it, which will be filled with the result
        and returned
    :param n: Number of repetitions
    :param args: Positional arguments to pass to ``func``
    :param kwargs: Keyword arguments to pass to ``fun``
    """

    results = [func(*args, **kwargs) for _ in range(n)]
    avg_time = sum(results) / len(results)

    return description.format(avg_time=avg_time)


def benchmark_da_extend_empty_docs(num_docs: int) -> float:
    da = DocumentArray()
    docs = [Document() for _ in range(num_docs)]

    with TimeContext() as t:
        da.extend(docs)

    return t.duration


def benchmark_da_extend_docs_with_text(num_docs: int) -> float:
    da = DocumentArray()
    docs = [Document(text=_generate_random_text()) for _ in range(num_docs)]

    with TimeContext() as t:
        da.extend(docs)

    return t.duration


def benchmark_da_extend_docs_with_blob(num_docs: int) -> float:
    da = DocumentArray()
    docs = [Document(blob=_generate_random_blob()) for _ in range(num_docs)]

    with TimeContext() as t:
        da.extend(docs)

    return t.duration


def benchmark_da_extend_docs_with_buffer(num_docs: int) -> float:
    da = DocumentArray()
    docs = [Document(buffer=_generate_random_buffer()) for _ in range(num_docs)]

    with TimeContext() as t:
        da.extend(docs)

    return t.duration


def benchmark_dam_extend_empty_docs(num_docs: int) -> float:
    with TemporaryDirectory() as tmpdir:
        dam = DocumentArrayMemmap(tmpdir + '/dam')
        docs = [Document() for _ in range(num_docs)]

        with TimeContext() as t:
            dam.extend(docs)

    return t.duration


def benchmark_dam_extend_docs_with_text(num_docs: int) -> float:
    with TemporaryDirectory() as tmpdir:
        dam = DocumentArrayMemmap(tmpdir + '/dam')
        docs = [Document(text=_generate_random_text()) for _ in range(num_docs)]

        with TimeContext() as t:
            dam.extend(docs)

    return t.duration


def benchmark_dam_extend_docs_with_blob(num_docs: int) -> float:
    with TemporaryDirectory() as tmpdir:
        dam = DocumentArrayMemmap(tmpdir + '/dam')
        docs = [Document(blob=_generate_random_blob()) for _ in range(num_docs)]

        with TimeContext() as t:
            dam.extend(docs)

    return t.duration


def benchmark_dam_extend_docs_with_buffer(num_docs: int) -> float:
    with TemporaryDirectory() as tmpdir:
        dam = DocumentArrayMemmap(tmpdir + '/dam')
        docs = [Document(buffer=_generate_random_buffer()) for _ in range(num_docs)]

        with TimeContext() as t:
            dam.extend(docs)

    return t.duration


def benchmark():

    output_dir = Path.cwd() / f'docs/static/artifacts/{__version__}'
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / f'{Path(__file__).stem}.txt', 'w+') as fp:
        for num_docs in NUM_DOCS:

            result = _average_benchmark(
                benchmark_da_extend_empty_docs,
                f"Extending DocumentArray by {num_docs} empty documents takes {{avg_time}} seconds\n",
                NUM_REPETITIONS,
                num_docs,
            )
            fp.write(result)

            result = _average_benchmark(
                benchmark_da_extend_docs_with_text,
                f"Extending DocumentArray by {num_docs} documents with text takes {{avg_time}} seconds\n",
                NUM_REPETITIONS,
                num_docs,
            )
            fp.write(result)

            result = _average_benchmark(
                benchmark_da_extend_docs_with_blob,
                f"Extending DocumentArray by {num_docs} documents with blob takes {{avg_time}} seconds\n",
                NUM_REPETITIONS,
                num_docs,
            )
            fp.write(result)

            result = _average_benchmark(
                benchmark_da_extend_docs_with_buffer,
                f"Extending DocumentArray by {num_docs} documents with buffer takes {{avg_time}} seconds\n",
                NUM_REPETITIONS,
                num_docs,
            )
            fp.write(result)

            result = _average_benchmark(
                benchmark_dam_extend_empty_docs,
                f"Extending DocumentArrayMemmap by {num_docs} empty documents takes {{avg_time}} seconds\n",
                NUM_REPETITIONS,
                num_docs,
            )
            fp.write(result)

            result = _average_benchmark(
                benchmark_dam_extend_docs_with_text,
                f"Extending DocumentArrayMemmap by {num_docs} documents with text takes {{avg_time}} seconds\n",
                NUM_REPETITIONS,
                num_docs,
            )
            fp.write(result)

            result = _average_benchmark(
                benchmark_dam_extend_docs_with_blob,
                f"Extending DocumentArrayMemmap by {num_docs} documents with blob takes {{avg_time}} seconds\n",
                NUM_REPETITIONS,
                num_docs,
            )
            fp.write(result)

            result = _average_benchmark(
                benchmark_dam_extend_docs_with_buffer,
                f"Extending DocumentArrayMemmap by {num_docs} documents with buffer takes {{avg_time}} seconds\n",
                NUM_REPETITIONS,
                num_docs,
            )
            fp.write(result)


if __name__ == "__main__":
    benchmark()
