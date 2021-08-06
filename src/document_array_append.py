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


def _generate_list_documents():
    """Used to benchmark construct DocumentArray from a list of documents."""
    docs = []
    for idx in range(NUM_DOCS):
        docs.append(Document(text=fake.text()))
    return docs


def benchmark_document_array_append(fp):
    docs = _generate_list_documents()
    da = DocumentArray()
    with TimeContext() as timer:
        for doc in docs:
            da.append(doc)
    fp.write(
        f'Append {NUM_DOCS} Document to DocumentArray from list of Documents took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n'
    )


def benchmark_document_array_memmap_append_with_flush(fp):
    docs = _generate_list_documents()
    dam = DocumentArrayMemmap(MEMMAP_PATH)
    with TimeContext() as timer:
        for doc in docs:
            dam.append(doc)
    fp.write(
        f'Append {NUM_DOCS} Document to DocumentArrayMemmap with flush from list of Documents took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n'
    )


def benchmark_document_array_memmap_append_without_flush(fp):
    docs = _generate_list_documents()
    dam = DocumentArrayMemmap(MEMMAP_PATH)
    with TimeContext() as timer:
        for doc in docs:
            dam.append(doc, flush=False)
    fp.write(
        f'Append {NUM_DOCS} Document to DocumentArrayMemmap without flush from list of Documents took {timer.duration}, {timer.duration / NUM_DOCS} per doc\n'
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
        benchmark_document_array_append(fp)
        benchmark_document_array_memmap_append_with_flush(fp)
        benchmark_document_array_memmap_append_without_flush(fp)


if __name__ == '__main__':
    benchmark()
