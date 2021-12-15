import os

import numpy as np
import pytest
from jina import Document

from .pages import Pages
from .utils.benchmark import benchmark_time

"""
This file contains tests for the following methods from Document:

- load_uri_to_image_blob
- convert_image_buffer_to_blob
- convert_image_datauri_to_blob
- convert_buffer_to_blob
- convert_image_blob_to_uri
- convert_blob_to_buffer
- load_uri_to_buffer
- convert_uri_to_datauri
- convert_buffer_to_uri
- convert_text_to_uri
- load_uri_to_text
- convert_content_to_uri
"""


cur_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_load_uri_to_image_blob(num_docs, json_writer):
    def _input_docs():
        image_dir = os.path.join(cur_dir, "utils", "test.png")
        return (), dict(docs=[Document(uri=image_dir) for _ in range(num_docs)])

    def _load_uri_to_image_blob(docs):
        for doc in docs:
            doc.load_uri_to_image_blob()

    result = benchmark_time(setup=_input_docs, func=_load_uri_to_image_blob)

    json_writer.append(
        page=Pages.DOCUMENT_CONVERSION,
        result=result,
        metadata=dict(num_docs=num_docs),
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

    def _load_uri_to_buffer(docs):
        for doc in docs:
            doc.load_uri_to_buffer()

    result = benchmark_time(setup=_input_docs, func=_load_uri_to_buffer)

    json_writer.append(
        page=Pages.DOCUMENT_CONVERSION,
        result=result,
        metadata=dict(num_docs=num_docs),
    )


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_image_buffer_to_blob(num_docs, json_writer):
    def _input_docs():
        image_dir = os.path.join(cur_dir, "utils", "test.png")
        docs = []
        for _ in range(num_docs):
            doc = Document(uri=image_dir)
            doc.load_uri_to_buffer()
            docs.append(doc)

        return (), dict(docs=docs)

    def _image_buffer_to_blob(docs):
        for doc in docs:
            doc.convert_buffer_to_image_blob()

    result = benchmark_time(setup=_input_docs, func=_image_buffer_to_blob)

    json_writer.append(
        page=Pages.DOCUMENT_CONVERSION,
        result=result,
        metadata=dict(num_docs=num_docs),
    )


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_image_datauri_to_blob(num_docs, json_writer):
    def _input_docs():
        image_dir = os.path.join(cur_dir, "utils", "test.png")
        docs = []
        for _ in range(num_docs):
            doc = Document(uri=image_dir)
            doc.convert_uri_to_datauri()
            docs.append(doc)

        return (), dict(docs=docs)

    def _load_uri_to_image_blob(docs):
        for doc in docs:
            doc.load_uri_to_image_blob()

    result = benchmark_time(setup=_input_docs, func=_load_uri_to_image_blob)

    json_writer.append(
        page=Pages.DOCUMENT_CONVERSION,
        result=result,
        metadata=dict(num_docs=num_docs),
    )


@pytest.mark.parametrize("num_docs", [1, 100, 1000])
def test_document_convert_uri_to_datauri(num_docs, json_writer):
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

    result = benchmark_time(setup=_input_docs, func=_convert_uri_to_datauri)

    json_writer.append(
        page=Pages.DOCUMENT_CONVERSION,
        result=result,
        metadata=dict(num_docs=num_docs),
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

    result = benchmark_time(setup=_input_docs, func=_convert_buffer_to_blob)

    json_writer.append(
        page=Pages.DOCUMENT_CONVERSION,
        result=result,
        metadata=dict(num_docs=num_docs),
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
            doc.convert_image_blob_to_uri()

    result = benchmark_time(setup=_input_docs, func=_convert_image_blob_to_uri)

    json_writer.append(
        page=Pages.DOCUMENT_CONVERSION,
        result=result,
        metadata=dict(num_docs=num_docs),
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

    result = benchmark_time(setup=_input_docs, func=_convert_content_to_uri)

    json_writer.append(
        page=Pages.DOCUMENT_CONVERSION,
        result=result,
        metadata=dict(num_docs=num_docs),
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
            _ = doc.dump_text_to_datauri

    result = benchmark_time(setup=_input_docs, func=_convert_text_to_uri)

    json_writer.append(
        page=Pages.DOCUMENT_CONVERSION,
        result=result,
        metadata=dict(num_docs=num_docs),
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

    result = benchmark_time(setup=_input_docs, func=_convert_buffer_to_uri)

    json_writer.append(
        page=Pages.DOCUMENT_CONVERSION,
        result=result,
        metadata=dict(num_docs=num_docs),
    )


@pytest.mark.parametrize("num_docs", [1, 5])
def test_document_load_uri_to_text(num_docs, json_writer):
    def _input_docs():
        return (
            (),
            dict(
                docs=[
                    Document(uri="http://google.com/index.html", mime_type="text/html")
                    for _ in range(num_docs)
                ]
            ),
        )

    def _load_uri_to_text(docs):
        for doc in docs:
            _ = doc.load_uri_to_text()

    result = benchmark_time(setup=_input_docs, func=_load_uri_to_text)

    json_writer.append(
        page=Pages.DOCUMENT_CONVERSION,
        result=result,
        metadata=dict(num_docs=num_docs),
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

    result = benchmark_time(setup=_input_docs, func=_convert_buffer_to_uri)

    json_writer.append(
        page=Pages.DOCUMENT_CONVERSION,
        result=result,
        metadata=dict(num_docs=num_docs),
    )
