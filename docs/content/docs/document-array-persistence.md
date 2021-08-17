---
title: Document Array Persistence
---
# Document Array Persistence

## Document Array Save

| Version | Mean Time (s) | Std Time (s) | Delta w.r.t. master | Num Docs Append | File Format | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| master | 0.314308 | 0.001866 | 0.0% | 100000 | binary | 5 |
| 2.0.18 | 0.317749 | 0.00117 | -1.09% | 100000 | binary | 5 |
| 2.0.17 | 0.334784 | 0.001397 | -6.51% | 100000 | binary | 5 |
| 2.0.16 | 0.336825 | 0.001666 | -7.16% | 100000 | binary | 5 |
| 2.0.15 | 0.337996 | 0.001661 | -7.54% | 100000 | binary | 5 |
## Document Array Load

| Version | Mean Time (s) | Std Time (s) | Delta w.r.t. master | Num Docs Append | File Format | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| master | 0.179929 | 0.00114 | 0.0% | 100000 | binary | 5 |
| 2.0.18 | 0.18207 | 0.000701 | -1.19% | 100000 | binary | 5 |
| 2.0.17 | 0.187106 | 0.001359 | -3.99% | 100000 | binary | 5 |
| 2.0.16 | 0.184668 | 0.001285 | -2.63% | 100000 | binary | 5 |
| 2.0.15 | 0.197358 | 0.002152 | -9.69% | 100000 | binary | 5 |
