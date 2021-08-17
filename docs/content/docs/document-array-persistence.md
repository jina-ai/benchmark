---
title: Document Array Persistence
---
# Document Array Persistence

## Document Array Save

| Version | Mean Time (s) | Std Time (s) | Delta | Num Docs Append | File Format | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| master | 0.314308 | 0.001866 | +1.08% | 100000 | binary | 5 |
| 2.0.18 | 0.317749 | 0.00117 | +5.09% | 100000 | binary | 5 |
| 2.0.17 | 0.334784 | 0.001397 | +0.61% | 100000 | binary | 5 |
| 2.0.16 | 0.336825 | 0.001666 | +0.35% | 100000 | binary | 5 |
| 2.0.15 | 0.337996 | 0.001661 | 0.0% | 100000 | binary | 5 |
## Document Array Load

| Version | Mean Time (s) | Std Time (s) | Delta | Num Docs Append | File Format | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| master | 0.179929 | 0.00114 | +1.18% | 100000 | binary | 5 |
| 2.0.18 | 0.18207 | 0.000701 | +2.69% | 100000 | binary | 5 |
| 2.0.17 | 0.187106 | 0.001359 | -1.32% | 100000 | binary | 5 |
| 2.0.16 | 0.184668 | 0.001285 | +6.43% | 100000 | binary | 5 |
| 2.0.15 | 0.197358 | 0.002152 | 0.0% | 100000 | binary | 5 |
