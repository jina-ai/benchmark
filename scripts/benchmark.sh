#!/usr/bin/python3

declare -r jina_version=$(jina --version)

mkdir -p docs/static/artifacts/${jina_version}

for file in src/*.py; do
    python3 ${file}
done