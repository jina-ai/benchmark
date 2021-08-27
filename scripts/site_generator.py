#!/usr/bin/python3

import json
import os
from typing import Any, Dict, List, Tuple

from packaging.version import parse


def __get_delta(mean_time: float, master_mean_time: float) -> str:
    try:
        delta = (1 - (mean_time / master_mean_time)) * 100

        if delta > 0:
            return f"+{round(delta, 2)}%"
        else:
            return f"{round(delta, 2)}%"

    except ZeroDivisionError:
        return "N/A"


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
    version_list: List[str] = []

    for folder in os.listdir(artifacts_dir):
        if os.path.isfile(os.path.join(artifacts_dir, folder, 'report.json')):
            version_list.append(folder)

    version_list.sort(
        key=lambda s: [int(u.replace('dev', '')) for u in s.split('.')], reverse=True
    )

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
        if os.path.isfile(report_file):
            with open(report_file) as fp:
                _raw_data = json.load(fp)

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

    def _convert_to_unit(time, time_unit, target_unit):
        if time_unit == target_unit:
            return time
        else:
            if time_unit == 's' and target_unit == 'ms':
                return time * 1000
            elif time_unit == 'ms' and target_unit == 's':
                return time / 1000

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

                mean_time_unit_by_version = {}
                common_unit = 's'
                for version, data in cum_data[k][v].items():
                    version_unit = data.get('unit', 's')
                    common_unit = version_unit if version_unit == 'ms' else common_unit
                    mean_time_unit_by_version[version] = {
                        'unit': data.get('unit', 's'),
                        'time': data['mean_time'],
                    }  # default to 's' because previously it was all 's'

                for version, data in cum_data[k][v].items():
                    version_unit = data.get('unit', 's')
                    data['mean_time'] = _convert_to_unit(
                        data['mean_time'], version_unit, common_unit
                    )
                    data['std_time'] = _convert_to_unit(
                        data['std_time'], version_unit, common_unit
                    )

                report_unit = common_unit
                fp.write(f'## {_cleaned_title(v)}\n\n')
                fp.write(
                    f'| Version | Mean Time ({report_unit}) | Std Time ({report_unit}) | Delta w.r.t. {last_benchmarked_version} | {title} | Iterations |\n'
                )
                fp.write(f'| :---: | :---: | :---: | :---: | {separator} | :---: |\n')

                for version, _data in cum_data[k][v].items():
                    std_time = _data['std_time']
                    mean_time = _data['mean_time']
                    wrt_mean_time = cum_data[k][v][last_benchmarked_version][
                        'mean_time'
                    ]

                    fp.write(
                        f'| {version} | {round(mean_time, 2)} | {round(std_time, 2)} | {__get_delta(mean_time, wrt_mean_time)} | {__get_metadata_values(_data)} | {_data["iterations"]} |\n'
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
