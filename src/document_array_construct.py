import os
import uuid

from faker import Faker

from jina import Document, DocumentArray, __version__
from jina.types.arrays.memmap import DocumentArrayMemmap
from jina.logging.profile import TimeContext

fake = Faker()
NUM_DOCS = 1000
MEMMAP_PATH = os.path.join(os.getcwd(), 'tmp/{}'.format(str(uuid.uuid4())))


def _generate_repeated_container():
    """Used to benchmark construct DocumentArray or DocumentArrayMemmap using .chunks or .matches"""
    d = Document()
    for idx in range(NUM_DOCS):
        d.chunks.append(Document(text=fake.text()))


def _generate_document_array():
    """Used to benchmark construct DocumentArray or DocumentArrayMemmap using another document array"""
    da = DocumentArray()
    for idx in range(NUM_DOCS):
        da.append(Document(text=fake.text()))


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


def _generate_yield_documents():
    """Used to benchmark construct DocumentArray from a document generator."""
    for idx in range(NUM_DOCS):
        yield Document(text=fake.text())


def _generate_document_array_memmap():
    """Used to benchmark construct DocumentArray from a document generator."""
    dam = DocumentArrayMemmap(MEMMAP_PATH)
    for idx in range(NUM_DOCS):
        dam.append(Document(text=fake.text()))
