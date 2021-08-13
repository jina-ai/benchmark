# Benchmark

We are currenty considering time metrics to benchmark Jina features and using [pytest](https://docs.pytest.org/en/6.2.x/) to run these tests.

## Playbook

### Run Locally

```bash
pip install -r requirements.txt
pytest
```

### Run on Docker

```bash
JINA_VER=master
docker build --build-arg JINA_VER=$JINA_VER -t bechmark .
docker run -v $(pwd):/app bechmark:latest
```

## Contributing

We welcome all kinds of contributions from the open-source community, individuals and partners. We owe our success to your active involvement.

Here're some quick notes you need to know before starting to contribute:

- Please keep all of your tests under `src` folder and ensure they behave as expected with `pytest`.
- Please save the benchmarking artifacts either in `JSON` format in `docs/static/artifacts/${JINA_VERSION}/report.json` file.
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
