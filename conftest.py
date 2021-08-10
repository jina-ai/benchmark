import json

import pytest


def pytest_addoption(parser):
    parser.addoption("--output-file", action="store", default="report.json")


@pytest.fixture(scope='session')
def json_writer(pytestconfig):
    results = []
    yield results

    file_name = pytestconfig.getoption("output_file")
    with open(file_name, 'w+') as file:
        json.dump(results, file)
