import json
import os

import pytest
from jina import __version__


def pytest_addoption(parser):
    parser.addoption('--output-file', action='store', default='report.json')


class ResultsCollector:
    def __init__(self):
        self.results = []

    def get_test_name():
        test = os.environ['PYTEST_CURRENT_TEST']
        removed_head = test.split('::')[-1]
        return removed_head.split('[')[0].split(' (')[0]

    def append(self, page, result, metadata=None, name=None):
        if metadata is None:
            metadata = {}

        if name is None:
            name = ResultsCollector.get_test_name()

        self.results.append(
            dict(
                name=name,
                page=page,
                iterations=result.iterations,
                mean_time=result.mean,
                std_time=result.std,
                metadata=metadata,
            )
        )

    def dump(self, filename):
        with open(filename, 'w+') as file:
            json.dump(self.results, file)


@pytest.fixture(scope='session')
def json_writer(pytestconfig):
    collector = ResultsCollector()
    yield collector

    from os import environ
    from pathlib import Path

    version = environ.get('JINA_VERSION', __version__)

    if version == 'master':
        version = __version__
    elif version.startswith('v'):
        version = version[1:]

    output_dir = f'docs/static/artifacts/{version}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    file_name = pytestconfig.getoption('output_file')

    collector.dump(f'{output_dir}/{file_name}')


@pytest.fixture()
def ephemeral_tmpdir(tmpdir):
    yield tmpdir

    import shutil

    shutil.rmtree(str(tmpdir))


@pytest.fixture()
def name():
    test = os.environ['PYTEST_CURRENT_TEST']
    removed_head = test.split('::')[-1]
    removed_tail = removed_head.split('[')[0].split(' (')[0]

    return removed_tail
