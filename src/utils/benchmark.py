from pathlib import Path
from typing import Any, Callable

from jina import __version__


def get_output_file_name(current_file: str) -> str:
    """Get the output file name based on the name of ``current_file``

    The output file name will be based on the jina version and the
    name you passed with ``current_file`` - you should use ``__file__``
    for that. For example, if your file is::

        src/document_array_append.py

    and you are working with jina 2.0.17, the function will return::

        docs/static/artifacts/2.0.17/document_array_append.txt
    """

    output_dir = Path.cwd() / f'docs/static/artifacts/{__version__}'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file_name = output_dir / f'{Path(current_file).stem}.txt'

    return output_file_name


def average_benchmark(
    func: Callable[[Any], float], description: str, n: int, *args, **kwargs
) -> str:
    """Get average benchmark result over multiple repetitions

    :param func: The function to benchmark
    :param description: the description of the result, should contain
        ``{avg_time}`` in it, which will be filled with the result
        and returned
    :param n: Number of repetitions
    :param args: Positional arguments to pass to ``func``
    :param kwargs: Keyword arguments to pass to ``func``
    """

    results = [func(*args, **kwargs) for _ in range(n)]
    avg_time = sum(results) / len(results)

    return description.format(avg_time=avg_time)
