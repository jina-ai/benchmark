import os
import uuid
from pathlib import Path

from faker import Faker

from jina import Document, DocumentArray, __version__
from jina.types.arrays.memmap import DocumentArrayMemmap
from utils.timecontext import TimeContext

fake = Faker()
NUM_DOCS = 10000
MEMMAP_PATH = os.path.join(os.getcwd(), 'tmp/{}'.format(str(uuid.uuid4())))


def _generate_repeated_container():
    """Used to benchmark construct DocumentArray or DocumentArrayMemmap using .chunks or .matches"""
    d = Document()
    for idx in range(NUM_DOCS):
        d.chunks.append(Document(text=fake.text()))
    return d


def _generate_document_array():
    """Used to benchmark construct DocumentArray or DocumentArrayMemmap using another document array"""
    da = DocumentArray()
    for idx in range(NUM_DOCS):
        da.append(Document(text=fake.text()))
    return da


def _generate_single_document():
    """Used to benchmark construct DocumentArray or DocumentArrayMemmap from a single document"""
    return Document(text=fake.text())


def _generate_list_documents():
    """Used to benchmark construct DocumentArray from a list of documents."""
    docs = []
    for idx in range(NUM_DOCS):
        docs.append(Document(text=fake.text()))
    return docs


def _generate_tuple_documents():
    """Used to benchmark construct DocumentArray from a tuple of documents."""
    return tuple(_generate_list_documents())


def _yield_documents():
    """Used to benchmark construct DocumentArray from a document generator."""
    for idx in range(NUM_DOCS):
        yield Document(text=fake.text())


def _generate_document_array_memmap():
    """Used to benchmark construct DocumentArray from a document generator."""
    dam = DocumentArrayMemmap(MEMMAP_PATH)
    for idx in range(NUM_DOCS):
        dam.append(Document(text=fake.text()))
    return dam


def benchmark_construct_document_array_from_repeated_container(fp):
    doc = _generate_repeated_container()
    with TimeContext() as timer:
        DocumentArray(doc.chunks)
    fp.write(
        f'Constructing DocumentArray from repeated container took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n'
    )


def benchmark_construct_document_array_from_another_document_array(fp):
    da = _generate_document_array()
    with TimeContext() as timer:
        DocumentArray(da)
    fp.write(
        f'Constructing DocumentArray from another document array took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n'
    )


def benchmark_construct_document_array_from_list_of_documents(fp):
    da = _generate_list_documents()
    with TimeContext() as timer:
        DocumentArray(da)
    fp.write(
        f'Constructing DocumentArray from list of documents took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n'
    )


def benchmark_construct_document_array_from_tuple_of_documents(fp):
    da = _generate_tuple_documents()
    with TimeContext() as timer:
        DocumentArray(da)
    fp.write(
        f'Constructing DocumentArray from tuple of documents took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n'
    )


def benchmark_construct_document_array_from_generator(fp):
    da = _yield_documents()
    with TimeContext() as timer:
        DocumentArray(da)
    fp.write(
        f'Constructing DocumentArray from generator took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n'
    )


def benchmark_construct_document_array_from_memmap(fp):
    da = _generate_document_array_memmap()
    with TimeContext() as timer:
        DocumentArray(da)
    fp.write(
        f'Constructing DocumentArray from document array memmap took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n'
    )


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
        benchmark_construct_document_array_from_repeated_container(fp)
        benchmark_construct_document_array_from_another_document_array(fp)
        benchmark_construct_document_array_from_list_of_documents(fp)
        benchmark_construct_document_array_from_tuple_of_documents(fp)
        benchmark_construct_document_array_from_generator(
            fp
        )  # slow since generate documents on-the-fly.
        benchmark_construct_document_array_from_memmap(fp)


if __name__ == '__main__':
    benchmark()
