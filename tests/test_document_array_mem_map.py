import os
import uuid
from pathlib import Path
from jina import Document, __version__
from jina.types.arrays.memmap import DocumentArrayMemmap


def _get_mem_map_path():
    mem_map_path = os.path.join(os.getcwd(), 'tmp/{}'.format(str(uuid.uuid4())))
    Path(mem_map_path).mkdir(parents=True, exist_ok=True)

    return mem_map_path


def _get_doc_list(dam_size=1000000):
    doc_list = []
    dam_size = dam_size

    for i in range(dam_size):
        doc_list.append(
            Document(
                text=f'This is the document number: {i}',
            )
        )

    return doc_list


def document_array_mem_map(doc_list, mem_map_path):
    dam = DocumentArrayMemmap(mem_map_path)
    dam.extend(doc_list)

    return len(doc_list)


def test_document_array_mem_map(benchmark):
    dam_size = 1000000
    mem_map_path = _get_mem_map_path()
    doc_list = _get_doc_list(dam_size)
    result = benchmark(document_array_mem_map, doc_list, mem_map_path)

    assert result == dam_size