#!/usr/bin/python3

import json
import os
import re
from sys import path, version
from typing import Any, Dict, Union


def _cleaned_title(raw_heading: str) -> str:
    """Return cleaned title of artifact name."""
    return raw_heading.replace('_', ' ').title()


def _cleaned_slug(raw_heading: str) -> str:
    """Return cleaned slug of artifact name."""
    return raw_heading.replace('_', '-')


def _get_cum_data(artifacts_dir: str) -> Dict[Any, Any]:
    """Generates cumulative data and return in a dict.

    Args:
        artifacts_dir: Absolute path to artifact directory.

    Return: Dict of cumulative data
    """
    data: Dict[Any, Any] = dict()
    for file in os.listdir(artifacts_dir):
        if file.endswith('.json'):
            with open(os.path.join(artifacts_dir, file)) as fp:
                _raw_data = json.load(fp)

            version = file.replace('.json', '')

            for i in _raw_data:
                k, v = i['name'].split('/')
                if k in data:
                    if v in data[k]:
                        data[k][v][version] = i
                    else:
                        data[k][v] = {
                            version: i
                        }
                else:
                    data[k] = {v: {version: i}}
    print(data)
    return data


def generate_docs(cum_data: Dict[Any, Any], output_dir: str) -> None:
    """This generate required docs from artifacts.

    Args:
        cum_data: Cumulative data in Dict.
        output_dir: Absolute path to Hugo docs directory.
    """
    for k in cum_data:
        for v in cum_data[k]:
            output_file = os.path.join(
                output_dir, '{}-{}.md'.format(_cleaned_slug(k), _cleaned_slug(v))
            )

            with open(output_file, 'w') as fp:
                fp.write('---\n')
                fp.write(
                    'title: {} - {}\n'.format(_cleaned_title(k), _cleaned_title(v))
                )
                fp.write('---\n')
                fp.write('# {} - {}\n\n'.format(_cleaned_title(k), _cleaned_title(v)))
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
        fp.write('- [Homepage]({{< relref "/" >}})\n')

        for k in cum_data:
            fp.write('- %s\n' % (_cleaned_title(k)))
            for v in cum_data[k]:
                fp.write(
                    '\t- [%s]({{< relref "/docs/%s-%s.md" >}})\n'
                    % (_cleaned_title(v), _cleaned_slug(k), _cleaned_slug(v))
                )


def main():
    base_dir = os.path.join(os.getcwd(), 'docs')
    content_dir = os.path.join(base_dir, 'content')
    docs_dir = os.path.join(content_dir, 'docs')
    artifacts_dir = os.path.join(base_dir, 'static/artifacts')

    cum_data = _get_cum_data(artifacts_dir)
    generate_docs(cum_data, docs_dir)
    generate_menus(cum_data, content_dir)


if __name__ == '__main__':
    main()
