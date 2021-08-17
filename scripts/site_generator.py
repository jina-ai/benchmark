#!/usr/bin/python3

import json
import os
from typing import Any, Dict, List, Tuple

import requests
from packaging.version import parse


def __get_latest_version(owner: str, repo: str) -> str:
    """Return latest released version of Jina Core."""
    res = requests.get(
        "https://api.github.com/repos/{}/{}/releases/latest".format(owner, repo)
    )
    res_data = res.json()

    return res_data["tag_name"].replace('v', '')


def __get_delta(mean_time: float, master_mean_time: float) -> str:
    delta = (1 - (mean_time / master_mean_time)) * 100

    if delta > 0:
        return "+{}%".format(round(delta, 2))
    else:
        return "{}%".format(round(delta, 2))


def _cleaned_title(raw_heading: str) -> str:
    """Return cleaned title of artifact name."""
    return raw_heading.replace('test_', '').replace('_', ' ').title()


def _cleaned_slug(raw_heading: str) -> str:
    """Return cleaned slug of artifact name."""
    return raw_heading.replace('test_', '').replace('_', '-')


def _get_metadata_items(raw_metadata: Dict[str, Any]) -> Tuple[str, str]:
    """Return metadata table title and table separator."""
    _keys = raw_metadata.keys()
    title = ' | '.join(_cleaned_title(k) for k in _keys)
    separator = ' | '.join([':---:'] * len(_keys))
    return title, separator


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

    version_list.sort(key=lambda s: [int(u) for u in s.split('.')], reverse=True)

    return version_list


def _get_cum_data(version_list: List[str], artifacts_dir: str) -> Dict[Any, Any]:
    """Generates cumulative data and return in a dict.

    Args:
        version_list: List of versions found in reports.
        artifacts_dir: Absolute path to artifact directory.

    Return: Dict of cumulative data
    """
    data: Dict[Any, Any] = dict()
    latest_version = __get_latest_version('jina-ai', 'jina')

    for version in version_list:
        report_file = os.path.join(artifacts_dir, version, 'report.json')
        if os.path.isfile(report_file):
            with open(report_file) as fp:
                _raw_data = json.load(fp)

            if version_list.index(version) == 0 and parse(version) >= parse(
                latest_version
            ):
                version = 'master'

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


def generate_docs(cum_data: Dict[Any, Any], output_dir: str) -> None:
    """This generate required docs from artifacts.

    Args:
        cum_data: Cumulative data in Dict.
        output_dir: Absolute path to Hugo docs directory.
    """
    for k in cum_data:
        output_file = os.path.join(output_dir, '{}.md'.format(_cleaned_slug(k)))

        with open(output_file, 'w') as fp:
            fp.write('---\n')
            fp.write('title: {}\n'.format(_cleaned_title(k)))
            fp.write('---\n')
            fp.write('# {}\n\n'.format(_cleaned_title(k)))

            for v in cum_data[k]:
                raw_metadata = list(cum_data[k][v].values())[0]['metadata']
                title, separator = _get_metadata_items(raw_metadata)

                first_mean_time = cum_data[k][v][list(cum_data[k][v].keys())[0]][
                    'mean_time'
                ]
                report_unit = 's' if first_mean_time > 1000 else 'ms'
                fp.write('## {}\n\n'.format(_cleaned_title(v)))
                fp.write(
                    f'| Version | Mean Time ({report_unit}) | Std Time ({report_unit}) | Delta w.r.t. master | {title} | Iterations |\n'
                )
                fp.write(
                    '| :---: | :---: | :---: | :---: | {} | :---: |\n'.format(separator)
                )

                for version in cum_data[k][v]:
                    _data = cum_data[k][v][version]
                    mean_time = _data['mean_time']
                    std_time = _data['std_time']
                    if report_unit == 's':
                        mean_time = mean_time // 1000
                        std_time = std_time // 1000

                    fp.write(
                        '| {} | {} | {} | {} | {} | {} |\n'.format(
                            version,
                            round(mean_time, 6),
                            round(std_time, 6),
                            __get_delta(
                                _data['mean_time'],
                                cum_data[k][v]['master']['mean_time'],
                            ),
                            ' | '.join(str(v) for v in _data['metadata'].values()),
                            _data['iterations'],
                        )
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
    generate_docs(cum_data, docs_dir)
    generate_menus(cum_data, content_dir)


if __name__ == '__main__':
    main()
