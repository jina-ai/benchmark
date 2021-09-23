import json
import os
from pathlib import Path

from collections import defaultdict

import pytest
from jina import __version__


def pytest_addoption(parser):
    parser.addoption('--output-file', action='store', default='report.json')


class ResultsCollector:
    def __init__(self, output_dir, default_filename):
        self.results = defaultdict(list)
        self.output_dir = output_dir
        self.default_filename = default_filename

    def get_test_name():
        test = os.environ['PYTEST_CURRENT_TEST']
        removed_head = test.split('::')[-1]
        return removed_head.split('[')[0].split(' (')[0]

    def append(self, page, result, metadata=None, name=None, target_file=None):
        if metadata is None:
            metadata = {}

        if name is None:
            name = ResultsCollector.get_test_name()
        if target_file is None:
            target_file = self.default_filename

        self.results[target_file].append(
            dict(
                name=name,
                page=page,
                iterations=result.iterations,
                mean_time=result.mean,
                std_time=result.std,
                metadata=metadata,
            )
        )

    def append_raw(self, dict_, target_file=None):
        if target_file is None:
            target_file = self.default_filename

        self.results[target_file].append(dict_)
        return self.results[target_file]

    def dump(self):
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        for filename, content in self.results.items():
            file_path = f'{self.output_dir}/{filename}'
            with open(file_path, 'w+') as file:
                json.dump(content, file)


@pytest.fixture(scope='session')
def json_writer(pytestconfig):
    version = os.environ.get('JINA_VERSION', __version__)

    if version == 'master':
        version = __version__
    elif version.startswith('v'):
        version = version[1:]
    output_dir = f'docs/static/artifacts/{version}'

    collector = ResultsCollector(output_dir, pytestconfig.getoption('output_file'))
    yield collector

    collector.dump()


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
