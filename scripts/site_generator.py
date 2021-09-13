#!/usr/bin/python3

import json
import os
import copy
from collections import defaultdict
from distutils.version import LooseVersion
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union


COLOR_VALUES = [
    '#88cf96',
    '#a4d2ac',
    '#bed5c1',
    '#d7d7d7',
    '#dcbfbe',
    '#dea7a6',
    '#de8e8e',
]

COLOR_NAN = '#8483a7'

NOT_A_NUMBER = 'N/A'


def __format(data: Union[int, float]) -> Any:
    if isinstance(data, bool):
        return str(data)
    elif isinstance(data, int) or isinstance(data, float):
        if data >= 1000:
            _data = data
            i = 0
            while abs(_data) >= 1000:
                i += 1
                _data /= 1000

            if isinstance(data, int):
                return '%d%s' % (_data, ['', 'K', 'M', 'G', 'T', 'P'][i])
            else:
                return '%.2f%s' % (_data, ['', 'K', 'M', 'G', 'T', 'P'][i])
        else:
            i = 1
            _data = round(data, i)
            while _data == 0 and i <= 5:
                i += 1
                _data = round(data, i)

            return _data
    else:
        return data


def _get_delta(mean_time: float, master_mean_time: float) -> str:
    try:
        delta = (1 - (float(mean_time) / float(master_mean_time))) * 100
        delta_string = f"{delta:+7.2f}%".replace(' ', '&nbsp;&nbsp;')
        if delta < 0:
            delta_string = '&nbsp;' + delta_string
        return delta_string
    except:
        return NOT_A_NUMBER


def _get_background(mean_time, master_mean_time):
    if mean_time is None or mean_time == NOT_A_NUMBER or master_mean_time == 0:
        return COLOR_NAN
    raw_bucket = int((float(mean_time) / float(master_mean_time) - 1) * 10)
    bucket = max(0, min(6, raw_bucket))

    return COLOR_VALUES[bucket]


def _get_cleaned_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Return cleaned data"""

    cleaned_data = dict()

    cleaned_data['mean_time'] = (
        f'{float(data["mean_time"]):7.2f}'
        if data.get('mean_time', None)
        else NOT_A_NUMBER
    )
    cleaned_data['std_time'] = (
        f'{float(data["std_time"]):5.2f}'
        if data.get('std_time', None)
        else '&nbsp;&nbsp;&nbsp;N/A'
    )
    cleaned_data['metadata'] = data.get('metadata', None)
    cleaned_data['iterations'] = __format(data.get('iterations', NOT_A_NUMBER))

    return cleaned_data


def _cleaned_title(raw_heading: str) -> str:
    """Return cleaned title of artifact name."""
    return raw_heading.replace('test_', '').replace('_', ' ').title()


def _get_metadata_titles(raw_data: List[Dict[str, Any]]) -> Tuple[str, str]:
    """Return metadata table title and table separator."""
    titles = []
    separators = []
    for result in raw_data:
        if 'metadata' in result:
            formatted_metadata = [
                f'{parameter}: {value}'
                for parameter, value in result['metadata'].items()
            ]
            content = '<br>'.join(formatted_metadata)

            titles.append(f'<span style="font-size:0.6em;">{content}</span>')
            separators.append('---:')

        else:
            titles.append(result['name'])
            separators.append('---:')
    return ' | '.join(titles), ' | '.join(separators)


def __get_metadata_values(metadata: Dict[str, Any]) -> str:
    """Return metadata table values."""
    if metadata:
        values = ' | '.join(str(__format(v)) for v in metadata.values())
        return values
    else:
        return NOT_A_NUMBER


def _get_version_list(artifacts_dir: str) -> List[str]:
    """Generates sorted list of all versions found in reports.

    Args:
        artifacts_dir: Absolute path to artifact directory.

    Return: List of versions found in reports.
    """
    lv = []

    for folder in os.listdir(artifacts_dir):
        if os.path.isfile(os.path.join(artifacts_dir, folder, 'report.json')):
            lv.append(LooseVersion(folder))

    lv.sort()
    sorted_dev = [v.vstring for v in lv]

    import re

    p = re.compile('dev\\d+$')

    i = 0
    while i + 1 < len(sorted_dev):
        tmp = sorted_dev[i]
        m = p.search(sorted_dev[i + 1])
        if m and sorted_dev[i + 1].startswith(tmp):
            sorted_dev[i] = sorted_dev[i + 1]
            sorted_dev[i + 1] = tmp
        i += 1

    version_list = [sorted_dev[i - 1] for i in range(len(sorted_dev), 1, -1)]

    return version_list


def _get_cum_data(version_list: List[str], artifacts_dir: str) -> Dict[Any, Any]:
    """Generates cumulative data and return in a dict.

    Args:
        version_list: List of versions found in reports.
        artifacts_dir: Absolute path to artifact directory.

    Return: Dict of cumulative data
    """
    data: Dict[Any, Any] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    )

    for version in version_list:
        report_file = os.path.join(artifacts_dir, version, 'report.json')
        searchers_compare_file = os.path.join(
            artifacts_dir, version, 'searchers_compare.json'
        )

        if os.path.isfile(report_file):
            with open(report_file) as fp:
                _raw_data = json.load(fp)

            if os.path.isfile(searchers_compare_file):
                with open(searchers_compare_file) as fp:
                    _raw_data.extend(json.load(fp))

            for i in _raw_data:
                page = i['page']
                test_name = i['name']
                metadata_hash = hash_run(i)

                data[page][test_name][version][metadata_hash] = i

    return data


def generate_homepage(output_dir: str) -> None:
    """This generate required homepage for the website.

    Args:
        output_dir: Absolute path to Hugo content directory.
    """
    src = os.path.join(os.getcwd(), 'README.md')
    dst = os.path.join(output_dir, '_index.md')
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if os.path.isfile(src):
        with open(src) as f:
            data = f.read()

        with open(dst, 'w') as fp:
            fp.write('---\n')
            fp.write('title: Benchmark Jina\n')
            fp.write('type: docs\n')
            fp.write('---\n')
            fp.write(data)


def hash_run(d):
    tmp_dict = copy.deepcopy(d)
    del tmp_dict['mean_time']
    del tmp_dict['std_time']

    return json.dumps(tmp_dict, sort_keys=True)


def _get_stats(test_data, last_benchmarked_version):
    results = defaultdict(dict)
    for version, test_results in test_data.items():
        for test_result in test_results.values():
            if 'metadata' in test_result:
                parameter_hash = hash_run(test_result)
                results[parameter_hash]['min'] = min(
                    results[parameter_hash].get('min', 1e10), test_result['mean_time']
                )
                results[parameter_hash]['max'] = max(
                    results[parameter_hash].get('max', 0), test_result['mean_time']
                )
                results[parameter_hash]['metadata'] = test_result['metadata']
                results[parameter_hash]['parameter_hash'] = parameter_hash

                if version == last_benchmarked_version:
                    results[parameter_hash]['last_version_mean'] = test_result[
                        'mean_time'
                    ]

    return list(results.values())


def get_header_entry(metadata):
    paramater_strings = [
        f'{parameter}: {value}' for parameter, value in metadata.items()
    ]
    return '<br>'.join(paramater_strings)


def generate_docs(
    version_list: List[str], cum_data: Dict[Any, Any], output_dir: str
) -> None:
    """This generate required docs from artifacts.

    Args:
        version_list: List of versions found in reports.
        cum_data: Cumulative data in Dict.
        output_dir: Absolute path to Hugo docs directory.
    """
    last_benchmarked_version: str = version_list[0]
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for page in cum_data:
        output_file = os.path.join(output_dir, f'{page}.md')

        with open(output_file, 'w') as fp:
            fp.write('---\n')
            fp.write(f'title: {_cleaned_title(page)}\n')
            fp.write('---\n')
            fp.write(f'# {_cleaned_title(page)}\n\n')

            for test_name, single_test_data in cum_data[page].items():
                stats = _get_stats(single_test_data, last_benchmarked_version)

                title, separator = _get_metadata_titles(stats)

                fp.write(f'## {_cleaned_title(test_name)}\n\n')
                fp.write(f'| Version | {title} |\n')
                fp.write(f'| :---: | {separator} |\n')

                for version, data_dict in single_test_data.items():
                    fp.write(f'| {version} |')
                    for run in stats:
                        run_hash = run['parameter_hash']
                        _data_point = _get_cleaned_data(data_dict[run_hash])

                        wrt_mean_time = run.get('last_version_mean', 100)
                        delta = _get_delta(
                            _data_point.get('mean_time', None), wrt_mean_time
                        )
                        mean_time = _data_point["mean_time"].replace(
                            ' ', '&nbsp;&nbsp;'
                        )
                        std_time = _data_point["std_time"].replace(' ', '&nbsp;&nbsp;')
                        background_color = _get_background(
                            _data_point.get('mean_time', None), run['min']
                        )
                        fp.write(
                            f' <span style="background-color:{background_color};">{mean_time} ± {std_time}</span> |'
                        )
                    fp.write('\n')
                fp.write('\n')


def generate_menus(cum_data: Dict[Any, Any], output_dir: str) -> None:
    """This generate required menus from artifacts.

    Args:
        cum_data: Cumulative data in Dict.
        output_dir: Absolute path to Hugo menus directory.
    """
    menu_dir = os.path.join(output_dir, 'menu')
    menu_index = os.path.join(menu_dir, 'index.md')
    Path(menu_dir).mkdir(parents=True, exist_ok=True)

    with open(menu_index, 'w') as fp:
        fp.write('---\n')
        fp.write('headless: true\n')
        fp.write('---\n\n')

        for page in cum_data:
            fp.write(
                '- [%s]({{< relref "/docs/%s.md" >}})\n' % (_cleaned_title(page), page)
            )


def main():
    """This is the main function to call."""
    base_dir = os.path.join(os.getcwd(), 'docs')
    content_dir = os.path.join(base_dir, 'content')
    docs_dir = os.path.join(content_dir, 'docs')
    artifacts_dir = os.path.join(base_dir, 'static/artifacts')

    version_list = _get_version_list(artifacts_dir)
    cum_data = _get_cum_data(version_list, artifacts_dir)

    generate_homepage(content_dir)
    generate_docs(version_list, cum_data, docs_dir)
    generate_menus(cum_data, content_dir)


if __name__ == '__main__':
    main()
