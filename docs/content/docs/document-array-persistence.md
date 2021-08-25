---
title: Document Array Persistence
---
# Document Array Persistence

## Document Array Save

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. master | Num Docs Append | File Format | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| master | 320.8 | 0.83666 | 0.0% | 100000 | binary | 5 |
| 2.0.19 | 314.308479 | 1.865808 | +2.02% | 100000 | binary | 5 |
| 2.0.18 | 317.749074 | 1.170213 | +0.95% | 100000 | binary | 5 |
| 2.0.17 | 334.78437 | 1.396529 | -4.36% | 100000 | binary | 5 |
| 2.0.16 | 336.825288 | 1.66647 | -5.0% | 100000 | binary | 5 |
| 2.0.15 | 337.995949 | 1.661098 | -5.36% | 100000 | binary | 5 |
## Document Array Load

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. master | Num Docs Append | File Format | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| master | 180.8 | 0.447214 | 0.0% | 100000 | binary | 5 |
| 2.0.19 | 179.929076 | 1.140092 | +0.48% | 100000 | binary | 5 |
| 2.0.18 | 182.069867 | 0.700743 | -0.7% | 100000 | binary | 5 |
| 2.0.17 | 187.10597 | 1.358603 | -3.49% | 100000 | binary | 5 |
| 2.0.16 | 184.667713 | 1.285244 | -2.14% | 100000 | binary | 5 |
| 2.0.15 | 197.358013 | 2.151581 | -9.16% | 100000 | binary | 5 |
