# Benchmark Jina

We are currenty considering time metrics to benchmark Jina features and using [pytest](https://docs.pytest.org) to run these tests.

## Playbook

### Prepare environment

```bash
pip install -r requirements.txt
pip install pre-commit==2.13.0
pre-commit install
git submodule update --init
```

### Run Locally

```bash
pytest
```

### Run on Docker

```bash
JINA_VER=master
docker build --build-arg JINA_VER=$JINA_VER -t bechmark .
docker run -v $(pwd):/app bechmark:latest
```

### Generate docs locally and run server

```bash
python scripts/site_generator.py
cd docs
hugo server -D
```

## Machine

We are running all tests sequentially for a version on a single machine of following properties:

| Item | Value |
| :---: | :---: |
| Cloud Vendor | AWS |
| Instance | c5.xlarge |
| Memory | 8 GiB |
| vCPU | 4 |
| Processor | Intel Xeon Platinum 8124M |
| Clock Speed | 3 GHz |
| Storage | EBS (gp2) |

## Contributing

We welcome all kinds of contributions from the open-source community, individuals and partners. We owe our success to your active involvement.

Here're some quick notes you need to know before starting to contribute:

- Please keep all of your tests under `src` folder and ensure they behave as expected with `pytest`.
- Please save the benchmarking artifacts in `JSON` format in `docs/static/artifacts/${JINA_VERSION}/report.json` file.
- Please enlist any Python dependency to `requirements.txt` file.
- Please run `scripts/site_generator.py` to generate the website everytime you generate new benchmarking artifacts.
- `report.json` file should have the following shema:

```json
[
  {
    "name": "document_array_append/test_docarray_append",
    "iterations": 5,
    "mean_time": 0.007944801799999368,
    "std_time": 0.0012715548259231583,
    "metadata": {
      "num_docs_append": 10000
    }
  }
]
```
