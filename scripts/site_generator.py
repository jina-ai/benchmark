#!/usr/bin/python3

import json
import os
from distutils.version import LooseVersion
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union


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


def __get_delta(mean_time: float, master_mean_time: float) -> str:
    try:
        delta = (1 - (float(mean_time) / float(master_mean_time))) * 100

        if delta > 0:
            return f"+{__format(delta)}%"
        else:
            return f"{__format(delta)}%"

    except:
        return "N/A"


def __get_cleaned_data_list(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return cleaned data"""
    cleaned_data_list: List[Dict[str, Any]] = []

    for data in data_list:
        cleaned_data = dict()

        cleaned_data['mean_time'] = (
            __format(data['mean_time']) if data.get('mean_time', None) else 'N/A'
        )
        cleaned_data['std_time'] = (
            __format(data['std_time']) if data.get('std_time', None) else 'N/A'
        )
        cleaned_data['metadata'] = data.get('metadata', None)
        cleaned_data['iterations'] = __format(data.get('iterations', 'N/A'))

        cleaned_data_list.append(cleaned_data)

    return cleaned_data_list


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


def __get_metadata_values(metadata: Dict[str, Any]) -> str:
    """Return metadata table values."""
    if metadata:
        values = ' | '.join(str(__format(v)) for v in metadata.values())
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
                        if version in data[k][v]:
                            temp = data[k][v][version]
                            temp.append(i)
                            data[k][v][version] = temp
                        else:
                            data[k][v][version] = [i]
                    else:
                        data[k][v] = {version: [i]}
                else:
                    data[k] = {v: {version: [i]}}

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

    for k in cum_data:
        output_file = os.path.join(output_dir, f'{_cleaned_slug(k)}.md')

        with open(output_file, 'w') as fp:
            fp.write('---\n')
            fp.write(f'title: {_cleaned_title(k)}\n')
            fp.write('---\n')
            fp.write(f'# {_cleaned_title(k)}\n\n')

            for v in cum_data[k]:
                title, separator = __get_metadata_titles(
                    cum_data[k][v][last_benchmarked_version][0]
                )

                fp.write(f'## {_cleaned_title(v)}\n\n')
                fp.write(
                    f'| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. {last_benchmarked_version} | {title} | Iterations |\n'
                )
                fp.write(f'| :---: | :---: | :---: | :---: | {separator} | :---: |\n')

                for version, _data_list in cum_data[k][v].items():
                    _data_list = __get_cleaned_data_list(_data_list)

                    for _data in _data_list:
                        try:
                            for lbv_data in cum_data[k][v][last_benchmarked_version]:
                                if (
                                    lbv_data['metadata'] == _data['metadata']
                                    and lbv_data['iterations'] == _data['iterations']
                                ):
                                    wrt_mean_time = lbv_data['mean_time']
                                    break
                        except KeyError:
                            wrt_mean_time = None

                        delta = __get_delta(_data.get('mean_time', None), wrt_mean_time)
                        metadata_values = __get_metadata_values(
                            _data.get('metadata', None)
                        )

                        fp.write(
                            f'| {version} | {_data["mean_time"]} | {_data["std_time"]} | {delta} | {metadata_values} | {_data["iterations"]} |\n'
                        )


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
