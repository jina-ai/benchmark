import os
import shutil
from collections import defaultdict
from statistics import mean, stdev

import numpy as np
import pytest
from jina import Document, DocumentArray, Executor, requests, DocumentArrayMemmap
from pympler import asizeof, tracker

from .pages import Pages
from .utils.timecontext import TimeContext

NUM_REPETITIONS = 5
NUM_REQUESTS = 100
TARGET_FILE = 'searchers_compare.json'


def _get_docs(number_of_documents, embedding_size):
    return [
        Document(embedding=np.random.rand(embedding_size), id=str(i))
        for i in range(number_of_documents)
    ]


def _get_dam(number_of_documents, embedding_size, dir_path, **kwargs):
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


@pytest.mark.skipif(
    'JINA_BENCHMARK_SEARCHERS' not in os.environ,
    reason='This test take a lot of time, to be run explicitly and isolated from the rest',
)
@pytest.mark.parametrize(
    'name,indexed_docs,docs_per_request,emb_size',
    [
        ('Tiny Index', 100, 1, 128),
        ('Small Index', 10000, 1, 128),
        ('Medium Index', 100000, 1, 128),
        # ('Big Index', 1000000, 1, 128),
        ('Batch requesting', 100000, 32, 128),
        ('Big embeddings', 100000, 1, 512),
    ],
)
@pytest.mark.parametrize(
    'dam_index,warmup', [(False, False), (True, False), (True, True)]
)
def test_search_compare(
    name,
    indexed_docs,
    docs_per_request,
    emb_size,
    dam_index,
    warmup,
    ephemeral_tmpdir,
    json_writer,
):
    def _get_indexer():
        path = _get_document_array(
            dam_index=dam_index,
            number_of_documents=indexed_docs,
            embedding_size=emb_size,
            dir_path=str(ephemeral_tmpdir),
        )

        return DocumentArraySearcher(
            indexed_docs_path=path, dam_index=dam_index, warmup=warmup
        )

    query_docs = [
        DocumentArray(_get_docs(docs_per_request, embedding_size=emb_size))
    ] * NUM_REQUESTS

    data_points = defaultdict(list)
    all_search_timings = []

    def _func():
        with TimeContext() as indexer_context:
            indexer = _get_indexer()
        print(f' indexer created/loaded in {indexer_context.duration / 1e6} ms')
        data_points['index_time'].append(indexer_context.duration)
        data_points['index_memory'].append(asizeof.asizeof(indexer))

        tr = tracker.SummaryTracker()
        sum1 = tr.create_summary()
        timings = []
        for i in range(NUM_REQUESTS):
            with TimeContext() as seach_context:
                indexer.search(query_docs[i])
            timings.append(seach_context.duration)
        sum2 = tr.create_summary()
        diff = tr.diff(sum1, sum2)
        print(f' search finished in {sum(timings) / 1e6} ms')
        data_points['search_time'].append(sum(timings))
        all_search_timings.extend(timings)
        data_points['search_memory'].append(sum([ob_sum[2] for ob_sum in diff]))

        shutil.rmtree(str(ephemeral_tmpdir), ignore_errors=True)
        os.makedirs(str(ephemeral_tmpdir))

    for i in range(NUM_REPETITIONS):
        _func()

    results = {}

    for field in ['index_time', 'index_memory', 'search_time', 'search_memory']:
        results[f'mean_{field}'], results[f'std_{field}'] = get_mean_and_std(
            data_points[field]
        )

    results['p90'] = get_percentile(all_search_timings, 90)
    results['p99'] = get_percentile(all_search_timings, 99)

    json_writer.append_raw(
        target_file=TARGET_FILE,
        dict_=dict(
            name=name,
            page=Pages.INDEXER_COMPARISON,
            iterations=NUM_REPETITIONS,
            results=results,
            metadata=dict(
                indexed_docs=indexed_docs,
                embedding_size=emb_size,
                docs_per_request=docs_per_request,
                num_requests=NUM_REQUESTS,
                dam_index=dam_index,
                warmup_embeddings=warmup,
            ),
        ),
    )


def get_mean_and_std(data):
    mean_ = mean(data)
    std_ = stdev(data) if len(data) > 1 else None
    return mean_, std_


def get_percentile(timings, percentile):
    array = np.array(timings)
    return np.percentile(array, percentile)
