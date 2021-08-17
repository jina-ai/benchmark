---
title: Document Array Construct
---
# Document Array Construct

## Construct Document Array From Repeated Container

| Version | Mean Time (s) | Std Time (s) | Num Chunks | Iterations |
| :---: | :---: | :---: | :---: | :---: |
| master | 0.007219 | 0.000203 | 10000 | 5 |
| 2.0.18 | 0.006901 | 0.00013 | 10000 | 5 |
| 2.0.17 | 0.009179 | 0.00048 | 10000 | 5 |
| 2.0.16 | 0.007037 | 0.000175 | 10000 | 5 |
| 2.0.15 | 0.00912 | 0.000557 | 10000 | 5 |
## Construct Document Array From Another Documentarray

| Version | Mean Time (s) | Std Time (s) | Num Docs | Iterations |
| :---: | :---: | :---: | :---: | :---: |
| master | 0.002836 | 0.000452 | 10000 | 5 |
| 2.0.18 | 0.002611 | 0.000526 | 10000 | 5 |
| 2.0.17 | 0.003637 | 0.00039 | 10000 | 5 |
| 2.0.16 | 0.002659 | 0.000536 | 10000 | 5 |
| 2.0.15 | 0.003146 | 0.000351 | 10000 | 5 |
## Construct Document Array From List Of Documents

| Version | Mean Time (s) | Std Time (s) | Num Docs | Iterations |
| :---: | :---: | :---: | :---: | :---: |
| master | 0.005304 | 0.001257 | 10000 | 5 |
| 2.0.18 | 0.004572 | 0.000845 | 10000 | 5 |
| 2.0.17 | 0.005257 | 0.000779 | 10000 | 5 |
| 2.0.16 | 0.004887 | 0.000597 | 10000 | 5 |
| 2.0.15 | 0.005604 | 0.000418 | 10000 | 5 |
## Construct Document Array From Tuple Of Documents

| Version | Mean Time (s) | Std Time (s) | Num Docs | Iterations |
| :---: | :---: | :---: | :---: | :---: |
| master | 0.004536 | 0.000705 | 10000 | 5 |
| 2.0.18 | 0.004428 | 0.000824 | 10000 | 5 |
| 2.0.17 | 0.005453 | 0.000429 | 10000 | 5 |
| 2.0.16 | 0.00479 | 0.00064 | 10000 | 5 |
| 2.0.15 | 0.005126 | 0.000523 | 10000 | 5 |
## Construct Document Array From Generator

| Version | Mean Time (s) | Std Time (s) | Num Docs | Iterations |
| :---: | :---: | :---: | :---: | :---: |
| master | 0.562678 | 0.009249 | 10000 | 5 |
| 2.0.18 | 0.559191 | 0.008755 | 10000 | 5 |
| 2.0.17 | 0.565819 | 0.010879 | 10000 | 5 |
| 2.0.16 | 0.523352 | 0.004215 | 10000 | 5 |
| 2.0.15 | 0.536692 | 0.013138 | 10000 | 5 |
## Construct Document Array From Another Documentarray Memmap

| Version | Mean Time (s) | Std Time (s) | Num Docs | Iterations |
| :---: | :---: | :---: | :---: | :---: |
| master | 0.114281 | 0.007485 | 10000 | 5 |
| 2.0.18 | 0.114257 | 0.002568 | 10000 | 5 |
| 2.0.17 | 0.117873 | 0.002103 | 10000 | 5 |
| 2.0.16 | 0.164904 | 0.00246 | 10000 | 5 |
| 2.0.15 | 0.160805 | 0.002821 | 10000 | 5 |
