import pytest
from faker import Faker
from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap

from .utils.benchmark import benchmark_time
from .pages import Pages

fake = Faker()
Faker.seed(42)
NUM_DOCS = 10000


@pytest.fixture
def docs():
    return [Document(text=fake.text()) for _ in range(NUM_DOCS)]


@pytest.fixture
def doc_with_chunks():
    d = Document()
    for idx in range(NUM_DOCS):
        d.chunks.append(Document(text=fake.text()))
    return d


@pytest.fixture()
def tuple_docs(docs):
    return tuple(docs)


@pytest.fixture
def doc_array(docs):
    return DocumentArray(docs)


@pytest.fixture
def doc_array_memmap(docs, ephemeral_tmpdir):
    dam = DocumentArrayMemmap(f'{str(ephemeral_tmpdir)}/memmap')
    dam.extend(docs)
    return dam


def test_construct_document_array_from_repeated_container(doc_with_chunks, json_writer):
    def _construct():
        DocumentArray(doc_with_chunks.chunks)

    result = benchmark_time(func=_construct)

    json_writer.append(
        page=Pages.DA_CONSTRUCT,
        result=result,
        metadata=dict(num_chunks=NUM_DOCS),
    )


def test_construct_document_array_from_another_documentarray(doc_array, json_writer):
    def _construct():
        DocumentArray(doc_array)

    result = benchmark_time(func=_construct)

    json_writer.append(
        page=Pages.DA_CONSTRUCT,
        result=result,
        metadata=dict(num_docs=len(doc_array)),
    )


def test_construct_document_array_from_list_of_documents(docs, json_writer):
    def _construct():
        DocumentArray(docs)

    result = benchmark_time(func=_construct)

    json_writer.append(
        page=Pages.DA_CONSTRUCT,
        result=result,
        metadata=dict(num_docs=len(docs)),
    )


def test_construct_document_array_from_tuple_of_documents(tuple_docs, json_writer):
    def _construct():
        DocumentArray(tuple_docs)

    result = benchmark_time(func=_construct)

    json_writer.append(
        page=Pages.DA_CONSTRUCT,
        result=result,
        metadata=dict(num_docs=len(tuple_docs)),
    )


def test_construct_document_array_from_generator(json_writer):
    def _yield_documents():
        """Used to benchmark construct DocumentArray from a document generator."""
        for idx in range(NUM_DOCS):
            yield Document(text=fake.text())

    def _construct():
        DocumentArray(_yield_documents())

    result = benchmark_time(func=_construct)

    json_writer.append(
        page=Pages.DA_CONSTRUCT,
        result=result,
        metadata=dict(num_docs=NUM_DOCS),
    )


def test_construct_document_array_from_another_documentarray_memmap(
    doc_array_memmap, json_writer
):
    def _construct():
        DocumentArray(doc_array_memmap)

    result = benchmark_time(func=_construct)

    json_writer.append(
        page=Pages.DA_CONSTRUCT,
        result=result,
        metadata=dict(num_docs=len(doc_array_memmap)),
    )
