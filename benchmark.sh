#!/usr/bin/python3

declare -r jina_version=$(jina --version)

mkdir -p docs/static/artifacts

for file in src/*.py; do
    output_json=$(echo $file | sed -r 's|.py|.json|g' | sed -r "s|src|docs/static/artifacts/${jina_version}|g")
    output_plot=$(echo $file | sed -r 's|.py|.png|g' | sed -r "s|src|docs/static/artifacts/${jina_version}|g")
    cmdbench --save-json=${output_json} --save-plot=${output_plot} python3 ${file}
done