import numpy as np
import pytest
from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap

from .utils.benchmark import benchmark_time
from .pages import Pages

NUM_REPETITIONS = 10


@pytest.mark.parametrize(
    'num_docs,num_feat', [(100, 128), (10_000, 128), (10_000, 256)]
)
def test_da_embeddings(name, num_docs, num_feat, json_writer):
    def _setup():
        da = DocumentArray(
            [Document(embedding=np.random.random(num_feat)) for i in range(num_docs)]
        )
        return (), dict(da=da)

    def _da_embeddings(da):
        embeddings = da.embeddings

    mean_time, std_time = benchmark_time(
        setup=_setup,
        func=_da_embeddings,
        n=NUM_REPETITIONS,
    )

    json_writer.append(
        dict(
            name=name,
            page=Pages.DA_GET_ATTRIBUTES,
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs, num_feat=num_feat),
        )
    )


@pytest.mark.parametrize(
    'num_docs,num_feat', [(100, 128), (10_000, 128), (10_000, 256)]
)
def test_dam_embeddings(name, num_docs, num_feat, json_writer, ephemeral_tmpdir):
    def _setup():
        dam = DocumentArrayMemmap((f'{str(ephemeral_tmpdir)}/memmap'))
        dam.extend(
            [Document(embedding=np.random.rand(num_feat)) for i in range(num_docs)]
        )
        return (), dict(dam=dam)

    def _dam_clear(dam):
        dam.clear()

    def _teardown():
        import shutil

        shutil.rmtree(f'{str(ephemeral_tmpdir)}/memmap')

    mean_time, std_time = benchmark_time(
        setup=_setup,
        func=_dam_clear,
        teardown=_teardown,
        n=NUM_REPETITIONS,
    )

    json_writer.append(
        dict(
            name=name,
            page=Pages.DA_GET_ATTRIBUTES,
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(num_docs=num_docs, num_feat=num_feat),
        )
    )
