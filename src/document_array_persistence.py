import pytest
from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time
from .pages import Pages

NUM_DOCS = 100000


@pytest.fixture
def doc_array():
    return DocumentArray(
        (Document(text=f'This is the document number: {i}') for i in range(NUM_DOCS))
    )


@pytest.mark.parametrize('file_format', ['json', 'binary'])
def test_da_save(doc_array, file_format, json_writer, ephemeral_tmpdir):
    extension = 'bin' if file_format == 'binary' else 'json'
    file = f'{str(ephemeral_tmpdir)}/doc_array.{extension}'

    def _save():
        doc_array.save(file, file_format=file_format)

    def _teardown():
        import os

        os.remove(file)

    result = benchmark_time(func=_save, teardown=_teardown)

    json_writer.append(
        page=Pages.DA_PERSISTENCE,
        result=result,
        metadata=dict(num_docs_append=NUM_DOCS, file_format=file_format),
    )


@pytest.mark.parametrize('file_format', ['json', 'binary'])
def test_da_load(doc_array, file_format, json_writer, ephemeral_tmpdir):
    extension = 'bin' if file_format == 'binary' else 'json'
    file = f'{str(ephemeral_tmpdir)}/doc_array.{extension}'

    def _save():
        doc_array.save(file, file_format=file_format)
        return (), dict()

    def _load():
        DocumentArray.load(file, file_format=file_format)

    def _teardown():
        import os

        os.remove(file)

    result = benchmark_time(setup=_save, func=_load, teardown=_teardown)

    json_writer.append(
        page=Pages.DA_PERSISTENCE,
        result=result,
        metadata=dict(num_docs_append=NUM_DOCS, file_format=file_format),
    )
