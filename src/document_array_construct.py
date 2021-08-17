import pytest

from faker import Faker

from jina import Document, DocumentArray, __version__
from jina.types.arrays.memmap import DocumentArrayMemmap
from .utils.benchmark import benchmark_time

fake = Faker()
NUM_DOCS = 10000
NUM_REPETITIONS = 5


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
def doc_array_memmap(docs, tmpdir):
    dam = DocumentArrayMemmap(f'{str(tmpdir)}/memmap')
    dam.extend(docs)
    return dam


def test_construct_document_array_from_repeated_container(doc_with_chunks, json_writer):
    def _construct():
        DocumentArray(doc_with_chunks.chunks)

    mean_time, std_time = benchmark_time(func=_construct, n=NUM_REPETITIONS)

    json_writer.append(
        dict(
            name='document_array_construct/test_construct_document_array_from_repeated_container',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_chunks=NUM_DOCS),
        )
    )


def test_construct_document_array_from_another_documentarray(doc_array, json_writer):
    def _construct():
        DocumentArray(doc_array)

    mean_time, std_time = benchmark_time(func=_construct, n=NUM_REPETITIONS)

    json_writer.append(
        dict(
            name='document_array_construct/test_construct_document_array_from_another_documentarray',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=len(doc_array)),
        )
    )


def test_construct_document_array_from_list_of_documents(docs, json_writer):
    def _construct():
        DocumentArray(docs)

    mean_time, std_time = benchmark_time(func=_construct, n=NUM_REPETITIONS)

    json_writer.append(
        dict(
            name='document_array_construct/test_construct_document_array_from_list_of_documents',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=len(docs)),
        )
    )


def test_construct_document_array_from_tuple_of_documents(tuple_docs, json_writer):
    def _construct():
        DocumentArray(tuple_docs)

    mean_time, std_time = benchmark_time(func=_construct, n=NUM_REPETITIONS)

    json_writer.append(
        dict(
            name='document_array_construct/test_construct_document_array_from_tuple_of_documents',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=len(tuple_docs)),
        )
    )


def test_construct_document_array_from_generator(json_writer):
    def _yield_documents():
        """Used to benchmark construct DocumentArray from a document generator."""
        for idx in range(NUM_DOCS):
            yield Document(text=fake.text())

    def _construct():
        DocumentArray(_yield_documents())

    mean_time, std_time = benchmark_time(func=_construct, n=NUM_REPETITIONS)

    json_writer.append(
        dict(
            name='document_array_construct/test_construct_document_array_from_generator',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=NUM_DOCS),
        )
    )


def test_construct_document_array_from_another_documentarray_memmap(
    doc_array_memmap, json_writer
):
    def _construct():
        DocumentArray(doc_array_memmap)

    mean_time, std_time = benchmark_time(func=_construct, n=NUM_REPETITIONS)

    json_writer.append(
        dict(
            name='document_array_construct/test_construct_document_array_from_another_documentarray_memmap',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=len(doc_array_memmap)),
        )
    )
