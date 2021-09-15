import pytest
import os
import numpy as np

from jina import Document, DocumentArray

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5

"""
This file contains tests for the following methods from Document:

- convert_image_uri_to_blob
- convert_image_buffer_to_blob
- convert_image_datauri_to_blob
- convert_buffer_to_blob
- convert_image_blob_to_uri
- convert_blob_to_buffer
- convert_uri_to_buffer
- convert_uri_to_datauri
- convert_buffer_to_uri
- convert_text_to_uri
- convert_uri_to_text
- convert_content_to_uri
"""


cur_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_image_uri_to_blob(num_docs, json_writer):
    def _input_docs():
        image_dir = os.path.join(cur_dir, "utils", "test.png")
        return (), dict(docs=[Document(uri=image_dir) for _ in range(num_docs)])

    def _image_uri_to_blob(docs):
        for doc in docs:
            doc.convert_image_uri_to_blob()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_image_uri_to_blob, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_conversions_blob_image_uri_text/test_document_convert_image_uri_to_blob",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_uri_to_buffer(num_docs, json_writer):
    def _input_docs():
        image_dir = os.path.join(cur_dir, "utils", "test.png")
        docs = []
        for _ in range(num_docs):
            doc = Document(uri=image_dir)
            docs.append(doc)

        return (), dict(docs=docs)

    def _convert_uri_to_buffer(docs):
        for doc in docs:
            doc.convert_uri_to_buffer()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_convert_uri_to_buffer, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_conversions_blob_image_uri_text/test_document_convert_uri_to_buffer",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_image_buffer_to_blob(num_docs, json_writer):
    def _input_docs():
        image_dir = os.path.join(cur_dir, "utils", "test.png")
        docs = []
        for _ in range(num_docs):
            doc = Document(uri=image_dir)
            doc.convert_uri_to_buffer()
            docs.append(doc)

        return (), dict(docs=docs)

    def _image_buffer_to_blob(docs):
        for doc in docs:
            doc.convert_image_buffer_to_blob()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_image_buffer_to_blob, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_conversions_blob_image_uri_text/test_document_convert_image_buffer_to_blob",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_image_buffer_to_blob(num_docs, json_writer):
    def _input_docs():
        image_dir = os.path.join(cur_dir, "utils", "test.png")
        docs = []
        for _ in range(num_docs):
            doc = Document(uri=image_dir)
            doc.convert_uri_to_datauri()
            docs.append(doc)

        return (), dict(docs=docs)

    def _convert_image_datauri_to_blob(docs):
        for doc in docs:
            doc.convert_image_datauri_to_blob()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_convert_image_datauri_to_blob, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_conversions_blob_image_uri_text/test_document_convert_image_buffer_to_blob",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_convert_uri_to_datauri(num_docs, json_writer):
    def _input_docs():
        image_dir = os.path.join(cur_dir, "utils", "test.png")
        docs = []
        for _ in range(num_docs):
            doc = Document(uri=image_dir)
            docs.append(doc)

        return (), dict(docs=docs)

    def _convert_uri_to_datauri(docs):
        for doc in docs:
            doc.convert_uri_to_datauri()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_convert_uri_to_datauri, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_conversions_blob_image_uri_text/test_document_convert_convert_uri_to_datauri",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_buffer_to_blob(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=[
                    Document(content=np.random.random((85, 152, 3)))
                    for _ in range(num_docs)
                ]
            ),
        )

    def _convert_buffer_to_blob(docs):
        for doc in docs:
            doc.convert_buffer_to_blob()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_convert_buffer_to_blob, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_conversions_blob_image_uri_text/test_document_convert_buffer_to_blob",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_image_blob_to_uri(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=[
                    Document(content=np.random.randint(0, 255, 32 * 28))
                    for _ in range(num_docs)
                ]
            ),
        )

    def _convert_image_blob_to_uri(docs):
        for doc in docs:
            doc.convert_image_blob_to_uri(32, 28)

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_convert_image_blob_to_uri, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_conversions_blob_image_uri_text/test_document_convert_image_blob_to_uri",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_content_to_uri(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=[
                    Document(content=np.random.randint(0, 255, 32 * 28))
                    for _ in range(num_docs)
                ]
            ),
        )

    def _convert_content_to_uri(docs):
        for doc in docs:
            _ = doc.convert_content_to_uri

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_convert_content_to_uri, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_conversions_blob_image_uri_text/test_document_convert_content_to_uri",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_text_to_uri(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=[
                    Document(content=np.random.randint(0, 255, 32 * 28))
                    for _ in range(num_docs)
                ]
            ),
        )

    def _convert_text_to_uri(docs):
        for doc in docs:
            _ = doc.convert_text_to_uri

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_convert_text_to_uri, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_conversions_blob_image_uri_text/test_document_convert_text_to_uri",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_buffer_to_uri(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=[
                    Document(uri=os.path.join(cur_dir, "test.png"))
                    for _ in range(num_docs)
                ]
            ),
        )

    def _convert_buffer_to_uri(docs):
        for doc in docs:
            _ = doc.convert_buffer_to_uri()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_convert_buffer_to_uri, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_conversions_blob_image_uri_text/test_document_convert_buffer_to_uri",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [1, 5])
def test_document_convert_uri_to_text(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=[
                    Document(
                        content="http://google.com/index.html", mime_type="text/html"
                    )
                    for _ in range(num_docs)
                ]
            ),
        )

    def _convert_uri_to_text(docs):
        for doc in docs:
            _ = doc.convert_uri_to_text()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_convert_uri_to_text, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_conversions_blob_image_uri_text/test_document_convert_uri_to_text",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_blob_to_buffer(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=[
                    Document(content=np.random.randint(0, 255, 32 * 28))
                    for _ in range(num_docs)
                ]
            ),
        )

    def _convert_buffer_to_uri(docs):
        for doc in docs:
            _ = doc.convert_blob_to_buffer()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_convert_buffer_to_uri, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_conversions_blob_image_uri_text/test_document_convert_blob_to_buffer",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )



@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_blob_to_buffer(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=[
                    Document(content=np.random.randint(0, 255, 32 * 28))
                    for _ in range(num_docs)
                ]
            ),
        )

    def _convert_buffer_to_uri(docs):
        for doc in docs:
            _ = doc.convert_blob_to_buffer()

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_convert_buffer_to_uri, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_conversions_blob_image_uri_text/test_document_convert_blob_to_buffer",
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(num_docs=num_docs),
        )
    )
