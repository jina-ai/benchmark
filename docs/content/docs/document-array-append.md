---
title: Document Array Append
---
# Document Array Append

## Docarray Append

| Version | Mean Time (s) | Std Time (s) | Num Docs Append | Iterations |
| :---: | :---: | :---: | :---: | :---: |
| master | 0.006872 | 0.000786 | 10000 | 5 |
| 2.0.18 | 0.006755 | 0.000864 | 10000 | 5 |
| 2.0.17 | 0.008251 | 0.000304 | 10000 | 5 |
| 2.0.16 | 0.007429 | 0.000782 | 10000 | 5 |
| 2.0.15 | 0.008027 | 0.000358 | 10000 | 5 |
## Document Array Memmap Append

| Version | Mean Time (s) | Std Time (s) | Num Docs Append | Flush | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: |
| master | 0.10026 | 0.000515 | 10000 | False | 5 |
| 2.0.18 | 0.10108 | 0.001383 | 10000 | False | 5 |
| 2.0.17 | 0.103613 | 0.00046 | 10000 | False | 5 |
| 2.0.16 | 0.090852 | 0.009628 | 10000 | False | 5 |
| 2.0.15 | 0.091499 | 0.01286 | 10000 | False | 5 |
