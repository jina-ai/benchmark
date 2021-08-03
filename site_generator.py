#!/usr/bin/python3

import os
from typing import Union


def _cleaned_heading(raw_heading: str) -> str:
    """Return cleaned heading of artifact name."""
    return raw_heading.replace('_', ' ').title()


def _cleaned_memory_profile_output(file_path: str) -> Union[str, None]:
    """Read memory profile log file and return markdown compatible output.

    Args:
        file_path: Absolute file path to memory profile log file.
    """
    with open(file_path) as fp:
        lines = fp.readlines()

    if len(lines) > 3:
        lines[0] = '```'
        lines[-1] = '```\n\n'
        return ''.join(lines)
    else:
        return None


def generate_docs(input_dir: str, output_dir: str) -> None:
    """This generate required docs from artifacts.

    Args:
        input_dir: Absolute path to artifact directory.
        output_dir: Absolute path to Hugo docs directory.
    """
    for folder_name in os.listdir(input_dir):
        folder = os.path.join(input_dir, folder_name)
        output_file = os.path.join(output_dir, '{}.md'.format(folder_name))

        artifact_list = []
        for filename in os.listdir(folder):
            file = os.path.join(folder, filename).split('static')[1]
            artifact_list.append(file)

        txt_artifact_list = []
        with open(output_file, 'w') as fp:
            fp.write('---\n')
            fp.write('title: {}\n'.format(folder_name))
            fp.write('---\n')
            fp.write('# {}\n\n'.format(folder_name))

            for artifact in artifact_list:
                artifact_name, extension = artifact.split('/')[-1].split('.')
                cleaned_heading = _cleaned_heading(artifact_name)
                if extension.lower() == 'png':
                    fp.write('## {}\n\n'.format(cleaned_heading))
                    fp.write('![{}]({})\n\n'.format(cleaned_heading, artifact))
                elif extension.lower() == 'txt':
                    txt_artifact_list.append(artifact_name)

            for artifact_name in txt_artifact_list:
                cleaned_heading = _cleaned_heading(artifact_name)
                txt_content = _cleaned_memory_profile_output(
                    os.path.join(folder, '{}.txt'.format(artifact_name))
                )
                if txt_content:
                    fp.write('## {}\n\n'.format(cleaned_heading))
                    fp.write(txt_content)


def generate_menus(input_dir: str, output_dir: str) -> None:
    """This generate required menus from artifacts.

    Args:
        input_dir: Absolute path to artifact directory.
        output_dir: Absolute path to Hugo menus directory.
    """
    menu_index = os.path.join(output_dir, 'menu/index.md')

    with open(menu_index, 'w') as fp:
        fp.write('---\n')
        fp.write('headless: true\n')
        fp.write('---\n\n')
        fp.write('- [Homepage]({{< relref "/" >}})\n')

        folder_list = list(os.listdir(input_dir))
        folder_list.sort(key=lambda s: [int(u) for u in s.split('.')], reverse=True)

        for folder_name in folder_list:
            fp.write(
                '- [%s]({{< relref "/docs/%s.md" >}})\n' % (folder_name, folder_name)
            )


def main():
    base_dir = os.path.join(os.getcwd(), 'docs')
    content_dir = os.path.join(base_dir, 'content')
    docs_dir = os.path.join(content_dir, 'docs')
    artifacts_dir = os.path.join(base_dir, 'static/artifacts')

    generate_docs(artifacts_dir, docs_dir)
    generate_menus(artifacts_dir, content_dir)


if __name__ == '__main__':
    main()
