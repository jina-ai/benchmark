#!/usr/bin/python3

import json
import os
from distutils.version import LooseVersion
from typing import Any, Dict, List, Tuple


def __get_delta(mean_time: float, master_mean_time: float) -> str:
    try:
        delta = (1 - (mean_time / master_mean_time)) * 100

        if delta > 0:
            return f"+{round(delta, 2)}%"
        else:
            return f"{round(delta, 2)}%"

    except:
        return "N/A"


def __get_cleaned_data(data: Dict[str, Any], wrt_mean_time: float) -> Dict[str, Any]:
    """Return cleaned data"""
    cleaned_data: Dict[str, Any] = dict()

    cleaned_data['mean_time'] = (
        round(data['mean_time'], 2) if data.get('mean_time', None) else 'N/A'
    )
    cleaned_data['std_time'] = (
        round(data['std_time'], 2) if data.get('std_time', None) else 'N/A'
    )
    cleaned_data['delta'] = __get_delta(data.get('mean_time', None), wrt_mean_time)
    cleaned_data['metadata_values'] = __get_metadata_values(data)
    cleaned_data['iterations'] = data.get('iterations', 'N/A')

    return cleaned_data


def _cleaned_title(raw_heading: str) -> str:
    """Return cleaned title of artifact name."""
    return raw_heading.replace('test_', '').replace('_', ' ').title()


def _cleaned_slug(raw_heading: str) -> str:
    """Return cleaned slug of artifact name."""
    return raw_heading.replace('test_', '').replace('_', '-')


def __get_metadata_titles(raw_data: Dict[str, Any]) -> Tuple[str, str]:
    """Return metadata table title and table separator."""
    if 'metadata' in raw_data:
        _keys = raw_data['metadata'].keys()
        title = ' | '.join(_cleaned_title(k) for k in _keys)
        separator = ' | '.join([':---:'] * len(_keys))
        return title, separator
    else:
        return 'Metadata', ':---:'


def __get_metadata_values(raw_data: Dict[str, Any]) -> str:
    """Return metadata table values."""
    if 'metadata' in raw_data:
        values = ' | '.join(str(v) for v in raw_data['metadata'].values())
        return values
    else:
        return 'N/A'


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
    data: Dict[Any, Any] = dict()

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
                k, v = i['name'].split('/')
                if k in data:
                    if v in data[k]:
                        data[k][v][version] = i
                    else:
                        data[k][v] = {version: i}
                else:
                    data[k] = {v: {version: i}}

    return data


def generate_homepage(output_dir: str) -> None:
    """This generate required homepage for the website.

    Args:
        output_dir: Absolute path to Hugo content directory.
    """
    src = os.path.join(os.getcwd(), 'README.md')
    dst = os.path.join(output_dir, '_index.md')

    if os.path.isfile(src):
        with open(src) as f:
            data = f.read()

        with open(dst, 'w') as fp:
            fp.write('---\n')
            fp.write('title: Benchmark Jina\n')
            fp.write('type: docs\n')
            fp.write('---\n')
            fp.write(data)


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

    for k in cum_data:
        output_file = os.path.join(output_dir, f'{_cleaned_slug(k)}.md')

        with open(output_file, 'w') as fp:
            fp.write('---\n')
            fp.write(f'title: {_cleaned_title(k)}\n')
            fp.write('---\n')
            fp.write(f'# {_cleaned_title(k)}\n\n')

            for v in cum_data[k]:
                title, separator = __get_metadata_titles(
                    list(cum_data[k][v].values())[0]
                )

                fp.write(f'## {_cleaned_title(v)}\n\n')
                fp.write(
                    f'| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. {last_benchmarked_version} | {title} | Iterations |\n'
                )
                fp.write(f'| :---: | :---: | :---: | :---: | {separator} | :---: |\n')

                for version, _data in cum_data[k][v].items():
                    try:
                        wrt_mean_time = cum_data[k][v][last_benchmarked_version][
                            'mean_time'
                        ]
                    except KeyError:
                        wrt_mean_time = None

                    _data = __get_cleaned_data(_data, wrt_mean_time)

                    fp.write(
                        f'| {version} | {_data["mean_time"]} | {_data["std_time"]} | {_data["delta"]} | {_data["metadata_values"]} | {_data["iterations"]} |\n'
                    )


def generate_menus(cum_data: Dict[Any, Any], output_dir: str) -> None:
    """This generate required menus from artifacts.

    Args:
        cum_data: Cumulative data in Dict.
        output_dir: Absolute path to Hugo menus directory.
    """
    menu_index = os.path.join(output_dir, 'menu/index.md')

    with open(menu_index, 'w') as fp:
        fp.write('---\n')
        fp.write('headless: true\n')
        fp.write('---\n\n')

        for k in cum_data:
            fp.write(
                '- [%s]({{< relref "/docs/%s.md" >}})\n'
                % (_cleaned_title(k), _cleaned_slug(k))
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
