# Benchmark

To do the resource benchmarking (CPU & Memory usage) of Jina features, you can use `benchmark.sh` file. This file actually benchmark scripts under `src` directory with [cmdbench](https://github.com/manzik/cmdbench) utility tool.

## Run

### Run Locally

```bash
pip install -r requirements.txt
bash benchmark.sh
```

### Run on Docker

```bash
JINA_VER=master
docker build --build-arg JINA_VER=$JINA_VER -t bechmark .
docker run -v $(pwd):/app bechmark:latest
```

## Contributing

We welcome all kinds of contributions from the open-source community, individuals and partners. We owe our success to your active involvement.

Here're some quick notes you need to know before start contributing:

- Please keep all of your test scripts under `src` folder and ensure each of them can run independently.
- Please save the benchmarking artifacts either in `.png` or `.txt` format in `docs/static/artifacts/${JINA_VERSION}` directory. Please don't forget to give a nice title to every file separated with `hyphen` only. Example: import_jina_memory_profile.txt
- Please enlist any Python dependency to `requirements.txt` file.
- Please run `site_generator.py` to generate the website everytime you generate new benchmarking artifacts.