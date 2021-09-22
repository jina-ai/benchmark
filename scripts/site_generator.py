#!/usr/bin/python3

import json
import os
import copy
from collections import defaultdict
from distutils.version import LooseVersion
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union, Optional


COLOR_VALUES = [
    '#10a100',
    '#7ead14',
    '#bab73c',
    '#e8c268',
    '#e59838',
    '#e36717',
    '#de1414',
]

COLOR_NAN = '#9b00a1'

NOT_A_NUMBER = 'N/A'

STD_MEAN_THRESHOLD = 0.5

COLOR_LEGEND = ' | '.join(
    [
        f'<span style="color:{color};">{i*10} - {(i+1)*10}%</span>'
        for i, color in enumerate(COLOR_VALUES)
    ]
)

LEGEND = f"""
The following data should be read as follows:

- Colors of cells display the percentage of the minimum value in the column:\n
  {COLOR_LEGEND}
- <s>1337</s>: unstable tests with "standard deviation / mean > {STD_MEAN_THRESHOLD}"
"""


def _format(data: Union[int, float]) -> Any:
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


def _get_color(mean_time, master_mean_time):
    if mean_time is None or mean_time == NOT_A_NUMBER or master_mean_time == 0:
        return COLOR_NAN
    raw_bucket = int((float(mean_time) / float(master_mean_time) - 1) * 10)
    bucket = max(0, min(6, raw_bucket))

    return COLOR_VALUES[bucket]


def _get_cleaned_mean_time(time: Optional[int], scaling: int) -> str:
    """Return cleaned data"""

    if time is not None:
        return str(int(int(time) / scaling))
    else:
        return NOT_A_NUMBER


def _cleaned_title(raw_heading: str) -> str:
    """Return cleaned title of artifact name."""
    return raw_heading.replace('test_', '').replace('_', ' ').title()


def is_test_unstable(run_stats):
    mean = run_stats.get('mean_time', 1e20)
    return mean != 0 and run_stats.get('std_time', 0.0) / mean > STD_MEAN_THRESHOLD


def _get_table_header(raw_data: List[Dict[str, Any]]) -> Tuple[str, str]:
    """Return metadata table title and table separator."""
    titles = {}
    for test_run in raw_data:
        for name in test_run['metadata']:
            titles[name] = []
        break
    separators = []
    for result in raw_data:
        separators.append('---:')
        for field in titles:
            if 'metadata' in result:
                value = result['metadata'].get(field, 'N/A')
                titles[field].append(f'**{value}**')

            else:
                titles[field].append('**N/A**')
    final = []
    for title, values in titles.items():
        final.append(f'| **{title}** | {" | ".join(values)} |\n')
    header = f'{final[0]}| :---: | {" | ".join(separators)} |\n{"".join(final[1:])}'
    return header


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

    version_list = [sorted_dev[i - 1] for i in range(len(sorted_dev), 0, -1)]

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
                page = i.get('page', 'unsorted_tests')
                test_name = i['name']
                metadata_hash = _hash_run(i)

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


def _hash_run(d):
    tmp_dict = copy.deepcopy(d)
    tmp_dict.pop('mean_time', None)
    tmp_dict.pop('std_time', None)
    tmp_dict.pop('iterations', None)
    tmp_dict.pop('results', None)

    return json.dumps(tmp_dict, sort_keys=True)


def _get_stats(test_data, latest_version):
    results = defaultdict(dict)
    for version, test_results in test_data.items():
        for test_result in test_results.values():
            parameter_hash = _hash_run(test_result)
            metadata = test_result.get('metadata', {})
            if not metadata:
                metadata = {'name': test_result['name']}
            results[parameter_hash]['metadata'] = metadata

            results[parameter_hash]['min'] = min(
                results[parameter_hash].get('min', 1e20), test_result['mean_time']
            )
            results[parameter_hash]['max'] = max(
                results[parameter_hash].get('max', 0), test_result['mean_time']
            )
            results[parameter_hash]['parameter_hash'] = parameter_hash

            if version == latest_version:
                results[parameter_hash]['last_version_mean'] = test_result['mean_time']

    stats = list(results.values())
    _add_scaling(stats)
    return stats


def _get_one_version_stats(test_results):
    results = defaultdict(lambda x: 1e20)
    results['min_mean_docs_per_sec'] = 0

    for test in test_results:
        results['min_time'] = min(results['min_time'], test['mean_time'])
        results['min_memory'] = min(results['min_memory'], test['mean_memory'])
        results['min_indexer_memory'] = min(
            results['min_indexer_memory'], test['mean_indexer_memory']
        )
        results['min_mean_docs_per_sec'] = max(
            results['min_mean_docs_per_sec'], test['mean_mean_docs_per_sec']
        )
        results['min_latency'] = min(results['min_latency'], test['mean_latency'])

    return results


def _add_scaling(stats):
    for run_stats in stats:
        if run_stats['min'] > 10_000_000_000:
            run_stats['scaling'] = 1_000_000_000
            run_stats['metadata']['unit'] = 's'
        if run_stats['min'] > 10_000_000:
            run_stats['scaling'] = 1_000_000
            run_stats['metadata']['unit'] = 'ms'
        elif run_stats['min'] > 10_000:
            run_stats['scaling'] = 1_000
            run_stats['metadata']['unit'] = 'μs'
        else:
            run_stats['scaling'] = 1
            run_stats['metadata']['unit'] = 'ns'
        run_stats['min'] = int(run_stats['min'] / run_stats['scaling'])
        run_stats['max'] = int(run_stats['max'] / run_stats['scaling'])


def generate_docs(
    version_list: List[str], cum_data: Dict[Any, Any], output_dir: str
) -> None:
    """This generate required docs from artifacts.

    Args:
        version_list: List of versions found in reports.
        cum_data: Cumulative data in Dict.
        output_dir: Absolute path to Hugo docs directory.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for page, page_data in cum_data.items():
        output_file = os.path.join(output_dir, f'{page}.md')
        if page == 'indexer_comparison':
            generate_comparison_test(page_data, output_file, _cleaned_title(page))
        else:
            generate_versioned_test(page_data, output_file, _cleaned_title(page))


def _get_last_version(single_test_data):
    versions = list(single_test_data.keys())
    if versions:
        return max(versions)
    else:
        return None


def generate_versioned_test(page_data, output_file, title):
    with open(output_file, 'w') as fp:
        fp.write('---\n')
        fp.write(f'title: {title}\n')
        fp.write('---\n')
        fp.write(f'# {title}\n\n')

        fp.write(f'{LEGEND}\n')

        for test_name, single_test_data in page_data.items():
            latest_version = _get_last_version(single_test_data)

            if latest_version is None:
                return

            stats = _get_stats(single_test_data, latest_version)
            header = _get_table_header(stats)

            fp.write(f'## {_cleaned_title(test_name)}\n')
            fp.write(header)

            for version, data_dict in single_test_data.items():
                fp.write(f'| {version} |')
                for run in stats:
                    run_data = data_dict[run['parameter_hash']]

                    mean_time = _get_cleaned_mean_time(
                        run_data.get('mean_time', None), run['scaling']
                    )
                    color = _get_color(mean_time, run['min'])

                    if is_test_unstable(run_data):
                        mean_time = f'<s>{mean_time}</s>'

                    fp.write(f' <span style="color:{color};">{mean_time}</span> |')
                fp.write('\n')
            fp.write('\n')


def generate_comparison_test(page_data, output_file, title):
    with open(output_file, 'w') as fp:
        fp.write('---\n')
        fp.write(f'title: {title}\n')
        fp.write('---\n')
        fp.write(f'# {title}\n\n')

        for test_name, single_test_data in page_data.items():
            latest_version = _get_last_version(single_test_data)

            if latest_version is None:
                continue

            table = []

            test_data = single_test_data[latest_version]

            header = _get_table_header(list(test_data.values()))

            fp.write(f'## {_cleaned_title(test_name)}\n')
            fp.write(f'Tests were performed against Jina {latest_version}.\n\n')
            fp.write(header)

            table.append(
                [
                    'index time in ms',
                    'search time in ms',
                    'index memory',
                    'search memory',
                    'p90 in ms',
                    'p99 in ms',
                    'RPS',
                    'Documents per second',
                ]
            )

            for run in test_data.values():

                table.append(
                    [
                        _get_cleaned_mean_time(run['results']['mean_index_time'], 1e6),
                        _get_cleaned_mean_time(run['results']['mean_search_time'], 1e6),
                        get_readable_size(run['results']['mean_search_memory']),
                        get_readable_size(run['results']['mean_index_memory']),
                        _get_cleaned_mean_time(run['results']['p90'], 1e6),
                        _get_cleaned_mean_time(run['results']['p99'], 1e6),
                        get_rps(run),
                        get_dps(run),
                    ]
                )

            transposed = list(map(list, zip(*table)))

            fp.write('|\n|'.join(' | '.join(row) for row in transposed))
            fp.write('\n\n')


def get_dps(run):
    total_docs = run['metadata']['docs_per_request'] * run['metadata']['num_requests']
    dps = total_docs / (run['results']['mean_search_time'] / 1e9)
    return f'{dps:.2f}'


def get_rps(run):
    rps = run['metadata']['num_requests'] / (run['results']['mean_search_time'] / 1e9)
    return f'{rps:.2f}'


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
