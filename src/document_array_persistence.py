import pytest

from jina import Document, DocumentArray, __version__

from .utils.benchmark import benchmark_time

NUM_DOCS = 100000

NUM_REPETITIONS = 5


@pytest.fixture
def doc_array():
    return DocumentArray(
        (Document(text=f'This is the document number: {i}') for i in range(NUM_DOCS))
    )


@pytest.mark.parametrize('file_format', ['json', 'binary'])
def test_document_array_save(doc_array, file_format, json_writer, tmpdir):
    extension = 'bin' if file_format == 'binary' else 'json'
    file = f'{str(tmpdir)}/doc_array.{extension}'

    def _save():
        doc_array.save(file, file_format=file_format)

    def _teardown():
        import os
        os.remove(file)

    mean_time, std_time = benchmark_time(
        func=_save,
        teardown=_teardown,
        n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name='document_array_persistence/test_document_array_save',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs_append=NUM_DOCS, file_format=file_format)
        )
    )


@pytest.mark.parametrize('file_format', ['json', 'binary'])
def test_document_array_load(doc_array, file_format, json_writer, tmpdir):
    extension = 'bin' if file_format == 'binary' else 'json'
    file = f'{str(tmpdir)}/doc_array.{extension}'

    def _save():
        doc_array.save(file, file_format=file_format)
        return (), dict()

    def _load():
        DocumentArray.load(file, file_format=file_format)

    def _teardown():
        import os
        os.remove(file)

    mean_time, std_time = benchmark_time(
        setup=_save,
        func=_load,
        teardown=_teardown,
        n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name='document_array_persistence/test_document_array_load',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs_append=NUM_DOCS, file_format=file_format)
        )
    )
