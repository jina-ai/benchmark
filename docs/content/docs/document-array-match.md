---
title: Document Array Match
---
# Document Array Match

## Match

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. master | Size X | Size Y | Dam X | Dam Y | Emb Size | Use Scipy | Metric | Top K | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| master | 1298.4 | 15.582041 | 0.0% | 10 | 100000 | False | False | 256 | False | euclidean | 3 | 5 |
| 2.0.19 | 8148.593423 | 28.660659 | -527.59% | 1000 | 100000 | True | False | 256 | False | euclidean | 100 | 5 |
| 2.0.18 | 8659.391482 | 100.068332 | -566.93% | 1000 | 100000 | True | False | 256 | False | euclidean | 100 | 5 |
| 2.0.17 | 8813.086167 | 68.035104 | -578.77% | 1000 | 100000 | True | False | 256 | False | euclidean | 100 | 5 |
