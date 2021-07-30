#!/usr/bin/python3

import os


def generate_docs(input_dir: str, output_dir: str) -> None:
    for folder_name in os.listdir(input_dir):
        folder = os.path.join(input_dir, folder_name)
        output_file = os.path.join(output_dir, '{}.md'.format(folder_name))
        
        artifact_list = []
        for filename in os.listdir(folder):
            file = os.path.join(folder, filename).split('static')[1]
            artifact_list.append(file)

        with open(output_file, 'w') as fp:
            title = '''
                ---
                title: {folder_name}
                ---
                # {folder_name}
            '''.format(folder_name=folder_name)
            fp.write('---\n')
            fp.write('title: {}\n'.format(folder_name))
            fp.write('---\n')
            fp.write('# {}\n\n'.format(folder_name))

            for artifact in artifact_list:
                artifact_name, extension = artifact.split('/')[-1].split('.')
                if extension.lower() == 'png':
                    fp.write('## {}\n\n'.format(artifact_name))
                    fp.write('![{}]({})\n\n'.format(artifact_name, artifact))
                elif extension.lower() == 'txt':
                    with open(artifact) as f:
                        txt_content = f.read()
                    fp.write('## {}\n\n'.format(artifact_name))
                    fp.write(txt_content)


def main():
    base_dir = os.path.join(os.getcwd(), 'docs')
    docs_dir = os.path.join(base_dir, 'content/docs')
    artifacts_dir = os.path.join(base_dir, 'static/artifacts')

    generate_docs(artifacts_dir, docs_dir)


if __name__ == '__main__':
    main()