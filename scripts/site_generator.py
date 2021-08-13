#!/usr/bin/python3

import json
import os
from typing import Any, Dict, List


def _cleaned_title(raw_heading: str) -> str:
    """Return cleaned title of artifact name."""
    return raw_heading.replace('test_', '').replace('_', ' ').title()


def _cleaned_slug(raw_heading: str) -> str:
    """Return cleaned slug of artifact name."""
    return raw_heading.replace('test_', '').replace('_', '-')


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
                fp.write('## {}\n\n'.format(_cleaned_title(v)))
                fp.write('| version | iterations | mean_time | std_time | metadata |\n')
                fp.write('| :---: | :---: | :---: | :---: | :---: |\n')

                for version in cum_data[k][v]:
                    _data = cum_data[k][v][version]
                    fp.write(
                        '| {} | {} | {} | {} | {} |\n'.format(
                            version,
                            _data['iterations'],
                            round(_data['mean_time'], 4),
                            round(_data['std_time'], 4),
                            _data['metadata'],
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
        # fp.write('- [Homepage]({{< relref "/" >}})\n')

        for k in cum_data:
            fp.write(
                '- [%s]({{< relref "/docs/%s.md" >}})\n'
                % (_cleaned_title(k), _cleaned_slug(k))
            )
            # for v in cum_data[k]:
            #     fp.write(
            #         '\t- [%s]({{< relref "/docs/%s.md#%s" >}})\n'
            #         % (_cleaned_title(v), _cleaned_slug(k), _cleaned_slug(v))
            #     )


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
