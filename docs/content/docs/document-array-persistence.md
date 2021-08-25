---
title: Document Array Persistence
---
# Document Array Persistence

## Document Array Save

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. master | Num Docs Append | File Format | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| master | 326.6 | 2.302173 | 0.0% | 100000 | binary | 5 |
| 2.0.19 | 314.308479 | 1.865808 | +3.76% | 100000 | binary | 5 |
| 2.0.18 | 317.749074 | 1.170213 | +2.71% | 100000 | binary | 5 |
| 2.0.17 | 334.78437 | 1.396529 | -2.51% | 100000 | binary | 5 |
| 2.0.16 | 336.825288 | 1.66647 | -3.13% | 100000 | binary | 5 |
| 2.0.15 | 337.995949 | 1.661098 | -3.49% | 100000 | binary | 5 |
## Document Array Load

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. master | Num Docs Append | File Format | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| master | 184 | 0.707107 | 0.0% | 100000 | binary | 5 |
| 2.0.19 | 179.929076 | 1.140092 | +2.21% | 100000 | binary | 5 |
| 2.0.18 | 182.069867 | 0.700743 | +1.05% | 100000 | binary | 5 |
| 2.0.17 | 187.10597 | 1.358603 | -1.69% | 100000 | binary | 5 |
| 2.0.16 | 184.667713 | 1.285244 | -0.36% | 100000 | binary | 5 |
| 2.0.15 | 197.358013 | 2.151581 | -7.26% | 100000 | binary | 5 |
