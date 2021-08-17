---
title: Document Array Append
---
# Document Array Append

## Docarray Append

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. master | Num Docs Append | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: |
| master | 0.006872 | 0.000786 | 0.0% | 10000 | 5 |
| 2.0.18 | 0.006755 | 0.000864 | +1.69% | 10000 | 5 |
| 2.0.17 | 0.008251 | 0.000304 | -20.07% | 10000 | 5 |
| 2.0.16 | 0.007429 | 0.000782 | -8.11% | 10000 | 5 |
| 2.0.15 | 0.008027 | 0.000358 | -16.81% | 10000 | 5 |
## Document Array Memmap Append

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. master | Num Docs Append | Flush | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| master | 0.10026 | 0.000515 | 0.0% | 10000 | False | 5 |
| 2.0.18 | 0.10108 | 0.001383 | -0.82% | 10000 | False | 5 |
| 2.0.17 | 0.103613 | 0.00046 | -3.34% | 10000 | False | 5 |
| 2.0.16 | 0.090852 | 0.009628 | +9.38% | 10000 | False | 5 |
| 2.0.15 | 0.091499 | 0.01286 | +8.74% | 10000 | False | 5 |
