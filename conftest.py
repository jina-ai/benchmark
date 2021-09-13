import json
import os

import pytest
from jina import __version__


def pytest_addoption(parser):
    parser.addoption("--output-file", action="store", default="report.json")


@pytest.fixture(scope='session')
def json_writer(pytestconfig):
    results = []
    yield results

    from os import environ
    from pathlib import Path

    version = environ.get('JINA_VERSION', __version__)

    if version == 'master':
        version = __version__
    elif version.startswith('v'):
        version = version[1:]

    output_dir = f'docs/static/artifacts/{version}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    file_name = pytestconfig.getoption("output_file")
    with open(f'{output_dir}/{file_name}', 'w+') as file:
        json.dump(results, file)


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
