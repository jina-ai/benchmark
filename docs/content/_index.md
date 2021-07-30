---
title: Benchmarking Jina
type: docs
---
# Benchmarking

To do the resource benchmarking (CPU & Memory usage) of Jina features, you can use `benchmark.sh` file. This file actually benchmark scripts under `src` directory with [cmdbench](https://github.com/manzik/cmdbench) utility tool.

## Run

### Run Locally

```bash
bash -x benchmark.sh
```

### Run on Docker

```bash
JINA_VER=master
docker build --build-arg JINA_VER=$JINA_VER -t bechmark .
docker run -v $(pwd):/app bechmark:latest
```
