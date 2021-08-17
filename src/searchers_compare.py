import json
import os
from statistics import mean, stdev
from typing import Union

import numpy as np
import pytest
from jina import Document, DocumentArray, Executor, Flow, __version__, requests
from jina.types.arrays.memmap import DocumentArrayMemmap
from pympler import asizeof, tracker

from .utils.timecontext import TimeContext

NUM_REPETITIONS = 5
NUM_REQUESTS = 5


def get_readable_size(num_bytes: Union[int, float]) -> str:
    """
    Transform the bytes into readable value with different units (e.g. 1 KB, 20 MB, 30.1 GB).

    :param num_bytes: Number of bytes.
    :return: Human readable string representation.
    """
    num_bytes = int(num_bytes)
    if num_bytes < 1024:
        return f'{num_bytes} Bytes'
    elif num_bytes < 1024 ** 2:
        return f'{num_bytes / 1024:.1f} KB'
    elif num_bytes < 1024 ** 3:
        return f'{num_bytes / (1024 ** 2):.1f} MB'
    else:
        return f'{num_bytes / (1024 ** 3):.1f} GB'


def _get_docs(number_of_documents, embedding_size):
    return [
        Document(embedding=np.random.rand(embedding_size), id=str(i))
        for i in range(number_of_documents)
    ]


def _get_dam(number_of_documents, embedding_size, dir_path, **kwargs):
    import shutil

    tmp_path = f'{dir_path}/memmap_{number_of_documents}_{embedding_size}_tmp'
    path = f'{dir_path}/memmap_{number_of_documents}_{embedding_size}'
    if os.path.exists(path):
        return path
    da = DocumentArrayMemmap(tmp_path)
    docs = _get_docs(number_of_documents, embedding_size)
    da.extend(docs)
    da.save()
    shutil.copytree(tmp_path, path)
    da.clear()
    da._last_mmap = None
    return path


def _get_da(number_of_documents, embedding_size, dir_path, **kwargs):
    path = f'{dir_path}/docs.bin'
    if os.path.exists(path):
        return path
    da = DocumentArray()
    docs = _get_docs(number_of_documents, embedding_size)
    da.extend(docs)
    da.save(path, file_format='binary')
    da.clear()
    return path


def _get_document_array(dam_index, **kwargs):
    return _get_dam(**kwargs) if dam_index else _get_da(**kwargs)


class DocumentArraySearcher(Executor):
    def __init__(
        self,
        indexed_docs_path,
        dam_index,
        warmup=False,
        top_k: int = 50,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.indexed_docs_path = indexed_docs_path
        self._index_docs = (
            DocumentArray.load(indexed_docs_path, file_format='binary')
            if not dam_index
            else DocumentArrayMemmap(indexed_docs_path)
        )
        if warmup:
            self._index_docs.get_attributes('embedding')
        self._top_k = top_k

    @requests
    def search(self, docs, **kwargs):
        docs.match(
            self._index_docs,
            metric='cosine',
            use_scipy=False,
            limit=self._top_k,
        )


@pytest.fixture(scope='module')
def searchers_compare_writer(pytestconfig):
    results = []
    yield results

    from pathlib import Path

    output_dir = 'docs/static/artifacts/{}'.format(__version__)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    with open(f'{output_dir}/searchers_compare.json', 'w+') as file:
        json.dump(results, file)


@pytest.mark.timeout(3600)
@pytest.mark.parametrize('number_of_indexed_documents', [10000, 100000, 1000000])
@pytest.mark.parametrize('number_of_documents_request', [1, 32, 64])
@pytest.mark.parametrize('emb_size', [128, 256, 512, 1024])
@pytest.mark.parametrize('dam_index', [False, True])
@pytest.mark.parametrize('warmup', [True, False])
def test_search_compare(
    number_of_indexed_documents,
    number_of_documents_request,
    emb_size,
    dam_index,
    warmup,
    tmpdir,
    searchers_compare_writer,
):
    if warmup and not dam_index:
        pytest.skip('Warmup is not relevant for `DocumentArray`')

    # make sure in case of timeout we can see which timedout
    searchers_compare_writer.append(
        dict(
            name='searchers_compare/test_search_compare',
            iterations=NUM_REPETITIONS,
            mean_time=None,
            std_time=None,
            mean_memory=None,
            std_memory=None,
            mean_indexer_memory=None,
            std_indexer_memory=None,
            unit='ms',
            metadata=dict(
                number_of_indexed_documents=number_of_indexed_documents,
                embedding_size=emb_size,
                query_docs=number_of_documents_request * NUM_REQUESTS,
                query_docs_per_request=number_of_documents_request,
                mean_docs_per_second=None,
                latency_per_doc=None,
                num_batches=NUM_REQUESTS,
                dam_index=dam_index,
                warmup_embeddings=warmup,
            ),
        )
    )

    result = searchers_compare_writer[-1]

    def _get_indexer():
        path = _get_document_array(
            dam_index=dam_index,
            number_of_documents=number_of_indexed_documents,
            embedding_size=emb_size,
            dir_path=str(tmpdir),
        )

        return DocumentArraySearcher(
            indexed_docs_path=path, dam_index=dam_index, warmup=warmup
        )

    query_docs = [
        DocumentArray(_get_docs(number_of_documents_request, embedding_size=emb_size))
    ] * NUM_REQUESTS

    def _func():
        with TimeContext() as indexer_ctx:
            indexer = _get_indexer()
        print(f' indexer created/loaded in {indexer_ctx.duration}')
        indexer_memory = asizeof.asizeof(indexer)

        tr = tracker.SummaryTracker()
        sum1 = tr.create_summary()

        with TimeContext() as time_context:
            for i in range(NUM_REQUESTS):
                indexer.search(query_docs[i])

        sum2 = tr.create_summary()
        diff = tr.diff(sum1, sum2)
        total_bytes = sum([ob_sum[2] for ob_sum in diff])

        return time_context.duration, total_bytes, indexer_memory

    indexer_memory_measures = []
    time_measures = []
    mem_measures = []
    for _ in range(NUM_REPETITIONS):
        time_measure, mem_measure, indexer_memory = _func()
        time_measures.append(time_measure)
        mem_measures.append(mem_measure)
        indexer_memory_measures.append(indexer_memory)

    mean_time = mean(time_measures)
    std_time = stdev(time_measures) if len(time_measures) > 1 else None

    mean_memory = mean(mem_measures)
    std_memory = stdev(mem_measures) if len(mem_measures) > 1 else None

    mean_indexer_memory = mean(indexer_memory_measures)
    std_indexer_memory = (
        stdev(indexer_memory_measures) if len(indexer_memory_measures) > 1 else None
    )

    result.update(
        dict(
            name='searchers_compare/test_search_compare',
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            mean_memory=get_readable_size(mean_memory),
            std_memory=get_readable_size(std_memory) if std_memory else None,
            mean_indexer_memory=get_readable_size(mean_indexer_memory),
            std_indexer_memory=get_readable_size(std_indexer_memory)
            if std_indexer_memory
            else None,
            unit='ms',
            metadata=dict(
                number_of_indexed_documents=number_of_indexed_documents,
                embedding_size=emb_size,
                query_docs=number_of_documents_request * NUM_REQUESTS,
                query_docs_per_request=number_of_documents_request,
                mean_docs_per_second=(number_of_documents_request * NUM_REQUESTS)
                / mean_time,
                latency_per_doc=mean_time
                / (number_of_documents_request * NUM_REQUESTS),
                num_batches=NUM_REQUESTS,
                dam_index=dam_index,
                warmup_embeddings=warmup,
            ),
        )
    )
